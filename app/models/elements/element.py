from app.common.database import Database
from app.common.utils import Utils
from app.models.basemodel import BaseModel
from app.models.elements.errors import ElementNotFound
from app.models.products.constants import COLLECTION as PRODUCT_COLLECTION
from app.models.brands.constants import COLLECTION as BRAND_COLLECTION
from app.models.categories.constants import COLLECTION as CATEGORY_COLLECTION
from app.models.channels.constants import COLLECTION as CHANNEL_COLLECTION


# clase base de todos los elementos (canales,categorias,marcas,productos y logs)
class Element(BaseModel):
    def __init__(self, name, sub_elements=None, _id=None):
        self.name = name
        self.sub_elements = sub_elements if sub_elements else []  # cuando guade el objeto excluir sub_elements
        BaseModel.__init__(self, _id)

    @classmethod
    def get_sub_elements(cls, _id):
        child_collection = Element.get_collection_by_name(cls.__name__, is_child=True)
        return [cls(**sub_element) for sub_element in Database.find(child_collection, {'parentElementId': _id})]

    def get_average(self):
        class_name = self.__class__.__name__
        if class_name != "Product":
            return Utils.mean(
                [element.get_average() for element in self.get_sub_elements(self.get_collection(), self._id)])
        else:
            return Utils.mean([log.price for log in self.get_sub_elements()])

    @classmethod
    def get_elements(cls):
        collection = Element.get_collection_by_name(cls.__name__)
        return [cls(**element) for element in Database.find(collection, {})]

    @classmethod
    def get_element(cls, element_id):
        collection = Element.get_collection_by_name(cls.__name__)
        element = cls(**Database.find_one(collection, {"_id": element_id}))
        if element:
            return element
        raise ElementNotFound("El elemento con el id y tipo dado no fue encontrado")

    def set_sub_elements(self):
        self.sub_elements = self.__class__.get_sub_elements(True)

    def get_collection(self, is_child=False):
        class_name = self.__class__.__name__
        if is_child:
            if class_name == "Channel":
                collection = CATEGORY_COLLECTION
            elif class_name == "Category":
                collection = BRAND_COLLECTION
            elif class_name == "Brand":
                collection = PRODUCT_COLLECTION
            else:
                collection = ""
        else:
            if class_name == "Channel":
                collection = CHANNEL_COLLECTION
            elif class_name == "Category":
                collection = CATEGORY_COLLECTION
            elif class_name == "Brand":
                collection = BRAND_COLLECTION
            else:
                collection = PRODUCT_COLLECTION

        return collection

    @staticmethod
    def get_collection_by_name(class_name, is_child=False):
        if is_child:
            if class_name == "Channel":
                collection = CATEGORY_COLLECTION
            elif class_name == "Category":
                collection = BRAND_COLLECTION
            elif class_name == "Brand":
                collection = PRODUCT_COLLECTION
            else:
                collection = ""
        else:
            if class_name == "Channel":
                collection = CHANNEL_COLLECTION
            elif class_name == "Category":
                collection = CATEGORY_COLLECTION
            elif class_name == "Brand":
                collection = BRAND_COLLECTION
            else:
                collection = PRODUCT_COLLECTION

        return collection

    @classmethod
    def get_by_name(cls, name):
        collection = Element.get_collection_by_name(cls.__name__)
        element = Database.find_one(collection, {"name": name})
        if element:
            return cls(**element)