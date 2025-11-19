from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idPais = db.Column(db.String(32), unique=False) #Paises
    idCliente = db.Column(db.Integer, unique=True) #SubPaises
    idSucursal = db.Column(db.String(32), unique=False) #Sucursales
    cliNombre = db.Column(db.String(2056), unique=False)
    cliApellido = db.Column(db.String(2056), unique=False)
    cliRazon = db.Column(db.String(2056), unique=False)
    cliFantasia = db.Column(db.String(2056), unique=False)
    idTipoID = db.Column(db.String(16), unique=False)
    nroID = db.Column(db.Integer, unique=False)
    idPais1 = db.Column(db.String(2), unique=False) #Paises
    idSubPais = db.Column(db.Integer, unique=False) #SubPaises
    idCiudad = db.Column(db.Integer, unique=False) #Ciudades
    idBarrio = db.Column(db.Integer, unique=False) #Barrios
    Calle = db.Column(db.String(2056), unique=False)
    nroPuerta = db.Column(db.String(128), unique=False)
    Apto = db.Column(db.String(128), unique=False)
    CodigoPostal = db.Column(db.String(128), unique=False)
    Telefono = db.Column(db.String(256), unique=False)
    Celular = db.Column(db.String(256), unique=False)
    idTipoPago = db.Column(db.Integer, unique=False) #TipoPago
    idFormaPago = db.Column(db.Integer, unique=False) #FormaPago
    eMailAviso = db.Column(db.String(2056), unique=False)
    idVendedor = db.Column(db.Integer, unique=False) #Vendedores
    FechaAlta = db.Column(db.DateTime)
    FechaBaja = db.Column(db.DateTime)
    idCausalBaja = db.Column(db.Integer, unique=False) #CausalesBaja
    CausalBaja = db.Column(db.String(256), unique=False)
    mailAviso = db.Column(db.String(2056), unique=False)
    Contacto = db.Column(db.String(2056), unique=False)
    idGNS = db.Column(db.Integer, unique=False)
    fechaSincronizacionGNS = db.Column(db.DateTime)
    obsGNS = db.Column(db.DateTime)
    fechaBajaGNS = db.Column(db.DateTime)
    bajaGNSPor = db.Column(db.String(256), unique=False)
    obsBajaGNS = db.Column(db.String(256), unique=False)

class TipoID(db.Model):
    idtipoid = db.Column(db.String(16), primary_key=True)
    descripcion = db.Column(db.String(256))
    id = db.Column(db.Integer, unique=False)
    idantel = db.Column(db.String(256), unique=False)
    id = db.Column(db.Integer, unique=False)
    idtipoidexterno = db.Column(db.Integer, unique=False)
    tipocli = db.Column(db.String(256), unique=False)
    visible = db.Column(db.Boolean)