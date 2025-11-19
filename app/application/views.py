from flask import request, jsonify
import base64
from ..models.Contract import Contract
from ..models.Product import Product,ProductField, ProductFieldValue
from ..models.Pais import Pais
from ..models.SubPais import SubPais
from ..models.TipoPago import TipoPago
from ..models.Cliente import TipoID, Cliente
from ..models.Vendedor import Vendedor
from ..models.User import User
from ..models.Oportunidad import TipoOportunidad, Oportunidad, EstadoOportunidad, TipoAccion, AccionOportunidad
from . import application
from time import gmtime, strftime
from app import db
from flask import Flask,render_template

@application.route('/')
def index():
    try:
        return render_template('/application/index.html')
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
        oportunidades = (
            db.session.query(Oportunidad, TipoOportunidad, Cliente)
            .join(TipoOportunidad, Oportunidad.idtipo == TipoOportunidad.id)
            .join(Cliente, Cliente.idCliente == Oportunidad.idcliente)
            .filter(Oportunidad.fechafin.is_(None))
            .all()
        )

        return render_template('/application/oportunidades.html',oportunidades=oportunidades)
    except Exception as e:
        return str(e)

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
        acciones = AccionOportunidad.query.filter_by(idoportunidad=id).all()
        return render_template('/application/oportunidad.html',oportunidad=oportunidad,cliente=cliente,tipooportunidad=tipooportunidad,usuario=usuario,subpais=subpais,estados=estados,tiposaccion=tiposaccion,acciones=acciones,contratos=contratos)
    except Exception as e:
        return str(e)

@application.route('/dinamic-form/<id>')
def dinamicform(id):
    try:
        campos_dinamicos = ProductField.query.filter_by(idProduct=id, visible=True).order_by(ProductField.order).all()
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