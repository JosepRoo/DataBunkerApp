from __future__ import annotations
from flask import session
from flask_restful import Resource

from app.common.response import Response
from app.models.elements.subelements.brands.brand import Brand
from app.models.elements.subelements.categories.category import Category
from app.models.elements.channels.channel import Channel
from app.models.elements.errors import ElementErrors
from app.models.privileges.errors import PrivilegeErrors
from app.models.elements.subelements.products.product import Product
from app.models.users.user import User as UserModel


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
                if element_type != "product":
                    return element_class.get_element(element_id).json({"sub_elements"})
                return element_class.get_element(element_id).json({"parentElementId"})
            res = list()
            for element in element_class.get_elements():
                if element_type != "product":
                    res.append(element.json(exclude={"sub_elements"}))
                else:
                    res.append(element.json())
            return res

        except ElementErrors as e:
            return Response(message=e.message).json(), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 401


class SubElement(Resource):
    def get(self, element_type, element_id):
        user = UserModel.get_by_email(session['email'])
        if user is None:
            return Response('No has iniciado sesión '), 401
        element_class = element_type.title()
        child_class = None
        if element_class == "Channel":
            element_class = Channel
            child_class = Category
        elif element_class == "Category":
            element_class = Category
            child_class = Brand
        elif element_class == "Brand":
            element_class = Brand
            child_class = Product
        try:
            if element_class != "Product":
                exclude = {'sub_elements'}
            else:
                exclude = None
            return [sub_element.json(exclude=exclude)
                    for sub_element in element_class.get_sub_elements(element_id, child_class, user)]

        except ElementErrors as e:
            return Response(e.message), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 403


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
    name_to_field = {
        "channel": "greatGrandParentId",
        "category": "grandParentId",
        "brand": "parentElementId",
        "product": "_id"
    }
    @staticmethod
    def get(element_type, element_ids, start_date, end_date):
        """
        Builds a report containing the information of the products that the current user has access to,
        given the id of a
        :return: XLSX report
        """
        try:
            user_id = session.get('_id')
            ids = element_ids.split("&&")
            user = UserModel.get_by_id(user_id)
            params = {
                "product_ids": ids,
                "begin_date": start_date,
                "end_date": end_date,
                "user": user,
                "field_name": BuildProductsReport.name_to_field[element_type]

            }
            return Product.build_products_report(**params)
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
            return Product.build_upc_channels_report(session.get('email')), 200
        except ElementErrors as e:
            return Response(message=e.message).json(), 404
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 401
