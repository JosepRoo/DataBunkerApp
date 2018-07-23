from flask import session
from flask_restful import Resource, reqparse

from app import Response
from app.models.privileges.errors import PrivilegeErrors
from app.models.users.user import User


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
    parser.add_argument('target_user_mail',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def put(self):
        data = Privilege.parser.parse_args()
        if not session.get('email') or 'data-bunker' not in session.get('email'):
            return Response(message="No tienes los privilegios para modificar privilegios").json(), 401
        user = User.get_by_email(data['target_user_mail'])
        try:
            return user.add_privilege(data['element_type'], data['element']), 200
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 400

    def delete(self):
        if 'data-bunker' not in session['email']:
            return Response(message="No tienes los privilegios para modificar privilegios"), 401
        data = Privilege.parser.parse_args()
        user = User.get_by_email(data['target_user_mail'])
        try:
            return user.remove_privilege(data['element_type'], data['element']), 200
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 400

    def get(self, target_user_mail):
        user = User.get_by_email(target_user_mail)
        try:
            return user.privileges.json(), 200
        except PrivilegeErrors as e:
            return Response(message=e.message).json(), 400
