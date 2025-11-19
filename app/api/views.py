from flask import request, jsonify
import base64, re
from ..models.Contract import Contract
from ..models.Product import ProductContract, ContractProductFieldValue, ProductFieldPrice, ProductFieldValue
from ..models.Equipo import Equipo, Marca, Modelo, Proveedor
from ..models.Oportunidad import Oportunidad, EtapaOportunidad, TipoOportunidad, AccionOportunidad, EstadoOportunidad
from ..models.Cliente import Cliente, TipoID
from ..models.SubPais import SubPais
from ..models.Pais import Pais
from ..models.Vendedor import Vendedor
from ..models.FormaPago import FormaPago
from ..models.TipoPago import TipoPago
from ..models.Ciudad import Ciudad
from . import api
from time import gmtime, strftime
from app import db
from sqlalchemy import or_, func
from datetime import datetime
from urllib.parse import unquote

@api.route('/')
def index():
    try:
        return "Netgate API For Clients 3io.netgate.com.uy"
    except Exception as e:
        return str(e)

@api.route('/contrato',methods=['POST'])
def addcontract():
    try:
        content = request.json
        contract = Contract()

        contract.fechavto = content['fechavto']
        contract.fechatope = content['fechatope']
        contract.idvendedor = content['idvendedor']
        contract.idoportunidad = content['idoportunidad']
        contract.fechaalta = datetime.now()
        contract.altapor = content['altapor']
        contract.mes = datetime.now().month
        contract.anio = datetime.now().year
        contract.sendmail  = 0
        db.session.add(contract)
        db.session.commit()

        productos = content['productos']
        for p in productos:
            productContract = ProductContract()
            productContract.idcontract = contract.id
            productContract.idproduct = p["idproducto"]
            productContract.idmoneda = p["idmoneda"]
            productContract.idperiodo = p["idperiodo"]
            productContract.importe = p["importe"]
            db.session.add(productContract)
            db.session.commit()

            #Tenemos que cargar los campos especificos de producto
            for key, value in p.items():
                if key.startswith("campo_"):
                    match = re.match(r"campo_(\d+)", key)
                    if match:
                        id_field = int(match.group(1))
                        field = ContractProductFieldValue()
                        field.idProduct = p["idproducto"]
                        field.idProductField = id_field
                        field.idContract = contract.id
                        field.value = value
                        db.session.add(field)
                        db.session.commit()

        return jsonify(
            contract=contract.id,
            observation="Contrato dado de alta.",
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

    except Exception as e:
        return jsonify(
            observation=str(e),
            error=True,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/equipo',methods=['POST'])
def addequipo():
    try:
        content = request.json
        equipo  = Equipo()
        equipo.altapor = content["altapor"]
        equipo.fechaalta = content["fechaalta"]
        equipo.idmarca = content["idmarca"]
        equipo.idmodelo = content["idmodelo"]
        equipo.idtipoequipo = content["idtipoequipo"]
        equipo.nroserie = content["nroserie"]
        equipo.idproveedor = content["idproveedor"]
        equipo.observacion = content["observacion"]
        db.session.add(equipo)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/marca',methods=['POST'])
def addmarca():
    try:
        content = request.json
        marca = Marca()
        marca.altapor = content["altapor"]
        marca.fechaalta = content["fechaalta"]
        marca.idgarantia = content["idgarantia"]
        marca.idtipoequipo = content["idtipoequipo"]
        marca.idgarantia = content["idgarantia"]
        marca.marca = content["marca"]
        marca.visible = 1
        marca.observacion = content["observacion"]
        db.session.add(marca)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/modelo',methods=['POST'])
def addmodelo():
    try:
        content = request.json
        modelo = Modelo()
        modelo.altapor = content["altapor"]
        modelo.fechaalta = content["fechaalta"]
        modelo.idgarantia = content["idgarantia"]
        modelo.idmarca = content["idmarca"]
        modelo.idtipoequipo = content["idtipoequipo"]
        modelo.idgarantia = content["idgarantia"]
        modelo.modelo = content["modelo"]
        modelo.visible = 1
        modelo.observacion = content["observacion"]
        modelo.idmoneda = content["idmoneda"]
        modelo.precio = content["precio"]
        modelo.idmonedacompra = content["idmonedacompra"]
        modelo.precioCompra = content["precioCompra"]

        db.session.add(modelo)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/proveedor', methods=['POST'])
def addproveedor():
    try:
        content = request.json
        proveedor = Proveedor()
        proveedor.altapor = content["altapor"]
        proveedor.fechaalta = content["fechaalta"]
        proveedor.proveedor = content["proveedor"]
        proveedor.visible = 1
        proveedor.observacion = content["observacion"]
        db.session.add(proveedor)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/oportunidad',methods=['POST'])
def addoportunidad():
    try:
        content = request.json
        #Cliente
        if content["idCliente"] == "0":
            idCliente = db.session.query(func.max(Cliente.idCliente)).scalar()
            idCliente = idCliente + 1
            cliente = Cliente()
            cliente.idPais = content["idPais"]
            cliente.idCliente = idCliente
            cliente.cliNombre = content["cliNombre"]
            cliente.cliApellido = content["cliApellido"]
            cliente.cliApellido = content["cliRazon"]
            cliente.cliApellido = content["cliFantasia"]
            cliente.cliApellido = content["idTipoID"]
            cliente.nroID = content["nroID"]
            cliente.idSubPais = content["idSubPais"]
            cliente.idCiudad = content["idCiudad"]
            cliente.Calle = content["Calle"]
            cliente.nroPuerta = content["nroPuerta"]
            cliente.Apto = content["Apto"]
            cliente.Telefono = content["Telefono"]
            cliente.Celular = content["Celular"]
            cliente.idTipoPago = content["idTipoPago"]
            cliente.idFormaPago = content["idFormaPago"]
            cliente.eMailAviso = content["eMailAviso"]
            cliente.FechaAlta = content["FechaAlta"]
            cliente.Contacto = content["Contacto"]
            db.session.add(cliente)
        else:
            #Actualizamos los datos del cliente
            cliente = Cliente.query.filter_by(idCliente=content["idCliente"]).first()
            cliente.idPais = content["idPais"]
            cliente.cliNombre = content["cliNombre"]
            cliente.cliApellido = content["cliApellido"]
            cliente.cliRazon = content["cliRazon"]
            cliente.cliFantasia = content["cliFantasia"]
            cliente.idTipoID = content["idTipoID"]
            cliente.nroID = content["nroID"]
            cliente.idSubPais = content["idSubPais"]
            cliente.idCiudad = content["idCiudad"]
            cliente.Calle = content["Calle"]
            cliente.nroPuerta = content["nroPuerta"]
            cliente.Apto = content["Apto"]
            cliente.Telefono = content["Telefono"]
            cliente.Celular = content["Celular"]
            cliente.idTipoPago = content["idTipoPago"]
            cliente.idFormaPago = content["idFormaPago"]
            cliente.eMailAviso = content["eMailAviso"]
            cliente.Contacto = content["Contacto"]
            db.session.merge(cliente)
            db.session.commit()

        # Debemos dar de alta las etapas de la oportunidad
        etapas_oportunidad = EtapaOportunidad.query.filter_by(idtipoportunidad=content["idtipo"]).all()
        etapa_0 = etapas_oportunidad[0]
        #Oportunidad
        oportunidad  = Oportunidad()
        oportunidad.idtipo = content["idtipo"]
        oportunidad.fechaalta = content["fechaAlta"]
        oportunidad.fechainicio = content["fechaInicio"]
        oportunidad.idcliente = content["idCliente"]
        oportunidad.responsable = content["responsable"]
        oportunidad.estado = etapa_0.nombre
        db.session.add(oportunidad)
        db.session.commit()


        for etapa in etapas_oportunidad:
            estado = EstadoOportunidad()
            estado.idoportunidad = oportunidad.id
            estado.idtipoportunidad = content["idtipo"]
            estado.icono = etapa.icono
            estado.predecesor = etapa.predecesor
            estado.notificar = etapa.notificar
            estado.sectorresponsable = etapa.sectorresponsable
            estado.idetapaoportunidad = etapa.id
            estado.fechaalta = datetime.now()
            estado.nombre = etapa.nombre
            estado.descripcion = etapa.descripcion
            db.session.add(estado)
            db.session.commit()
        return jsonify(
            id=oportunidad.id,
            observation="Oportunidad dada de alta",
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/accionoportunidad',methods=['POST'])
def addaccionoportunidad():
    try:
        content = request.json
        accion = AccionOportunidad()
        accion.idoportunidad = content["idoportunidad"]
        accion.altapor = content["altapor"]
        accion.fechaalta = datetime.now()
        accion.accion = content["accion"]
        accion.idtipoaccion = content["idtipoaccion"]
        db.session.add(accion)
        db.session.commit()

        return jsonify(
            id=accion.id,
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )
    except Exception as e:
        return jsonify(
            observation=str(e),
            error=True,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/tipooportunidad',methods=['POST'])
def addotipoportunidad():
    try:
        content = request.json
        tipooportunidad  = TipoOportunidad()
        tipooportunidad.nombre = content["nombre"]
        tipooportunidad.descripcion = content["descripcion"]
        db.session.add(tipooportunidad)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/etapaoportunidad',methods=['POST'])
def addetapaoportunidad():
    try:
        content = request.json
        etapaoportunidad  = EtapaOportunidad()
        etapaoportunidad.nombre = content["nombre"]
        etapaoportunidad.descripcion = content["descripcion"]
        etapaoportunidad.predecesor = content["predecesor"]
        etapaoportunidad.sectorresponsable = content["sectorresponsable"]
        db.session.add(etapaoportunidad)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/cliente',methods=['POST'])
def addcliente():
    try:
        content = request.json
        cliente  = Cliente()
        cliente.idpais = content["idpais"]
        cliente.idcliente = content["idcliente"]
        cliente.idsucursal = content["idsucursal"]
        cliente.clinombre = content["clinombre"]
        cliente.cliapellido = content["cliapellido"]
        cliente.clirazon = content["clirazon"]
        cliente.clifantasia = content["clifantasia"]
        cliente.idtipoid = content["idtipoid"]
        cliente.nroid = content["nroid"]
        cliente.idpais1 = content["idpais1"]
        cliente.idsubpais = content["idsubpais"]
        cliente.idciudad = content["idciudad"]
        cliente.idbarrio = content["idbarrio"]
        cliente.calle = content["calle"]
        cliente.nropuerta = content["nropuerta"]
        cliente.idciudad = content["idciudad"]
        cliente.apto = content["apto"]
        cliente.codigopostal = content["codigopostal"]
        cliente.telefono = content["telefono"]
        cliente.celular = content["celular"]
        cliente.idtipopago = content["idtipopago"]
        cliente.idformapago = content["idformapago"]
        cliente.emailaviso = content["emailaviso"]
        cliente.idvendedor = content["idvendedor"]
        cliente.fechaalta = content["fechaalta"]
        cliente.mailaviso = content["mailaviso"]
        cliente.idformapago = content["idformapago"]
        cliente.contacto = content["contacto"]
        db.session.add(cliente)
        db.session.commit()
    except Exception as e:
        return jsonify(
            observation=str(e),
            error="yes",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

@api.route('/cliente/filter/', methods=['GET'])
def get_cliente_filter():
    q = request.args.get('q')
    clientes = Cliente.query.filter(or_(
            Cliente.cliNombre.ilike(f"%{q}%"),
            Cliente.cliApellido.ilike(f"%{q}%"),
            Cliente.nroID.ilike(f"%{q}%"),
            Cliente.cliFantasia.ilike(f"%{q}%")
        )
    ).all()

    data = []
    for cliente in clientes:
        data.append({
            'idpais': cliente.idPais,
            'idcliente': cliente.idCliente,
            'idsucursal': cliente.idSucursal,
            'clinombre': cliente.cliNombre,
            'cliapellido': cliente.cliApellido,
            'clirazon': cliente.cliRazon,
            'clifantasia': cliente.cliFantasia,
            'idtipoid': cliente.idTipoID,
            'nroid': cliente.nroID,
            'idsubpais': cliente.idSubPais,
            'idciudad': cliente.idCiudad,
            'idbarrio': cliente.idBarrio,
            'calle': cliente.Calle,
            'nropuerta': cliente.nroPuerta,
            'apto': cliente.Apto,
            'codigopostal': cliente.CodigoPostal,
            'telefono': cliente.Telefono,
            'celular': cliente.Celular,
            'idtipopago': cliente.idTipoPago,
            'idformapago': cliente.idFormaPago,
            'emailaviso': cliente.eMailAviso,
            'idvendedor': cliente.idVendedor,
            'fechaalta': cliente.FechaAlta,
            'contacto': cliente.Contacto,
        })
    return jsonify(data)

@api.route('/product-price/<idproduct>/<idfiled>/<id>', methods=['GET'])
def get_price(idproduct,idfiled,id):
    price = ProductFieldPrice.query.filter_by(idProduct=idproduct,idField=idfiled,value=id).first()
    if price:
        return jsonify({
            'id': price.id,
            'idproduct': price.idProduct,
            'idfield': price.idField,
            'value': price.value,
            'idmoneda': price.idmoneda,
            'importe': price.importe
        }), 200
    else:
        return jsonify({'error': 'Precio no encontrato'}), 404

@api.route('/cliente/<int:idCliente>', methods=['GET'])
def get_cliente(idCliente):
    cliente = Cliente.query.filter_by(idCliente=idCliente).first()
    if cliente:
        return jsonify({
            'idPais': cliente.idPais,
            'idcliente': cliente.idCliente,
            'idsucursal': cliente.idSucursal,
            'clinombre': cliente.cliNombre,
            'cliapellido': cliente.cliApellido,
            'clirazon': cliente.cliRazon,
            'clifantasia': cliente.cliFantasia,
            'idtipoid': cliente.idTipoID,
            'nroid': cliente.nroID,
            'idsubpais': cliente.idSubPais,
            'idciudad': cliente.idCiudad,
            'idbarrio': cliente.idBarrio,
            'Calle': cliente.Calle,
            'nropuerta': cliente.nroPuerta,
            'apto': cliente.Apto,
            'codigopostal': cliente.CodigoPostal,
            'telefono': cliente.Telefono,
            'celular': cliente.Celular,
            'idtipopago': cliente.idTipoPago,
            'idformapago': cliente.idFormaPago,
            'emailaviso': cliente.eMailAviso,
            'idvendedor': cliente.idVendedor,
            'fechaalta': cliente.FechaAlta,
            'contacto': cliente.Contacto,
        }), 200
    else:
        return jsonify({'error': 'Cliente no encontrado'}), 404

@api.route('/subpaises/<idPais>', methods=['GET'])
def get_subpaises(idPais):
    subpaises = SubPais.query.filter_by(idPais=idPais).order_by(SubPais.nombre).all()
    data = []
    for s in subpaises:
        data.append({
            "idPais": s.idPais,
            "idSubPais": s.idSubPais,
            "nombre": s.nombre
        })
    return jsonify(data)

@api.route('/product-field-values/<idProduct>/<idField>', methods=['GET'])
def get_productfieldsvalues(idProduct,idField):
    values = ProductFieldValue.query.filter_by(idProduct=idProduct,idField=idField).order_by(ProductFieldValue.order).all()
    data = []
    for v in values:
        data.append({
            "id": v.id,
            "idProduct": v.idProduct,
            "idField": v.idField,
            "value": v.value
        })
    return jsonify(data)

@api.route('/product-field-filter/<idProduct>/<idField>/<idFieldFilter>', methods=['GET'])
def get_productfieldsfilter(idProduct,idField,idFieldFilter):
    values = ProductFieldValue.query.filter_by(idProduct=idProduct,idField=idField,idFieldFilter=idFieldFilter).order_by(ProductFieldValue.value).all()
    data = []
    for v in values:
        data.append({
            "id": v.id,
            "idProduct": v.idProduct,
            "idField": v.idField,
            "value": v.value
        })
    return jsonify(data)

@api.route('/ciudades/<idPais>/<idSubPais>', methods=['GET'])
def get_ciudades(idPais,idSubPais):
    ciudades = Ciudad.query.filter_by(idPais=idPais,idSubPais=idSubPais).order_by(Ciudad.nombre).all()
    data = []
    for c in ciudades:
        data.append({
            "idPais": c.idPais,
            "idSubPais": c.idSubPais,
            "idSubPais": c.idSubPais,
            "idCiudad": c.idCiudad,
            "nombre": c.nombre
        })
    return jsonify(data)

@api.route('/forma_pago/<idTipoPago>', methods=['GET'])
def get_forma_pago(idTipoPago):
    formaspago = FormaPago.query.filter_by(idTipoPago=idTipoPago).all()
    data = []
    for fp in formaspago:
        data.append({
            "idTipoPago": fp.idTipoPago,
            "idFormaPago": fp.idFormaPago,
            "descripcion": fp.descripcion
        })
    return jsonify(data)