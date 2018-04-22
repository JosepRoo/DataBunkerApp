from app.common.database import Database
import uuid
from app.models.users.user import User
from app.models.users.constants import COLLECTION

class Company(object):
    def __init__(self, name, _id=None):
        self.name = name
        self.users = []
        self._id = uuid.uuid4().hex if _id is None else _id

    def add_delete_user(self, user_id, operation):
        if operation == "add":
            self.users.append(user_id)
        elif operation == "remove":
            self.users.remove(user_id)
        modified_count = Database.update(COLLECTION, {'_id': self._id}, self.json())
        if modified_count == 1:
            return True #Response(success=True, msg_response='registro modificado con exito').json()
        return False #Response(success=False, msg_response='Registro no modificado').json()

    def get_users(self, user_id=None, user_email=None):
        if user_id is not None and user_id in self.users:
            users = User.get_by_id(user_id)
            if users is None:
                return False #Response(success=False, msg_response="Usuario no asignado a esta compania o id incorrecto").json()
        elif user_email is not None:
            users = User.get_by_email(user_email)
            if users is None or users.get_id() not in self.users:
                return False #Response(success=False,msg_response="Usuario no asignado a esta compania o email incorrecto")
        else:
            users = User.get_by_ids(self.users)
            users.json()
        return users

    @classmethod
    def get_company_by_id(cls, _id):
        data = Database.find_one("companies", {"_id": _id})
        if data is not None:
            return cls(**data)

    def add_delete_privilege(self, privilege_id, operation):
        if operation == "add":
            self.users.append(privilege_id)
        elif operation == "remove":
            self.users.remove(privilege_id)
        modified_count = Database.update({'_id': self._id}, self.json())
        return modified_count

    '''
    def get_users(self, user_id=None):
        if user_id is not None:
            users = Database.find('users', {"$in:": self.users})
            return [User(user['_id'], user['email'], user['name']) for user in users]
    '''

    def save_to_mongo(self):
        Database.insert('companies', self.json())

    def json(self):
        return {'name': self.name,
                'users': self.users,
                '_id': self._id}
