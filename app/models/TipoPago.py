from app import db

class TipoPago(db.Model):
    idTipoPago = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean, unique=False)