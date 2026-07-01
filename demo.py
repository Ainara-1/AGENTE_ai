def propuestas_demo():
    return {
        "Opción A - Cumpleaños creativo": {
            "descripcion": "Una propuesta tranquila con manualidades, juegos musicales y decoración personalizada.",
            "actividades": [
                "Manualidades temáticas",
                "Estatuas musicales",
                "Decoración de máscaras"
            ],
            "motivo": "Es una opción segura, sencilla y fácil de adaptar a distintas edades."
        },
        "Opción B - Cumpleaños activo": {
            "descripcion": "Una propuesta con juegos dinámicos, movimiento y actividades por equipos.",
            "actividades": [
                "Búsqueda del tesoro",
                "Gymkana por equipos",
                "Carrera de relevos"
            ],
            "motivo": "Aprovecha bien el espacio y mantiene a los niños entretenidos."
        },
        "Opción C - Cumpleaños equilibrado": {
            "descripcion": "Una mezcla de juegos activos, momentos tranquilos, merienda y tarta.",
            "actividades": [
                "Juego de mímica",
                "Manualidades rápidas",
                "Tarta y fotos"
            ],
            "motivo": "Combina diversión, descanso y momentos importantes de la celebración."
        }
    }


def plan_demo(validacion, datos):
    presupuesto = datos.get("presupuesto", 0)

    comida = round(presupuesto * 0.35, 2)
    decoracion = round(presupuesto * 0.15, 2)
    actividades = round(presupuesto * 0.20, 2)
    tarta = round(presupuesto * 0.20, 2)
    imprevistos = round(presupuesto * 0.10, 2)

    return {
        "plan_texto": f"""
1. Resumen del cumpleaños

El cumpleaños está pensado para una celebración infantil personalizada, adaptada a la edad de {datos.get("edad")} años, con {datos.get("num_ninos")} niños invitados y {datos.get("num_adultos")} adultos. Se celebrará en un espacio {datos.get("tipo_espacio")} y tendrá una duración aproximada de {datos.get("duracion")} horas.

2. Presupuesto

- Comida y bebida: {comida} €
- Decoración: {decoracion} €
- Actividades: {actividades} €
- Tarta: {tarta} €
- Imprevistos: {imprevistos} €

3. Cronograma

- 15:00 Recepción de invitados.
- 15:15 Primera actividad principal.
- 16:00 Merienda y descanso.
- 16:30 Segunda actividad.
- 17:15 Tarta, fotos y despedida.

4. Actividades recomendadas

- Juego inicial para romper el hielo.
- Actividad principal relacionada con la temática.
- Juego tranquilo antes de la merienda.
- Momento final con tarta y fotos.

5. Comida y bebida

Se recomienda preparar comida sencilla, bebida sin gas y una tarta adaptada al número de invitados.

Antes de comprar comida, se deben revisar alergias o necesidades especiales.

6. Lista de compras y materiales

- Platos.
- Vasos.
- Servilletas.
- Mantel.
- Decoración temática.
- Material para juegos.
- Bolsas de basura.
- Velas para la tarta.

7. Tareas pendientes

- Confirmar número final de invitados.
- Revisar alergias.
- Comprar materiales.
- Preparar decoración.
- Organizar el espacio antes de la fiesta.

8. Advertencias y datos sin confirmar

Comprobar que el espacio permite realizar todas las actividades y confirmar cualquier necesidad especial.

9. Plan alternativo

Si la celebración es en exterior, preparar una alternativa cubierta en caso de lluvia.
""",
        "advertencias": validacion["advertencias"],
        "datos_tecnicos": datos
    }