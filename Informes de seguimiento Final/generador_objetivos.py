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
    """Construye el frame de objetivos dinámicos con extracción robusta."""
    
    # Destruir frame existente si hay widgets previos
    for widget in parent_frame.winfo_children():
        widget.destroy()

    frame = tk.Frame(parent_frame, bg="#FFFFFF")
    frame.grid(row=13, column=1, padx=10, pady=5, sticky="w")

    try:
        with open("objetivos.json", "r", encoding="utf-8") as f:
            objetivos_data = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando objetivos: {str(e)}")
        return frame

    nuevos_objetivos = campos_modificados.get("nuevos_objetivos", [])

    # Generar estructura jerárquica para la extracción recursiva
    for idx, obj_id in enumerate(nuevos_objetivos):
        if obj_id not in objetivos_data:
            continue

        # Frame contenedor por objetivo (nivel 1)
        frame_objetivo = tk.Frame(frame, bg="#FFFFFF")
        frame_objetivo.grid(row=idx, column=0, sticky="w", pady=2)

        # Subframe para controles (nivel 2)
        subframe = tk.Frame(frame_objetivo, bg="#FFFFFF")
        subframe.grid(row=0, column=0, sticky="w")

        # Entry con ID del objetivo (visible para extracción)
        entry_id = tk.Entry(subframe, width=5, bg="#FFFFFF")
        entry_id.insert(0, obj_id)
        entry_id.grid(row=0, column=1, padx=5)
        
        # Entry con descripción (opcional)
        entry_desc = tk.Entry(subframe, width=50, bg="#FFFFFF")
        entry_desc.insert(0, objetivos_data[obj_id].get("Nombre", ""))
        entry_desc.grid(row=0, column=2)

        # Guardar referencias en estructura plana
        campos_modificados[f"obj_{idx}_id"] = entry_id
        campos_modificados[f"obj_{idx}_desc"] = entry_desc

    # Forzar jerarquía de widgets antes de retornar
    frame.update_idletasks()
    
    # Debug: Mostrar estructura del frame
    print("\n🔥 Estructura del frame reconstruido:")
    for child in frame.winfo_children():
        print(f"- {child} (Tipo: {type(child)})")
        for subchild in child.winfo_children():
            print(f"  └ {subchild} (Tipo: {type(subchild)})")

    return frame

def actualizar_nuevos_objetivos(expediente, campos_modificados):
    """Actualiza automáticamente `nuevos_objetivos` cuando cambia el estado de los avances."""
    nuevos_objetivos = generar_nuevos_objetivos(expediente, campos_modificados)

    # ✅ Almacenar en `campos_modificados` como lista real
    campos_modificados["nuevos_objetivos"] = nuevos_objetivos  

