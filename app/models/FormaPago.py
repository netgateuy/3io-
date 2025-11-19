from app import db
from sqlalchemy import ForeignKeyConstraint

class FormaPago(db.Model):
    idTipoPago = db.Column(db.Integer, primary_key=True)
    idFormaPago = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(32), unique=False)
    visible = db.Column(db.Boolean, unique=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['idTipoPago'], ['tipo_pago.idTipoPago']
        ),
    )