# app/admin/__init__.py

from flask import Blueprint

application = Blueprint('application', __name__)

from . import views