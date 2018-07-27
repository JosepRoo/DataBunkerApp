from flask import session
from flask_restful import Resource, reqparse

from app.common.response import Response
from app.models.brands.brand import Brand
from app.models.categories.category import Category
from app.models.channels.channels import Channel
from app.models.elements.errors import ElementErrors
from app.models.privileges.errors import PrivilegeErrors
from app.models.products.product import Product


class Element(Resource):
    def get(self, element_type, element_id=None):
        """
        Function to get the data about the element depending the given type and id
        if an element_id is given it return a json array with all the elements of that type
        :param element_type:
        :param element_id:
        :return: elemen_type(Element(element_id)).json() || List(elemen_type(Element(element_id)).json())
        """
        element_type_title = element_type.title()
        try:
            element_class = globals()[element_type_title]
            if element_id:
                return element_class.get_element(element_id).json(
                    ("sub_elements",)) if element_type != "product" else element_class.get_element(
                    element_id).json("parentElementId")
            return [element.json(("sub_elements",)) if element_type != "product" else element.json() for element in
                    element_class.get_elements()]

        except ElementErrors as e:
            return Response(message=e.message).json(), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 401


class SubElement(Resource):
    def get(self, element_type, element_id):
        element_type_title = element_type.title()
        child_class = None
        if element_type_title == "Channel":
            child_class = globals()["Category"]
        elif element_type_title == "Category":
            child_class = globals()["Brand"]
        elif element_type_title == "Brand":
            child_class = globals()["Product"]
        try:
            element_class = globals()[element_type_title]
            return [sub_element.json(("sub_elements",))
                    if element_type != "product"
                    else sub_element.json() for sub_element in
                    element_class.get_sub_elements(element_id, child_class)]

        except ElementErrors as e:
            return Response(e.message), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 401


class ElementValue(Resource):
    def get(self, element_type, element_id, begin_date, end_date):
        res = None
        if element_type == "channel":
            res = Channel.get_average(element_id, begin_date, end_date)
        elif element_type == "category":
            res = Category.get_average(element_id, begin_date, end_date)
        elif element_type == "brand":
            res = Brand.get_average(element_id, begin_date, end_date)
        elif element_type == "product":
            res = Product.get_average(element_id, begin_date, end_date)

        return res


class BuildProductsReport(Resource):
    @staticmethod
    def get(element_type, element_ids, start_date, end_date):
        """
        Builds a report containing the information of the products that the current user has access to,
        given the id of a
        :return: XLSX report
        """
        try:
            ids = element_ids.split("&&")
            if element_type == "channel":
                return Product.build_products_report(ids, start_date, end_date, "greatGrandParentId").json(), 200
            elif element_type == "category":
                return Product.build_products_report(ids, start_date, end_date, "grandParentId").json(), 200
            elif element_type == "brand":
                return Product.build_products_report(ids, start_date, end_date, "parentElementId").json(), 200
            elif element_type == "product":
                return Product.build_products_report(ids, start_date, end_date, "_id").json(), 200
        except ElementErrors as e:
            return Response(message=e.message).json(), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 401


class BuildComparatorTable(Resource):
    @staticmethod
    def get():
        """
        Builds a table comparing the prices of different products that the current user has access to,
        with other prices of other channels
        :return: Comparator Table
        """
        try:
            return Product.build_upc_channels_report(), 200
        except ElementErrors as e:
            return Response(message=e.message).json(), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 401