# -*- coding: UTF-8 -*-


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from app.controllers import product
    from app.views import main

    api_version = app.config['API_VERSION']

    app.register_blueprint(product.ProductController(scope=api_version, element_name='product').blueprint)
    app.register_blueprint(main)

    return app
