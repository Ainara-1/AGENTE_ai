from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generar_pdf(plan_texto):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=30,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#ff4b8b"),
        alignment=1,
        spaceAfter=14
    )

    seccion = ParagraphStyle(
        "Seccion",
        parent=styles["Heading2"],
        fontSize=15,
        textColor=colors.HexColor("#1e88e5"),
        spaceBefore=14,
        spaceAfter=8
    )

    texto = ParagraphStyle(
        "Texto",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=15,
        spaceAfter=6
    )

    elementos = []

    # Banner superior
    banner = Image("images/logo_cumpleplan.png", width=505, height=135)
    elementos.append(banner)
    elementos.append(Spacer(1, 16))

    elementos.append(
        Paragraph("PLAN PERSONALIZADO DE CUMPLEAÑOS", titulo)
    )

    elementos.append(Spacer(1, 10))

    for linea in plan_texto.splitlines():
        linea = linea.strip()

        if not linea:
            elementos.append(Spacer(1, 6))
            continue

        linea = linea.replace("€", "EUR")

        if linea[0].isdigit() and "." in linea[:3]:
            elementos.append(Paragraph(linea, seccion))
        else:
            elementos.append(Paragraph(linea, texto))

    doc.build(elementos)

    buffer.seek(0)
    return buffer