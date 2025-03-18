import tkinter as tk
from tkinter import messagebox
import json
import os

def cargar_programas():
    """
    Carga los programas desde el archivo objetivos.json.
    """
    try:
        ruta_archivo = os.path.join(os.path.dirname(__file__), "objetivos.json")
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo 'objetivos.json' no encontrado.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Formato inválido en 'objetivos.json'.")
        return None

def seleccionar_programas_nuevos(campos_modificados, expedientes, nuevos_obj_frame, construir_nuevos_objetivos_frame):
    """
    Función para seleccionar programas y actualizar el frame de avance_objetivos.
    """
    programas = cargar_programas()
    if programas is None:
        return

    if not isinstance(campos_modificados, dict) or "nuevos_objetivos" not in campos_modificados:
        messagebox.showerror("Error", "Se requiere 'nuevos_objetivos' en campos_modificados.")
        return

    # Crear ventana de selección
    ventana_seleccion = tk.Toplevel()
    ventana_seleccion.title("Seleccionar Nuevos Objetivos")
    ventana_seleccion.geometry("400x300")

    # Frame contenedor con scrollbar
    frame_contenedor = tk.Frame(ventana_seleccion)
    frame_contenedor.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    ventana_seleccion.grid_rowconfigure(0, weight=1)
    ventana_seleccion.grid_columnconfigure(0, weight=1)

    # Canvas y scrollbar
    canvas = tk.Canvas(frame_contenedor)
    scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
    
    # Frame scrollable
    frame_scrollable = tk.Frame(canvas)
    frame_scrollable.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame_contenedor.grid_rowconfigure(0, weight=1)
    frame_contenedor.grid_columnconfigure(0, weight=1)

    # Obtener la lista actual desde campos_modificados
    objetivos_actuales = campos_modificados.get("nuevos_objetivos", [])

    seleccionados = []
    for i, (programa_id, programa_info) in enumerate(programas.items()):
        var = tk.IntVar()
        
        # Verificar si el programa ya está seleccionado en campos_modificados
        if programa_id in objetivos_actuales:
            var.set(1)  # Marcar el checkbox
        
        check = tk.Checkbutton(
            frame_scrollable,
            text=programa_info["Nombre"], 
            variable=var
        )
        check.grid(row=i, column=0, sticky="w", pady=2)
        seleccionados.append((programa_id, var))

    def confirmar_seleccion():
        nonlocal nuevos_obj_frame
        ids_seleccionados = [id for id, var in seleccionados if var.get() == 1]
        
        # Actualizar datos
        campos_modificados["nuevos_objetivos"] = ids_seleccionados
        expedientes["nuevos_objetivos"] = ids_seleccionados
        
        # Destruir y reconstruir frame
        if nuevos_obj_frame:
            parent = nuevos_obj_frame.master
            nuevos_obj_frame.destroy()
            
            # Crear nuevo frame con mismo padre
            nuevos_obj_frame = tk.Frame(parent, bg="#FFFFFF")
            nuevos_obj_frame.grid(row=13, column=1, padx=10, pady=5, sticky="w")
            
            # Construir con nueva data
            construir_nuevos_objetivos_frame(expedientes, nuevos_obj_frame, campos_modificados)
            
            # Actualizar referencia global
            if hasattr(parent, 'nuevos_obj_frame_ref'):
                parent.nuevos_obj_frame_ref = nuevos_obj_frame
            
            # Forzar actualización completa
            parent.update_idletasks()
            parent.update()
        
        ventana_seleccion.destroy()
    # Botón de confirmación
    boton_confirmar = tk.Button(
        ventana_seleccion, 
        text="Confirmar", 
        command=confirmar_seleccion
    )
    boton_confirmar.grid(row=1, column=0, pady=10)
