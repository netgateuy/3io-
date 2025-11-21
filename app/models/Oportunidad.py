from app import db
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.mysql import LONGBLOB


class Oportunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idtipo = db.Column(db.Integer)
    fechaalta = db.Column(db.DateTime)
    fechacancelado = db.Column(db.DateTime)
    fechainicio = db.Column(db.Date)
    fechafin = db.Column(db.Date)
    idcliente = db.Column(db.Integer, unique=False)
    responsable = db.Column(db.Integer, unique=False)
    estado = db.Column(db.String(256), unique=False)


class ArchivoOportunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idoportunidad = db.Column(db.Integer)
    idtipoarchivo = db.Column(db.Integer)
    filename = db.Column(db.String(256), unique=False)
    fechaalta = db.Column(db.DateTime)
    altapor = db.Column(db.String(256), unique=False)
    archivo = db.Column(LONGBLOB)
    observaciones = db.Column(db.Text, unique=False)

class TipoArchivo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), unique=False)
    abreviacion = db.Column(db.String(256), unique=False)
    idexterno = db.Column(db.String(256), unique=False)
    visible = db.Column(db.Boolean)

class AccionOportunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idoportunidad = db.Column(db.Integer)
    idtipoaccion = db.Column(db.Integer)
    altapor = db.Column(db.String(256), unique=False)
    fechaalta = db.Column(db.DateTime)
    accion = db.Column(db.Text, unique=False)

class TipoAccion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text, unique=False)
    visible = db.Column(db.Boolean)
    responsable = db.Column(db.Integer, unique=False)

class TipoOportunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text, unique=False)
    visible = db.Column(db.Boolean)

class EstadoOportunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idoportunidad = db.Column(db.Integer)
    idtipoportunidad = db.Column(db.Integer, unique=False)
    idetapaoportunidad = db.Column(db.Integer, unique=False)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text, unique=False)
    fechaalta = db.Column(db.DateTime)
    fecharealizado = db.Column(db.DateTime)
    predecesor = db.Column(db.Integer, unique=False)
    notificar = db.Column(db.String(4096), unique=False)
    sectorresponsable = db.Column(db.Integer, unique=False)
    icono = db.Column(db.String(256), unique=False)
    uri = db.Column(db.String(4096), unique=False)
    fechanotificado = db.Column(db.DateTime)
    notifica = db.Column(db.Boolean)
    automatica = db.Column(db.Boolean)

class EtapaOportunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idtipoportunidad = db.Column(db.Integer, unique=False)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text, unique=False)
    predecesor = db.Column(db.Integer, unique=False)
    sectorresponsable = db.Column(db.Integer, unique=False)
    notificar = db.Column(db.String(4096), unique=False)
    icono = db.Column(db.String(256), unique=False)
    uri = db.Column(db.String(4096), unique=False)
    fechanotificado = db.Column(db.DateTime)
    notifica = db.Column(db.Boolean)
    automatica = db.Column(db.Boolean)

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.Text, unique=False)

