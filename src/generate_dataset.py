import pandas as pd
import numpy as np

np.random.seed(42)

n = 3000

data = []

for _ in range(n):

    edad = np.random.randint(1, 95)

    temperatura = round(np.random.uniform(35, 41), 1)

    frecuencia_cardiaca = np.random.randint(50, 160)

    presion_sistolica = np.random.randint(80, 200)

    saturacion = np.random.randint(80, 100)

    if saturacion < 88 or frecuencia_cardiaca > 130:
        triage = 1

    elif saturacion < 92 or frecuencia_cardiaca > 115:
        triage = 2

    elif temperatura > 38.5:
        triage = 3

    elif edad > 70:
        triage = 4

    else:
        triage = 5

    data.append([
        edad,
        temperatura,
        frecuencia_cardiaca,
        presion_sistolica,
        saturacion,
        triage
    ])

df = pd.DataFrame(data, columns=[
    "edad",
    "temperatura",
    "frecuencia_cardiaca",
    "presion_sistolica",
    "saturacion",
    "triage"
])

df.to_csv("data/triage_dataset.csv", index=False)

print(df.head())
print("Dataset generado correctamente.")