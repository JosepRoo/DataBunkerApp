import datetime

from app import Database
from app.models.elements.element import Element
from app.models.elements.errors import ElementNotFound
from app.models.logs.log import Log
from app.models.products.constants import COLLECTION


class Product(Element):
    def __init__(self, UPC, name, parentElementId, sub_elements, image=None, _id=None, grandParentId=None, greatGrandParentId=None):
        Element.__init__(self, name=name, _id=_id)
        self.parentElementId = parentElementId
        self.grandParentId = grandParentId
        self.greatGrandParentId = greatGrandParentId
        self.UPC = UPC
        self.image = image
        self.sub_elements = [Log(**sub_element) for sub_element in sub_elements]

    @classmethod
    def get_by_UPC(cls, upc):
        product = Database.find_one(COLLECTION, {'UPC': upc})
        if product:
            return cls(**product)

    def is_duplicated_date(self, new_date):
        if list(filter(lambda x: x.date == new_date, self.sub_elements)):
            return True
        return False

    @staticmethod
    def get_average(element_id, begin_date, end_date):
        first_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        last_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        last_date = last_date + datetime.timedelta(days=1)
        expressions = list()
        expressions.append({'$match': {'_id': element_id}})
        expressions.append({'$unwind': '$sub_elements'})
        expressions.append(
            {'$project': {'sub_elements.date': 1, 'sub_elements.value': 1,
                          'day': {'$dayOfMonth': '$sub_elements.date'},
                          'month': {'$month': '$sub_elements.date'}}})
        expressions.append({'$match': {'sub_elements.date': {'$gte': first_date, '$lte': last_date}}})
        expressions.append({'$group': {'_id': '$sub_elements.date',
                                       'average': {'$avg': '$sub_elements.value'}}})

        result = list(Database.aggregate(COLLECTION, expressions))
        for element in result:
            element["_id"] = element["_id"].strftime("%Y/%m/%d")
        return result

    @classmethod
    def get_element(cls, element_id):
        collection = Element.get_collection_by_name(cls.__name__)
        element = cls(**Database.find_one(collection, {"_id": element_id}))
        if element:
            element.sub_elements = [element.sub_elements[-2], element.sub_elements[-1]]
            return element
        raise ElementNotFound("El elemento con el id y tipo dado no fue encontrado")
