# app/admin/__init__.py

from flask import Blueprint

ia = Blueprint('ia', __name__)

from . import views