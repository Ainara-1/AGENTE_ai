def normalizar_texto(valor):
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    return valor


def normalizar_datos(datos):
    datos_limpios = datos.copy()

    campos_texto = [
        "lugar",
        "tipo_espacio",
        "tematica",
        "preferencias",
        "alergias",
        "materiales"
    ]

    for campo in campos_texto:
        datos_limpios[campo] = normalizar_texto(datos_limpios.get(campo))

    return datos_limpios


def validar_datos(datos):
    errores = []
    advertencias = []

    if not datos.get("edad"):
        errores.append("Falta indicar la edad del niño/a.")

    if datos.get("presupuesto", 0) <= 0:
        errores.append("El presupuesto debe ser mayor que 0 €.")

    if datos.get("num_ninos", 0) <= 0:
        errores.append("Debe haber al menos un niño invitado.")

    if datos.get("duracion", 0) < 1:
        errores.append("La duración debe ser al menos de 1 hora.")

    if not datos.get("lugar"):
        advertencias.append("No se ha indicado un lugar concreto de celebración.")

    if not datos.get("tematica"):
        advertencias.append("No se ha indicado una temática. El agente propondrá una opción general.")

    if not datos.get("alergias"):
        advertencias.append("No se han indicado alergias o necesidades especiales. Conviene confirmarlo antes de preparar comida.")

    if datos.get("tipo_espacio") == "Exterior":
        advertencias.append("Al ser un evento exterior, será recomendable preparar un plan alternativo por lluvia o mal tiempo.")

    if datos.get("presupuesto", 0) < datos.get("num_ninos", 0) * 5:
        advertencias.append("El presupuesto puede ser ajustado para el número de niños invitados.")

    return {
        "valido": len(errores) == 0,
        "errores": errores,
        "advertencias": advertencias
    }


def enriquecer_datos(datos):
    datos_enriquecidos = datos.copy()

    total_personas = datos.get("num_ninos", 0) + datos.get("num_adultos", 0)
    presupuesto_por_persona = datos.get("presupuesto", 0) / total_personas if total_personas > 0 else 0

    datos_enriquecidos["total_personas"] = total_personas
    datos_enriquecidos["presupuesto_por_persona"] = round(presupuesto_por_persona, 2)

    if datos.get("tipo_espacio") == "Exterior":
        datos_enriquecidos["requiere_plan_alternativo"] = True
    else:
        datos_enriquecidos["requiere_plan_alternativo"] = False

    return datos_enriquecidos


def preparar_datos(datos):
    datos_limpios = normalizar_datos(datos)
    resultado_validacion = validar_datos(datos_limpios)
    datos_enriquecidos = enriquecer_datos(datos_limpios)

    return {
        "datos": datos_enriquecidos,
        "validacion": resultado_validacion
    }