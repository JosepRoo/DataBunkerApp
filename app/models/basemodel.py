import uuid

from app.common.database import Database


class BaseModel:
    def __init__(self, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self, exclude=None, date_to_string=True):
        if exclude:
            return {attrib: [element.json(date_to_string=date_to_string) for element in self.__getattribute__(attrib)]
                    if type(self.__getattribute__(attrib)) is list else self.__getattribute__(attrib)
                    for attrib in self.__dict__.keys() if attrib not in exclude}

        return {attrib: [element.json(date_to_string=date_to_string) for element in self.__getattribute__(attrib)]
                if type(self.__getattribute__(attrib)) is list else self.__getattribute__(attrib)
                for attrib in self.__dict__.keys()}

    def delete_from_mongo(self, collection):
        Database.remove(collection, {"_id": self._id})

    def update_mongo(self, collection, exclude=None):
        Database.update(collection, {"_id": self._id}, self.json(exclude, date_to_string=False))

    def save_to_mongo(self, collection,exclude=None):
        Database.insert(collection, self.json(exclude, date_to_string=False))

    @classmethod
    def get_by_id(cls, _id, collection):
        return cls(**Database.find_one(collection, {'_id': _id}))
