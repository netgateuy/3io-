from app import db

class Pais(db.Model):
    idPais = db.Column(db.String(2), primary_key=True)
    nombre = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean)
    idPaisGNS = db.Column(db.Integer, unique=False)