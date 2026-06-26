def explicar_paciente(data):
    
    factores = []
    interpretacion = []

    # Saturación
    if data["saturacion"] < 90:
        factores.append("Saturación de oxígeno críticamente baja")
        interpretacion.append("Posible compromiso respiratorio")

    elif data["saturacion"] < 93:
        factores.append("Saturación de oxígeno reducida")
        interpretacion.append("Riesgo respiratorio moderado")

    # Frecuencia cardíaca
    if data["frecuencia_cardiaca"] > 120:
        factores.append("Taquicardia significativa")
        interpretacion.append("Posible respuesta a estrés fisiológico o infección")

    elif data["frecuencia_cardiaca"] > 100:
        factores.append("Frecuencia cardíaca elevada")
        interpretacion.append("Posible alteración hemodinámica leve")

    # Temperatura
    if data["temperatura"] > 38.5:
        factores.append("Fiebre")
        interpretacion.append("Posible proceso infeccioso")

    # Edad
    if data["edad"] > 70:
        factores.append("Paciente adulto mayor")
        interpretacion.append("Mayor riesgo de complicaciones")

    return factores, interpretacion