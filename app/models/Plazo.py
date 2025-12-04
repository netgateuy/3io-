from app import db

class Plazo(db.Model):
    idPlazo = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean, unique=False)