# generador_objetivos.py
import json
import tkinter as tk
from tkinter import messagebox

def generar_nuevos_objetivos(expediente, campos_modificados):
    """
    Genera nuevos objetivos basados en el avance de los iniciales
    con la estructura específica de tu JSON.
    """
    try:
        with open("objetivos.json", "r", encoding="utf-8") as f:
            objetivos = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando objetivos: {str(e)}")
        return []

    nuevos_objetivos = []
    objetivos_iniciales = expediente.get("Objetivos Iniciales", [])
    
    # Paso 1: Reusar objetivos no cumplidos
    for obj_id in objetivos_iniciales:
        estado_key = f"avance_objetivo_{obj_id}"
        estado = campos_modificados.get(estado_key, "sin_ayuda")
        
        if isinstance(estado, tk.StringVar):
            estado = estado.get()
        
        if estado in ["con_ayuda", "no_logra"]:
            nuevos_objetivos.append(obj_id)
    
    # Paso 2: Generar secuencia numérica ascendente
    contador = 1
    max_objetivos = 50  # Límite máximo de búsqueda
    
    while len(nuevos_objetivos) < 10 and contador <= max_objetivos:
        nuevo_id = str(contador)
        
        # Verificar si el objetivo existe y no está en listas
        if (nuevo_id in objetivos and 
            nuevo_id not in objetivos_iniciales and 
            nuevo_id not in nuevos_objetivos):
            nuevos_objetivos.append(nuevo_id)
        
        contador += 1
    
    return nuevos_objetivos[:10]

def construir_nuevos_objetivos_frame(expediente, parent_frame):
    """Construye el frame de visualización con tu estructura de objetivos"""
    frame = tk.Frame(parent_frame, bg="#FFFFFF")
    frame.grid(row=13, column=1, padx=10, pady=5, sticky="w")  # Usar grid en lugar de pack
    
    try:
        with open("objetivos.json", "r", encoding="utf-8") as f:
            objetivos_data = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando objetivos: {str(e)}")
        return frame
    
    for idx, obj_id in enumerate(expediente.get("nuevos_objetivos", [])):
        if obj_id not in objetivos_data:
            continue
        
        # Frame por fila
        fila = tk.Frame(frame, bg="#FFFFFF")
        fila.grid(row=idx, column=0, sticky="w", pady=2)  # Usar grid para posicionar la fila
        
        # Número de objetivo
        tk.Label(fila, 
                text=f"Objetivo {idx+1}:", 
                bg="#FFFFFF",
                width=12,
                anchor="w").grid(row=0, column=0, sticky="w")  # Usar grid para el Label
        
        # Nombre del objetivo
        tk.Label(fila, 
                text=objetivos_data[obj_id]["Nombre"], 
                bg="#FFFFFF",
                anchor="w").grid(row=0, column=1, sticky="w")  # Usar grid para el Label
    
    return frame
