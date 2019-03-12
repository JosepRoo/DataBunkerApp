import uuid
from dataclasses import dataclass

from mongoengine import *

from app.common.tree import Tree
from app.models.baseEmbeddedDocument import BaseEmbeddedDocument
from app.models.elements.channels.channel import Channel
from app.models.elements.subelements.brands.brand import Brand
from app.models.elements.subelements.categories.category import Category
from app.models.elements.subelements.products.product import Product
from app.models.privileges.errors import WrongElementType, WrongPrivilegeAssignment, PrivilegeDoesNotExist


@dataclass(init=False)
class Privilege(BaseEmbeddedDocument):
    _id: StringField = StringField(primary_key=True, default=lambda: uuid.uuid4().hex)
    privilege_tree: Tree = DictField(default={})
    channels: list = ListField(default=[])
    categories: list = ListField(default=[])
    brands: list = ListField(default=[])
    products: list = ListField(default=[])

    def add_remove_privilege(self, element_type, element_to_add, action=True):
        """
        Function to add a privilege to the privilege tree of a user
        """
        elements_types = {"channel": (Channel, self.channels),
                          "category": (Category, self.categories),
                          "brand": (Brand, self.brands),
                          "product": (Product, self.products)}
        element, priv_list = elements_types.get(element_type, (None, None))
        if not element or not element.get_by_id(element_to_add):
            raise WrongPrivilegeAssignment(f"El elemento de tipo {element_type} con id {element_to_add} no existe")
        if action:
            if element in priv_list:
                raise WrongPrivilegeAssignment(
                    f"El elemento de tipo {element_type} con id {element_to_add} ya fue agregado")
            # priv_list.append(element_to_add)
        else:
            if element not in priv_list:
                return self
            priv_list.remove(element_to_add)
        return self

    def get_privilege(self, element_type: type, parent_id=None):
        """
        Function to find if given an element_id it is on the user privileges
        :param element_type: parameter to know the type of element we are searching for
        :param parent_id:
        :return: returns the _id of the elements
        """
        if element_type is Channel:
            if not self.channels:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            return self.channels
        if element_type is Category:
            if parent_id in self.channels:
                return "All"
            if not self.categories:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            return self.categories
        if element_type is Brand:
            category = Category.get_by_id(parent_id)
            channel_id = category.parentElementId._id
            if channel_id in self.channels or category._id in self.categories:
                return "All"
            if not self.brands:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            return self.brands
        if element_type is Product:
            brand = Brand.get_by_id(parent_id)
            category_id = brand.parentElementId._id
            channel_id = brand.grandParentId._id
            if brand._id in self.brands or category_id in self.categories or channel_id in self.channels:
                return "All"
            if not self.products:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            return self.products
