from flask import Flask

from app.common.database import Database
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.before_first_request
    def init_db():
        Database.initialize()

    # Register our blueprints
    from .default import default as default_blueprint
    from app.models.users.views import user_blueprint
    app.register_blueprint(default_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/users')
    return app
