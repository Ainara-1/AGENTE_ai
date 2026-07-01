import json

from prompts import SYSTEM_PROMPT
from pipeline import preparar_datos
from llm import llamar_llm
from demo import propuestas_demo, plan_demo

from herramientas import (
    buscar_actividades_cumpleanos,
    calcular_presupuesto_cumpleanos,
    crear_cronograma_cumpleanos,
    sugerir_comida_bebida,
    generar_lista_materiales
)

#USAR_IA = False   # no usa IA

USAR_IA = True   #usa IA


def limpiar_json_respuesta(respuesta):
    respuesta = respuesta.strip()

    if respuesta.startswith("```json"):
        respuesta = respuesta.replace("```json", "").replace("```", "").strip()

    elif respuesta.startswith("```"):
        respuesta = respuesta.replace("```", "").strip()

    return respuesta


def generar_propuestas(datos):
    resultado_pipeline = preparar_datos(datos)
    datos = resultado_pipeline["datos"]
    validacion = resultado_pipeline["validacion"]

    if not validacion["valido"]:
        return {
            "error": validacion["errores"],
            "advertencias": validacion["advertencias"]
        }

    if not USAR_IA:
        return propuestas_demo()

    prompt_usuario = f"""
    Genera 3 propuestas resumidas para un cumpleaños infantil.

    Datos del cumpleaños:
    {json.dumps(datos, ensure_ascii=False, indent=2)}

    Advertencias:
    {json.dumps(validacion["advertencias"], ensure_ascii=False, indent=2)}

    Usa herramientas si las necesitas.

    No uses bloques markdown. No escribas ```json. Devuelve únicamente el objeto JSON puro.
    Devuelve SOLO un JSON válido con esta estructura:

    {{
        "Opción A - Nombre": {{
            "descripcion": "...",
            "actividades": ["...", "..."],
            "motivo": "..."
        }},
        "Opción B - Nombre": {{
            "descripcion": "...",
            "actividades": ["...", "..."],
            "motivo": "..."
        }},
        "Opción C - Nombre": {{
            "descripcion": "...",
            "actividades": ["...", "..."],
            "motivo": "..."
        }}
    }}
    """

    respuesta = llamar_llm(SYSTEM_PROMPT, prompt_usuario)

    try:
        respuesta_limpia = limpiar_json_respuesta(respuesta)
        return json.loads(respuesta_limpia)
    except json.JSONDecodeError:
        return {
            "error": ["El modelo no devolvió un JSON válido."],
            "respuesta_modelo": respuesta
        }


def generar_plan_final(datos, propuesta_elegida):
    resultado_pipeline = preparar_datos(datos)
    datos = resultado_pipeline["datos"]
    validacion = resultado_pipeline["validacion"]

    if not validacion["valido"]:
        return {
            "error": validacion["errores"],
            "advertencias": validacion["advertencias"]
        }

    if not USAR_IA:
        return plan_demo(validacion, datos)

    actividades = buscar_actividades_cumpleanos(
        datos["edad"],
        datos["tipo_espacio"],
        datos["tematica"]
    )

    presupuesto = calcular_presupuesto_cumpleanos(datos["presupuesto"])

    cronograma = crear_cronograma_cumpleanos(
        datos["duracion"],
        actividades
    )

    comida_bebida = sugerir_comida_bebida(
        datos["num_ninos"],
        datos["num_adultos"],
        datos["alergias"]
    )

    materiales = generar_lista_materiales(actividades)

    informacion_plan = {
        "datos": datos,
        "propuesta_elegida": propuesta_elegida,
        "actividades": actividades,
        "presupuesto": presupuesto,
        "cronograma": cronograma,
        "comida_bebida": comida_bebida,
        "materiales": materiales,
        "advertencias": validacion["advertencias"]
    }

    prompt_usuario = f"""
    Crea el plan final completo del cumpleaños infantil.

    IMPORTANTE:
    No llames a herramientas.
    Usa únicamente la información ya calculada que aparece abajo.
    No inventes precios, materiales ni actividades nuevas.
    Redacta el plan de forma clara, útil y organizada.

    Información disponible:
    {json.dumps(informacion_plan, ensure_ascii=False, indent=2)}

    Devuelve el plan utilizando EXACTAMENTE este formato:

    1. Resumen del cumpleaños

    Explica brevemente el tipo de celebración, la edad, el lugar, la duración y la propuesta elegida.

    2. Presupuesto

    • Comida y bebida:

    • Decoración:

    • Actividades:

    • Tarta:

    • Imprevistos:

    3. Cronograma

    15:00 Recepción de invitados

    15:15 Primera actividad

    16:00 Merienda

    16:30 Segunda actividad

    17:30 Tarta y despedida

    4. Actividades recomendadas

    • Actividad 1

    • Actividad 2

    • Actividad 3

    5. Comida y bebida

    Describe el menú recomendado y ten en cuenta las alergias o necesidades especiales.

    6. Lista de compras y materiales

    • Material 1

    • Material 2

    • Material 3

    7. Tareas pendientes

    • Tarea 1

    • Tarea 2
    
    • Tarea 3

    8. Advertencias y datos sin confirmar

    Describe posibles riesgos, información pendiente o aspectos a revisar.

    9. Plan alternativo

    Explica una alternativa si cambia el tiempo o surge algún imprevisto.


    MUY IMPORTANTE:
    - Cada título debe estar en una línea independiente.
    - Después de cada título deja una línea en blanco.
    - Cada elemento de una lista debe ir en una línea distinta.
    - No escribas varias actividades, importes u horarios en la misma línea.
    - Usa siempre guiones para las listas, así:
    - Elemento 1
    - Elemento 2
    - Elemento 3
    - Nunca uses puntos medios "•" para juntar elementos en una misma línea.
    - Nunca escribas el contenido en la misma línea que el título.



    
    """

    plan_texto = llamar_llm(SYSTEM_PROMPT, prompt_usuario)

    return {
        "plan_texto": plan_texto,
        "advertencias": validacion["advertencias"],
        "datos_tecnicos": informacion_plan
    }