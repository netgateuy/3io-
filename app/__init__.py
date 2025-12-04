# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

import pymysql

pymysql.install_as_MySQLdb()

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
# Session initialization
login_manager = LoginManager()

def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    Bootstrap(app)

    from .clients import clients as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/clients')

    from .netgate import netgate as netgate_blueprint
    app.register_blueprint(netgate_blueprint, url_prefix='/netgate')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .application import application as application_blueprint
    app.register_blueprint(application_blueprint, url_prefix='/application')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)



    return app