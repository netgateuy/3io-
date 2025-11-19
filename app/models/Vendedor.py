from app import db

class Vendedor(db.Model):
    idVendedor = db.Column(db.Integer, primary_key=True)
    idGrupoVendedor = db.Column(db.Integer)
    nombre = db.Column(db.String(32))
    contacto = db.Column(db.String(32))
    email = db.Column(db.String(512))
    telefono = db.Column(db.String(256))
    celular = db.Column(db.String(256))
    cedula = db.Column(db.String(256))
    agente = db.Column(db.String(256))
    interno = db.Column(db.String(256))
    visible = db.Column(db.Boolean)