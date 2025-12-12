from flask import request, jsonify
import base64, re
from ..models.Contract import Contract
from ..models.Product import ProductContract, ContractProductFieldValue, ProductFieldPrice, ProductFieldValue, ProductField, Product
from ..models.Equipo import Equipo, Marca, Modelo, Proveedor, EquipoTipo, EquipoFamilia
from ..models.Oportunidad import Oportunidad, EtapaOportunidad, TipoOportunidad, AccionOportunidad, EstadoOportunidad, ArchivoOportunidad
from ..models.Cliente import Cliente, TipoID
from ..models.SubPais import SubPais
from ..models.Moneda import Moneda
from ..models.Plazo import Plazo
from ..models.Pais import Pais
from ..models.Vendedor import Vendedor
from ..models.FormaPago import FormaPago
from ..models.TipoPago import TipoPago
from ..models.Ciudad import Ciudad
from ..models.Agenda import Agenda
from . import api
from time import gmtime, strftime
from app import db
from sqlalchemy import or_, func
from datetime import datetime
from urllib.parse import unquote
import requests

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
        equipo = Equipo()
        equipo.altapor = content["altapor"]
        equipo.fechaalta = content["fechaalta"]
        equipo.idmarca = content["idmarca"]
        equipo.idmodelo = content["idmodelo"]
        equipo.idfamilia = content["idfamilia"]
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
            estado.uri = etapa.uri
            estado.notifica = etapa.notifica
            estado.descripcion = etapa.descripcion
            estado.automatica = etapa.automatica
            estado.redirige = etapa.redirige
            estado.uriredireccion = etapa.uriredireccion

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

@api.route("/subir-archivo", methods=["POST"])
def subir_archivo():
    archivo = request.files.get("archivo")
    if not archivo:
        return jsonify(
            observation="Debe adjuntar un archivo.",
            error=True,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

    archivo_nuevo = ArchivoOportunidad(
        idoportunidad=request.form.get("idoportunidad"),
        filename=archivo.filename,
        fechaalta=datetime.now(),
        archivo=archivo.read(),
        observaciones=request.form.get("observaciones"),
        altapor=request.form.get("altapor"),
        idtipoarchivo=request.form.get("idtipoarchivo")
    )

    db.session.add(archivo_nuevo)
    db.session.commit()

    return jsonify(
        id=archivo_nuevo.id,
        idoportunidad="Archivo dado de alta correctamente.",
        observation="Archivo dado de alta correctamente.",
        error=False,
        serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    )


def getOportunidad(oportunidad, contratos, cliente):
    # Convertimos oportunidad a dict
    oportunidad_json = {
        "id": oportunidad.id,
        "fechaalta": str(oportunidad.fechaalta),
        "estado": oportunidad.estado,
        "idtipo": oportunidad.idtipo,
        "fechacancelado": str(oportunidad.fechacancelado) if oportunidad.fechacancelado else None,
        "fechainicio": str(oportunidad.fechainicio) if oportunidad.fechainicio else None,
        "fechafin": str(oportunidad.fechafin) if oportunidad.fechafin else None,
        "idcliente": oportunidad.idcliente,
        "responsable": oportunidad.responsable,
        "idformapago": cliente.idFormaPago,
        "idtipopago": cliente.idTipoPago
    }

    cliente_json = {}
    pais = Pais.query.filter_by(idPais = cliente.idPais).first()
    subpais = SubPais.query.filter_by(idPais = cliente.idPais,idSubPais = cliente.idSubPais).first()
    ciudad = Ciudad.query.filter_by(idPais = cliente.idPais,idSubPais = cliente.idSubPais,idCiudad = cliente.idCiudad).first()

    cliente_json["id"] = cliente.idCliente
    cliente_json["clinombre"] = cliente.cliNombre
    cliente_json["cliapellido"] = cliente.cliApellido
    cliente_json["clirazon"] = cliente.cliRazon
    cliente_json["nroid"] = cliente.nroID
    cliente_json["emailaviso"] = cliente.eMailAviso
    cliente_json["telefono"] = cliente.Telefono
    cliente_json["calle"] = cliente.Calle
    cliente_json["nropuerta"] = cliente.nroPuerta
    cliente_json["apto"] = cliente.Apto
    cliente_json["departamento"] = subpais.nombre
    cliente_json["ciudad"] = ciudad.nombre
    cliente_json["pais"] = pais.nombre

    #Obtenemos el tipo documento
    tipodoc = TipoID.query.filter_by(idtipoid=cliente.idTipoID).first()
    tipodoc_json = {}
    tipodoc_json["idtipoid"] = tipodoc.idtipoid
    tipodoc_json["descripcion"] = tipodoc.descripcion
    tipodoc_json["idantel"] = tipodoc.idantel
    tipodoc_json["idtipoidexterno"] = tipodoc.idtipoidexterno
    tipodoc_json["tipocli"] = tipodoc.tipocli
    tipodoc_json["visible"] = tipodoc.visible
    cliente_json["tipodocumento"] = tipodoc_json


    # Convertimos contratos a una lista de dicts
    contratos_json = []
    for c in contratos:
        productos_json = []
        productos = (
            db.session.query(ProductContract, Product)
            .join(Product, Product.id == ProductContract.idproduct)
            .filter(ProductContract.idcontract == c.id)
            .all()
        )
        for p, tp in productos:
            fields_json = []
            fields = (
                db.session.query(ContractProductFieldValue, ProductField)
                .join(ProductField, ProductField.id == ContractProductFieldValue.idProductField)
                .filter(ContractProductFieldValue.idContract == c.id)
                .all()
            )
            for fc, f in fields:
                if f.type == "COMBO":
                    #Hay que buscar el field real
                    pc = ProductFieldValue.query.filter_by(id = fc.value,idProduct = fc.idProduct, idField = fc.idProductField).first()
                    if pc:
                        fc.value = pc.value
                fields_json.append({"id": f.id, "nombre": f.name, "value": fc.value})
            moneda = Moneda.query.filter_by(idMoneda=p.idmoneda).first()
            plazo = Plazo.query.filter_by(idPlazo=p.idperiodo).first()
            productos_json.append({"id": p.id,"identificador": p.identificador, "producto": {"id": tp.id, "nombre": tp.name , "tipo": tp.type, "externalid": tp.externalid}, "moneda": {"id":moneda.idMoneda,"descripcion":moneda.descripcion,"idexterno":moneda.idExterno,"abreviacion":moneda.abreviacion}, "plazo": {"id":plazo.idPlazo,"descripcion":plazo.descripcion}, "importe":p.importe, "fields": fields_json})

        v = Vendedor.query.filter_by(idVendedor = c.idvendedor).first()
        contratos_json.append({
            "id": c.id,
            "fechaalta": str(c.fechaalta),
            "mes": c.mes,
            "anio": c.mes,
            "fechacontratado": str(c.fechacontratado) if c.fechacontratado else None,
            "altapor": c.altapor,
            "fechavto": str(c.fechavto) if c.fechavto else None,
            "fechatope": str(c.fechatope) if c.fechatope else None,
            "fechaconfirmado": str(c.fechaconfirmado) if c.fechaconfirmado else None,
            "confirmadopor": c.confirmadopor,
            "codigo": c.codigo,
            "fechabaja": str(c.fechabaja) if c.fechabaja else None,
            "bajapor": c.bajapor,
            "sendmail": c.sendmail,
            "comercial": c.comercial,
            "vendedor": {"id": v.idVendedor, "nombre": v.nombre, "email":v.email,"celular": v.celular},
            "contrato": c.contrato,
            "md5": c.md5,
            "productos": productos_json,
            "fechasincronizado": str(c.fechasincronizado) if c.fechasincronizado else None,
        })

    acciones_a = AccionOportunidad.query.filter_by(idoportunidad=oportunidad.id).all()
    #acciones
    acciones = []
    for a in acciones_a:
        acciones.append({
            "id": a.id,
            "idtipoaccion": a.idtipoaccion,
            "altapor": a.altapor,
            "fechaalta": str(a.fechaalta) if a.fechaalta else None,
            "accion" : a.accion
        })

    # archivos
    archivos = []

    oportunidad_json["acciones"] = acciones
    oportunidad_json["archivos"] = archivos
    oportunidad_json["contratos"] = contratos_json
    oportunidad_json["cliente"] = cliente_json

    # JSON final
    return oportunidad_json

@api.route("/avanzar-etapa/<idoportunidad>", methods=["POST"])
def avanzar_etapa(idoportunidad):
    #Obtengo la primer etapa sin realizar
    oportunidad = Oportunidad.query.filter_by(id=idoportunidad).first()
    contratos = Contract.query.filter_by(idoportunidad=idoportunidad).all()
    cliente = Cliente.query.filter_by(idCliente=oportunidad.idcliente).first()
    etapa = EstadoOportunidad.query.filter_by(idoportunidad=idoportunidad,fecharealizado=None).order_by(EstadoOportunidad.id).first()
    oportunidad = getOportunidad(oportunidad, contratos, cliente)

    if etapa.automatica is None:
        if etapa.notificar:
            response = requests.post(
                etapa.uri,
                json=oportunidad,
            )

            if not response.status_code == 200:
                return jsonify(
                    observation="Error al intentar avanzar la etapa.",
                    error=False,
                    serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
                ), 500

    etapa.fecharealizado = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    try:
        db.session.commit()
        return jsonify(
            observation="Etapa avanzada correctamente.",
            error=False,
            redirige=etapa.redirige,
            uriredireccion=etapa.uriredireccion,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ), 200
    except Exception as e:
        return jsonify(
            observation="Error al intentar avanzar la etapa.",
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ), 500


@api.route('/agendar', methods=['POST'])
def crear_agenda():
    data = request.json

    try:
        # Parsers de fecha y hora (Strings -> Objetos Python)
        # Asume formato fecha: "YYYY-MM-DD" y hora: "HH:MM"

        fecha_obj = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        hora_inicio_obj = datetime.strptime(data['hora_inicio'], '%H:%M').time()

        # Hora fin es opcional, manejamos si viene o no
        hora_fin_obj = None
        if data.get('hora_fin'):
            hora_fin_obj = datetime.strptime(data['hora_fin'], '%H:%M').time()

        nueva_agenda = Agenda(
            descripcion=data.get('descripcion'),
            idoportunidad=data.get('idoportunidad'),
            idcliente=data.get('idcliente'),
            idtipoagenda=data.get('idtipoagenda'),
            notas=data.get('notas'),
            direccion=data.get('direccion'),
            fecha=fecha_obj,
            hora_inicio=hora_inicio_obj,
            hora_fin=hora_fin_obj,
            fechacancelado=None,
            fechacompletado=None
        )

        db.session.add(nueva_agenda)
        db.session.commit()

        return jsonify({'mensaje': 'Agenda creada', 'id': nueva_agenda.id}), 201

    except ValueError as e:
        return jsonify({'error': 'Formato de fecha/hora inválido. Use YYYY-MM-DD y HH:MM', 'detalle': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error interno', 'detalle': str(e)}), 500

@api.route('/agenda/<int:id>', methods=['GET'])
def obtener_agenda(id):
    agenda = Agenda.query.get_or_404(id)
    # Usamos el helper to_dict() que creamos en la clase
    return jsonify(agenda.to_dict()), 200


@api.route('/agenda/<int:id>', methods=['PUT'])
def modificar_agenda(id):
    agenda = Agenda.query.get_or_404(id)
    data = request.json

    try:
        # Actualizamos solo si el campo viene en el JSON
        if 'descripcion' in data:
            agenda.descripcion = data['descripcion']

        if 'idoportunidad' in data:
            agenda.idoportunidad = data['idoportunidad']

        if 'idcliente' in data:
            agenda.idcliente = data['idcliente']

        # Manejo de Fechas (Strings -> Objetos)
        if 'fecha' in data and data['fecha']:
            agenda.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()

        if 'fechacancelado' in data:
            # Si envían null o vacío, lo guardamos como None
            if data['fechacancelado']:
                agenda.fechacancelado = datetime.strptime(data['fechacancelado'], '%Y-%m-%d').date()
            else:
                agenda.fechacancelado = None

        if 'fechacompletado' in data:
            if data['fechacompletado']:
                agenda.fechacompletado = datetime.strptime(data['fechacompletado'], '%Y-%m-%d').date()
            else:
                agenda.fechacompletado = None

        # Manejo de Horas
        if 'hora_inicio' in data and data['hora_inicio']:
            agenda.hora_inicio = datetime.strptime(data['hora_inicio'], '%H:%M').time()

        if 'hora_fin' in data:
            if data['hora_fin']:
                agenda.hora_fin = datetime.strptime(data['hora_fin'], '%H:%M').time()
            else:
                agenda.hora_fin = None

        db.session.commit()
        return jsonify({'mensaje': 'Agenda actualizada', 'agenda': agenda.to_dict()}), 200

    except ValueError:
        return jsonify({'error': 'Formato de fecha/hora inválido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api.route('/agenda', methods=['GET'])
def obtener_agenda_rango():
    agenda = []
    fecha = request.args.get('fecha')
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    except:
        return jsonify({"error": "Fechas de inicio o fin inválidas"}), 400

    agenda_eventos = Agenda.query.filter(
         Agenda.fecha == fecha
    ).order_by(Agenda.id).all()

    for evento in agenda_eventos:
        cliente = {}
        oportunidad = {}
        if evento.idcliente:
            cl = Cliente.query.filter_by(idCliente=evento.idcliente).first()
            if cl:
                cliente["id"] = cl.id
                cliente["idcliente"] = cl.idCliente
                cliente["clinombre"] = cl.cliNombre
                cliente["cliapellido"] = cl.cliApellido
                cliente["clirazon"] = cl.cliRazon

            op = Oportunidad.query.filter_by(id=evento.idoportunidad).first()
            if op:
               oportunidad["id"] = op.id
        estado = "pending"
        estadoTexto  = "Pendiente"
        if evento.fechacancelado:
            estado = "cancelled"
            estadoTexto = "Cancelado"
        if evento.fechacompletado:
            estado = "completed"
            estadoTexto = "Completado"

        agenda.append({"id":evento.id, "estado": estado, "estadoTexto": estadoTexto, "fecha": evento.fecha.isoformat() if evento.fecha else None, "oportunidad": oportunidad, "cliente": cliente, "idtipoagenda": evento.idtipoagenda, "fechacompletado": evento.fechacompletado.isoformat() if evento.fechacompletado else None, "descripcion": evento.descripcion, "direccion":evento.direccion, "notas":evento.notas, "hora_inicio": evento.hora_inicio.strftime('%H:%M') if evento.hora_inicio else None, "hora_fin": evento.hora_fin.strftime('%H:%M') if evento.hora_fin else None})

    return jsonify({
        "data": agenda
    })


@api.route('/equipos/serie/<string:nro_serie>', methods=['GET'])
def buscar_equipo_por_serie(nro_serie):
    """
    Busca un equipo por su número de serie (nroserie)
    y devuelve el resultado en formato JSON.
    """
    try:
        equipo = Equipo.query.filter_by(nroserie=nro_serie).one_or_none()

        if equipo is None:
            return jsonify({
                "mensaje": f"Equipo con serie '{nro_serie}' no encontrado."
            }), 404

        equipo = {}
        equipo["id"] = 1234

        # 4. Devolver la respuesta JSON con código 200 (OK)
        return jsonify(equipo), 200

    except Exception as e:
        # Manejo de otros posibles errores (e.g., error de DB)
        print(f"Error al buscar equipo: {e}")
        return jsonify({
            "mensaje": "Ocurrió un error interno del servidor.",
            "error": str(e)
        }), 500