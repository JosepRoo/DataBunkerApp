from flask import request, Blueprint, jsonify
from app.models.users.user import User
from app.models.users.errors import UserError
user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=["POST"])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login()
        return jsonify({'msg_response':"Login Successful"})
    return jsonify({'msg_response':"Login Failed"})


@user_blueprint.route('/get_user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_data = User.get_by_id(user_id)
        user_data_json = user_data.json()
        user_data_json.pop("password")
        return jsonify(user_data_json)
    except UserError as e:
        return jsonify({'msg_response': e.message})


'''
@user_blueprint.before_request
def before_request():
    if session.get('email') is None:
        return jsonify(Response(msg_response="Not Logged in").json())
'''