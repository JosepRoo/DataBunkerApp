from server.databunker.src.common.database import Database
from server.databunker.src.common.response import Response
import uuid

from src.models.user import User


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
        modified_count = Database.update_one(collection='users', filter={'_id': self._id}, query={'user': self.users})
        if modified_count == 1:
            return Response(success=True, msgResponse='registro modificado con exito').json()
        return Response(success=False, msgResponse='Registro no modificado').json()

    def get_users(self, user_id=None, user_email=None):
        if user_id is not None and user_id in self.users:
            users = User.get_by_id(user_id)
            if users is None:
                return Response(success=False, msgResponse="Usuario no asignado a esta compania o id incorrecto").json()
        elif user_email is not None:
            users = User.get_by_email(user_email)
            if users is None or users.get_id() not in self.users:
                return Response(success=False,msgResponse="Usuario no asignado a esta compania o email incorrecto")
        else:
            users = User.get_by_ids(self.users)
            users.json()
        return users

    @classmethod
    def get_company_by_id(cls, _id):
        data = Database.find_one("companies", {"_id": _id})
        if data is not None:
            return cls(**data)

    def save_to_mongo(self):
        Database.insert('companies', self.json())

    def json(self):
        return {'name': self.name,
                'users': self.users,
                '_id': self._id}
