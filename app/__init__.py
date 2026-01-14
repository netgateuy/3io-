# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_session import Session

import pymysql

pymysql.install_as_MySQLdb()

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
# Session initialization
login_manager = LoginManager()

# JWTManager
jwt = JWTManager()

def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.config["JWT_SECRET_KEY"] = "cc38ac85979fb0ef6145be495ba1a2982925ba53c62fc64f"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
    jwt.init_app(app)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"  # Se guarda en una carpeta temporal del servidor
    Session(app)

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

    from .ia import ia as ia_blueprint
    app.register_blueprint(ia_blueprint, url_prefix='/ia')



    return app