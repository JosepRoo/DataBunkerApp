import hashlib
from flask import session
from server.databunker.src.common.database import Database
import uuid


class User(object):
    def __init__(self, email, name, password=None, _id=None):
        self.email = email
        self.password = password
        self.name = name
        self.privileges = []
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_ids(cls, ids):
        data = Database.find('users', {"$in:": ids})
        if data is not None:
            return [cls(**user) for user in data]

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password

    @classmethod
    def register(cls, email, password, name):
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(email, hashlib.sha224(password.encode('utf-8')).hexdigest(), name)
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

    def add_delete_privilege(self,privilege_id, operation):
        if operation == "add":
            self.users.append(privilege_id)
        elif operation == "remove":
            self.users.remove(privilege_id)
        modified_count = Database.update_one({'_id': self._id}, {'user': self.users})
        return modified_count

    def get_users(self, user_id=None):
        if user_id is not None:
            users = Database.find('users', {"$in:": self.users})
            return [User(user['_id'], user['email'], user['name']) for user in users]

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
