import streamlit as st
from agente import generar_propuestas, generar_plan_final

from exportar import generar_pdf

st.set_page_config(
    page_title="CumplePlan",
    page_icon="🎂",
    layout="wide"
)

# -----------------------------
# ESTADO INICIAL
# -----------------------------
def inicializar_estado():
    valores = {
        "paso": 1,
        "datos_cumple": None,
        "propuestas": None,
        "propuesta_elegida": None,
        "plan_final": None,
    }

    for clave, valor in valores.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def ir_a_paso(paso):
    st.session_state.paso = paso


def reiniciar_cumple():
    st.session_state.paso = 1
    st.session_state.datos_cumple = None
    st.session_state.propuestas = None
    st.session_state.propuesta_elegida = None
    st.session_state.plan_final = None


inicializar_estado()


# -----------------------------
# NAVEGACIÓN VISUAL
# -----------------------------
def mostrar_pasos():
    paso_actual = st.session_state.paso - 1

    pasos = [
        ("📝", "Datos"),
        ("⭐", "Propuesta"),
        ("📋", "Plan")
    ]

    cols = st.columns(3)

    for i, (icono, texto) in enumerate(pasos):
        paso = i + 1

        if paso == paso_actual:
            color = "#ff4b8b"
            fondo = "#ffe5f0"
        else:
            color = "#5c5c5c"
            fondo = "#f4f4f4"

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background:{fondo};
                    border-radius:15px;
                    padding:12px;
                    text-align:center;
                    border:2px solid {color};
                    font-weight:bold;
                    color:{color};
                    font-size:18px;
                ">
                    <div style="font-size:28px">{icono}</div>
                    {texto}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# MOSTRAR PLAN POR SECCIONES
# -----------------------------

def formatear_contenido_seccion(titulo, contenido):
    import re

    texto = "\n".join(contenido).strip()

    if "cronograma" in titulo.lower():
        texto = re.sub(r"\s*(\d{1,2}:\d{2})", r"\n- \1", texto)

        texto = texto.strip()
        if texto.startswith("-"):
            return texto
        return "- " + texto
    
    if "presupuesto" in titulo.lower():
        texto = texto.replace(" • ", "\n- ")
        texto = texto.replace("• ", "- ")

    if (
        "actividades" in titulo.lower()
        or "materiales" in titulo.lower()
        or "tareas" in titulo.lower()
    ):
        texto = texto.replace(" • ", "\n- ")
        texto = texto.replace("• ", "- ")

    return texto


def mostrar_plan_por_secciones(plan_texto):
    iconos = {
        "resumen": "📌",
        "presupuesto": "💰",
        "cronograma": "⏰",
        "actividades": "🎈",
        "comida": "🍕",
        "lista": "🛒",
        "materiales": "🛒",
        "tareas": "✅",
        "advertencias": "⚠️",
        "plan alternativo": "☔"
    }

    lineas = plan_texto.splitlines()
    secciones = []
    seccion_actual = None

    for linea in lineas:
        texto = linea.strip()

        es_titulo = (
            texto
            and len(texto) > 2
            and texto[0].isdigit()
            and "." in texto[:3]
        )

        if es_titulo:
            if seccion_actual:
                secciones.append(seccion_actual)

            icono = "📋"
            titulo_lower = texto.lower()

            for clave, valor in iconos.items():
                if clave in titulo_lower:
                    icono = valor
                    break

            seccion_actual = {
                "titulo": f"{icono} {texto}",
                "contenido": []
            }

        else:
            if seccion_actual:
                seccion_actual["contenido"].append(linea)

    if seccion_actual:
        secciones.append(seccion_actual)

    if not secciones:
        st.markdown(plan_texto)
        return

    for seccion in secciones:

        if "resumen" in seccion["titulo"].lower():
            continue

        with st.container(border=True):
            st.subheader(seccion["titulo"])

            contenido = formatear_contenido_seccion(
                seccion["titulo"],
                seccion["contenido"]
            )

            if contenido:
                st.markdown(contenido)











# -----------------------------
# PASO 1: PORTADA
# -----------------------------
if st.session_state.paso == 1:

    st.image("images/portada_cumpleplan.png", use_container_width=True)

    #st.markdown(
    #    "<h3 style='text-align:center;'>Planifica un cumpleaños infantil personalizado en pocos minutos mediante inteligencia artificial.</h3>",
    #    unsafe_allow_html=True
    #)

    if st.button("🚀 Comenzar planificación", use_container_width=True):
        ir_a_paso(2)
        st.rerun()


# -----------------------------
# CABECERA RESTO DE PASOS
# -----------------------------
else:
    mostrar_pasos()


# -----------------------------
# PASO 2: FORMULARIO
# -----------------------------
if st.session_state.paso == 2:

    st.header("1. Datos del cumpleaños")
    st.write("Complete la siguiente información para que CumplePlan pueda generar varias propuestas personalizadas.")

    with st.form("formulario_cumple"):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("👶 Datos")
            edad = st.number_input("Edad", min_value=1, max_value=14, step=1)
            fecha = st.date_input("Fecha")
            num_ninos = st.number_input("Niños invitados", min_value=1, step=1)
            num_adultos = st.number_input("Adultos", min_value=0, step=1)
            presupuesto = st.number_input("Presupuesto (€)", min_value=0, step=10)

        with col2:
            st.subheader("🎈 Celebración")
            lugar = st.text_input("Lugar")
            tipo_espacio = st.selectbox("Espacio", ["Interior", "Exterior", "Mixto"])
            duracion = st.slider("Duración (horas)", 1, 8, 3)

        with col3:
            st.subheader("⭐ Información extra")
            tematica = st.text_input("Temática")
            preferencias = st.text_area("Preferencias", height=90)
            alergias = st.text_area("Alergias o necesidades especiales", height=90)
            materiales = st.text_area("Material disponible", height=90)

        enviar = st.form_submit_button(
            "🎂 Generar propuestas",
            use_container_width=True
        )

    if enviar:
        st.session_state.datos_cumple = {
            "edad": edad,
            "fecha": str(fecha),
            "num_ninos": num_ninos,
            "num_adultos": num_adultos,
            "presupuesto": presupuesto,
            "lugar": lugar,
            "tipo_espacio": tipo_espacio,
            "duracion": duracion,
            "tematica": tematica,
            "preferencias": preferencias,
            "alergias": alergias,
            "materiales": materiales
        }

        # Si los datos cambian, las propuestas y el plan anterior ya no son válidos
        st.session_state.propuestas = None
        st.session_state.propuesta_elegida = None
        st.session_state.plan_final = None

        ir_a_paso(3)
        st.rerun()


# -----------------------------
# PASO 3: PROPUESTAS
# -----------------------------


elif st.session_state.paso == 3:

    st.header("🎉 2. Elige una propuesta")
    st.write("CumplePlan ha preparado tres opciones personalizadas. Elige la que más encaje con tu idea.")

    if st.session_state.propuestas is None:
        with st.spinner("🎈 CumplePlan está generando propuestas personalizadas..."):
            st.session_state.propuestas = generar_propuestas(
                st.session_state.datos_cumple
            )

    propuestas = st.session_state.propuestas

    if "error" in propuestas:
        st.error("Hay datos que debes corregir antes de generar propuestas.")

        for error in propuestas["error"]:
            st.warning(error)

        if st.button("← Volver a corregir datos", use_container_width=True):
            st.session_state.propuestas = None
            ir_a_paso(2)
            st.rerun()

        st.stop()

    colores = [
        {
            "borde": "#ff4b8b",
            "etiqueta": "#ff4b8b",
            "emoji": "🎨",
            "opcion": "OPCIÓN A"
        },
        {
            "borde": "#1e88e5",
            "etiqueta": "#1e88e5",
            "emoji": "🚀",
            "opcion": "OPCIÓN B"
        },
        {
            "borde": "#2ecc71",
            "etiqueta": "#2ecc71",
            "emoji": "🎂",
            "opcion": "OPCIÓN C"
        }
    ]

    for i, (nombre, contenido) in enumerate(propuestas.items()):
        color = colores[i % len(colores)]
        titulo = nombre.split(" - ", 1)[1] if " - " in nombre else nombre

        #st.markdown(

        st.markdown(
            f"""
            <div style="
                border-top:6px solid {color["borde"]};
                border-left:6px solid {color["borde"]};
                border-right:6px solid {color["borde"]};
                border-radius:22px 22px 0 0;
                padding:20px 24px 0 24px;
                margin-top:24px;
                box-shadow:0 0 18px {color["borde"]}88;
            ">
            """,
            unsafe_allow_html=True
        )



        st.markdown("<br>", unsafe_allow_html=True)



        col_icono, col_info, col_actividades, col_motivo = st.columns([0.7, 2, 2.2, 2])

        with col_icono:
            st.markdown(
                f"""
                <div style="
                    width:90px;
                    height:90px;
                    border-radius:50%;
                    background:{color["borde"]};
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:44px;
                    margin-top:20px;
                ">
                    {color["emoji"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_info:
            st.markdown(
                f"""
                <div style="
                    display:inline-block;
                    background:{color["etiqueta"]};
                    color:white;
                    padding:6px 16px;
                    border-radius:12px;
                    font-weight:800;
                    font-size:15px;
                    letter-spacing:1px;
                    margin-bottom:10px;
                ">
                    ⭐ {color["opcion"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(f"### {titulo}")

            st.markdown("#### 🎈 Descripción")
            st.write(contenido.get("descripcion", ""))


        with col_actividades:
            st.markdown("### 🎯 Actividades")
            for actividad in contenido.get("actividades", []):
                st.success(f"✅ {actividad}")

        with col_motivo:
            st.markdown("### 💡 Motivo")
            st.info(contenido.get("motivo", "Propuesta adaptada a los datos indicados."))

            if st.button(
                " 🎂 Elegir esta propuesta",
                key=f"elegir_propuesta_{i}",
                #key=f"elegir_{nombre}",
                use_container_width=True
            ):
                st.session_state.propuesta_elegida = nombre
                st.session_state.plan_final = None
                ir_a_paso(4)
                st.rerun()


        

        st.markdown(
            f"""
            <div style="
                border-bottom:6px solid {color["borde"]};
                border-left:6px solid {color["borde"]};
                border-right:6px solid {color["borde"]};
                border-radius:0 0 22px 22px;
                padding:0 24px 20px 24px;
                margin-bottom:24px;
                box-shadow:0 0 18px {color["borde"]}88;
            "></div>
            """,
            unsafe_allow_html=True
        )


    if st.button("← Modificar datos", use_container_width=True):
        st.session_state.propuestas = None
        st.session_state.plan_final = None
        ir_a_paso(2)
        st.rerun()


# -----------------------------
# PASO 4: PLAN FINAL
# -----------------------------
elif st.session_state.paso == 4:

    st.header("📋 3. Plan completo")

    datos = st.session_state.datos_cumple

    propuesta_limpia = (
        st.session_state.propuesta_elegida.split(" - ", 1)[1]
        if " - " in st.session_state.propuesta_elegida
        else st.session_state.propuesta_elegida
    )

    with st.container(border=True):
        st.markdown("### 🎂 1. Datos del cumpleaños")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("👶 Edad", f"{datos['edad']} años")

        with col2:
            st.metric("👧 Niños", datos["num_ninos"])

        with col3:
            st.metric("💰 Presupuesto", f"{datos['presupuesto']} €")

        with col4:
            st.metric("📍 Espacio", datos["tipo_espacio"])

        with col5:
            st.metric("⏰ Duración", f"{datos['duracion']} h")

        st.success(f"⭐ Propuesta elegida: {propuesta_limpia}")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.plan_final is None:
        with st.spinner("📋 CumplePlan está preparando el plan completo..."):
            st.session_state.plan_final = generar_plan_final(
                st.session_state.datos_cumple,
                st.session_state.propuesta_elegida
            )

    plan = st.session_state.plan_final

    if "error" in plan:
        st.error(plan["error"])
        st.stop()

    mostrar_plan_por_secciones(plan["plan_texto"])


    col_pdf, col_txt = st.columns(2)

    with col_pdf:
        pdf = generar_pdf(plan["plan_texto"])

        st.download_button(
            "📄 Descargar PDF",
            data=pdf,
            file_name="plan_cumpleplan.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with col_txt:
        st.download_button(
            "📝 Descargar TXT",
            data=plan["plan_texto"],
            file_name="plan_cumpleplan.txt",
            mime="text/plain",
            use_container_width=True
        )


    

    if plan.get("advertencias"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚠️ Recomendaciones importantes")

        for advertencia in plan["advertencias"]:
            st.warning(advertencia)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("← Cambiar propuesta", use_container_width=True):
            ir_a_paso(3)
            st.rerun()

    with col2:
        if st.button("📝 Modificar datos", use_container_width=True):
            st.session_state.propuestas = None
            st.session_state.propuesta_elegida = None
            st.session_state.plan_final = None
            ir_a_paso(2)
            st.rerun()

    with col3:
        if st.button("🎂 Nuevo cumpleaños", use_container_width=True):
            reiniciar_cumple()
            st.rerun()