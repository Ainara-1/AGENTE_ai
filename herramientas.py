def buscar_actividades_cumpleanos(edad, tipo_espacio, tematica=None):
    actividades = []

    if edad <= 4:
        actividades = [
            {
                "nombre": "Juegos con música",
                "duracion": 20,
                "material": "Altavoz y canciones infantiles",
                "motivo": "Actividad sencilla, segura y adecuada para niños pequeños."
            },
            {
                "nombre": "Cuentacuentos",
                "duracion": 20,
                "material": "Cuento o marionetas",
                "motivo": "Actividad tranquila que ayuda a evitar sobreestimulación."
            },
            {
                "nombre": "Pompas de jabón",
                "duracion": 15,
                "material": "Pomperos infantiles",
                "motivo": "Actividad visual y segura con supervisión adulta."
            }
        ]

    elif edad <= 7:
        actividades = [
            {
                "nombre": "Búsqueda del tesoro",
                "duracion": 30,
                "material": "Pistas, bolsas y pequeños premios",
                "motivo": "Actividad participativa y adaptable a distintas temáticas."
            },
            {
                "nombre": "Manualidades temáticas",
                "duracion": 30,
                "material": "Cartulinas, pegatinas, pinturas y tijeras infantiles",
                "motivo": "Permite personalizar la celebración según la temática."
            },
            {
                "nombre": "Estatuas musicales",
                "duracion": 20,
                "material": "Música",
                "motivo": "Juego sencillo, divertido y fácil de organizar."
            }
        ]

    else:
        actividades = [
            {
                "nombre": "Gymkana por equipos",
                "duracion": 40,
                "material": "Tarjetas de pruebas, conos y pequeños premios",
                "motivo": "Actividad dinámica adecuada para niños más mayores."
            },
            {
                "nombre": "Concurso de retos",
                "duracion": 30,
                "material": "Tarjetas con retos seguros",
                "motivo": "Fomenta la participación y el trabajo en equipo."
            },
            {
                "nombre": "Escape room sencillo",
                "duracion": 35,
                "material": "Pistas, candados simbólicos y sobres",
                "motivo": "Actividad más compleja y motivadora para edades mayores."
            }
        ]

    if tipo_espacio == "Interior":
        actividades.append({
            "nombre": "Juego de mímica",
            "duracion": 20,
            "material": "Tarjetas con acciones",
            "motivo": "Actividad adecuada para espacios cerrados."
        })

    if tipo_espacio == "Exterior":
        actividades.append({
            "nombre": "Carrera de relevos suave",
            "duracion": 25,
            "material": "Conos o marcas en el suelo",
            "motivo": "Aprovecha el espacio abierto sin ser una actividad peligrosa."
        })

    return actividades


def calcular_presupuesto_cumpleanos(presupuesto):
    presupuesto = float(presupuesto)

    return {
        "Comida y bebida": round(presupuesto * 0.35, 2),
        "Decoración": round(presupuesto * 0.15, 2),
        "Actividades": round(presupuesto * 0.20, 2),
        "Tarta": round(presupuesto * 0.20, 2),
        "Imprevistos": round(presupuesto * 0.10, 2)
    }



def crear_cronograma_cumpleanos(duracion_horas, actividades):
    duracion_minutos = int(duracion_horas) * 60

    cronograma = []
    tiempo_usado = 0

    cronograma.append({
        "momento": "Inicio",
        "actividad": "Recepción de invitados",
        "duracion": 15
    })
    tiempo_usado += 15

    tiempo_reservado_final = 45

    for actividad in actividades:

        if isinstance(actividad, dict):
            nombre_actividad = actividad.get("nombre", "Actividad")
            duracion_actividad = actividad.get("duracion", 20)

        elif isinstance(actividad, str):
            nombre_actividad = actividad
            duracion_actividad = 20

        else:
            continue

        if tiempo_usado + duracion_actividad <= duracion_minutos - tiempo_reservado_final:
            cronograma.append({
                "momento": "Durante la fiesta",
                "actividad": nombre_actividad,
                "duracion": duracion_actividad
            })
            tiempo_usado += duracion_actividad

    cronograma.append({
        "momento": "Merienda",
        "actividad": "Comida, bebida y descanso",
        "duracion": 25
    })

    cronograma.append({
        "momento": "Final",
        "actividad": "Tarta, fotos y despedida",
        "duracion": 20
    })

    return cronograma




def sugerir_comida_bebida(num_ninos, num_adultos, alergias=None):
    total_personas = num_ninos + num_adultos

    comida = {
        "bebida": f"{max(1, round(total_personas * 0.5))} litros de agua o bebida sin gas",
        "salado": f"{num_ninos * 2} raciones pequeñas de comida salada",
        "dulce": f"{num_ninos * 2} raciones pequeñas de dulce",
        "tarta": "Tarta adaptada al número de invitados",
        "nota_alergias": "Comprobar alergias e intolerancias antes de comprar comida."
    }

    if alergias:
        comida["nota_alergias"] = f"Tener en cuenta estas alergias o necesidades: {alergias}. Validar siempre con un adulto responsable."

    return comida

def generar_lista_materiales(actividades):
    materiales = []

    for actividad in actividades:

        if isinstance(actividad, dict):
            material = actividad.get("material")
            if material:
                materiales.append(material)

        elif isinstance(actividad, str):
            materiales.append(f"Material general para: {actividad}")

    materiales.extend([
        "Servilletas",
        "Vasos",
        "Platos",
        "Mantel",
        "Bolsas de basura",
        "Velas para la tarta"
    ])

    return list(set(materiales))





