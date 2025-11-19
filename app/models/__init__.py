# coding=utf-8
# app/models.py
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

from flask import session
import hashlib

from werkzeug.security import generate_password_hash, check_password_hash