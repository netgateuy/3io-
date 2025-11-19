from app import db

class Sucursal(db.Model):
    idPais = db.Column(db.String(2), primary_key=True)
    idSucursal = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), unique=False)