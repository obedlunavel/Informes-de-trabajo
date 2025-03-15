import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from PT_Word import GeneradorDocumento


# Crear una instancia de GeneradorDocumento
generador = GeneradorDocumento(config_path='configuracion.json')
# Diccionario con los programas de intervención
programas = {}

# Verificar si el archivo 'programas.json' existe
if os.path.exists("programas.json"):
    # Si el archivo existe, cargar su contenido en programas
    with open("programas.json", "r") as file:
        programas_json = json.load(file)
    
    # Limpiar y actualizar el diccionario `programas` con los datos del archivo
    programas.clear()
    programas.update({int(k): v for k, v in programas_json.items()})
else:
    # Si el archivo no existe, crearlo con un diccionario vacío
    with open("programas.json", "w") as file:
        json.dump(programas, file, indent=4)
class RevisarPlanesTrabajo:
    def __init__(self, body_frame, guardar_planes_trabajo, usar_crear_documento, programas, generador):
        """
        Inicializa la clase RevisarPlanesTrabajo.

        Parámetros:
            body_frame (tk.Frame): El frame donde se mostrará la interfaz.
            guardar_planes_trabajo (function): Función para guardar los planes de trabajo.
            usar_crear_documento (function): Función para crear un documento.
            programas (dict): Diccionario con los programas disponibles.
        """
        self.body_frame = body_frame
        self.guardar_planes_trabajo = guardar_planes_trabajo
        self.usar_crear_documento = usar_crear_documento
        self.programas = programas
        # Crear una instancia de GeneradorDocumento
        self.generador = generador

    def recuperar_datos(self, expediente):
        # Cargar los datos desde el archivo JSON
        with open("planes_trabajo.json", "r") as file:
            planes_trabajo = json.load(file)
        
        # Verificar si el expediente existe
        if expediente in planes_trabajo:
            return planes_trabajo[expediente]
        else:
            raise ValueError(f"No se encontró el expediente {expediente}.")
    def usar_crear_documento(self, expediente):
        try:
            datos = self.recuperar_datos(expediente)
            generador.crear_documento(datos)  # Crear el documento con los datos recuperados
            messagebox.showinfo("Éxito", f"Documento creado para el expediente {expediente}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    def revisar_planes_trabajo(self):
        archivo_planes = "planes_trabajo.json"  # Usamos el archivo centralizado
    
        if not os.path.exists(archivo_planes):
            messagebox.showinfo("Error", "No se han encontrado planes de trabajo guardados.")
            return
    
        with open(archivo_planes, "r") as f:
            planes_trabajo = json.load(f)
    
        if not planes_trabajo:
            messagebox.showinfo("Error", "No hay planes de trabajo disponibles.")
            return
    
        self.clear_body_frame()
    
        # Título
        tk.Label(
            self.body_frame,
            text="Revisar planes de trabajo",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#800000"
        ).grid(row=0, column=0, pady=10)
    
        # Configurar el grid para el body_frame
        self.body_frame.grid_rowconfigure(1, weight=1)
        self.body_frame.grid_columnconfigure(0, weight=1)
    
        # Contenedor principal
        revisar_frame = tk.Frame(self.body_frame, bg="#FFFFFF")
        revisar_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
        # Configurar el grid para revisar_frame
        revisar_frame.grid_rowconfigure(0, weight=1)
        revisar_frame.grid_columnconfigure(0, weight=1)
    
        # Crear el Treeview
        tree = ttk.Treeview(revisar_frame, columns=("Expediente"), show="headings", height=10)
        tree.heading("Expediente", text="Expediente")
        tree.column("Expediente", anchor="w")
        tree.grid(row=0, column=0, sticky="nsew")
    
        # Crear la Scrollbar
        scrollbar = tk.Scrollbar(revisar_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)
    
        # Ordenar expedientes alfabéticamente antes de añadirlos
        expedientes_ordenados = sorted(planes_trabajo.keys())
        for expediente in expedientes_ordenados:
            tree.insert("", "end", values=(expediente,))
            
            # Función para seleccionar programas
            def seleccionar_programas():
                # Crear una nueva ventana para seleccionar programas
                ventana_seleccion = tk.Toplevel()
                ventana_seleccion.title("Seleccionar Programas")
                ventana_seleccion.geometry("400x300")  # Tamaño de la ventana para que sea más visible
            
                # Frame contenedor con scrollbar
                frame_contenedor = tk.Frame(ventana_seleccion)
                frame_contenedor.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            
                # Configuración del grid de la ventana
                ventana_seleccion.grid_rowconfigure(0, weight=1)
                ventana_seleccion.grid_columnconfigure(0, weight=1)
            
                # Canvas y scrollbar
                canvas = tk.Canvas(frame_contenedor)
                scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
                frame_scrollable = tk.Frame(canvas)
            
                # Configuración de scrollbar
                frame_scrollable.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
            
                # Colocar el frame scrollable en el canvas
                canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
            
                # Colocar canvas y scrollbar en el grid
                canvas.grid(row=0, column=0, sticky="nsew")
                scrollbar.grid(row=0, column=1, sticky="ns")
            
                # Expandir el frame contenedor y el canvas para ajustarse al tamaño de la ventana
                frame_contenedor.grid_rowconfigure(0, weight=1)
                frame_contenedor.grid_columnconfigure(0, weight=1)
            
                seleccionados = []  # Lista para almacenar los programas seleccionados
            
                for i, (programa_id, programa_info) in enumerate(programas.items()):
                    var = tk.IntVar()  # Variable que se usará para marcar el checkbox
                    check = tk.Checkbutton(frame_scrollable, text=programa_info["Nombre"], variable=var)
                    check.grid(row=i, column=0, sticky='w', pady=2)  # Usar grid para colocar los checkboxes
                    seleccionados.append((programa_id, var))  # Guardar el id y el estado de selección
            
                # Variable para almacenar los programas seleccionados
                seleccion_final = []
            
                # Función que se ejecuta cuando se confirman los programas seleccionados
                def confirmar_seleccion():
                    global seleccion_final
                    # Convertir los IDs seleccionados a enteros
                    seleccion_final = [int(id) for id, var in seleccionados if var.get() == 1]
            
                    # Actualizar el campo "Programas Seleccionados" en la ventana de detalles
                    if "Programas Seleccionados" in campos_modificados:
                        # Limpiar el campo antes de insertar los nuevos valores
                        campos_modificados["Programas Seleccionados"].delete(0, tk.END)
                        # Insertar los IDs de los programas seleccionados separados por comas (convertidos a strings para mostrar)
                        campos_modificados["Programas Seleccionados"].insert(0, ','.join(map(str, seleccion_final)))
            
                    # Cerrar la ventana de selección después de confirmar
                    ventana_seleccion.destroy()
            
                # Botón para confirmar la selección
                boton_confirmar = tk.Button(ventana_seleccion, text="Confirmar", command=confirmar_seleccion)
                boton_confirmar.grid(row=1, column=0, pady=10)  # Usar grid para colocar el botón
            
                ventana_seleccion.mainloop()
            
        
    
            # Función para mostrar detalles
            def mostrar_detalles():
                seleccion = tree.selection()
                if not seleccion:
                    messagebox.showinfo("Error", "Por favor, seleccione un plan de trabajo.")
                    return
            
                expediente_seleccionado = tree.item(seleccion, "values")[0]
                datos_plan = planes_trabajo[expediente_seleccionado]
            
                # Crear un diccionario para almacenar los campos modificados
                campos_modificados = {}   
            
                self.clear_body_frame()             
            
                # Título
                tk.Label(
                    self.body_frame,
                    text="Detalles del plan seleccionado",
                    font=("Arial", 16, "bold"),
                    bg="#FFFFFF",
                    fg="#000000"
                ).grid(row=0, column=0, columnspan=2, pady=10)
            
                # Contenedor para los detalles
                detalles_frame = tk.Frame(self.body_frame, bg="#FFFFFF")
                detalles_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            
                self.body_frame.grid_rowconfigure(1, weight=1)
                self.body_frame.grid_columnconfigure(0, weight=1)
            
                # Canvas con barra de desplazamiento
                canvas = tk.Canvas(detalles_frame, bg="#FFFFFF")
                scrollbar = tk.Scrollbar(detalles_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")
                scrollable_frame.grid_columnconfigure(0, weight=1)  # Para las etiquetas
                scrollable_frame.grid_columnconfigure(1, weight=2)  # Para los campos de entrada
            
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
            
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
            
                canvas.grid(row=0, column=0, sticky="nsew")
                scrollbar.grid(row=0, column=1, sticky="ns")
            
                detalles_frame.grid_rowconfigure(0, weight=1)
                detalles_frame.grid_columnconfigure(0, weight=1)
            
                # Crear una fila para cada campo
                for idx, (key, value) in enumerate(datos_plan.items()):
                    # Etiqueta para el nombre del campo
                    etiqueta = tk.Label(
                        scrollable_frame, 
                        text=key, 
                        bg="#FFFFFF",
                        anchor="e",
                        justify="right",
                        width=20
                    )
                    etiqueta.grid(row=idx, column=0, padx=10, pady=5, sticky="e")
            
                    # Campo de entrada para el valor
                    entry = tk.Entry(scrollable_frame, width=40)
                    entry.insert(0, value if not isinstance(value, list) else ','.join(map(str, value)))
                    entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            
                    # Almacenar los campos modificados
                    campos_modificados[key] = entry
                    
                # Mostrar los programas seleccionados en el plan de trabajo
                row_offset = idx + 1  # Iniciar desde la fila siguiente al último índice utilizado
                etiqueta_programas = tk.Label(
                    scrollable_frame, 
                    text="Programas Seleccionados:", 
                    font=("Arial", 10, "bold"),
                    bg="#FFFFFF"
                )
                etiqueta_programas.grid(row=row_offset, column=0, columnspan=2, padx=10, pady=10, sticky="n")
                
                # Iterar sobre los programas seleccionados
                for i, programa in enumerate(datos_plan.get("Programas Seleccionados", []), start=row_offset + 1):
                    programa_int = int(programa)  # Convertir a entero si es necesario
                    nombre_programa = programas.get(programa_int, {}).get("Nombre", f"Programa {programa} no encontrado")
                    
                    # Etiqueta para cada programa centrada
                    etiqueta_programa = tk.Label(
                        scrollable_frame, 
                        text=f"- {nombre_programa}", 
                        font=("Arial", 9),
                        bg="white", 
                        anchor="center",
                        justify="center"
                    )
                    etiqueta_programa.grid(row=i, column=0, columnspan=2, padx=20, pady=5, sticky="n")
                    
            
                    # Función para guardar los cambios
                    def guardar_todos_los_cambios():
                        # Iterar sobre los campos modificados y guardar sus nuevos valores
                        for key, entry in campos_modificados.items():
                            nuevo_valor = entry.get()
                            if key == "Programas Seleccionados":  # Si es la lista de programas, procesarlo como una lista
                                datos_plan[key] = nuevo_valor.split(',')  # Convertir la cadena en lista
                            else:
                                datos_plan[key] = nuevo_valor  # Guardar el nuevo valor del campo
                    
                        # Guardar los datos actualizados en el diccionario de planes de trabajo
                        planes_trabajo[expediente_seleccionado] = datos_plan
                    
                        # Guardar los cambios a nivel de almacenamiento
                        self.guardar_planes_trabajo(planes_trabajo)
                    
                        messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")
                        self.clear_body_frame()  # Limpiar el área principal antes de mostrar el formulario
                        
                    def modificar_programas():
                        seleccion_actual = datos_plan.get("Programas Seleccionados", [])
                        seleccion_actual = set(map(int, seleccion_actual))  # Convertir a conjunto de enteros
                    
                        # Crear una nueva ventana para seleccionar programas
                        ventana_seleccion = tk.Toplevel()
                        ventana_seleccion.title("Seleccionar Programas")
                        ventana_seleccion.geometry("400x300")
                    
                        # Frame contenedor con scrollbar
                        frame_contenedor = tk.Frame(ventana_seleccion, bg="white")
                        frame_contenedor.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
                    
                        ventana_seleccion.grid_rowconfigure(0, weight=1)
                        ventana_seleccion.grid_columnconfigure(0, weight=1)
                    
                        # Canvas y scrollbar
                        canvas = tk.Canvas(frame_contenedor, bg="white")
                        scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
                        frame_scrollable = tk.Frame(canvas, bg="white")
                    
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
                    
                        # Lista para almacenar las opciones seleccionadas
                        seleccionados = []
                    
                        # Crear el checklist
                        for programa_id, programa_data in programas.items():
                            var = tk.IntVar(value=1 if programa_id in seleccion_actual else 0)  # Marcar si está seleccionado
                            chk = tk.Checkbutton(
                                frame_scrollable,
                                text=programa_data["Nombre"],
                                variable=var,
                                bg="#FFFFFF",
                                anchor="w",
                                justify="left"
                            )
                            chk.pack(fill="x", padx=5, pady=2, anchor="w")
                            seleccionados.append((programa_id, var))
                    
                        # Función para confirmar la selección
                        def confirmar_seleccion():
                            seleccion_final = [
                                str(programa_id) for programa_id, var in seleccionados if var.get() == 1
                            ]
                    
                            # Actualizar el campo "Programas Seleccionados" en `campos_modificados`
                            if "Programas Seleccionados" in campos_modificados:
                                entry = campos_modificados["Programas Seleccionados"]
                                entry.delete(0, tk.END)  # Limpiar el campo de entrada
                                entry.insert(0, ','.join(seleccion_final))  # Insertar los programas seleccionados
                    
                            # Actualizar los datos en el plan actual
                            datos_plan["Programas Seleccionados"] = seleccion_final
                    
                            messagebox.showinfo(
                                "Selección Confirmada", f"Programas seleccionados: {', '.join(seleccion_final)}"
                            )
                            ventana_seleccion.destroy()
                    
                        # Función para borrar toda la selección
                        def borrar_seleccion():
                            for _, var in seleccionados:
                                var.set(0)  # Desmarcar todas las opciones
                    
                        # Botón para confirmar la selección
                        boton_confirmar = tk.Button(
                            ventana_seleccion,
                            text="Confirmar Selección",
                            command=confirmar_seleccion,
                            bg="#A52A2A",
                            fg="white",
                            font=("Arial", 12)
                        )
                        boton_confirmar.grid(row=1, column=0, pady=10, sticky="ew")
                    
                        # Botón para borrar la selección
                        boton_borrar = tk.Button(
                            ventana_seleccion,
                            text="Borrar Selección",
                            command=borrar_seleccion,
                            bg="#007BFF",
                            fg="white",
                            font=("Arial", 12)
                        )
                        boton_borrar.grid(row=2, column=0, pady=10, sticky="ew")
                    
                        ventana_seleccion.mainloop()
                    
                 
                # Contenedor para los botones
                botones_frame = tk.Frame(self.body_frame, bg="#FFFFFF")
                botones_frame.grid(row=row_offset + 2, column=0, columnspan=2, pady=20, sticky="ew")
            
                # Configuración para distribuir botones uniformemente
                botones_frame.grid_columnconfigure(0, weight=1)
                botones_frame.grid_columnconfigure(1, weight=1)
                botones_frame.grid_columnconfigure(2, weight=1)
            
                # Botón para guardar todos los cambios
                boton_guardar = tk.Button(
                    botones_frame, 
                    text="Guardar Cambios", 
                    command=guardar_todos_los_cambios, 
                    width=20
                )
                boton_guardar.grid(row=0, column=0, padx=10, pady=5)
            
                # Botón para modificar los programas
                boton_modificar_programas = tk.Button(
                    botones_frame, 
                    text="Modificar Programas", 
                    command=modificar_programas, 
                    width=20
                )
                boton_modificar_programas.grid(row=0, column=1, padx=10, pady=5)
            
                # Botón para crear un documento
                boton_crear_documento = tk.Button(
                    botones_frame, 
                    text="Crear Documento", 
                    command=lambda: self.usar_crear_documento(expediente_seleccionado), 
                    width=20
                )
                boton_crear_documento.grid(row=0, column=2, padx=10, pady=5)

            # Botón para ver detalles
            boton_detalles = tk.Button(
                self.body_frame,
                text="Ver Detalles",
                command=mostrar_detalles,
                bg="#A52A2A",
                fg="white",
                font=("Arial", 12),
                relief="flat",
                activebackground="#800000",
                activeforeground="white"
            )
            boton_detalles.grid(row=2, column=0, pady=10, sticky="ew")


            
    def clear_body_frame(self):
        """
        Limpia el frame eliminando todos los widgets.
        """
        for widget in self.body_frame.winfo_children():
            widget.destroy()
