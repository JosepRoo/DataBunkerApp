from flask import app, request, Blueprint, jsonify

from app.common.response import Response
from app.models.users.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=["POST"])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login()
        return jsonify(Response(success=True, msg_response="Login Successful").json())
    return jsonify(Response(success=False, msg_response="Login Failed").json())


@user_blueprint.route('/get_user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = User.get_by_id(user_id)
    return jsonify(Response(success=True, records=1, data=user_data.json(), msg_response="").json())
