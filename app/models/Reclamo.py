from app import db
from sqlalchemy.dialects.mysql import LONGBLOB

class Reclamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idPais = db.Column(db.String(2), unique=False)
    idCliente = db.Column(db.Integer, unique=False)
    idTipoReclamo = db.Column(db.Integer, unique=False)
    idProductoCliente = db.Column(db.Integer, unique=False)
    obsAlta = db.Column(db.Text)
    fechaAlta = db.Column(db.DateTime)
    altaPor = db.Column(db.String(32), unique=False)
    fechaSolucion = db.Column(db.DateTime)
    solucionPor = db.Column(db.String(32), unique=False)
    idTipoSolucion = db.Column(db.Integer, unique=False)
    obsSolucion = db.Column(db.Text)
    proximoAviso = db.Column(db.DateTime)
    pospuestoPor = db.Column(db.String(32), unique=False)
    idPrioridad = db.Column(db.Integer, unique=False)
    reclamadoPor = db.Column(db.String(32), unique=False)
    idHoras = db.Column(db.Integer, unique=False)
    idMinutos = db.Column(db.Integer, unique=False)
    emailAviso = db.Column(db.String(256), unique=False)
    telefonoAviso = db.Column(db.String(256), unique=False)
    celularAviso = db.Column(db.String(256), unique=False)
    prioridad = db.Column(db.Integer, unique=False)
    whatsapp = db.Column(db.Boolean, unique=False)

class ReclamoAccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idReclamo = db.Column(db.Integer)
    fechaAccion = db.Column(db.DateTime)
    accionPor = db.Column(db.String(32), unique=False)
    idTipoReclamo = db.Column(db.Integer, unique=False)
    idTipoAccion = db.Column(db.Integer, unique=False)
    obsAccion = db.Column(db.Text)
    idHoras = db.Column(db.Integer, unique=False)
    idMinutos = db.Column(db.Integer, unique=False)

class TipoAccionReclamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idTipoReclamo = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    idGRPorigen = db.Column(db.Integer)
    idGRPdestino = db.Column(db.Integer)
    aviso = db.Column(db.Boolean)
    visible = db.Column(db.Boolean)
    mailFrom = db.Column(db.String(256), unique=False)
    mailTo = db.Column(db.String(256), unique=False)


class TipoReclamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificador = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text)
    idGRPorigen = db.Column(db.Integer)
    visible = db.Column(db.Boolean)
    postBaja = db.Column(db.Boolean)

class TipoSolucionReclamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idTipoReclamo = db.Column(db.Integer)
    identificador = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text)
    visible = db.Column(db.Boolean)

class ReclamoHoras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text)

class ReclamoMinutos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text)

class Prioridades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text)

class ReclamoArchivo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idreclamo = db.Column(db.Integer)
    idtipoarchivo = db.Column(db.Integer)
    filename = db.Column(db.String(256), unique=False)
    fechaalta = db.Column(db.DateTime)
    altapor = db.Column(db.String(256), unique=False)
    archivo = db.Column(LONGBLOB)
    observaciones = db.Column(db.Text, unique=False)