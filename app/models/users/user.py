import requests
from flask import session
from app.common.database import Database
import uuid
from app.models.users.constants import COLLECTION
from app.common.utils import Utils
from app.models.recoveries.recovery import Recovery
import app.models.users.errors as UserErrors
import ast


class User(object):
    def __init__(self, email, name, password=None, _id=None, enterprise_id=None, privileges=None):
        self.email = email
        self.password = password
        self.name = name
        self.privileges = eval(privileges) if privileges else []
        self._id = uuid.uuid4().hex if _id is None else _id
        self.enterprise_id = enterprise_id

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
        else:
            raise UserErrors.UserError("id no existe")

    @classmethod
    def get_by_enterprise_id(cls, enterprise_id):
        data = Database.find(COLLECTION, {"enterprise_id": enterprise_id})
        if data is not None:
            return [cls(**user) for user in data]

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None and Utils.check_hashed_password(password, user.password) and Utils.email_is_valid(email):
            User.login(email, user._id)
            return True
        raise UserErrors.InvalidLogin("Email o Contraseña incorrectos")

    @classmethod
    def register(cls, kwargs):
        email = kwargs['email']
        user = User.get_by_email(email)
        if user is None:
            print(kwargs['enterprise_id'])
            new_user = cls(**kwargs)
            new_user.save_to_mongo()
            User.login(new_user.email, new_user._id)
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

    def json_mongo(self):
        return {'email': self.email,
                '_id': self._id,
                'password': self.password,
                'name': self.name,
                'privileges': self.privileges,
                'enterprise_id': self.enterprise_id
                }

    def json(self):
        return {'email': self.email,
                '_id': self._id,
                'name': self.name,
                'privileges': self.privileges,
                'enterprise_id': self.enterprise_id
                }

    def save_to_mongo(self):
        Database.insert('users', self.json_mongo())

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
        Database.update(COLLECTION, {'_id': self._id}, self.json_mongo())

    def delete_user(self):
        Database.remove(COLLECTION, {'_id': self._id})

    @staticmethod
    def recover_password(recovery_id, email, password):
        Recovery.recover_password(recovery_id, email, password)
        user = User.get_by_email(email)
        user.set_password(password)
        user.update_user()

    '''
    @user_blueprint.before_request
    def before_request():
        if session.get('email') is None:
            return jsonify(Response(msg_response="Not Logged in").json())
    '''
