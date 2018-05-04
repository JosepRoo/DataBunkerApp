from flask import session
from flask_restful import Resource, reqparse

from app.models.users.errors import UserError
from app.common.response import Response
from app.models.users.user import User as UserModel


class UserStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        try:
            data = UserStatus.parser.parse_args()
            email = data['email']
            password = data['password']
            if UserModel.login_valid(email, password):
                return Response(True, "Inicio de Sesion exitoso").json(), 200
        except UserError as e:
            return Response(message=e.message).json(), 401

    def delete(self):
        UserModel.logout()
        return Response(True, "Sesion Finalizada").json(), 200


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('privileges',
                        type=str,
                        required=False
                        )
    parser.add_argument('email',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('_id',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('enterprise_id',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    def get(self, email=None):
        _id = session['_id'] if session.get('_id', None) else None
        if email:
            return UserModel.get_by_email(email).json(), 200
        if _id:
            return UserModel.get_by_id(_id).json(), 200
        return Response(message='Not Logged In or Data not given').json(), 400

    def put(self, email=None):
        data = User.parser.parse_args()
        email = email if email else data['email']
        user = UserModel.get_by_email(email)
        if data.get('privileges', None):
            user.privileges = data['privileges']
        user.update_user()
        return user.json()

    def post(self, email=None):
        data = User.parser.parse_args()
        try:
            new_user = UserModel.register(data)
            return Response(success=True, message="Registro de usuario {} exitoso".format(new_user.email)).json(), 200
        except UserError as e:
            return Response(message=e.message).json(), 400

    def delete(self, email=None):
        _id = session['_id'] if session.get('_id', None) else None
        user = None
        if email:
            user = UserModel.get_by_email(email)
        if _id:
            user = UserModel.get_by_id(_id)
        if user:
            user.delete_user()
            return Response(success=True, message='User deleted').json(), 200
        return Response(message='Data not given').json(), 400