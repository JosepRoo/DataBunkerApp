from flask import request, Blueprint, jsonify
from app.models.users.user import User
from app.models.users.errors import UserError

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['POST'])
def login_user():
    try:
        #email = request.form['email']
        #password = request.form['password']
        json = request.json
        email = json['email']
        password = json['password']
        if User.login_valid(email, password):
            return jsonify({'msg_response': "Inicio de sesión exitoso"})
    except UserError as e:
            return jsonify({'msg_response': e.message})


@user_blueprint.route('/get_user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_data = User.get_by_id(user_id)
        user_data_json = user_data.json()
        user_data_json.pop("password")
        return jsonify(user_data_json)
    except UserError as e:
        return jsonify({'msg_response': e.message})


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    try:
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        User.register(email, password, name)
        return jsonify('msg_response', "Registro de usuario {} exitoso".format(email))
    except UserError as e:
        return jsonify({'msg_response': e.message})


'''
@user_blueprint.before_request
def before_request():
    if session.get('email') is None:
        return jsonify(Response(msg_response="Not Logged in").json())
'''
