from app import Database
from app.models.elements.element import Element
from app.models.logs.log import Log
from app.models.products.constants import COLLECTION


class Product(Element):
    def __init__(self, UPC, name, parentElementId, sub_elements, _id=None):
        Element.__init__(self, name=name, _id=_id)
        self.parentElementId = parentElementId
        self.UPC = UPC
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
