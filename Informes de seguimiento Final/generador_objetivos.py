# generador_objetivos.py
import json
import tkinter as tk
from tkinter import messagebox

def generar_nuevos_objetivos(expediente, campos_modificados):
    """
    Genera nuevos objetivos basados en el avance de los iniciales
    y actualiza `campos_modificados["nuevos_objetivos"]` en tiempo real.
    """
    try:
        with open("objetivos.json", "r", encoding="utf-8") as f:
            objetivos = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando objetivos: {str(e)}")
        return []

    nuevos_objetivos = []
    objetivos_iniciales = expediente.get("Objetivos Iniciales", [])
    
    # 🔹 Paso 1: Reusar objetivos no cumplidos
    for obj_id in objetivos_iniciales:
        estado_key = f"avance_objetivo_{obj_id}"
        estado = campos_modificados.get(estado_key, "sin_ayuda")

        if isinstance(estado, tk.StringVar):
            estado = estado.get()

        if estado in ["con_ayuda", "no_logra"]:  # Si no ha logrado el objetivo
            nuevos_objetivos.append(str(obj_id))  # Asegurar que sean strings
    
    # 🔹 Paso 2: Generar secuencia numérica ascendente
    contador = 1
    max_objetivos = 50  # Límite máximo de búsqueda

    while len(nuevos_objetivos) < 10 and contador <= max_objetivos:
        nuevo_id = str(contador)
        
        # Verificar si el objetivo existe y no está repetido
        if (nuevo_id in objetivos and 
            nuevo_id not in objetivos_iniciales and 
            nuevo_id not in nuevos_objetivos):
            nuevos_objetivos.append(nuevo_id)

        contador += 1
    
    # 🔥 ✅ Actualizar `campos_modificados` como lista real, no como string
    campos_modificados["nuevos_objetivos"] = nuevos_objetivos  


    return nuevos_objetivos

def construir_nuevos_objetivos_frame(expediente, parent_frame, campos_modificados):
    """Construye el frame de visualización de nuevos objetivos y actualiza dinámicamente."""
    frame = tk.Frame(parent_frame, bg="#FFFFFF")
    frame.grid(row=13, column=1, padx=10, pady=5, sticky="w")  

    try:
        with open("objetivos.json", "r", encoding="utf-8") as f:
            objetivos_data = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando objetivos: {str(e)}")
        return frame

    nuevos_objetivos = campos_modificados.get("nuevos_objetivos", [])  # ✅ Buscar en campos_modificados

    for idx, obj_id in enumerate(nuevos_objetivos):
        if obj_id not in objetivos_data:
            continue

        # Frame por fila
        fila = tk.Frame(frame, bg="#FFFFFF")
        fila.grid(row=idx, column=0, sticky="w", pady=2)

        # Número de objetivo
        tk.Label(fila, 
                text=f"Objetivo {idx+1}:", 
                bg="#FFFFFF",
                width=12,
                anchor="w").grid(row=0, column=0, sticky="w")

        # ✅ Cambiar Label por Entry para poder extraer los valores después
        entry = tk.Entry(fila, bg="#FFFFFF")
        entry.insert(0, obj_id)  # Prellenar con el ID del objetivo
        entry.grid(row=0, column=1, sticky="w")

        # ✅ Guardar referencia en campos_modificados
        campos_modificados[f"nuevo_objetivo_{idx}"] = entry  

    # 🔥 ✅ Forzar actualización y extraer nuevos objetivos automáticamente
    frame.update_idletasks()
    actualizar_nuevos_objetivos(expediente, campos_modificados)

    return frame

def actualizar_nuevos_objetivos(expediente, campos_modificados):
    """Actualiza automáticamente `nuevos_objetivos` cuando cambia el estado de los avances."""
    nuevos_objetivos = generar_nuevos_objetivos(expediente, campos_modificados)

    # ✅ Almacenar en `campos_modificados` como lista real
    campos_modificados["nuevos_objetivos"] = nuevos_objetivos  

