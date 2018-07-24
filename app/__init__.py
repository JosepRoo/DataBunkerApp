import datetime
from flask import Flask, session, jsonify, request, url_for
from flask_compress import Compress
from flask_restful import Api
from werkzeug.utils import redirect

from app.common.database import Database
from app.common.response import Response
from app.resources.company import Company
from app.resources.element import Element, SubElement, ElementValue
from app.resources.privilege import Privilege
from app.resources.uploadData import UploadData
from app.resources.user import UserStatus, User, UserFavorites
from config import config


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config[config_name])
    Compress(app)
    # Register our blueprints
    from .default import default as default_blueprint, groupon
    app.register_blueprint(default_blueprint)
    app.register_blueprint(groupon, url_prefix="/groupon")

    api.add_resource(UserStatus, '/userstatus')
    api.add_resource(User, '/user/<string:email>', '/user')
    api.add_resource(Company, '/company', '/company/<string:_id>')
    api.add_resource(Element, '/elements/<string:element_type>', '/elements/<string:element_type>/<string:element_id>')
    api.add_resource(SubElement, '/subelements/<string:element_type>/<string:element_id>')
    api.add_resource(ElementValue,
                     '/elementvalue/<string:element_type>/<string:element_id>/<string:begin_date>/<string:end_date>')
    api.add_resource(UserFavorites, '/user/favorites')
    api.add_resource(Privilege, '/user/privilege', '/user/privilege/<string:target_user_mail>')
    api.add_resource(UploadData, '/uploaddata')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.before_first_request
    def init_db():
        Database.initialize()
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(days=7)

    @app.before_request
    def check_login():
        print(request.path)
        apiCall = request.path.lstrip('/').split('/')[0]
        apiCalls = ['company', 'user', 'elements', 'subelements', 'elementvalue']
        if session.get('email') is None and session.get('_id') is None and apiCall in apiCalls:
            if apiCall != 'user' and request.method != 'POST':
                return redirect('/#/screen')

    return app
