from __future__ import annotations
import datetime
import requests
from flask import session
from dataclasses import dataclass
from mongoengine import *

from app.common.tree import Tree
from app.models.baseModel import BaseModel
from app.models.privileges.privilege import Privilege
from app.models.recoveries.errors import UnableToRecoverPassword
from app.models.users.constants import COLLECTION
from app.common.utils import Utils
from app.models.recoveries.recovery import Recovery
from app.models.users.errors import FavoriteAlreadyAdded, FavoriteNotFound

import app.models.users.errors as UserErrors


# TODO cambiar privilegios a channels:[], categories:[]...
@dataclass(init=False)
class User(BaseModel):
    email: str = StringField(required=True)
    name: str = StringField(required=True)
    channel_id: str = StringField()
    password: str = StringField(required=True)
    enterprise_id: str = StringField()
    privileges: Privilege = EmbeddedDocumentField(Privilege, default=lambda: Privilege())  # EmbeddedDocumentField(Privilege)
    favorites: list = ListField(default=lambda: list())
    meta = {'collection': COLLECTION}

    @classmethod
    def get_by_email(cls, email: str) -> User:
        user = cls.objects(email=email)
        if user:
            user = user[0]
            return user

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None and Utils.check_hashed_password(password, user.password) and Utils.email_is_valid(email):
            User.login(email, user._id)
            return user
        raise UserErrors.InvalidLogin("Email o Contraseña incorrectos")

    @classmethod
    def register(cls, kwargs):
        email = kwargs['email']
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(**kwargs)
            new_user.password = Utils.hash_password(new_user.password)
            new_user.add_privilege('channel', new_user.channel_id)
            return new_user
        raise UserErrors.UserAlreadyRegisteredError("El Usuario ya existe")

    @staticmethod
    def login(user_email, user_id):
        session['email'] = user_email
        session['_id'] = user_id
        session['time_created'] = datetime.datetime.now()

    @staticmethod
    def logout():
        session['email'] = None
        session['_id'] = None

    def send_recovery_message(self):
        recovery = Recovery(user_email=self.email)
        recovery.save_to_mongo()
        return requests.post(
            "https://api.mailgun.net/v3/sandbox6b23254da94c47f2b75358b425dd997a.mailgun.org/messages",
            auth=("api", "key-f96e4370f78e79e03e3dd6b9abe2ce10"),  # cambiar a eniroment var en produccion
            data={"from": "Databunker <postmaster@sandbox6b23254da94c47f2b75358b425dd997a.mailgun.org>",
                  # cambiar a eniroment var en produccion
                  "to": "{} <{}>".format(self.name, self.email),
                  "subject": "Recuperacion de contraseña",
                  "text": "para reestablecer la contrasenia de clic en el siguiente link: databunker.com/recuperarconstrasenia/{}".format(
                      recovery._id)})

    def set_password(self, password):
        self.password = Utils.hash_password(password)

    @staticmethod
    def recover_password(recovery_id, email, password):
        if Recovery.recover_in_db(recovery_id, email):
            user = User.get_by_email(email)
            user.set_password(password)
            user.save()
        else:
            raise UnableToRecoverPassword("No se pudo hacer la recuperacion de la contraseña")

    def add_favorite(self, product_id):
        from app.models.elements.subelements.products.product import Product
        if product_id in self.favorites:
            raise FavoriteAlreadyAdded("El producto ya fue agregado anteriormente")
        else:
            self.favorites.append(product_id)
            self.save()
            return Product.get_by_id(product_id)

    def remove_favorite(self, product_id):
        from app.models.elements.subelements.products.product import Product
        if product_id not in self.favorites:
            raise FavoriteNotFound("El producto no esta en la lista de favoritos")
        else:
            self.favorites.remove(product_id)
            self.save()
            return Product.get_by_id(product_id)

    def get_favorites(self):
        from app.models.elements.subelements.products.product import Product
        favorites = [Product.get_by_id(favorite) for favorite in self.favorites]
        return favorites if favorites else []

    def add_privilege(self, element_type, element):
        self.privileges.add_remove_privilege(element_type, element)
        print(self.__repr__())
        self.save()
        return self.privileges.json()

    def remove_privilege(self, element_type, element):
        self.privileges.add_remove_privilege(element_type, element, False)
        self.save()
        return self.privileges.json()

