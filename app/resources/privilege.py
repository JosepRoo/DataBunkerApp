from flask import session
from flask_restful import Resource, reqparse

from app import Response
from app.models.privileges.errors import PrivilegeErrors
from app.models.users.user import User
from app.models.users.constants import COLLECTION as USERCOLLECTION


class Privilege(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('element_type',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('element',
                        type=dict,
                        required=True,
                        help="This field cannot be blank."
                        )

    def put(self):
        data = Privilege.parser.parse_args()
        user = User.get_by_id(session['_id'], USERCOLLECTION)
        try:
            return user.add_privilege(data['element_type'], data['element']), 200
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 400

    def delete(self):
        data = Privilege.parser.parse_args()
        user = User.get_by_id(session['_id'], USERCOLLECTION)
        try:
            return user.remove_privilege(data['element_type'], data['element']), 200
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 400

    def get(self):
        user = User.get_by_id(session['_id'], USERCOLLECTION)
        try:
            return user.privileges.json(), 200
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 400