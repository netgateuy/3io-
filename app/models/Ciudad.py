from app import db
from sqlalchemy import ForeignKeyConstraint

class Ciudad(db.Model):
    idPais = db.Column(db.String(2), primary_key=True)
    idSubPais = db.Column(db.Integer, primary_key=True)
    idCiudad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), unique=False)
    idCiudadGNS = db.Column(db.Integer, unique=False)
    visible = db.Column(db.Boolean)
    __table_args__ = (
        ForeignKeyConstraint(
            ['idPais'], ['pais.idPais']
        ),
        ForeignKeyConstraint(
            ['idPais', 'idSubPais'], ['sub_pais.idPais', 'sub_pais.idSubPais']
        ),
    )