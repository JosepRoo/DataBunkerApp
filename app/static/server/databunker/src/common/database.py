import pymongo
class Database(object):
    URI = "mongodb://richogtz:cloudstrifeFF7!@127.0.0.1:27017"
    USER = 'richogtz'
    PWD = 'cloudstrifeFF7!'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        client.admin
        Database.DATABASE = client['databunker']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update_one(collection, query, filter):
        result = Database.DATABASE[collection].update_one(filter, query)
        return result.modified_count
