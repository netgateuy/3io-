from ..models.Contract import Contract
from flask import request, jsonify
from time import gmtime, strftime
from ..models.Product import Product, ProductField, ProductFieldValue, ProductContract, ProductClient, ClientProductFieldValue
from ..models.Pais import Pais
from ..models.SubPais import SubPais
from ..models.Ciudad import Ciudad
from ..models.TipoPago import TipoPago
from ..models.FormaPago import FormaPago
from ..models.Cliente import TipoID, Cliente
from ..models.Moneda import Moneda
from ..models.Vendedor import Vendedor
from ..models.User import User
from ..models.Agenda import Agenda, TipoAgenda
from ..models.Equipo import EquipoTipo, Proveedor
from ..models.Sucursal import Sucursal
from ..models.Oportunidad import TipoOportunidad, Oportunidad, EstadoOportunidad, TipoAccion, AccionOportunidad, ArchivoOportunidad, TipoArchivo, EstadoOportunidad
from ..models.Reclamo import Reclamo, TipoReclamo, Prioridades, ReclamoAccion, TipoAccionReclamo, TipoSolucionReclamo, ReclamoArchivo
from . import application
from app import db
from flask import render_template, abort, Response, request, session
from sqlalchemy import func, desc, or_, and_
import mimetypes

@application.route('/')
@application.route('/dashboard')
def index():
    try:
        oportunidades_abiertas = db.session.query(func.count(Oportunidad.id)).filter(
            Oportunidad.responsable == session['user_id'] ,
            Oportunidad.fechafin == None
        ).scalar()
        return render_template('/application/index.html',oportunidades_abiertas=oportunidades_abiertas)
    except Exception as e:
        return str(e)

@application.route('/login')
def login():
    try:
        return render_template('/application/login.html')
    except Exception as e:
        return str(e)

@application.route('/clientes')
def clientes():
    try:
        sucursales = Sucursal.query.filter_by(visible=1).all()
        paises = Pais.query.all()
        tipoids = TipoID.query.filter_by(visible=1).all()
        tipo_pago = TipoPago.query.filter_by(visible=1).all()
        vendedores = Vendedor.query.filter_by(visible=1).all()
        return render_template('/application/clientes.html',sucursales=sucursales,paises=paises,tipoids=tipoids,tipo_pago=tipo_pago,vendedores=vendedores)
    except Exception as e:
        return str(e)

@application.route('/reclamo/<id>')
def reclamo(id):
    try:
        reclamo = Reclamo.query.filter_by(id=id).first()
        cliente = Cliente.query.filter_by(idCliente=reclamo.idCliente).first()
        tipoReclamo = TipoReclamo.query.filter_by(id=reclamo.idTipoReclamo).first()
        producto =  ProductClient.query.filter_by(id=reclamo.idProductoCliente).first()
        tipoProducto = Product.query.filter_by(id=producto.idproduct).first()
        prioridad = Prioridades.query.filter_by(id=reclamo.idPrioridad).first()
        tiposarchivos = TipoArchivo.query.filter_by(visible=1).order_by(TipoArchivo.nombre.asc()).all()
        prioridades = Prioridades.query.all()
        archivos = (
            db.session.query(ReclamoArchivo, TipoArchivo)
            .join(TipoArchivo, ReclamoArchivo.idtipoarchivo == TipoArchivo.id)
            .filter(ReclamoArchivo.idreclamo == id)
            .all()
        )

        tipoSolucion = None
        if reclamo.idTipoSolucion:
            tipoSolucion = TipoSolucionReclamo.query.filter_by(id=reclamo.idTipoSolucion).first()
        tiposSolucion = TipoSolucionReclamo.query.filter_by(visible=1,idTipoReclamo=reclamo.idTipoReclamo).all()
        tiposAccion = TipoAccionReclamo.query.filter_by(visible=1,idTipoReclamo=reclamo.idTipoReclamo).all()
        acciones = (
            db.session.query(ReclamoAccion, TipoAccionReclamo)
            .join(TipoAccionReclamo, TipoAccionReclamo.id == ReclamoAccion.idTipoAccion)
            .filter(ReclamoAccion.idReclamo==id)
            .order_by(desc(ReclamoAccion.fechaAccion))
            .all()
        )

        return render_template('/application/reclamo.html', reclamo=reclamo, cliente=cliente,tipoReclamo=tipoReclamo,producto=producto,tipoProducto=tipoProducto,prioridad=prioridad,acciones=acciones,tiposSolucion=tiposSolucion,tiposAccion=tiposAccion,tipoSolucion=tipoSolucion,tiposarchivos=tiposarchivos,archivos=archivos,prioridades=prioridades)
    except Exception as e:
        return str(e)

@application.route('/reclamos')
def reclamos():
    try:
        tiposReclamos = TipoReclamo.query.filter_by(visible=1).all()
        prioridades = Prioridades.query.all()
        usuario_actual = session['user_name']
        id_grupo_actual = session['sector_id']

        subquery_ultimo_destino = (
            db.session.query(TipoAccionReclamo.idGRPdestino)
            .join(ReclamoAccion, ReclamoAccion.idTipoAccion == TipoAccionReclamo.id)
            .filter(ReclamoAccion.idReclamo == Reclamo.id)
            .order_by(desc(ReclamoAccion.fechaAccion), desc(ReclamoAccion.id))
            .limit(1)
            .correlate(Reclamo)
            .scalar_subquery()
        )

        # 2. Consulta Principal
        reclamos = (
            db.session.query(Reclamo, Cliente, ProductClient, Product, TipoReclamo)
            .join(Cliente, Cliente.idCliente == Reclamo.idCliente)
            .join(ProductClient, ProductClient.id == Reclamo.idProductoCliente)
            .join(Product, ProductClient.idproduct == Product.id)
            .join(TipoReclamo, TipoReclamo.id == Reclamo.idTipoReclamo)
            .filter(
                Reclamo.fechaSolucion == None,  # Solo reclamos abiertos

                or_(
                    # CASO A: La última acción fue enviada explícitamente a mi grupo
                    subquery_ultimo_destino == id_grupo_actual,

                    # CASO B: La última acción tiene destino NULO (None) Y yo creé el reclamo
                    and_(
                        subquery_ultimo_destino.is_(None),
                        Reclamo.altaPor == usuario_actual
                    )
                )
            )
            .all()
        )
        return render_template('/application/reclamos.html',tiposReclamos=tiposReclamos,prioridades=prioridades,reclamos=reclamos)
    except Exception as e:
        return str(e)

@application.route('/cliente/<idcliente>')
def cliente(idcliente):
    try:
        cliente = Cliente.query.filter_by(idCliente=idcliente).first()
        monedas = Moneda.query.filter_by(visible=1).all()
        tipopago = TipoPago.query.filter_by(idTipoPago=cliente.idTipoPago).first()
        formapago = FormaPago.query.filter_by(idTipoPago=cliente.idTipoPago,idFormaPago=cliente.idFormaPago).first()
        productos_filtrados = Product.query.filter_by(visible=True).all()
        return render_template('/application/cliente.html',cliente=cliente,productos_filtrados=productos_filtrados,monedas=monedas,tipopago=tipopago,formapago=formapago)
    except Exception as e:
        return str(e)

@application.route('/editar-cliente/<idcliente>')
def editarcliente(idcliente):
    try:
        cliente = Cliente.query.filter_by(idCliente=idcliente).first()
        paises = Pais.query.all()
        subpaises = SubPais.query.filter_by(idPais=cliente.idPais).all()
        ciudades = Ciudad.query.filter_by(idPais=cliente.idPais,idSubPais=cliente.idSubPais).all()
        tipospago = TipoPago.query.all()
        tipoids = TipoID.query.filter_by(visible=1).all()
        formaspago = FormaPago.query.filter_by(idTipoPago=cliente.idTipoPago).all()
        vendedores = Vendedor.query.all()
        return render_template('/application/editar-cliente.html',cliente=cliente,paises=paises,subpaises=subpaises,ciudades=ciudades,tipospago=tipospago,formaspago=formaspago,vendedores=vendedores,tipoids=tipoids)
    except Exception as e:
        return str(e)


@application.route('/alta-contrato/<idoportunidad>')
def nuevocontrato(idoportunidad):
    try:
        oportunidad =  Oportunidad.query.filter_by(id=idoportunidad).first()
        cliente = Cliente.query.filter_by(idCliente=oportunidad.idcliente)
        productos_filtrados = Product.query.filter_by(visible=True).all()
        tipooportunidad = TipoOportunidad.query.filter_by(id=oportunidad.idtipo).first()
        usuario = User.query.filter_by(id=oportunidad.responsable).first()
        vendedores = Vendedor.query.filter_by(visible=1).all()
        return render_template('/application/altacontrato.html',productos_filtrados=productos_filtrados,idoportunidad=idoportunidad,oportunidad=oportunidad,cliente=cliente,tipooportunidad=tipooportunidad,usuario=usuario,vendedores=vendedores)
    except Exception as e:
        return str(e)

@application.route('/alta-oportunidad')
def nuevaoportunidad():
    try:
        paises = Pais.query.filter_by(visible=True).all()
        tipo_pago = TipoPago.query.filter_by(visible=True).all()
        tipo_id = TipoID.query.filter_by(visible=1)
        usuarios = User.query.filter_by(visible=1)
        tipooportunidad = TipoOportunidad.query.filter_by(visible=1)
        return render_template('/application/altaoportunidad.html',paises=paises,tipo_pago=tipo_pago,tipo_id=tipo_id,usuarios=usuarios,tipooportunidad=tipooportunidad)
    except Exception as e:
        return str(e)

@application.route('/oportunidades')
def oportunidades():
    try:
        usuario_actual = session['user_name']
        id_sector_actual = session['sector_id']

        q = request.args.get('q')
        etapa = request.args.get('etapa')
        tipo = request.args.get('tipo', type=int)

        sq_primer_pendiente = (
            db.session.query(EstadoOportunidad.id)
            .filter(EstadoOportunidad.idoportunidad == Oportunidad.id)
            .filter(EstadoOportunidad.fecharealizado.is_(None))  # Solo pendientes
            .order_by(EstadoOportunidad.id.asc())  # El primero en la fila (FIFO)
            .limit(1)
            .correlate(Oportunidad)
            .scalar_subquery()
        )

        sq_ultimo_historico = (
            db.session.query(EstadoOportunidad.id)
            .filter(EstadoOportunidad.idoportunidad == Oportunidad.id)
            .order_by(EstadoOportunidad.id.desc())  # El último creado
            .limit(1)
            .correlate(Oportunidad)
            .scalar_subquery()
        )

        tipo_oportunidades = TipoOportunidad.query.filter_by(visible=1).all()

        oportunidades = (
            db.session.query(Oportunidad, TipoOportunidad, Cliente, EstadoOportunidad)
            .join(TipoOportunidad, Oportunidad.idtipo == TipoOportunidad.id)
            .join(Cliente, Cliente.idCliente == Oportunidad.idcliente)

            # TRUCO MAESTRO: COALESCE
            # Significa: "Usa el ID del primer pendiente. ¿Es nulo? Entonces usa el último histórico."
            .join(EstadoOportunidad, EstadoOportunidad.id == func.coalesce(sq_primer_pendiente, sq_ultimo_historico))

            .filter(
                Oportunidad.fechafin.is_(None),

                # Tu lógica de permisos se mantiene igual
                or_(
                    Oportunidad.altapor == usuario_actual,

                    # Nota: Aquí usamos la lógica del estado que seleccionó el COALESCE.
                    # Si seleccionó un pendiente, verificamos si es mi sector.
                    # Si seleccionó el último realizado, verificamos si fue mi sector (aunque ya esté hecho).
                    EstadoOportunidad.sectorresponsable == id_sector_actual
                )
            )
        )

        if q:
            search_term = f"%{q}%"
            oportunidades = oportunidades.filter(
                or_(
                    Cliente.idCliente.ilike(search_term),
                    Cliente.cliNombre.ilike(search_term),
                    Cliente.cliApellido.ilike(search_term),
                    Cliente.cliRazon.ilike(search_term),
                    TipoOportunidad.nombre.ilike(search_term)
                )
            )

        if etapa == "PROCESS":
            oportunidades = oportunidades.filter(
                and_(Oportunidad.fechafin.is_(None
                                              ), Oportunidad.fechafin.is_(
                     None)))
        if etapa == "COMPLETED":
            oportunidades = oportunidades.filter(
                and_(Oportunidad.fechafin.is_(None
                                              ), Oportunidad.fechafin.isnot(
                    None)))
        if etapa == "CANCELED":
            oportunidades = oportunidades.filter(Oportunidad.fechacancelado.isnot(None))

        if tipo:
            oportunidades = oportunidades.filter(Oportunidad.idtipo == tipo)

        return render_template('/application/oportunidades.html',oportunidades=oportunidades,tipo_oportunidades=tipo_oportunidades,q=q,etapa=etapa,tipo=tipo)
    except Exception as e:
        return str(e)

@application.route('/agenda')
def agenda():
    return render_template('/application/agenda.html')

@application.route('/agendar')
def agendar():
    id_cliente = request.args.get('idcliente', default=None, type=int)
    id_oportunidad = request.args.get('idoportunidad', default=None, type=int)
    oportunidad = None
    cliente = None
    if id_oportunidad:
        #Obtenemos la oportunidad
        oportunidad = Oportunidad.query.filter_by(id=id_oportunidad).first()
        cliente = Cliente.query.filter_by(idCliente=oportunidad.idcliente).first()
    else:
        cliente = Cliente.query.filter_by(idCliente=id_cliente).first()

    tipoagenda = TipoAgenda.query.filter_by(visible=1).all()
    return render_template('/application/agendar.html',tipoagenda=tipoagenda, oportunidad=oportunidad, cliente=cliente, id_oportunidad=id_oportunidad)

@application.route('/equipos')
def equipos():

    idoportunidad = request.args.get('idoportunidad', default=None, type=int)
    oportunidad = Oportunidad.query.filter_by(id=idoportunidad).first()
    contratos = Contract.query.filter_by(idoportunidad=idoportunidad).all()
    productos = []
    for contrato in contratos:
        productoscontrato = ProductContract.query.filter_by(idcontract=contrato.id).all()
        for p in productoscontrato:
            moneda = Moneda.query.filter_by(idMoneda=p.idmoneda).first()
            product = Product.query.filter_by(id=p.idproduct).first()
            p.product = product
            p.moneda = moneda
            productos.append(p)
    return render_template('/application/equipos.html', oportunidad=oportunidad, productos=productos)

@application.route('/altaequipo')
def altaequipo():
    tiposquipo = EquipoTipo.query.filter_by(visible=1).all()
    proveedores = Proveedor.query.filter_by(visible=1).all()
    return render_template('/application/altaequipo.html', tiposquipo=tiposquipo,proveedores=proveedores)


@application.route('/oportunidad/<id>')
def oportunidad(id):
    try:
        oportunidad = Oportunidad.query.filter_by(id=id).first()
        cliente = Cliente.query.filter_by(idCliente=oportunidad.idcliente).first()
        tipooportunidad  = TipoOportunidad.query.filter_by(id=oportunidad.idtipo).first()
        usuario = User.query.filter_by(id=oportunidad.responsable).first()
        subpais = SubPais.query.filter_by(idSubPais=cliente.idSubPais).first()
        estados = EstadoOportunidad.query.filter_by(idoportunidad=id).all()
        tiposaccion = TipoAccion.query.filter_by(visible=1).all()
        contratos = Contract.query.filter_by(idoportunidad=id).all()
        tiposarchivos = TipoArchivo.query.filter_by(visible=1).order_by(TipoArchivo.nombre.asc()).all()
        archivos = (
            db.session.query(ArchivoOportunidad, TipoArchivo)
            .join(TipoArchivo, ArchivoOportunidad.idtipoarchivo == TipoArchivo.id)
            .filter(ArchivoOportunidad.idoportunidad == id)
            .all()
        )
        for c in contratos:
            c.productos = (db.session.query(ProductContract, Product, Moneda)
                .join(Product, ProductContract.idproduct == Product.id)
                .join(Moneda, ProductContract.idmoneda == Moneda.idMoneda)
                .filter(ProductContract.idcontract == c.id)
                .all())

        acciones = AccionOportunidad.query.filter_by(idoportunidad=id).all()
        return render_template('/application/oportunidad.html',oportunidad=oportunidad,cliente=cliente,tipooportunidad=tipooportunidad,usuario=usuario,subpais=subpais,estados=estados,tiposaccion=tiposaccion,acciones=acciones,contratos=contratos,archivos=archivos,tiposarchivos=tiposarchivos)
    except Exception as e:
        return str(e)

@application.route('/dinamic-form/<id>')
def dinamicform(id):
    try:
        campos_dinamicos = ProductField.query.filter_by(idProduct=id, visible=True, automatic=None).order_by(ProductField.order).all()
        for campo in campos_dinamicos:
            if campo.type == 'COMBO':
                # Llamar al método de clase para obtener la lista de strings
                valores = ProductFieldValue.get_combo_values(
                    producto_id=campo.idProduct,  # Usando el ID del producto
                    field_id=campo.id  # Usando el ID del campo actual
                )
                # Adjuntar la lista de strings al objeto campo para Jinja
                campo.opciones_combo = valores
        return render_template('/application/dinamicform.html',campos=campos_dinamicos)
    except Exception as e:
        return str(e)

@application.route('/dinamic-form/<id>/<idproduct>')
def dinamicformproduct(id,idproduct):
    try:
        campos_dinamicos = (
            db.session.query(ProductField, ClientProductFieldValue)
            .join(ClientProductFieldValue, (ProductField.id == ClientProductFieldValue.idProductField) &
                  (ProductField.id == ClientProductFieldValue.idProductField) &
                  (ClientProductFieldValue.idProductClient == idproduct)
                  )
            .filter(ProductField.idProduct==id,ProductField.visible==True)
            .order_by(ProductField.order)
            .all()
        )

        for campo, value in campos_dinamicos:
            if campo.type == 'COMBO':
                # Llamar al método de clase para obtener la lista de strings
                valores = ProductFieldValue.get_combo_values(
                    producto_id=campo.idProduct,  # Usando el ID del producto
                    field_id=campo.id  # Usando el ID del campo actual
                )
                # Adjuntar la lista de strings al objeto campo para Jinja
                campo.opciones_combo = valores
        return render_template('/application/dinamicformvalue.html',campos=campos_dinamicos)
    except Exception as e:
        return str(e)

@application.route("/archivo-oportunidad/<int:idoportunidad>/<int:idarchivo>")
def ver_archivo(idoportunidad, idarchivo):
    archivo = (
        ArchivoOportunidad
        .query
        .filter_by(id=idarchivo, idoportunidad=idoportunidad)
        .first()
    )

    if not archivo:
        abort(404)

    # Detectar el MIME según la extensión
    mimetype, _ = mimetypes.guess_type(archivo.filename)
    if mimetype is None:
        mimetype = "application/octet-stream"

    return Response(
        archivo.archivo,          # binario desde la BD
        mimetype=mimetype,        # tipo real
        headers={
            "Content-Disposition": f"inline; filename={archivo.filename}"
        }
    )

@application.route("/archivo-reclamo/<int:idreclamo>/<int:idarchivo>")
def ver_archivo_reclamo(idreclamo, idarchivo):
    archivo = (
        ReclamoArchivo
        .query
        .filter_by(id=idarchivo, idreclamo=idreclamo)
        .first()
    )

    if not archivo:
        abort(404)

    # Detectar el MIME según la extensión
    mimetype, _ = mimetypes.guess_type(archivo.filename)
    if mimetype is None:
        mimetype = "application/octet-stream"

    return Response(
        archivo.archivo,          # binario desde la BD
        mimetype=mimetype,        # tipo real
        headers={
            "Content-Disposition": f"inline; filename={archivo.filename}"
        }
    )

@application.route('/alta-productos', methods=["POST"])
def alta_productos():
    try:
        content = request.json
        # Hay que migrar los productos a la ficha del cliente
        for contrato in content['contratos']:
            productos = contrato["productos"]
            for p in productos:
                product = ProductClient()
                product.idclient = p["idclient"]
                product.idproduct = p["idproduct"]
                product.idmoneda = p["idmoneda"]
                product.importe = p["importe"]
                db.session.add(product)

        db.session.commit()

    except Exception as e:
        return jsonify(
            observation="Archivo dado de alta correctamente.",
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ), 500