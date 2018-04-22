from flask import Flask

from app.common.database import Database
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register our blueprints
    from .default import default as default_blueprint
    from app.models.users.views import user_blueprint
    app.register_blueprint(default_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/users')

    Database.initialize()
    return app
