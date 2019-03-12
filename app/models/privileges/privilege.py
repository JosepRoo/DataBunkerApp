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
            channels = list()
            if self.channels:
                channels += self.channels
            if self.categories:
                cats_parents = list({cat.parenElementId._id for cat in Category.objects(_id__in=self.categories)})
                channels += [ch._id for ch in Channel.objects(_id__in=cats_parents)]
            if self.brands:
                brand_parents = list({br.grandParentId._id for br in Brand.objects(_id__in=self.brands)})
                channels += [ch._id for ch in Channel.objects(_id__in=brand_parents)]
            if self.products:
                pr_parents = list({pr.greatGrandParentId._id for pr in Product.objects(_id__in=self.products)})
                channels += [ch._id for ch in Channel.objects(_id__in=pr_parents)]
            if not channels:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            channels = list(set(channels))
            return channels
        if element_type is Category:
            categories = list()
            if parent_id in self.channels:
                return "All"
            if self.categories:
                categories += [cat._id for cat in Category.objects(_id__in=self.categories, parentElementId=parent_id)]
            if self.brands:
                brand_parents = list({br.parentElementId._id for br in Brand.objects(_id__in=self.brands)})
                categories += [cat._id for cat in Category.objects(_id__in=brand_parents, parentElementId=parent_id)]
            if self.products:
                pr_parents = list({pr.grandParentId._id for pr in Product.objects(_id__in=self.products)})
                categories += [cat._id for cat in Category.objects(_id__in=pr_parents, parentElementId=parent_id)]
            if not categories:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            categories = list(set(categories))
            return categories
        if element_type is Brand:
            category = Category.get_by_id(parent_id)
            channel_id = category.parentElementId._id
            brands = list()
            if channel_id in self.channels or category._id in self.categories:
                return "All"
            if self.brands:
                brands += [br._id for br in Brand.objects(_id__in=self.brands, parentElementId=parent_id)]
            if self.products:
                pr_parents = list({pr.ParentElementId._id for pr in Product.objects(id__in=self.products)})
                brands += [br._id for br in Brand.objects(_id__in=pr_parents, parentElementId=parent_id)]
            if not brands:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            brands = list(set(brands))
            return brands
        if element_type is Product:
            brand = Brand.get_by_id(parent_id)
            category_id = brand.parentElementId._id
            channel_id = brand.grandParentId._id
            products = list()
            if brand._id in self.brands or category_id in self.categories or channel_id in self.channels:
                return "All"
            if self.products:
                products += [pr._id for pr in Product.objects(id__in=self.products, parentElementId=parent_id)]
            if not products:
                raise PrivilegeDoesNotExist("No se tiene el privilegio para ver este elemento")
            return products
