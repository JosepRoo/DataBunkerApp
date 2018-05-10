from flask_restful import Resource

from app.common.response import Response
from app.models.channels.channels import Channel
from app.models.categories.category import Category
from app.models.brands.brand import Brand
from app.models.products.product import Product
from app.models.elements.errors import ElementErrors


class Element(Resource):
    def get(self, element_type, element_id=None):
        """
        Function to get the data about the element depending the given type and id
        if an element_id is given it return a json array with all the elements of that type
        :param element_type:
        :param element_id:
        :return: elemen_type(Element(element_id)).json()
        """
        element_type_title = element_type.title()
        try:
            element_class = globals()[element_type_title]
            if element_id:
                return {"element": element_class.get_element(element_id).json()}
            return {"elements": [element.json() for element in element_class.get_elements()]}

        except ElementErrors as e:
            return Response(e.message)
