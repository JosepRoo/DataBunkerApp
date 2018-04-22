import requests
from flask import session
from app.common.database import Database
import uuid
from app.models.users.constants import COLLECTION
from app.common.utils import Utils
from app.models.recoveries.recovery import Recovery


class User(object):
    def __init__(self, email, name, password=None, _id=None):
        self.email = email
        self.password = password
        self.name = name
        self.privileges = []
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(COLLECTION, {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(COLLECTION, {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_ids(cls, ids):
        data = Database.find(COLLECTION, {"$in:": ids})
        if data is not None:
            return [cls(**user) for user in data]

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            User.login(email)
            return Utils.check_hashed_password(user.password, password)

    @classmethod
    def register(cls, email, password, name):
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(email, Utils.hash_password(password), name)
            new_user.save_to_mongo()
            session['email'] = email
            session['_id'] = new_user._id
            return True
        return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_id(self):
        return self._id

    def json(self):
        return {'email': self.email,
                '_id': self._id,
                'password': self.password,
                'name': self.name
        }

    def save_to_mongo(self):
        Database.insert('users', self.json())

    def send_recovery_message(self):
        recovery = Recovery(user_email=self.email)
        recovery.save_to_mongo()
        return requests.post(
            "https://api.mailgun.net/v3/sandbox6b23254da94c47f2b75358b425dd997a.mailgun.org/messages",
            auth=("api", "key-f96e4370f78e79e03e3dd6b9abe2ce10"), #cambiar a eniroment var en produccion
            data={"from": "Databunker <postmaster@sandbox6b23254da94c47f2b75358b425dd997a.mailgun.org>", #cambiar a eniroment var en produccion
                  "to": "{} <{}>".format(self.name, self.email),
                  "subject": "Recuperacion de contraseña",
                  "text": "para reestablecer la contrasenia de clic en el siguiente link: databunker.com/recuperarconstrasenia/{}".format(recovery._id)})

    def set_password(self, password):
        self.password = Utils.hash_password(password)

    def update_user(self):
        Database.update(COLLECTION, {self._id}, self.json())
