from app import db

class SubPais(db.Model):
    idPais = db.Column(db.String(2), db.ForeignKey('pais.idPais'), primary_key=True)
    idSubPais = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), unique=False)
    idSubPaisGNS = db.Column(db.Integer, unique=False)
    visible = db.Column(db.Boolean, unique=False)