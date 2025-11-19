# app/admin/__init__.py

from flask import Blueprint

clients = Blueprint('clients', __name__)

from . import views