from __future__ import annotations
from dataclasses import dataclass

from flask import session
from mongoengine import *
from app.common.database import Database
from app.models.baseModel import BaseModel
from app.models.elements.errors import ElementNotFound
from app.models.elements.subelements.products.constants import COLLECTION as PRODUCT_COLLECTION
from app.models.elements.subelements.brands.constants import COLLECTION as BRAND_COLLECTION
from app.models.elements.subelements.categories.constants import COLLECTION as CATEGORY_COLLECTION
from app.models.elements.channels.constants import COLLECTION as CHANNEL_COLLECTION


# clase base de todos los elementos (canales,categorias,marcas,productos y logs)


@dataclass(init=False)
class Element(BaseModel):
    name: str = StringField(required=True)
    sub_elements: list = ListField(default=lambda: list())
    meta = {'allow_inheritance': True,
            'abstract': True}

    @classmethod
    def get_sub_elements(cls, _id: str, child_class: function, user):
        privileges = user.privileges.get_privilege(child_class, _id)
        child_collection = Element.get_collection_by_name(cls.__name__, is_child=True)
        if privileges == "All":
            return [child_class(**sub_element) for sub_element in
                    Database.find(child_collection, {'parentElementId': _id})]
        return [child_class(**sub_element) for sub_element in
                Database.find(child_collection, {'parentElementId': _id, "_id": {"$in": privileges}})]

    @staticmethod
    def get_average(element_id, begin_date, end_date):
        pass

    @classmethod
    def get_elements(cls):
        collection = Element.get_collection_by_name(cls.__name__)
        from app.models.users.user import User
        user = User.get_by_email(session['email'])
        privileges = user.privileges.get_privilege(cls)
        return [cls(**element) for element in Database.find(collection, {"_id": {"$in": privileges}})]

    @classmethod
    def get_element(cls, element_id):
        collection = Element.get_collection_by_name(cls.__name__)
        element = cls(**Database.find_one(collection, {"_id": element_id}))
        if element:
            return element
        raise ElementNotFound("El elemento con el id y tipo dado no fue encontrado")

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
    def get_by_name(cls, name, parent_id=None):
        collection = Element.get_collection_by_name(cls.__name__)
        if parent_id is not None:
            element = Database.find_one(collection, {"name": name})
        else:
            element = Database.find_one(collection, {"name": name, 'parentElementId': parent_id})
        if element:
            return cls(**element)

    @classmethod
    def get_by_name_and_parent_id(cls, name, parent_element_id):
        collection = Element.get_collection_by_name(cls.__name__)
        element = Database.find_one(collection, {"name": name, "parentElementId": parent_element_id})
        if element:
            return cls(**element)

    @staticmethod
    def get_parent_id_by_child_id(_id, element_type):
        collction = Element.get_collection_by_name(element_type.title())
        parent = Database.find_one(collction, {"_id": _id})
        return parent["parentElementId"]

    def __repr__(self):
        return f"({self.__class__.__name__} id={self._id}, name={self.name})"
