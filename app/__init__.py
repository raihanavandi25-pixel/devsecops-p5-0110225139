"""Application factory untuk Task Tracker."""
from flask import Flask

from . import models
from .config import Config
from .routes import bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    models.init_db(app.config["DATABASE"])
    app.register_blueprint(bp)
    return app
