# coding: utf-8
from . import clients
from flask_login import login_required

@clients.route('/')
def index():
    try:
        return "Netgate API For Clients 3io.netgate.com.uy"
    except Exception as e:
        return str(e)


@clients.route('/contratos')
@login_required
def contratos():
    try:
        return "Netgate contratos"
    except Exception as e:
        return str(e)
