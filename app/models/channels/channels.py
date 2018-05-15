import datetime

from app import Database
from app.models.channels.constants import COLLECTION
from app.models.elements.element import Element


class Channel(Element):
    def __init__(self, name, sub_elements=None, _id=None):
        Element.__init__(self, name, sub_elements, _id)

    @staticmethod
    def get_average(element_id, begin_date, end_date):
        first_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        expressions = list()
        expressions.append({'$match': {'_id': element_id}})
        expressions.append(
            {'$lookup': {'from': 'categories', 'localField': '_id', 'foreignField': 'parentElementId',
                         'as': 'categories'}})
        expressions.append({'$unwind': '$categories'})
        expressions.append(
            {'$lookup': {'from': 'brands', 'localField': 'categories._id', 'foreignField': 'parentElementId',
                         'as': 'brands'}})
        expressions.append({'$unwind': '$brands'})
        expressions.append(
            {'$lookup': {'from': 'products', 'localField': 'brands._id', 'foreignField': 'parentElementId',
                         'as': 'products'}})
        expressions.append({'$unwind': '$products'})
        expressions.append({'$unwind': '$products.sub_elements'})
        expressions.append(
            {'$project': {'products.sub_elements.date': 1, 'products.sub_elements.value': 1,
                          'day': {'$dayOfMonth': '$products.sub_elements.date'},
                          'month': {'$month': '$products.sub_elements.date'}}})
        expressions.append({'$match': {'products.sub_elements.date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({'$group': {'_id': '$products.sub_elements.date',
                                       'average': {'$avg': '$products.sub_elements.value'}}})

        result = list(Database.aggregate(COLLECTION, expressions))
        for element in result:
            element["_id"] = element["_id"].strftime("%Y/%m/%d")
        return result
