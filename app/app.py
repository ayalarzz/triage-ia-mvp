import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

import sys
import os

sys.path.append(os.path.abspath(".."))
from explain import explicar_paciente
from utils import generar_pdf, graficar_distribucion

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# =========================
# CONFIGURACIÓN UI
# =========================
st.set_page_config(
    page_title="Sistema IA de Triage",
    page_icon="🏥",
    layout="centered"
)

# =========================
# CARGAR MODELO
# =========================
model = joblib.load("models/triage_model.pkl")

# =========================
# BASE DE DATOS
# =========================
conn = sqlite3.connect("data/triage.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    edad INTEGER,
    temperatura REAL,
    frecuencia_cardiaca INTEGER,
    presion REAL,
    saturacion INTEGER,
    triage INTEGER,
    confianza REAL,
    fecha TEXT
)
""")
conn.commit()

# =========================
# FUNCIONES AUXILIARES
# =========================
def color_triage(triage):
    if triage == 1:
        return "🔴 CRÍTICO"
    elif triage == 2:
        return "🟠 URGENTE"
    elif triage == 3:
        return "🟡 MODERADO"
    elif triage == 4:
        return "🟢 LEVE"
    else:
        return "🔵 NO URGENTE"


def generar_pdf(paciente, triage, confianza, factores, interpretacion):

    file_name = "reporte_paciente.pdf"
    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("REPORTE CLÍNICO - IA TRIAGE", styles["Title"]))
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


def graficar_distribucion(df):
    conteo = df["triage"].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.bar(conteo.index.astype(str), conteo.values)

    ax.set_title("Distribución de Triage")
    ax.set_xlabel("Nivel de Triage")
    ax.set_ylabel("Cantidad de pacientes")

    st.pyplot(fig)

# =========================
# INTERFAZ
# =========================
st.title("🏥 Sistema IA de Apoyo al Triage")
st.write("Ingrese los datos del paciente para evaluación clínica.")

edad = st.number_input("Edad", 0, 120, 30)
temperatura = st.number_input("Temperatura", 30.0, 45.0, 36.5)
fc = st.number_input("Frecuencia cardíaca", 30, 200, 80)
presion = st.number_input("Presión sistólica", 50, 250, 120)
saturacion = st.number_input("Saturación O2", 50, 100, 98)

# =========================
# EVALUACIÓN
# =========================
if st.button("Evaluar paciente"):

    paciente = {
        "edad": edad,
        "temperatura": temperatura,
        "frecuencia_cardiaca": fc,
        "presion_sistolica": presion,
        "saturacion": saturacion
    }

    df_input = pd.DataFrame([paciente])

    pred = model.predict(df_input)[0]
    proba = model.predict_proba(df_input)[0]
    confianza = max(proba)

    factores, interpretacion = explicar_paciente(paciente)

    estado = color_triage(pred)

    # =========================
    # RESULTADOS
    # =========================
    st.subheader("📊 Resultado clínico")

    st.markdown(f"### {estado}")
    st.success(f"Triage sugerido: {pred}")
    st.info(f"Confianza del modelo: {round(confianza*100,2)}%")

    st.subheader("⚠ Factores de riesgo")
    if factores:
        for f in factores:
            st.write("🩺", f)
    else:
        st.success("Sin factores críticos detectados")

    st.subheader("🧠 Interpretación clínica")
    if interpretacion:
        for i in interpretacion:
            st.write("•", i)
    else:
        st.info("Paciente estable según variables")

    # =========================
    # GUARDAR BD
    # =========================
    cursor.execute("""
        INSERT INTO registros (
            edad, temperatura, frecuencia_cardiaca,
            presion, saturacion, triage, confianza, fecha
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        edad, temperatura, fc,
        presion, saturacion,
        int(pred),
        float(confianza),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

    # =========================
    # PDF DESCARGA
    # =========================
    pdf_file = generar_pdf(
        paciente,
        pred,
        confianza,
        factores,
        interpretacion
    )

    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Descargar reporte clínico PDF",
            data=file,
            file_name="reporte_paciente.pdf",
            mime="application/pdf"
        )

    st.success("Registro guardado correctamente")

# =========================
# HISTORIAL
# =========================
st.subheader("📁 Historial de pacientes")

df = pd.read_sql_query("SELECT * FROM registros ORDER BY id DESC", conn)
st.dataframe(df)

# =========================
# GRÁFICO
# =========================
st.subheader("📊 Distribución de triage")

if len(df) > 0:
    graficar_distribucion(df)