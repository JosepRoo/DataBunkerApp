import uuid

from app.common.database import Database


class BaseModel:
    def __init__(self, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self, exclude=None):
        if exclude:
            return {attrib: [element.json() for element in self.__getattribute__(attrib)]
                    if type(self.__getattribute__(attrib)) is list else self.__getattribute__(attrib)
                    for attrib in self.__dict__.keys() if attrib not in exclude}

        return {attrib: [element.json() for element in self.__getattribute__(attrib)]
                if type(self.__getattribute__(attrib)) is list else self.__getattribute__(attrib)
                for attrib in self.__dict__.keys()}

    def delete_from_mongo(self, collection):
        Database.remove(collection, {"_id": self._id})

    def update_mongo(self, collection, exclude=None):
        if exclude:
            Database.update(collection, {"_id": self._id}, self.json(exclude))
        else:
            Database.update(collection, {"_id": self._id}, self.json())

    def save_to_mongo(self, collection,exclude=None):
        Database.insert(collection, self.json(exclude))

    @classmethod
    def get_by_id(cls, _id, collection):
        return cls(**Database.find_one(collection, {'_id': _id}))
