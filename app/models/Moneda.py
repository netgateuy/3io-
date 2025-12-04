from app import db

class Moneda(db.Model):
    idMoneda = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(32), unique=False)
    abreviacion = db.Column(db.String(32), unique=False)
    idExterno = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean, unique=False)