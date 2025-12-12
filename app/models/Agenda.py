from app import db

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(32), unique=False)
    idoportunidad = db.Column(db.Integer)
    idtipoagenda = db.Column(db.Integer)
    idcliente = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    fechacancelado = db.Column(db.Date)
    fechacompletado = db.Column(db.Date)
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    notas = db.Column(db.Text)
    direccion = db.Column(db.Text)

class TipoAgenda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(256), unique=False)
    descripcion = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean)