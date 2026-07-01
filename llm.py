import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from herramientas import (
    buscar_actividades_cumpleanos,
    calcular_presupuesto_cumpleanos,
    crear_cronograma_cumpleanos,
    sugerir_comida_bebida,
    generar_lista_materiales
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"


tools = [
    {
        "type": "function",
        "function": {
            "name": "buscar_actividades_cumpleanos",
            "description": "Busca actividades adecuadas para un cumpleaños infantil según edad, espacio y temática.",
            "parameters": {
                "type": "object",
                "properties": {
                    "edad": {"type": "integer"},
                    "tipo_espacio": {"type": "string"},
                    "tematica": {"type": "string"}
                },
                "required": ["edad", "tipo_espacio"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_presupuesto_cumpleanos",
            "description": "Distribuye el presupuesto total del cumpleaños entre categorías.",
            "parameters": {
                "type": "object",
                "properties": {
                    "presupuesto": {"type": "number"}
                },
                "required": ["presupuesto"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crear_cronograma_cumpleanos",
            "description": "Crea un cronograma realista para el cumpleaños usando duración y actividades.",
            "parameters": {
                "type": "object",
                "properties": {
                    "duracion_horas": {"type": "integer"},
                    "actividades": {"type": "array"}
                },
                "required": ["duracion_horas", "actividades"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sugerir_comida_bebida",
            "description": "Sugiere comida y bebida según niños, adultos y alergias.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_ninos": {"type": "integer"},
                    "num_adultos": {"type": "integer"},
                    "alergias": {"type": "string"}
                },
                "required": ["num_ninos", "num_adultos"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generar_lista_materiales",
            "description": "Genera una lista de materiales a partir de actividades seleccionadas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "actividades": {"type": "array"}
                },
                "required": ["actividades"]
            }
        }
    }
]


funciones_disponibles = {
    "buscar_actividades_cumpleanos": buscar_actividades_cumpleanos,
    "calcular_presupuesto_cumpleanos": calcular_presupuesto_cumpleanos,
    "crear_cronograma_cumpleanos": crear_cronograma_cumpleanos,
    "sugerir_comida_bebida": sugerir_comida_bebida,
    "generar_lista_materiales": generar_lista_materiales
}


def llamar_llm(system_prompt, user_prompt):
    mensajes = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    for _ in range(3):
        respuesta = client.chat.completions.create(
            model=MODEL,
            messages=mensajes,
            tools=tools,
            tool_choice="auto",
            temperature=0.4
        )

        mensaje = respuesta.choices[0].message

        if not mensaje.tool_calls:
            return mensaje.content

        mensajes.append(mensaje)

        for tool_call in mensaje.tool_calls:
            nombre_funcion = tool_call.function.name
            argumentos = json.loads(tool_call.function.arguments)

            for clave, valor in argumentos.items():   # con este for convierte alergias de null a texto vacio
                if valor is None:
                    argumentos[clave] = ""

            if nombre_funcion not in funciones_disponibles:
                resultado = {"error": f"Herramienta no disponible: {nombre_funcion}"}
            else:
                funcion = funciones_disponibles[nombre_funcion]
                resultado = funcion(**argumentos)

            mensajes.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(resultado, ensure_ascii=False)
            })

    return "No se pudo completar la respuesta después de ejecutar varias herramientas."