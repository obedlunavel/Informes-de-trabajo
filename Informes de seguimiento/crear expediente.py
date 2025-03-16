import json

# Cargar el archivo planes_trabajo.json
with open('planes_trabajo.json', 'r', encoding='utf-8') as file:
    datos = json.load(file)

# Crear una lista para almacenar los expedientes procesados
expedientes = []

# Recorrer cada expediente en el archivo
for expediente_id, expediente in datos.items():
    # Extraer los campos requeridos
    expediente_procesado = {
        "Unidad": expediente.get("Unidad", ""),
        "Número de Expediente": expediente.get("Número de Expediente", ""),
        "Nombre del Paciente": expediente.get("Nombre del Paciente", ""),
        "Fecha de Nacimiento": expediente.get("Fecha de Nacimiento", ""),
        "Diagnóstico": expediente.get("Diagnóstico", ""),
        "Área de Intervención": expediente.get("Área de Intervención", ""),
        "Observaciones Clínicas": expediente.get("Observaciones Clínicas", ""),
        "Objetivos Iniciales": expediente.get("Programas Seleccionados", [])
    }
    # Agregar el expediente procesado a la lista
    expedientes.append(expediente_procesado)

# Guardar los expedientes procesados en un nuevo archivo expedientes.json
with open('expedientes.json', 'w', encoding='utf-8') as file:
    json.dump(expedientes, file, ensure_ascii=False, indent=4)

print("Los expedientes han sido extraídos y guardados en 'expedientes.json'.")
