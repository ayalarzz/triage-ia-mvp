# =========================
# PDF DEL PACIENTE
# =========================
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf(paciente, triage, confianza, factores, interpretacion):

    file_name = "reporte_paciente.pdf"
    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("REPORTE CLÍNICO - SISTEMA IA TRIAGE", styles["Title"]))
    content.append(Spacer(1, 12))

    for k, v in paciente.items():
        content.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Triage: {triage}", styles["Heading2"]))
    content.append(Paragraph(f"Confianza: {round(confianza*100,2)}%", styles["Normal"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Factores de riesgo:", styles["Heading3"]))
    for f in factores:
        content.append(Paragraph(f"- {f}", styles["Normal"]))

    content.append(Spacer(1, 12))
    content.append(Paragraph("Interpretación clínica:", styles["Heading3"]))
    for i in interpretacion:
        content.append(Paragraph(f"- {i}", styles["Normal"]))

    doc.build(content)

    return file_name


# =========================
# GRÁFICA DE DISTRIBUCIÓN
# =========================
import matplotlib.pyplot as plt
import streamlit as st

def graficar_distribucion(df):

    conteo = df["triage"].value_counts().sort_index()

    fig, ax = plt.subplots()

    ax.bar(conteo.index.astype(str), conteo.values)

    ax.set_title("Distribución de Triage")
    ax.set_xlabel("Nivel de Triage")
    ax.set_ylabel("Cantidad de pacientes")

    st.pyplot(fig)