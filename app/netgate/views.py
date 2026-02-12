# coding: utf-8
from . import netgate
from flask import request, jsonify, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import gmtime, strftime
from pypdf import PdfReader, PdfWriter
from datetime import datetime
from pypdf.generic import NameObject, DictionaryObject
import os
import requests
import smtplib
import base64
import json
from zeep import Client
from zeep.exceptions import Fault

WSDL_URL = 'https://server2.gns-mas.com/sistema/2.0/interfase/netgate/server.php?wsdl' #GNS

# Datos de autenticación comunes (según el WSDL se piden en cada llamada)
AUTH_DATA = {
    'empresa': 'netgate',
    'usuario': 'interfase',
    'password': 'Interfaz.2021'
}

try:
    client = Client(wsdl=WSDL_URL)
    client.service._binding_options['address'] = WSDL_URL
except Exception as e:
    print(f"Error cargando WSDL (verifica la URL o archivo): {e}")
    exit()

endpoint_payments = "https://payments.netgate.com.uy/siemprepago/"
def send_mail(to,subject,body,cc,bcc,files,url_descarga,nm):
    msg = MIMEMultipart("alternative")
    msg['From'] = 'ventas@netgate.com.uy'
    msg['To'] = to

    msg.add_header('Content-Type', 'text/html')

    for path in files:
        try:
            with open(path, 'rb') as file:
                filename = os.path.basename(path)
                payload = MIMEBase('application', 'octate-stream', Name=filename)
                payload.set_payload((file).read())

                # enconding the binary into base64
                encoders.encode_base64(payload)

                # add header with pdf name
                payload.add_header('Content-Decomposition', 'attachment', filename=filename)
                msg.attach(payload)

        except Exception as e:
            body = str(e)

    if len(url_descarga) > 0:
        response = requests.get(url_descarga)
        if response.status_code == 200:
            # Preparamos el adjunto
            payload = MIMEBase('application', 'octet-stream')
            payload.set_payload(response.content)  # Usamos el contenido binario directo
            encoders.encode_base64(payload)

            # Definimos el nombre del archivo en el adjunto
            # Usamos la variable 'nm' que definiste arriba como nombre de archivo
            payload.add_header('Content-Disposition', 'attachment', filename=os.path.basename(nm))

            msg.attach(payload)

    msg['Subject'] = subject
    body_part = MIMEText(body, "html", "utf-8")
    msg.attach(body_part)
    #msg.set_charset('utf8')
    s = smtplib.SMTP('190.64.214.126', 587)
    s.starttls()
    s.login("3iotest@netgate.com.uy",
            "netgate.2840")
    s.sendmail(msg['From'], [msg['To'],cc,bcc], msg.as_string())
    s.quit()
    s.close()


def get_especificaciones(contract, client, importe, especificaciones):
    data = {
        "name": f"{client['clinombre']} {client['cliapellido']} {client['clirazon']}",
        "address": contract['Calle'] + " " + contract['Numero Puerta'] + " " + contract['Manzana']  + " " + contract['Solar'],  # cell.getCalleADSL()
        "nameform":  f"{client['clinombre']} {client['cliapellido']} {client['clirazon']}",  # cell.getNombreCliente()
        "product": contract['Tipo Tarifa'],
        "cellphoneform": client['celular'],
        "price": str(importe),  # mobjRSet.getString("precioAntel")
        "email": client['emailaviso'],  # mobjRSet.getString("emailaviso")
        "contract": str(contract['nro_contrato'] or ""),  # cell.getNroContrato()
        "nextcontract": str(contract['nro_contrato'] or ""),  # cell.getNroContrato()
        "cellphone": client['celular'],  # cell.getNroMovil()
        "connectionfee": "0",
        "conditions": "Sin costo. Sujeto a promociones provistas por Antel",
        "telephone": contract['Teléfono ADSL'],
        "file": especificaciones,
        "uploadvelocity": f"{contract['Upstream']}MB",
        "downloadvelocity": f"{contract['Downstream']}MB"
    }

    json_string = json.dumps(data)
    encoded_bytes = base64.b64encode(json_string.encode('utf-8'))
    encoded_base64 = encoded_bytes.decode('utf-8')  # Convertimos bytes de vuelta a string para la URL

    # Construimos el nombre del archivo y la URL final
    nm = f"{contract['nro_contrato']}_esp.jpg"
    url_descarga = f"https://servicios.netgate.com.uy/clients/product/esp/?dt={encoded_base64}&nm={nm}"
    return url_descarga, nm

@netgate.route('/')
def index():
    try:
        return "Netgate API For Clients 3io.netgate.com.uy"
    except Exception as e:
        return str(e)

@netgate.route('/enviar-contrato', methods=["POST"])
def enviar_contrato():
    #Enviamos el contratato al cliente
    return ""

@netgate.route('/proceso-adsl', methods=["POST"])
def proceso_adsl():
    #Enviamos el contratato al cliente
    return ""

def get_mes(numero_mes):
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    return meses[numero_mes]

def get_periodo(idperiodo):
    periodo = ""
    if idperiodo == "0":
        periodo = "Unica Vez"
    elif idperiodo == "1":
        periodo = "Mensual"
    elif idperiodo == "2":
        periodo = "Bimestral"
    elif idperiodo == "3":
        periodo = "Trimestral"
    elif idperiodo == "12":
        periodo = "Anual"
    elif idperiodo == "24":
        periodo = "Dos Años"
    return periodo

def generar_contrato_adsl(contract, client):
    root_path = netgate.root_path
    input_file_path = os.path.join(root_path,"..", 'templates', 'netgate', 'contrato_contingencia-internet.pdf')
    output_file_path = os.path.join(root_path, "..", 'templates', 'netgate', "contratos", contract['nro_contrato'] + ".pdf")

    reader = PdfReader(input_file_path)
    writer = PdfWriter()

    # Copiamos las páginas del original
    writer.append_pages_from_reader(reader)

    if "/AcroForm" in reader.root_object:
        # Copiamos la estructura del formulario al nuevo PDF
        writer.root_object.update({
            NameObject("/AcroForm"): reader.root_object["/AcroForm"]
        })

    # 1. PREPARACIÓN DE DATOS
    # Lógica de Nombre (Java: replace("  ", ""))
    nombre_completo = f"{client['clinombre']} {client['cliapellido']} {client['clirazon']}"
    nombre_limpio = nombre_completo.replace("  ", "")

    # Lógica de Tipo de Documento
    tipo_doc_map = {
        "RUC": "RUC",
        "CI": "Cédula de Identidad",
        "PAS": "Pasaporte",
        "BPS": "BPS"
    }

    desc_tipo_doc = tipo_doc_map.get(client['tipodocumento']['idtipoid'], "")

    # Lógica de Velocidades
    #velocidades = view_velocidad(grst_contrato, contract['serie_contrato'])

    # Lógica de Observaciones (Concatenación)
    #obs = view_tipo_descripcion(contract['tipo_contrato'], contract.get('contrato_anterior'),
                                #contract['nro_contrato'])

    obs = ""
    obs_final = obs + "\n- Sujeto a promociones vigentes de Antel"

    velocidades = ["","","","","","","",""]

    fechainicio = datetime.strptime(contract["fechainicio"], "%Y-%m-%d")

    # 2. MAPEO DE CAMPOS (AcroFields)
    # Creamos un diccionario con "NombreDelCampo": "Valor"
    campos_a_llenar = {
        "1": "NETGATE - 424",
        "2": str(contract['nro_contrato']),
        "3": str(fechainicio.day),
        "4": get_mes(fechainicio.month),
        "5": str(fechainicio.year),
        "6": get_periodo(contract['idperiodo']),
        "8": nombre_limpio,
        "9": desc_tipo_doc,
        "10": str(client['nroid'] or "") ,
        "15": client['calle'] or "",
        "16": str(client['nropuerta'] or ""),
        "17": str(client['apto'] or ""),
        "18": client['padron'] or "",  # manzana
        "19": client['manzana']or "", #manzana
        "20": client['solar'] or "", #solar
        "21": client['departamento'] or "",
        "22": client['ciudad'] or "",
        "23": client['telefono'] or "",
        "24": client['celular'] or "",
        "25": client['emailaviso'] or "",
        "26": contract['Tipo Contrato'] or "",
        "34": str(contract['nro_contrato'] or ""),
        "35": contract['Teléfono ADSL'] or "",
        "36": " " + contract['Tipo Tarifa'],
        "37": f"$ {contract['tarifaconexion']}",

        # Velocidades (Cuidado con los índices, Python es base 0 igual que Java arrays)
        "41": contract['Upstream'],
        "42": contract['Downstream'],
        "43": contract['Tope'],
        "44": contract['DownstreamTope'],
        "45": contract['UpstreamTope'],
        "46": contract['SuperadoTope'],
        "54": contract['Calle'],
        "55": str(contract['Numero Puerta']),
        "56": str(contract['Apartamento']),
        "57": contract['Padrón'],
        "58": contract['Manzana'],
        "59": contract['Solar'],
        "60": contract['Barrio'],
        "61": contract['Departamento'],
        "74": client['emailaviso'],
        "76": obs_final,
        "Texto106": "NETGATE",
        "Texto107": "424",
    }

    # 3. RELLENAR EL PDF
    writer.update_page_form_field_values(
        writer.pages[0],
        campos_a_llenar
    )

    writer.update_page_form_field_values(
        writer.pages[1],
        campos_a_llenar
    )

    # 4. GUARDAR
    with open(output_file_path, "wb") as output_stream:
        writer.write(output_stream)
    return output_file_path

@netgate.route('/enviar-antel', methods=["POST"])
def enviar_antel():
    try:
        # Obtenemos la oportunidad
        oportunidad = request.json
        cliente = oportunidad["cliente"]
        for contrato in oportunidad["contratos"]:
            for producto in contrato["productos"]:
                #Caregamos los datos adicionales al contrato
                for field in producto["fields"]:
                    contrato[field["name"]] = field["value"]
                    for extraf in field["extrafields"]:
                        contrato[extraf["name"]] = extraf["value"]
                contrato["clinombre"] = oportunidad["cliente"]["clinombre"]
                contrato["cliapellido"] = oportunidad["cliente"]["cliapellido"]
                contrato["clirazon"] = oportunidad["cliente"]["clirazon"]
                contrato["idtipoid"] = oportunidad["cliente"]["clirazon"]
                contrato["nroid"] = oportunidad["cliente"]["nroid"]
                contrato["idtipoid"] = cliente["tipodocumento"]["idtipoid"]
                contrato["emailaviso"] = cliente["emailaviso"]
                contrato["idcliente"] = oportunidad["cliente"]["id"]
                contrato["idoportunidad"] = oportunidad["id"]
                contrato["idcontrato"] = contrato["id"]
                contrato["idproducto"] = producto["id"]

                #Hacemos un request from a seguridad.netgate.com.uy
                url = "https://seguridadng.netgate.com.uy/adsl/api/solicitudes/add_solicitud.asp"
                response = requests.post(url, data=contrato)

        return jsonify(
            observation="Solicitud ingresada en Antel.",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ), 200
    except Exception as e:
        return jsonify(
            observation=str(e),
            error=True,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ), 500

@netgate.route('/notificacion-cliente', methods=["POST"])
def notificacion_cliente():
    cliente = request.json
    datos_entrada = {
        **AUTH_DATA,

        # --- Datos de Contacto ---
        'manteCliRapContactNombre': str(cliente["clinombre"] or ''),
        'manteCliRapContactApellido1': str(cliente["cliapellido"] or ''),
        'manteCliRapContactCelular': str(cliente["clinombre"] or ''),
        'manteCliRapContactTelefono': str(cliente["telefono"] or ''),
        'manteCliRapContactEmail': str(cliente["email"] or ''),
        'manteCliRapContactIdTipoContacto': '7',
        'manteCliRapContactObservaciones': f"Localidad: {cliente["telefono"] or ''}",

        # --- Dirección ---
        'manteCliRapDircontitDireccion': str(cliente["direccion"] or ''),
        'manteCliRapDircontitIdPais': str(cliente["pais"]["id"] or ''),
        'manteCliRapDircontitIdDepartamento': '-1',  # Hardcodeado
        'manteCliRapDircontitIdLocalidad': '-1',  # Hardcodeado
        'manteCliRapDircontitZona': '-1',  # Hardcodeado

        # --- Datos Cliente ---
        'manteCliRapEMailGenerico': str(cliente["email"] or 'D'),  # En Java era c.getEmailAvisoFactura()
        'manteCliRapIdTipoDocumento': str(cliente["tipoid"]["idexterno"]  or 'D'),
        'manteCliRapNumeroDocumento': str(cliente["nroid"] or 'F'),
        'manteCliRapNombreFantasia': str(cliente["clifantasia"] or cliente["clinombre"]),
        'manteCliRapRazonSocial': str(cliente["clirazon"] or ''),
        'manteCliRapNroCliente': str(cliente["idcliente"] or ''),
        'manteCliRapTelefonoCliente': str(cliente["telefono"] or ''),
        'manteCliRapTipo': str(cliente["tipoid"]["tipocli"] or ''),

        # --- Flags y Constantes ---
        'manteCliRapIndCliente': '1',
        'manteCliRapIndProveedor': '',
        'manteCliRapControlaAtraso': 'N',
        'manteCliRapCobraMora': 'N',
        'manteCliRapNroAgencia': '',

        # --- Datos de Pago ---
        'manteCliRapTitularPago': "",
        'manteCliRapTipoPago': "",
        'manteCliRapNroCuentaPago': "",
        'manteCliRapFormaPago': str(cliente["formapago"]["idexterno"] or ''),
        'manteCliRapFechaVmtoTarjeta': ""
    }

    respuesta = client.service.altaRapidaCliente(datosEnt=datos_entrada)

    id_gns = respuesta.idCliente

    return jsonify(
        externalid=id_gns,
        observation="Cliente dado de alta correctamente.",
        msg=respuesta.msg,
        serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ), 200

@netgate.route('/notificacion-producto', methods=["POST"])
def notificacion_producto():
    try:
        producto = request.json
        if producto["event.type"] == "product.created":
            #Damos de alta el producto
            producto = request.json
            datos_entrada = {
                **AUTH_DATA,
                'idCliente': str(producto["cliente"]["idexterno"]),
                'manteDatServArticulo': str(producto["idproductoexterno"]),
                'manteDatServMoneda': str(producto["moneda"]["idexterno"]),
                'manteDatServMonto': str(producto["importe"]),
                'manteDatServFechaDesde': str(producto["fechainicio"]),
                'manteDatServFechaHasta': str(producto["fechafin"]),
                'manteDatServPeriodicidad': str(producto["idperiodo"]),
                'manteDatServDescripcion': str(producto["obs"])
            }

            try:
                # Llamada al método SOAP
                respuesta = client.service.altaServicio(datosEnt=datos_entrada)

                return jsonify(
                    externalid=respuesta.idServicio,
                    observation="Servicio dado de alta correctamente.",
                    serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
                ), 200

            except Exception as e:
                return jsonify(
                    observation=str(e),
                    serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
                ), 500
        elif producto["event.type"] == "product.updated":
            datos_modificacion = {
                **AUTH_DATA,  # Desempaqueta usuario, pass y empresa
                'idServicio': str(producto["idservicioexterno"]),
                'idMoneda': str(producto["moneda"]["idexterno"]),
                'montoServicio': str(producto["importe"]),
                'fechaDesde': str(producto["fechainicio"]),
                'periServicio': str(producto["idperiodo"]),
                'descServicio': str(producto["obs"])
            }
            respuesta = client.service.modificarServicio(datosEnt=datos_modificacion)
            if respuesta:
                if(producto["fechafin"] is None or len(producto["fechafin"]) == 0): producto["fechafin"] = "2800/10/10"
                datos_baja = {
                    **AUTH_DATA,
                    'idServicio': str(producto["idservicioexterno"]),
                    'fecha': str(producto["fechafin"])
                }
                obsfechafin = client.service.bajaServicio(datosEnt=datos_baja)
                return jsonify({'externalid': str(producto["idservicioexterno"]), "status": "success", "mensaje": "Producto modificado correctamente", "observaciones": str(obsfechafin)})
            else:
                # Devuelves un JSON con error 500
                return jsonify({"externalid": str(producto["idservicioexterno"]) , "status": "error", "mensaje": "Fallo en el webservice"}), 500
    except Exception as e:
        return str(e)

@netgate.route('/notificar-cliente', methods=["POST"])
def notificar_cliente():
    try:
        #Obtenemos la oportunidad
        oportunidad = request.json

        #Hay que armar el contrato y especificaciones para el cliente
        producto_adsl = ""
        for contrato in oportunidad["contratos"]:
            nombre_vendedor = contrato["vendedor"]["nombre"]
            mail_vendedor = contrato["vendedor"]["email"]
            interno_vendedor = contrato["vendedor"]["interno"]

            for producto in contrato["productos"]:
                producto_adsl, especificaciones, tarifaconexion = get_producto_adsl(producto)
                nro_contrato = get_nro_contrato(producto)
                contrato["nro_contrato"] = nro_contrato
                contrato["fechainicio"] = oportunidad["fechainicio"]
                importe = int(producto["importe"] * 1.22) #Precio sin iva, se le aplica IVA
                condiciones = "Sin costo. Sujeto a promociones provistas por Antel."
                html_renderizado = render_template('netgate/' + especificaciones, nombre_vendedor=nombre_vendedor, mail_vendedor=mail_vendedor,  interno_vendedor=interno_vendedor,importe=importe,condiciones=condiciones, tarifaconexion=tarifaconexion)
                contrato["idperiodo"] = producto["idperiodo"]
                contrato["tarifaconexion"] = tarifaconexion

                for field in producto["fields"]:
                    html_renderizado = html_renderizado.replace("#" + field["name"] + "#", field["value"])
                    contrato[field["name"]] = field["value"]
                    for extraf in field["extrafields"]:
                        contrato[extraf["name"]] = extraf["value"]

                url_descarga, nm = get_especificaciones(contrato, oportunidad["cliente"], importe, especificaciones)

                contrato_pdf = generar_contrato_adsl(contrato, oportunidad["cliente"])

                if "emp" not in producto_adsl and "pyme" not in producto_adsl:
                    send_mail(oportunidad["cliente"]["emailaviso"], "Especificaciones de contratación de servicio de ADSL " + nro_contrato, html_renderizado, "", "", [contrato_pdf],url_descarga, nm)
                else:
                    send_mail(oportunidad["cliente"]["emailaviso"], "Especificaciones de contratación de servicio de ADSL" + nro_contrato,
                              html_renderizado, "", "", [contrato_pdf], url_descarga, nm)

        return jsonify(
            observation="Etapa avanzada correctamente.",
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ), 200
    except Exception as e:
        return jsonify(
            observation=str(e),
            error=True,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ),500

def get_nro_contrato(producto):
    nrocontrato = "N/A"
    for field in producto["fields"]:
        if field["name"] == "Nro Contrato":
            return field["value"]
    return nrocontrato #Por las dudas que no lo encuentre

def get_producto_adsl(producto):
    value = "N/A"
    especificaciones= "N/A"
    tarifaconexion = "N/A"
    for field in producto["fields"]:
        for extraf in field["extrafields"]:
            if extraf["name"] == "tarifa conexion":
                tarifaconexion = extraf["value"]
            elif extraf["name"] == "especificaciones":
                especificaciones = extraf["value"]
        if field["name"] == "Tipo Tarifa":
            return field["value"], especificaciones, tarifaconexion
    return value, especificaciones, tarifaconexion

def generar_html_correo(content,total_dolares,total_pesos,cliente_bamboo):
    html_renderizado = render_template('netgate/mailing.html', content=content,total_dolares=total_dolares,total_pesos=total_pesos,cliente_bamboo=cliente_bamboo)
    return html_renderizado

def login_gns():
    uri = "https://gns-mas.com/api/v1/login"
    payload = {
        'api_key': "QD8P8mDZMtu0ocFg",
        'api_secret': "5gQpVCSB9vXc8DAI8uGdU589Ukip3Ubq"
    }
    response = requests.post(uri,data=payload)
    #Devolvemos el token
    return response.json()["token"]

def get_orden_gns(oportunidad, idmoneda):
    payload = {}
    cli_razon = ""
    if oportunidad["cliente"]["clirazon"]:
        cli_razon = oportunidad["cliente"]["clirazon"]

    payload["nombre"] = cli_razon + ' ' + oportunidad["cliente"]["clinombre"] + ' ' + oportunidad["cliente"]["cliapellido"]
    payload["telefono"] = oportunidad["cliente"]["telefono"]
    payload["email"] = oportunidad["cliente"]["emailaviso"]
    payload["idTipoDocumento"] = oportunidad["cliente"]["tipodocumento"]["idtipoidexterno"]
    payload["numeroDocumento"] = oportunidad["cliente"]["nroid"]
    payload["ciudad"] = oportunidad["cliente"]["ciudad"]
    payload["direccion"] = oportunidad["cliente"]["calle"] + " " + str(oportunidad["cliente"]["nropuerta"]) + " " + str(oportunidad["cliente"]["apto"])
    payload["fechaemision"] = ""
    payload["fechaemision"] = ""
    payload["idMoneda"] = idmoneda
    payload["nroOrdenCompra"] = oportunidad["id"]
    payload["idContexto"] = "1"
    payload["nroAuto"] = "0"
    payload["cuotas"] = "0"

    i = 0
    for contrato in oportunidad["contratos"]:
        for producto in contrato["productos"]:
            if producto["moneda"]["idexterno"] == idmoneda:
                payload[f"items[{i}][codigo]"] = producto["producto"]["externalid"]
                payload[f"items[{i}][cantidad]"] = "1"
                payload[f"items[{i}][precio]"] = producto["importe"]
                payload[f"items[{i}][descripcion]"] = producto["producto"]["nombre"]
                i = i + 1
    if i > 0:
        return payload
    else:
        return {}


def alta_orden_gns(token, orden):
    uri = "https://gns-mas.com/api/v1/ingresarVenta"
    headers = {"Authorization" : "Bearer " + token}
    response = requests.post(uri, headers=headers, data=orden)
    return response


@netgate.route('/procesar-pago', methods=["POST"])
def procesar_pago():
    try:
        #Si es bamboo hay que crear link de bamboo
        oportunidad = request.json

        #Hay que cargar las facturas en gns
        token_gns = login_gns()
        orden_dolares = get_orden_gns(oportunidad, "2")
        orden_pesos = get_orden_gns(oportunidad, "1")

        error_dolares = False
        error_pesos = False
        if orden_dolares:
            result = alta_orden_gns(token_gns,orden_dolares)
            if result.status_code != 200:
                error_dolares = True


        if orden_pesos:
            result = alta_orden_gns(token_gns,orden_pesos)
            if result.status_code != 200:
                error_pesos = True

        if not error_dolares and not error_pesos:
            return jsonify(
                observation="Facturas ingresadas correctamente.",
                error_pesos=error_pesos,
                error_dolares=error_dolares,
                serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
            ), 200
        else:
            return jsonify(
                observation=str(e),
                error_pesos=error_pesos,
                error_dolares=error_dolares,
                serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
            ), 500

    except Exception as e:
        return jsonify(
            observation=str(e),
            error=True,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ),500

@netgate.route('/iniciar-pago', methods=["POST"])
def iniciar_pago():
    try:
        #Si es bamboo hay que crear link de bamboo
        content = request.json
        cliente_bamboo = None
        if content['idformapago'] == 7 and content['idtipopago'] == 2:
            #Debemos chequear si tiene perfil creado
            uri = endpoint_payments + "get.php?id=" + str(content["idcliente"])
            response = requests.get(uri)

            # 3. Chequear el código de estado (status_code)
            if response.status_code == 200:
                cliente_bamboo = response.json()
            else:
                cliente_bamboo = {}
                cliente_bamboo["idcliente"] = content["email"]
                cliente_bamboo["email"] = content["email"]
                cliente_bamboo["firstname"] = content["cliNombre"] + content["cliRazon"]
                cliente_bamboo["lastname"] = content["cliApellido"]
                cliente_bamboo["documenttypeid"] = content["idTipoID"]
                cliente_bamboo["docnumber"] = content["nroID"]
                cliente_bamboo["phonenumber"] = content["celular"]
                cliente_bamboo["addressdetail"] = content["calle"] + " " + content["nroPuerta"] + " " + content["apto"]
                cliente_bamboo["city"] = content["ciudad"]
                cliente_bamboo["state"] = content["departamente"]
                cliente_bamboo["country"] = content["pais"]
                cliente_bamboo["codigopostal"] = content["codigopostal"]

                uri = endpoint_payments + "add.php"
                response = requests.post(
                    uri,
                    json=cliente_bamboo,
                )
                if response.status_code == 200:
                    cliente_bamboo = response.json()
                else:
                    cliente_bamboo = None

        #Enviamos al cliente notificación de que tiene productos nuevos cargados
        total_dolares = 0
        total_pesos = 0
        for contrato in content['contratos']:
            productos = contrato["productos"]
            for p in productos:
                if p["moneda"]["id"] == 1:
                    total_pesos = total_pesos + p["importe"]
                else:
                    total_dolares = total_dolares + p["importe"]


        html_final = generar_html_correo(
                        content=content,total_dolares=total_dolares,total_pesos=total_pesos,cliente_bamboo=cliente_bamboo
                    )
        send_mail(content["cliente"]["emailaviso"], "[Netgate] - Nueva orden de compra", html_final, "", "", [])

        return jsonify(
            id=content["id"],
            observation="Notificacion, ingresada.",
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )
    except Exception as e:
        return jsonify(
            observation="Archivo dado de alta correctamente.",
            error=False,
            serverdate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ),500