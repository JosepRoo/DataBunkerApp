import uuid

import datetime

from app.common.database import Database


class BaseModel:
    def __init__(self, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self, exclude=None, date_to_string=True):
        result = dict()
        for attrib in self.__dict__.keys():
            if exclude is not None and attrib in exclude:
                continue
            attrib_value = self.__getattribute__(attrib)
            if type(attrib_value) is list:
                result[attrib] = list()
                for element in attrib_value:
                    if type(element) is datetime.datetime and date_to_string:
                        result[attrib].append(element.strftime("%Y-%m-%d %H:%M"))
                    elif not isinstance(element, str) and not isinstance(element, int) and not isinstance(element, datetime.datetime):
                        result[attrib].append(element.json(date_to_string=date_to_string))
                    else:
                        result[attrib].append(element)

            elif type(attrib_value) is datetime.datetime and date_to_string:
                    result[attrib] = attrib_value.strftime("%Y-%m-%d %H:%M")
            else:
                result[attrib] = attrib_value
        return result

    def delete_from_mongo(self, collection):
        Database.remove(collection, {"_id": self._id})

    def update_mongo(self, collection, exclude=None):
        Database.update(collection, {"_id": self._id}, self.json(exclude, date_to_string=False))

    def save_to_mongo(self, collection, exclude=None):
        Database.insert(collection, self.json(exclude, date_to_string=False))

    @classmethod
    def get_by_id(cls, _id, collection):
        return cls(**Database.find_one(collection, {'_id': _id}))
