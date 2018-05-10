from app.common.database import Database
from app.models.basemodel import BaseModel
from app.models.companies.errors import CompanyAlreadyExists
from app.models.users.user import User
from app.models.companies.constants import COLLECTION


class Company(BaseModel):
    def __init__(self, name, _id=None):
        BaseModel.__init__(self,_id)
        self.name = name
        self.users = []

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
