# coding: utf-8
from . import netgate
from flask import request, jsonify, render_template
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from time import gmtime, strftime

endpoint_payments = "https://payments.netgate.com.uy/siemprepago/"
def send_mail(to,subject,body,cc,bcc,files):
    msg = MIMEMultipart("alternative")
    msg['From'] = 'ventas@netgate.com.uy'
    msg['To'] = to

    msg.add_header('Content-Type', 'text/html')

    for path in files:
        try:
            with open(path, 'r') as file:
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