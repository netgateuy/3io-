from app import db

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mes = db.Column(db.String(32), unique=False)
    anio = db.Column(db.String(32), unique=False)
    fechacontratado = db.Column(db.DateTime)
    fechaalta = db.Column(db.DateTime)
    altapor = db.Column(db.String(128), unique=False)
    fechavto = db.Column(db.DateTime)
    fechatope = db.Column(db.DateTime)
    idoportunidad = db.Column(db.Integer, unique=False)
    fechaconfirmado = db.Column(db.DateTime)
    confirmadopor = db.Column(db.String(128), unique=False)
    codigo = db.Column(db.String(32), unique=False)
    fechabaja = db.Column(db.DateTime)
    bajapor = db.Column(db.String(128), unique=False)
    sendmail = db.Column(db.Integer, unique=False)
    comercial = db.Column(db.String(256), unique=False)
    idvendedor = db.Column(db.Integer, unique=False)
    contrato = db.Column(db.Text, unique=False)
    md5 = db.Column(db.String(128), unique=False)
    fechasincronizado = db.Column(db.DateTime)


