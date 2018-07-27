import requests
from flask import session

from app.common.database import Database
from app.models.basemodel import BaseModel
from app.models.privileges.privilege import Privilege
from app.models.products.product import Product
from app.models.recoveries.errors import UnableToRecoverPassword
from app.models.users.constants import COLLECTION
from app.models.products.constants import COLLECTION as PRODUCTCOLLECTION
from app.common.utils import Utils
from app.models.recoveries.recovery import Recovery
import app.models.users.errors as UserErrors
from app.models.users.errors import FavoriteAlreadyAdded, FavoriteNotFound


class User(BaseModel):
    def __init__(self, email, name, channel_id=None, password=None, _id=None, enterprise_id=None,
                 privileges=dict(), favorites=None):
        BaseModel.__init__(self, _id)
        self.email = email
        self.password = password
        self.name = name
        self.channel_id = channel_id
        self.privileges = Privilege(privileges)
        self.enterprise_id = enterprise_id
        self.favorites = favorites if favorites else []

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_list(cls):
        data = Database.find(COLLECTION, {})
        if data is not None:
            return [cls(**user) for user in data]

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
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(**kwargs)
            new_user.password = Utils.hash_password(new_user.password)
            new_user.save_to_mongo(COLLECTION)
            # User.login(new_user.email, new_user._id)
            return new_user
        raise UserErrors.UserAlreadyRegisteredError("El Usuario ya existe")

    @staticmethod
    def login(user_email, user_id):
        session['email'] = user_email
        session['_id'] = user_id

    @staticmethod
    def logout():
        session['email'] = None
        session['_id'] = None

    def get_id(self):
        return self._id

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

    def update_user(self):
        self.update_mongo(COLLECTION)

    def delete_user(self):
        self.delete_from_mongo(COLLECTION)

    @staticmethod
    def recover_password(recovery_id, email, password):
        if Recovery.recover_in_db(recovery_id, email):
            user = User.get_by_email(email)
            user.set_password(password)
            user.update_mongo(collection=COLLECTION)
        else:
            raise UnableToRecoverPassword("No se pudo hacer la recuperacion de la contraseña")

    def add_favorite(self, product_id):
        if product_id in self.favorites:
            raise FavoriteAlreadyAdded("El producto ya fue agregado anteriormente")
        else:
            self.favorites.append(product_id)
            self.update_mongo(COLLECTION)
            return Product.get_by_id(product_id, PRODUCTCOLLECTION)

    def remove_favorite(self, product_id):
        if product_id not in self.favorites:
            raise FavoriteNotFound("El producto no esta en la lista de favoritos")
        else:
            self.favorites.remove(product_id)
            self.update_mongo(COLLECTION)
            return Product.get_by_id(product_id, PRODUCTCOLLECTION)

    def get_favorites(self):
        favorites = [Product.get_by_id(favorite, PRODUCTCOLLECTION) for favorite in self.favorites]
        return favorites if favorites else []

    def add_privilege(self, element_type, element):
        self.privileges.add_privilege(element_type, element)
        self.update_mongo(COLLECTION)
        return self.privileges.json()

    def remove_privilege(self, element_type, element):
        self.privileges.remove_privilege(element_type, element)
        self.update_mongo(COLLECTION)
        return self.privileges.json()

    def json(self, exclude=None, date_to_string=True):
        if exclude:
            return {
            attrib: [element.json(date_to_string=date_to_string) if not isinstance(element, str) else element for
                     element in self.__getattribute__(attrib)]
                    if type(self.__getattribute__(attrib)) is list else self.__getattribute__(attrib).json()
                    if isinstance(self.__getattribute__(attrib), Privilege) else self.__getattribute__(attrib)
                    for attrib in self.__dict__.keys() if attrib not in exclude}

        return {
        attrib: [element.json(date_to_string=date_to_string) if not isinstance(element, str) else element for element in
                 self.__getattribute__(attrib)]
                if type(self.__getattribute__(attrib)) is list else self.__getattribute__(attrib).json()
                if isinstance(self.__getattribute__(attrib), Privilege) else self.__getattribute__(attrib)
                for attrib in self.__dict__.keys()}