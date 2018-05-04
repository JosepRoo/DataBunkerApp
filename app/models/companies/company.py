from app.common.database import Database
import uuid

from app.models.companies.errors import CompanyAlreadyExists
from app.models.users.user import User
from app.models.companies.constants import COLLECTION


class Company(object):
    def __init__(self, name, _id=None):
        self.name = name
        self.users = []
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_users(self):
        users = User.get_by_enterprise_id(self._id)
        if users:
            self.users = users
        return self

    @classmethod
    def get_company_by_id(cls, _id):
        data = Database.find_one("companies", {"_id": _id})
        if data:
            return cls(**data)

    @classmethod
    def get_company_by_name(cls, name):
        data = Database.find_one("companies", {"name": name})
        if data:
            return cls(**data)

    @classmethod
    def register(cls, kwargs):
        name = kwargs['name']
        company = Company.get_company_by_name(name)
        if company:
            raise CompanyAlreadyExists("Company with name {} already exists".format(name))
        new_company = cls(**kwargs)
        new_company.save_to_mongo()
        return new_company

    def delete_company(self):
        Database.remove(COLLECTION, {'_id': self._id})

    def save_to_mongo(self):
        Database.insert('companies', self.json_Mongo())

    def json(self):
        return {'name': self.name,
                'users': [user.json() for user in self.users],
                '_id': self._id}

    def json_Mongo(self):
        return {'name': self.name,
                '_id': self._id}

    @classmethod
    def get_all_companies(cls):
        return [cls(**company) for company in Database.find(COLLECTION, {})]
