from app import db

class Equipo(db.Model):
    idequipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idtipoequipo = db.Column(db.Integer)
    idmarca = db.Column(db.Integer)
    idmodelo = db.Column(db.Integer)
    idproveedor = db.Column(db.Integer)
    idfamilia = db.Column(db.Integer)
    fechaalta = db.Column(db.DateTime)
    altapor = db.Column(db.String(128))
    fechabaja = db.Column(db.DateTime)
    bajapor  = db.Column(db.String(128))
    nroserie = db.Column(db.String(2056), unique=False)
    fechaasignado = db.Column(db.DateTime)
    asignadopor = db.Column(db.String(128))
    idcliente = db.Column(db.Integer)
    observacion = db.Column(db.Text)
    notas = db.Column(db.Text)
    fechaadquisicion = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'idequipo': self.idequipo,
            'idtipoequipo': self.idtipoequipo,
            'idmarca': self.idmarca,
            'idmodelo': self.idmodelo,
            'idproveedor': self.idproveedor,
            'idfamilia': self.idfamilia,
            'fechaalta': self.fechaalta,
            'altapor': self.altapor,
            'fechabaja': self.fechabaja,
            'nroserie': self.nroserie,
            'fechasignado': self.fechasignado,
            'asignadopor': self.asignadopor,
            'idcliente': self.idcliente,
            'observacion': self.observacion,
            'fechaadquisicion': self.fechaadquisicion
        }

class Marca(db.Model):
    idMarca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idtipoequipo = db.Column(db.Integer)
    marca = db.Column(db.String(512))
    visible = db.Column(db.Boolean)
    fechaalta = db.Column(db.DateTime)
    altapor =  db.Column(db.String(128))
    fechamodificado = db.Column(db.DateTime)
    modificadopor = db.Column(db.String(128))
    idgarantia = db.Column(db.Integer)
    observacion = db.Column(db.Text)

    def to_dict(self):
        return {
            'idmarca': self.idMarca,
            'idtipoequipo': self.idtipoequipo,
            'marca': self.marca,
            'visible': self.visible,
            'fechaalta': self.fechaalta,
            'altapor': self.altapor,
            'fechamodificado': self.fechamodificado,
            'modificadopor': self.modificadopor,
            'idgarantia': self.idgarantia,
            'observacion': self.observacion,
        }

class Modelo(db.Model):
    idmodelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMarca = db.Column(db.Integer)
    idtipoequipo = db.Column(db.Integer)
    modelo = db.Column(db.String(512))
    visible = db.Column(db.Boolean)
    fechaalta = db.Column(db.DateTime)
    altapor =  db.Column(db.String(128))
    fechamodificado = db.Column(db.DateTime)
    modificadopor = db.Column(db.String(128))
    idgarantia = db.Column(db.Integer)
    observacion = db.Column(db.Text)
    idmoneda = db.Column(db.Integer)
    precio = db.Column(db.DECIMAL(10, 2))
    idmonedacompra = db.Column(db.Integer)
    precioCompra = db.Column(db.DECIMAL(10, 2))

    def to_dict(self):
        return {
            'idmodelo': self.idmodelo,
            'idMarca': self.idMarca,
            'idtipoequipo': self.idtipoequipo,
            'modelo': self.modelo,
            'visible': self.visible,
            'fechaalta': self.fechaalta,
            'altapor': self.altapor,
            'fechamodificado': self.fechamodificado,
            'modificadopor': self.modificadopor,
            'idgarantia': self.idgarantia,
            'observacion': self.observacion,
            'idmoneda': self.idmoneda,
            'precio': self.precio,
            'idmonedacompra': self.idmonedacompra,
            'precioCompra': self.precioCompra,
        }

class Proveedor(db.Model):
    idProveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedor = db.Column(db.String(512))
    observacion = db.Column(db.Text)
    visible = db.Column(db.Boolean)
    fechaalta = db.Column(db.DateTime)
    altapor = db.Column(db.String(128))
    fechamodificado = db.Column(db.DateTime)
    modificadopor = db.Column(db.String(128))

    def to_dict(self):
        return {
            'idproveedor': self.idProveedor,
            'proveedor': self.proveedor,
            'observacion': self.observacion,
            'visible': self.visible,
            'fechaalta': self.fechaalta,
        }

class EquipoTipo(db.Model):
    idTipoEquipo = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(512))
    observacion = db.Column(db.Text)
    visible = db.Column(db.Boolean)
    idEquipoFamilia = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {
            'idTipoEquipo': self.idTipoEquipo,
            'descripcion': self.descripcion,
            'observacion': self.observacion,
            'visible': self.visible,
            'idEquipoFamilia': self.idEquipoFamilia
        }

class EquipoContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idEquipo = db.Column(db.Integer)
    idProductContract = db.Column(db.Integer)
    idOportunidad = db.Column(db.Integer)
    fechaalta = db.Column(db.DateTime)
    altapor = db.Column(db.String(128))

class EquipoFamilia(db.Model):
    idEquipoFamilia = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(512))
    observacion = db.Column(db.Text)
    visible = db.Column(db.Boolean)

    def to_dict(self):
        return {
            'idEquipoFamilia': self.idEquipoFamilia,
            'descripcion': self.descripcion,
            'observacion': self.observacion,
            'visible': self.visible,
        }