import tkinter as tk
from tkinter import messagebox
import json
from generar_documento import generar_documento_word
from SeleccionarObjetivos import seleccionar_programas
from AvanceFrame import actualizar_objetivos_iniciales, construir_avance_frame  # Importar funciones
from generador_objetivos import generar_nuevos_objetivos, construir_nuevos_objetivos_frame
from SeleccionarNuevosObjetivos import seleccionar_programas_nuevos


class DetallesExpediente:
    def __init__(self, body_frame, expedientes, programas, planes_trabajo, guardar_planes_trabajo, generar_documento_word):
        """
        Inicializa la clase DetallesExpediente.

        Parámetros:
            body_frame (tk.Frame): El frame donde se mostrarán los detalles.
            expedientes (dict): Diccionario con los datos de los expedientes.
            programas (dict): Diccionario con los datos de los programas.
            planes_trabajo (dict): Diccionario con los planes de trabajo.
            guardar_planes_trabajo (function): Función para guardar los planes de trabajo.
            generar_documento_word (function): Función para generar el documento Word.
        """
        self.body_frame = body_frame
        self.expedientes = expedientes
        self.programas = programas
        self.planes_trabajo = planes_trabajo
        self.guardar_planes_trabajo = guardar_planes_trabajo
        self.generar_documento_word = generar_documento_word
        self.campos_modificados = {}  # Inicializar el diccionario de campos modificados
        self.avance_frame = None  # Inicializar como atributo de la clase
        self.nuevos_obj_frame = None
        self.scrollable_frame = None  # Inicializar scrollable_frame como None

        
    def actualizar_nuevos_objetivos(self):
        # Verificar si self.scrollable_frame está inicializado
        if self.scrollable_frame is None:
            messagebox.showerror("Error", "El frame desplazable no está inicializado.")
            return

        # Generar nuevos objetivos
        nuevos = generar_nuevos_objetivos(
            self.expedientes,
            self.campos_modificados,
        )
        
        # Actualizar expediente
        self.expedientes["nuevos_objetivos"] = nuevos
        
        # Reconstruir frame
        if self.nuevos_obj_frame:
            self.nuevos_obj_frame.destroy()  # Destruir el frame existente
        
        # Crear un nuevo frame
        self.nuevos_obj_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        row_position = self.nuevos_objetivos_row

        self.nuevos_obj_frame.grid(row=row_position, column=1, padx=10, pady=5, sticky="w")
        
        # Llamar a la función para construir el frame de nuevos objetivos
        construir_nuevos_objetivos_frame(self.expedientes, self.nuevos_obj_frame)
    def construir_avance_frame(self):
        """
        Método para construir el frame de avance_objetivos.
        """
        # Paso 1: Preservar selecciones previas
        selecciones_guardadas = {
            key: var.get() 
            for key, var in self.campos_modificados.items() 
            if key.startswith("avance_objetivo_")
        }
        
        # Paso 2: Limpiar el frame si ya existe
        if self.avance_frame:
            for widget in self.avance_frame.winfo_children():
                widget.destroy()
        else:
            self.avance_frame = tk.Frame(self.body_frame, bg="#FFFFFF")
            self.avance_frame.grid(row=idx, column=1, padx=10, pady=5, sticky="w")  # Asegúrate de definir 'idx'

        # Paso 3: Cargar objetivos desde JSON
        with open("objetivos.json", "r", encoding="utf-8") as file:
            objetivos = json.load(file)

        # Crear elementos para cada objetivo
        for i, id_obj in enumerate(self.expedientes.get("Objetivos Iniciales", [])):
            if id_obj not in objetivos:
                continue

            datos_obj = objetivos[id_obj]
            
            # Etiqueta
            lbl = tk.Label(self.avance_frame, text=datos_obj["Nombre"], bg="#FFFFFF")
            lbl.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            
            # Dropdown
            opciones = ["sin_ayuda", "con_ayuda", "no_logra"]
            var = tk.StringVar(self.avance_frame)
            var.set(selecciones_guardadas.get(f"avance_objetivo_{id_obj}", opciones[0]))
            
            opt_menu = tk.OptionMenu(self.avance_frame, var, *opciones)
            opt_menu.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            # Guardar en campos_modificados
            self.campos_modificados[f"avance_objetivo_{id_obj}"] = var
    def clear_body_frame(self):
        """Limpia el frame eliminando todos los widgets."""
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def crear_informe(self):
        # Limpiar el frame antes de mostrar los detalles
        self.clear_body_frame()

        # Título
        tk.Label(
            self.body_frame,
            text="Detalles del Expediente",
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
        self.scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")  # Asignar a self.scrollable_frame
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Para las etiquetas
        self.scrollable_frame.grid_columnconfigure(1, weight=2)  # Para los campos de entrada

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        detalles_frame.grid_rowconfigure(0, weight=1)
        detalles_frame.grid_columnconfigure(0, weight=1)



        # Campos del expediente (todos los campos necesarios)
        campos = [
            "fecha", "Unidad", "Número de Expediente", "Nombre del Paciente",
            "edad", "Fecha de Nacimiento", "Diagnóstico", "Área de Intervención",
            "periodo_intervencion", "terapias_recibidas",
            "faltas", "Objetivos Iniciales", "avance_objetivos", "nuevos_objetivos",
            "Observaciones Clínicas", "tratamiento", "sugerencias_casa", "elaborado_por", "cedula"
        ]
        self.nuevos_objetivos_row = campos.index("nuevos_objetivos")

        # Crear una fila para cada campo
        for idx, campo in enumerate(campos):
            # Etiqueta para el nombre del campo
            etiqueta = tk.Label(
                self.scrollable_frame, 
                text=campo.replace("_", " ").title(),  # Formatear el nombre del campo
                bg="#FFFFFF",
                anchor="e",
                justify="right",
                width=20
            )
            etiqueta.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

            # Campo de entrada para el valor
            entry = tk.Entry(self.scrollable_frame, width=40)
            if campo == "Objetivos Iniciales":
                # Convertir la lista de programas a una cadena
                programas = ", ".join(self.expedientes.get(campo, []))
                entry.insert(0, programas)
                # Botón para modificar los programas (colocado en la misma fila, columna 2)
                boton_modificar_programas = tk.Button(
                    self.scrollable_frame,  # Usar el mismo frame para que esté alineado
                    text="Modificar Objetivos", 
                    command=lambda: seleccionar_programas(
                    self.campos_modificados,  # Campo de entrada
                    self.expedientes,          # Datos del expediente (¡Nuevo parámetro!)
                    self.avance_frame,         # Frame a actualizar (¡Nuevo parámetro!)
                    self.construir_avance_frame  # Función de reconstrucción (¡Nuevo parámetro!)
                ),
                    width=20
                )
                boton_modificar_programas.grid(row=idx, column=2, padx=10, pady=5, sticky="w")

            elif campo == "avance_objetivos":
                # Frame para mostrar los objetivos y sus niveles de cumplimiento
                self.avance_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
                self.avance_frame.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

                # Llamar a la función para construir el frame de avance_objetivos
                construir_avance_frame(self.expedientes, self.avance_frame, self.campos_modificados)
            elif campo == "nuevos_objetivos":
                # Crear el frame para nuevos objetivos
                self.nuevos_obj_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
                self.nuevos_obj_frame.grid(row=idx, column=1, padx=10, pady=5, sticky="w")  # Usar .grid() para posicionar

                # Llamar a la función para construir el frame de nuevos objetivos
                construir_nuevos_objetivos_frame(self.expedientes, self.nuevos_obj_frame)
                
                # Convertir la lista de programas a una cadena
                programas = ", ".join(self.expedientes.get(campo, []))
                entry.insert(0, programas)

                boton_generar_nuevos_objetivos = tk.Button(
                    self.scrollable_frame,  # Usar el mismo frame para que esté alineado
                    text="Generar Nuevos Objetivos", 
                    command=lambda: self.actualizar_nuevos_objetivos(),
                    width=20
                )
                # Botón para modificar los programas (colocado en la misma fila, columna 2)
                boton_modificar_nuevos_objetivos = tk.Button(
                    self.scrollable_frame,  # Usar el mismo frame para que esté alineado
                    text="Modificar Nuevos Objetivos", 
                    command=lambda: seleccionar_programas_nuevos(
                    self.campos_modificados,  # Diccionario de campos modificados
                    self.expedientes,         # Datos del expediente
                    self.nuevos_obj_frame,  # Frame de nuevos objetivos
                    construir_nuevos_objetivos_frame  # Función para construir el frame
                ),
                    width=20
                )
                boton_generar_nuevos_objetivos.grid(row=idx, column=2, padx=10, pady=5, sticky="w")
                boton_modificar_nuevos_objetivos.grid(row=idx, column=3, padx=10, pady=5, sticky="w")

            else:
                entry.insert(0, self.expedientes.get(campo, ""))  # Usar valor existente o vacío
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
                
            # Almacenar los campos modificados
            self.campos_modificados[campo] = entry


        # Contenedor para los botones
        botones_frame = tk.Frame(self.body_frame, bg="#FFFFFF")
        botones_frame.grid(row=len(campos) + 1, column=0, columnspan=2, pady=20, sticky="ew")

        # Configuración para distribuir botones uniformemente
        botones_frame.grid_columnconfigure(0, weight=1)
        botones_frame.grid_columnconfigure(1, weight=1)

        # Botón para guardar todos los cambios
        boton_guardar = tk.Button(
            botones_frame, 
            text="Guardar Cambios", 
            command=self.guardar_todos_los_cambios, 
            width=20
        )
        boton_guardar.grid(row=0, column=0, padx=10, pady=5)

        # Botón para generar el documento Word
        boton_generar_documento = tk.Button(
            botones_frame, 
            text="Generar Documento", 
            command=lambda: self.generar_documento_word(self.expedientes), 
            width=20
        )
        boton_generar_documento.grid(row=0, column=1, padx=10, pady=5)

    def guardar_todos_los_cambios(self):
        """Guarda todos los cambios realizados en los campos modificados."""
        for key, entry in self.campos_modificados.items():
            nuevo_valor = entry.get()
            self.expedientes[key] = nuevo_valor  # Guardar el nuevo valor del campo

        # Guardar los cambios a nivel de almacenamiento
        self.guardar_planes_trabajo(self.planes_trabajo)

        messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")
        self.clear_body_frame()  # Limpiar el área principal antes de mostrar el formulario

    def generar_documento(self, datos_plan):
        """Genera un documento Word con los datos del expediente."""
        datos = {
            "fecha": datos_plan.get("fecha", ""),
            "unidad": datos_plan.get("unidad", ""),
            "expediente": datos_plan.get("expediente", ""),
            "nombre": datos_plan.get("nombre", ""),
            "edad": datos_plan.get("edad", ""),
            "fecha_nacimiento": datos_plan.get("fecha_nacimiento", ""),
            "diagnostico": datos_plan.get("diagnostico", ""),
            "area_intervencion": datos_plan.get("area_intervencion", ""),
            "periodo_intervencion": datos_plan.get("periodo_intervencion", ""),
            "terapias_recibidas": datos_plan.get("terapias_recibidas", ""),
            "faltas": datos_plan.get("faltas", ""),
            "avance_objetivos": datos_plan.get("avance_objetivos", ""),
            "nuevos_objetivos": datos_plan.get("nuevos_objetivos", ""),
            "observaciones": datos_plan.get("observaciones", ""),
            "tratamiento": datos_plan.get("tratamiento", ""),
            "sugerencias_casa": datos_plan.get("sugerencias_casa", ""),
            "elaborado_por": datos_plan.get("elaborado_por", ""),
            "cedula": datos_plan.get("cedula", "")
        }

        # Generar el documento Word
        nombre_archivo = f"IS_{datos['nombre'].replace(' ', '_')}_{datos['expediente']}_LIBERADO_Replica.docx"
        self.generar_documento_word(datos, nombre_archivo)

        messagebox.showinfo("Éxito", f"Documento generado: {nombre_archivo}")
