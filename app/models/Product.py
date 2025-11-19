from app import db
from sqlalchemy.dialects.mysql import BIT

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=False)
    description = db.Column(db.String(256), unique=False)
    type = db.Column(db.String(256), unique=False)
    visible = db.Column(BIT(1))

class ProductField(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduct = db.Column(db.Integer)
    name = db.Column(db.String(32), unique=False)
    description = db.Column(db.String(256), unique=False)
    type = db.Column(db.String(256), unique=False)
    visible = db.Column(BIT(1))
    pricefilter = db.Column(BIT(1))
    filterby = db.Column(db.Integer)
    regex = db.Column(db.Text, unique=False)
    order = db.Column(db.Integer)

class ProductFieldPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduct = db.Column(db.Integer)
    idField = db.Column(db.Integer)
    visible = db.Column(BIT(1))
    idmoneda = db.Column(db.Integer)
    importe = db.Column(db.Double)
    value = db.Column(db.Text, unique=False)

class ProductFieldValue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduct = db.Column(db.Integer)
    idField = db.Column(db.Integer)
    value = db.Column(db.Text, unique=False)
    idFieldFilter = db.Column(db.Integer) #Por si son combos encadenados - por ahora un nivel
    value = db.Column(db.Text, unique=False)

    # ==============================================================
    # MÉTODO DE CLASE PARA OBTENER LOS VALORES DEL COMBO
    # ==============================================================
    @classmethod
    def get_combo_values(cls, producto_id, field_id):
        """
        Devuelve una lista de strings con los valores de opción
        para un producto y un campo específicos.
        """
        # Consulta que filtra por ambos IDs y ordena los resultados
        valores_obj = cls.query.filter_by(
            idProduct=producto_id,
            idField=field_id
        ).order_by(cls.value).all()

        # Extrae solo la cadena de valor (valor_opcion) de los objetos
        opciones = []
        for v in valores_obj:
            opciones.append({
                'id': v.id,  # El ID que usaremos en la etiqueta 'value' del HTML
                'valor': v.value  # El valor que se mostrará al usuario
            })
        return  opciones

class ProductContract(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idcontract = db.Column(db.Integer, primary_key=True)
    idproduct = db.Column(db.Integer)
    idmoneda = db.Column(db.Integer)
    idperiodo = db.Column(db.Integer)
    importe = db.Column(db.Double)

class ProductClient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idclient  = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, primary_key=True)

class ContractProductFieldValue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduct = db.Column(db.Integer)
    idProductField = db.Column(db.Integer)
    idContract = db.Column(db.Integer)
    value = db.Column(db.Text, unique=False)

class ClientProductFieldValue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduct = db.Column(db.Integer)
    idProductField = db.Column(db.Integer)
    idContract = db.Column(db.Integer)
    value = db.Column(db.Text, unique=False)
