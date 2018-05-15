from flask import Flask, session, jsonify, request, render_template
from flask_restful import Api

from app.common.database import Database
from app.common.response import Response
from app.resources.company import Company
from app.resources.element import Element, SubElement, ElementValue
from app.resources.user import UserStatus, User
from config import config


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config[config_name])

    # Register our blueprints
    from .default import default as default_blueprint
    app.register_blueprint(default_blueprint)

    api.add_resource(UserStatus, '/userstatus')
    api.add_resource(User, '/user/<string:email>', '/user')
    api.add_resource(Company, '/company', '/company/<string:_id>')
    api.add_resource(Element, '/elements/<string:element_type>', '/elements/<string:element_type>/<string:element_id>')
    api.add_resource(SubElement, '/subelements/<string:element_type>/<string:element_id>')
    api.add_resource(ElementValue,
                     '/elementvalue/<string:element_type>/<string:element_id>/<string:begin_date>/<string:end_date>')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.before_first_request
    def init_db():
        Database.initialize()

    @app.before_request
    def check_login():
        if session.get('email') is None and session.get('_id') is None \
                and request.path != '/userstatus' and request.method != 'POST':
            return default_blueprint.send_static_file('index.html')


    return app
