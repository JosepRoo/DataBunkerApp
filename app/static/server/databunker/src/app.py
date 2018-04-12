from flask import Flask, session, request, jsonify
from server.databunker.src.common.database import Database
from server.databunker.src.models.user import User

app = Flask(__name__)
app.secret_key = "D4t4Bunk3r"

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    passwrod = request.form['password']

    if User.login_valid(email, passwrod):
        User.login(email)
        return {"success": True, "msgResponse":" Login Successful"}
    session['email'] = None
    return {"success":False,"msgResponse":"Login Failed, Email or Password Incorrect"}


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    passwrod = request.form['password']
    name = request.form['name']

    if not User.register(email, passwrod, name):
        return jsonify({"success": False, "msgResponse": "Registration Failed, email already registered"})
    return jsonify({"success": True, "msgResponse": "Registration Succesful", "id": session["_id"]})




if __name__ == '__main__':
    app.run()

