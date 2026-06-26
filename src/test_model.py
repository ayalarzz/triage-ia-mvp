import joblib
import pandas as pd
from explain import explicar_paciente

model = joblib.load("models/triage_model.pkl")

paciente = {
    "edad": 25,
    "temperatura": 36.5,
    "frecuencia_cardiaca": 75,
    "presion_sistolica": 110,
    "saturacion": 98
}

df = pd.DataFrame([paciente])

pred = model.predict(df)[0]
proba = model.predict_proba(df)[0]
confianza = max(proba)

factores, interpretacion = explicar_paciente(paciente)

# RESULTADO FINAL
print("\n===== RESULTADO IA TRIAGE =====\n")

print(f"Triage sugerido: {pred}")
print(f"Confianza del modelo: {round(confianza*100,2)}%")

print("\n--- Factores de riesgo detectados ---")
if factores:
    for f in factores:
        print("•", f)
else:
    print("• Ninguno relevante detectado")

print("\n--- Interpretación clínica ---")
if interpretacion:
    for i in interpretacion:
        print("•", i)
else:
    print("• Estado clínico estable según variables ingresadas")

print("\n=====================================\n")