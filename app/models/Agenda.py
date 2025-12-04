from app import db

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(32), unique=False)
    idoportunidad = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    fechacancelado = db.Column(db.Date)
    fechacompletado = db.Column(db.Date)

class TipoAgenda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean)