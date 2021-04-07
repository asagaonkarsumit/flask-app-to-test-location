from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.main.config import config_by_name
from flask_caching import Cache

cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)
    app.config.from_object(config_by_name[config_name])

    from main.controller.service import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
