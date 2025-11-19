from app import db

class Barrio(db.Model):
    idPais = db.Column(db.String(2), db.ForeignKey('Pais.idPais'), primary_key=True)
    idSubPais = db.Column(db.Integer, db.ForeignKey('SubPais.idSubPais'), primary_key=True)
    idCiudad = db.Column(db.Integer,db.ForeignKey('Ciudad.idCiudad'), primary_key=True)
    idBarrio = db.Column(db.String(256),  primary_key=True)
    idCiudadGNS = db.Column(db.Integer, unique=False)