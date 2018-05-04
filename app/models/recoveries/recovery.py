import uuid
from app.models.recoveries.constants import COLLECTION
from app.common.database import Database


class Recovery(object):
    def __init__(self, user_email, _id=None):
        self.user_email = user_email
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        "recovery with id {} for user: {}".format(self._id, self.user_email)

    def save_to_mongo(self):
        Database.insert(COLLECTION, self.json())

    def remove_from_mongo(self):
        Database.remove(COLLECTION, self.json())

    @classmethod
    def get_recovery(cls, _id=None):
        if _id is None:
            return [cls(**recovery) for recovery in Database.find(COLLECTION, {})]

        else:
            return [cls(Database.find_one(COLLECTION, {'_id': _id}))]

    @classmethod
    def get_recovery_by_email(cls, user_email):
        Database.find_one(COLLECTION, {'user_email': user_email})

    def json(self):
        return {
            '_id': self._id,
            'user_email': self.user_email
        }

    @staticmethod
    def recover_password(recovery_id, email, new_password):
        recovery = Recovery(email, recovery_id)
        recovery_in_DB = Database.find_one(COLLECTION, recovery.json())
        if recovery_in_DB is None:
            return False
        else:
            Database.remove(COLLECTION,recovery.json())
            return True
