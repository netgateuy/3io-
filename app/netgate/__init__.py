# app/admin/__init__.py

from flask import Blueprint

netgate = Blueprint('netgate', __name__)

from . import views