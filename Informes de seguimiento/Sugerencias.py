import json
import tkinter as tk
from tkinter import messagebox

def cargar_sugerencias():
    """Carga las sugerencias desde el archivo JSON"""
    try:
        with open('SugerenciasProgramas.json', 'r', encoding='utf-8') as f:
            return json.load(f)['Categorías']
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo SugerenciasProgramas.json no encontrado")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decodificando el archivo JSON")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        return []

def crear_frame_seleccion(parent, row, column, expediente, campos_modificados):
    """Crea un frame de selección de categorías con scroll y actualiza campos_modificados"""
    frame = tk.Frame(parent, bg="#FFFFFF", bd=2, relief="groove")
    frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew", columnspan=2)  
    
    lbl_titulo = tk.Label(frame, 
                        text="Programas Sugeridos", 
                        font=("Arial", 10, "bold"), 
                        bg="#F0F0F0",
                        padx=10,
                        pady=5)
    lbl_titulo.pack(fill="x", pady=(0, 5))
    
    canvas = tk.Canvas(frame, bg="#FFFFFF", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#FFFFFF")
    
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    vars_control = {}
    seleccion_previa = set(expediente.get('programas', []))

    def actualizar_campos():
        """Actualiza campos_modificados con la selección actual de programas."""
        programas_seleccionados = [nombre for nombre, var in vars_control.items() if var.get()]
        campos_modificados["sugerencias_casa"] = "\n".join(programas_seleccionados) if programas_seleccionados else ""
        
        # 🔎 Depuración: Verificar qué se está guardando
        print(f"🔍 sugerencias_casa actualizado en campos_modificados: {campos_modificados['sugerencias_casa']}")

    categorias = cargar_sugerencias()
    for cat in categorias:
        var = tk.BooleanVar(value=cat['Nombre'] in seleccion_previa)

        chk = tk.Checkbutton(
            scroll_frame, 
            text=f"  {cat['Icono']} {cat['Nombre']}", 
            variable=var,
            bg="#FFFFFF",
            anchor="w",
            padx=10,
            pady=2,
            selectcolor="#E0F7FA",
            command=actualizar_campos  # ✅ Se ejecuta al cambiar la selección
        )
        chk.pack(fill="x", pady=2)

        vars_control[cat['Nombre']] = var  

    # 🔥 Inicializar correctamente el campo en campos_modificados
    actualizar_campos()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame.update_idletasks()
    canvas.config(height=min(200, scroll_frame.winfo_height()))

    return frame, vars_control



def _actualizar_preview(categoria, parent):
    """Actualiza la vista previa de sugerencias"""
    # Implementación básica (puedes expandir según necesidades)
    preview_frame = tk.Frame(parent, bg="#FFFFFF")
    preview_frame.grid(row=1, column=1, sticky="nsew")
    
    # Limpiar frame existente
    for widget in preview_frame.winfo_children():
        widget.destroy()
    
    # Mostrar detalles de la categoría
    tk.Label(preview_frame, 
            text=f"Detalles de {categoria['Nombre']}", 
            font=("Arial", 10, "bold"),
            bg="#FFFFFF").pack(pady=5)
    
    for sug in categoria['Sugerencias']:
        tk.Label(preview_frame, 
                text=f"• {', '.join(sug['Objetivos'])}",  # Paréntesis corregido aquí
                bg="#FFFFFF",
                anchor="w").pack(fill="x", padx=10)

def generar_seccion_word(doc, programas_seleccionados):
    """Genera la sección de sugerencias en Word"""
    if not isinstance(doc, Document):
        raise ValueError("El parámetro doc debe ser un objeto Document de python-docx")
    
    categorias = cargar_sugerencias()
    
    if not categorias:
        return
    
    # Título de la sección
    doc.add_heading('Sugerencias para Casa', level=1)
    
    for cat in categorias:
        if cat['Nombre'] in programas_seleccionados:
            # Encabezado de categoría
            doc.add_heading(f"{cat['Icono']} {cat['Nombre']}", level=2)
            
            # Contenido de sugerencias
            for sug in cat['Sugerencias']:
                doc.add_paragraph(f"Objetivo: {', '.join(sug['Objetivos'])}", style='Heading3')  # Paréntesis corregido aquí
                
                # Ejemplos prácticos
                p = doc.add_paragraph()
                p.add_run("Ejemplos prácticos:").bold = True
                for ej in sug['Ejemplos']:
                    doc.add_paragraph(f"- {ej}", style='ListBullet')
            
            # Espaciado entre categorías
            doc.add_paragraph()

# Función adicional para obtener programas seleccionados
def obtener_programas_seleccionados(vars_control):
    """Devuelve lista de nombres de programas seleccionados"""
    return [nombre for nombre, var in vars_control.items() if var.get()]
