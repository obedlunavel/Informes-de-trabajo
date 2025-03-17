import tkinter as tk
import json

def actualizar_objetivos_iniciales(entry, expedientes, avance_frame, campos_modificados):
    """
    Actualiza la lista de objetivos iniciales y reconstruye el frame.
    
    Parámetros:
        entry (tk.Entry): Campo de entrada de objetivos.
        expedientes (dict): Datos del expediente.
        avance_frame (tk.Frame): Frame a actualizar.
        campos_modificados (dict): Selecciones del usuario.
    """
    nuevos_objetivos = entry.get().split(", ")
    expedientes["Objetivos Iniciales"] = nuevos_jetivos
    
    # Reconstruir frame con nuevos objetivos
    construir_avance_frame(expedientes, avance_frame, campos_modificados)


def construir_avance_frame(expedientes, avance_frame, campos_modificados):
    """
    Construye/actualiza el frame dinámicamente preservando selecciones.
    
    Parámetros:
        expedientes (dict): Datos del expediente.
        avance_frame (tk.Frame): Frame a construir.
        campos_modificados (dict): Diccionario para guardar cambios.
    """
    # Preservar selecciones actuales
    selecciones_guardadas = {
        key: var.get() 
        for key, var in campos_modificados.items() 
        if key.startswith("avance_objetivo_")
    }
    
    # Limpiar frame
    for widget in avance_frame.winfo_children():
        widget.destroy()
    
    # Cargar objetivos desde JSON
    with open("objetivos.json", "r", encoding="utf-8") as f:
        objetivos = json.load(f)
    
    # Crear elementos para cada objetivo
    for i, id_obj in enumerate(expedientes.get("Objetivos Iniciales", [])):
        if id_obj not in objetivos:
            continue
            
        datos_obj = objetivos[id_obj]
        
        # Etiqueta del objetivo
        lbl = tk.Label(
            avance_frame, 
            text=datos_obj["Nombre"], 
            bg="#FFFFFF", 
            anchor="w"
        )
        lbl.grid(row=i, column=0, padx=5, pady=2, sticky="w")
        
        # Dropdown de avance
        opciones = ["sin_ayuda", "con_ayuda", "no_logra"]
        var = tk.StringVar(avance_frame)
        
        # Restaurar selección previa si existe
        clave = f"avance_objetivo_{id_obj}"
        if clave in selecciones_guardadas:
            var.set(selecciones_guardadas[clave])
        else:
            var.set(opciones[0])
            
        opt_menu = tk.OptionMenu(avance_frame, var, *opciones)
        opt_menu.grid(row=i, column=1, padx=5, pady=2, sticky="w")
        
        # Guardar en campos_modificados
        campos_modificados[clave] = var
