import json

# Cargar el archivo planes_trabajo.json
with open('planes_trabajo.json', 'r', encoding='utf-8') as file:
    datos = json.load(file)

# Crear una lista para almacenar los expedientes procesados
expedientes = []

# Recorrer cada expediente en el archivo
for expediente_id, expediente in datos.items():
    # Extraer y mapear los campos requeridos
    expediente_procesado = {
        "Unidad": expediente.get("Unidad", ""),
        "Número de Expediente": expediente.get("Número de Expediente", ""),
        "Nombre del Paciente": expediente.get("Nombre del Paciente", ""),
        "Fecha de Nacimiento": expediente.get("Fecha de Nacimiento", ""),
        "Diagnóstico": expediente.get("Diagnóstico", ""),
        "Área de Intervención": expediente.get("Área de Intervención", ""),
        "Observaciones Clínicas": expediente.get("Observaciones Clínicas", ""),
        "Objetivos Iniciales": expediente.get("Programas Seleccionados", []),
        "fecha": expediente.get("fecha", ""),
        "edad": expediente.get("edad", ""),
        "periodo_intervencion": expediente.get("periodo_intervencion", ""),
        "terapias_recibidas": expediente.get("terapias_recibidas", ""),
        "faltas": expediente.get("faltas", ""),
        "avance_objetivos": expediente.get("avance_objetivos", ""),
        "nuevos_objetivos": expediente.get("nuevos_objetivos", []),
        "tratamiento": expediente.get("tratamiento", ""),
        "sugerencias_casa": expediente.get("sugerencias_casa", ""),
        "elaborado_por": expediente.get("elaborado_por", ""),
        "cedula": expediente.get("cedula", "")
    }
    # Agregar el expediente procesado a la lista
    expedientes.append(expediente_procesado)

# Guardar los expedientes procesados en un nuevo archivo expedientes.json
with open('expedientes.json', 'w', encoding='utf-8') as file:
    json.dump(expedientes, file, ensure_ascii=False, indent=4)

print("Los expedientes han sido extraídos y guardados en 'expedientes.json'.")
