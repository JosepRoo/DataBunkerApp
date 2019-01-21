import os
import pymongo

__author__ = 'lrgl'


# class Database:
#     # URI = "mongodb://richogtz:cloudstrifeFF7!@127.0.0.1:27017/databunker"
#     URI = os.environ.get('MONGODB_URI') or "mongodb://127.0.0.1:27017/databunker"
#     DATABASE = None
#
#     @staticmethod
#     def initialize():
#         client = pymongo.MongoClient(Database.URI)
#         Database.DATABASE = client.get_database()
#
#     @staticmethod
#     def insert(collection, data):
#         return Database.DATABASE[collection].insert(data)
#
#     @staticmethod
#     def insert_many(collection, data_list):
#         return Database.DATABASE[collection].insert_many(data_list)
#
#     @staticmethod
#     def find(collection, query):
#         return Database.DATABASE[collection].find(query)
#
#     @staticmethod
#     def find_ids(collection, query):
#         return Database.DATABASE[collection].find(query, projection={'_id': True})
#
#     @staticmethod
#     def find_one(collection, query):
#         return Database.DATABASE[collection].find_one(query)
#
#     @staticmethod
#     def update(collection, query, data):
#         Database.DATABASE[collection].update(query, data, upsert=True)
#
#     @staticmethod
#     def remove(collection, query):
#         return Database.DATABASE[collection].remove(query)
#
#     @staticmethod
#     def aggregate(collection, queries):
#         return Database.DATABASE[collection].aggregate(queries)

import os
from dataclasses import dataclass
from mongoengine import connect

import pymongo
from pymongo.cursor import Cursor


@dataclass
class Database:
    DATABASE = None
    URI: str = os.environ.get('MONGODB_URI') or "mongodb://127.0.0.1:27017/databunker"

    @classmethod
    def initialize(cls) -> None:
        """
        intializes the connection to the database
        """
        client = connect(host=Database.URI)
        cls.DATABASE = client.get_database()

    @classmethod
    def find(cls, collection: str, query: dict) -> Cursor:
        """
        finds an object given a query from the given collection
        :param collection: str
        :param query: dict
        :return:
        """
        return cls.DATABASE[collection].find(query)

    @classmethod
    def find_one(cls, collection: str, query: dict) -> dict:
        """
        retrieves one objectgiven a query from the given collection
        :param collection: str
        :param query: dict
        :return: dict
        """
        return cls.DATABASE[collection].find_one(query)

    @classmethod
    def remove(cls, collection: str, query: dict) -> Cursor:
        """
        remove an object to the given collection
        :param collection: str
        :param query: dict
        :return: Cursor
        """
        return cls.DATABASE[collection].remove(query)

    @classmethod
    def aggregate(cls, collection: str, queries: list) -> Cursor:
        """
        given the aggregate queries, it retrieves the information form the given collection
        :param collection: str
        :param queries: list
        :return: Cursor
        """
        return cls.DATABASE[collection].aggregate(queries)

    @staticmethod
    def find_ids(collection, query):
        return Database.DATABASE[collection].find(query, projection={'_id': True})

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def insert_many(collection, data_list):
        return Database.DATABASE[collection].insert_many(data_list)
