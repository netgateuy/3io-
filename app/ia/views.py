import os
from flask import Flask, request, jsonify, session
from google import genai
from google.genai import types
from . import ia
import re
from ..models.Oportunidad import Oportunidad

# Configuración del nuevo cliente
# La API KEY se pasa directamente al instanciar el cliente
client = genai.Client(api_key="AIzaSyBg4f7Z_7r7JEuamOKBqcVvBqLk3y7Fn3k",http_options={'api_version': 'v1beta'})

# --- FUNCIONES SIMULADAS DE TU CRM ---
def consultar_estado_oportunidad(idoportunidad: str):
    oportunidad = Oportunidad.query.filter_by(id=int(idoportunidad)).first()

    # Serializamos manualmente a un diccionario
    oportunidad = {
        "id": oportunidad.id,
        "cliente": oportunidad.idcliente,
        "estado": oportunidad.estado,
        "responsable": oportunidad.responsable,
        "fechainicio": str(oportunidad.fechainicio),
        "fechafin": str(oportunidad.fechafin),
        "fechaalta": str(oportunidad.fechaalta),
    }
    return {"idoportunidad": idoportunidad, "oportunidad": oportunidad}

def listar_reclamos_pendientes(cliente: str):
    """Obtiene la lista de reclamos abiertos de un cliente."""
    return {"cliente": cliente, "reclamos": ["Retraso en entrega", "Tarambana"]}

def obtener_datos_reclamo(idreclamo: str):
    return {
            "id": "REC-001",
            "asunto": "Corte de servicio de Internet",
            "estado": "En revisión técnica",
            "fecha_creacion": "2026-01-05",
            "prioridad": "Alta",
            "tiempo_estimado": "4 horas",
            "tecnico_asignado": "Carlos Rodríguez"
        }

# --- CONFIGURACIÓN DE HERRAMIENTAS ---
# En el nuevo SDK, las herramientas se definen en la configuración
tools = [consultar_estado_oportunidad, listar_reclamos_pendientes, obtener_datos_reclamo]
config = types.GenerateContentConfig(
    tools=tools,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
    system_instruction="""ERES EL ASISTENTE VIRTUAL INTEGRADO DEL CRM 3iO+.
    REGLA DE ORO: TU SALIDA DEBE SER EXCLUSIVAMENTE EL TEXTO FINAL QUE VERÁ EL USUARIO. ESTÁ TERMINANTEMENTE PROHIBIDO INCLUIR INTRODUCCIONES (EJ: "AQUÍ TIENES..."), COMENTARIOS, EXPLICACIONES O SUGERENCIAS POSTERIORES.
    
    FORMATO OBLIGATORIO:
    1. USA ÚNICAMENTE HTML PARA EL FORMATO.
    2. ESTÁ TOTALMENTE PROHIBIDO EL USO DE MARKDOWN O ASTERISCOS (*). NO ESCRIBAS NUNCA '**'.
    3. SI QUIERES RESALTAR ALGO, USA LA ETIQUETA <strong>.
    4. SI QUIERES HACER UNA LISTA, USA LAS ETIQUETAS <ul> Y <li>.
    
    COMPORTAMIENTO:
    - RESPONDE DIRECTAMENTE AL USUARIO DE FORMA BREVE Y PROFESIONAL.
    - SI EL USUARIO SALUDA, RESPONDE: "Hola. Bienvenido al CRM <strong>3iO+</strong>. ¿Cómo puedo ayudarte hoy con tus oportunidades o reclamos?".
    - POR ERRORES TÉCNICOS, INDICA QUE DEBEN HABLAR CON SOPORTE.""")

@ia.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("mensaje")
    history_data = session.get('chat_history', [])

    # Iniciamos la sesión de chat con la configuración de herramientas
    chat_session = client.chats.create(
        model='gemini-flash-latest',
        config=config,
        history=history_data
    )

    # Enviamos el mensaje
    response = chat_session.send_message(user_input)

    serializable_history = []
    for content in chat_session._curated_history:
        # El SDK de GenAI suele tener un método .model_dump() o puedes usar vars()
        # En la versión 3.13 de Python y el nuevo SDK de GenAI, lo ideal es:
        serializable_history.append(content.model_dump())

    # 3. Guardamos la lista de diccionarios (esto sí es JSON serializable)
    session['chat_history'] = serializable_history

    texto_ia = response.text

    # 2. Usamos Regex para convertir **texto** en <strong>texto</strong>
    # Esto busca el patrón de asteriscos y lo reemplaza por etiquetas HTML
    texto_limpio = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto_ia)

    # 3. (Opcional) Convertir asteriscos simples en itálica
    texto_limpio = re.sub(r'\*(.*?)\*', r'<i>\1</i>', texto_limpio)

    # Mantenemos exactamente tu misma estructura de respuesta JSON
    return jsonify({
        "respuesta_ia": texto_limpio,
        "historial_llamadas": [
            str(part.function_call)
            for part in response.candidates[0].content.parts
            if part.function_call
        ]
    })