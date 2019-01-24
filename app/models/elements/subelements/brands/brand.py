from __future__ import annotations
import datetime
from dataclasses import dataclass
from mongoengine import *
from app.common.database import Database
from app.models.elements.channels.channel import Channel
from app.models.elements.subelements.brands.constants import COLLECTION
from app.models.elements.subelements.categories.category import Category
from app.models.elements.subelements.products.constants import COLLECTION as PRODUCTS_COLLECTION
from app.models.elements.subelements.subelement import SubElement


@dataclass(init=False)
class Brand(SubElement):
    parentElementId: Category = ReferenceField("Category", required=True)
    grandParentId: Channel = ReferenceField("Channel", required=True)
    sub_elements: list = ListField(ReferenceField("Product"), default=lambda: list())
    meta = {'collection': COLLECTION}

    @staticmethod
    def get_average(element_id, begin_date, end_date):
        first_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        last_date = last_date + datetime.timedelta(days=1)
        expressions = list()
        expressions.append({'$match': {'parentElementId': element_id}})
        expressions.append({'$unwind': '$sub_elements'})
        expressions.append(
            {'$project': {'sub_elements.date': 1, 'sub_elements.value': 1,
                          'day': {'$dayOfMonth': '$sub_elements.date'},
                          'month': {'$month': '$sub_elements.date'}}})
        expressions.append({'$match': {'sub_elements.date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({'$group': {'_id': '$sub_elements.date',
                                       'average': {'$avg': '$sub_elements.value'}}})
        expressions.append({'$sort': {'_id': 1}})

        result = list(Database.aggregate(PRODUCTS_COLLECTION, expressions))
        for element in result:
            element["_id"] = element["_id"].strftime("%Y/%m/%d")
        return result
