from flask import session
from flask_restful import Resource, reqparse

from app.models.users.errors import UserError
from app.common.response import Response
from app.models.users.user import User as UserModel
from app.models.elements.channels.channel import Channel as ChannelModel
from app.models.users.constants import COLLECTION


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
            return UserModel.login_valid(email, password).json(), 200
        except UserError as e:
            return Response(message=e.message).json(), 401

    def delete(self):
        UserModel.logout()
        return Response(True, "Sesion Finalizada").json(), 200

    def get(self):
        return True if session.get("email") else False


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
    parser.add_argument('name',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('channel_id',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def get(self, email=None):
        _id = session.get('_id')
        email = session.get('email') if email is None else email
        user = None
        if email is not None:
            user = UserModel.get_by_email(email)
        elif _id is not None:
            user = UserModel.get_by_id(_id)
        if user is not None and user.channel_id is not None:
            channel_name = ChannelModel.get_by_id(user.channel_id).json(
                exclude=('sub_elements', '_id')).get('name')
            user_json = user.json(exclude={'password'})
            user_json['channel_name'] = channel_name
            return user_json, 200

        return Response(message='Not Logged In or Data not given').json(), 400

    def put(self, email=None):
        data = User.parser.parse_args()
        email = email if email else data['email']
        user = UserModel.get_by_email(email)
        if data.get('privileges', None):
            user.privileges = data['privileges']
        user.save()
        return user.json(exclude={'password'})

    def post(self, email=None):
        data = User.parser.parse_args()
        try:
            new_user = UserModel.register(data)
            return Response(success=True, message="Registro de usuario {} exitoso".format(new_user.email)).json(), 200
        except UserError as e:
            return Response(message=e.message).json(), 400

    def delete(self, email=None):
        _id = session.get('_id')
        user = None
        if email:
            user = UserModel.get_by_email(email)
        elif _id:
            user = UserModel.get_by_id(_id, COLLECTION)
        if user:
            user.delete()
            return Response(success=True, message='User deleted').json(), 200
        return Response(message='Data not given').json(), 400


class UserFavorites(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id',
                        type=str,
                        required=True
                        )

    def get(self):
        _id = session['_id'] if session.get('_id', None) else None
        if _id:
            user = UserModel.get_by_id(_id, COLLECTION)
            favorites = user.get_favorites()
            return [product.json(["sub_elements", "parentElementId"]) for product in
                    favorites if product] if favorites else favorites, 200
        return Response(message='User Data not given').json(), 400

    def put(self):
        data = UserFavorites.parser.parse_args()
        _id = session['_id'] if session.get('_id', None) else None
        if _id:
            try:
                user = UserModel.get_by_id(_id, COLLECTION)
                product = user.add_favorite(data['product_id'])
                return Response(success=True,
                                message="El producto {} fue agregado a favortios".format(product.name)).json(), 200
            except UserError as e:
                return Response(message=e.message).json(), 400
        return Response(message='User Data not given').json(), 400

    def post(self):
        data = UserFavorites.parser.parse_args()
        _id = session['_id'] if session.get('_id', None) else None
        if _id:
            try:
                user = UserModel.get_by_id(_id, COLLECTION)
                product = user.remove_favorite(data['product_id'])
                return Response(success=True,
                                message="El producto {} fue elminado de favortios".format(product.name)).json(), 200
            except UserError as e:
                return Response(message=e.message).json(), 400

        return Response(message='User Data not given').json(), 400


class UserList(Resource):
    def get(self):
        if session.get('email') is None:
            return Response(message='Not Logged In or Data not given').json(), 401
        elif "data-bunker.com" not in session.get('email'):
            return Response(message='No cuentas con los privilegios para hacer esa peticion').json(), 401
        return [user.json(exclude=('password', 'enterprise_id')) for user in UserModel.objects()]
