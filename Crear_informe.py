import tkinter as tk
from tkinter import messagebox
import json
from generar_documento import generar_documento_word


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

    def clear_body_frame(self):
        """Limpia el frame eliminando todos los widgets."""
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def crear_informe(self):
        """
        Muestra los detalles del expediente seleccionado en los campos correspondientes.
        """
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

        # Campos del expediente (todos los campos necesarios)
        campos = [
            "Unidad", "Número de Expediente", "Nombre del Paciente",
            "Fecha de Nacimiento", "Diagnóstico", "Área de Intervención",
            "Observaciones Clínicas", "Programas Seleccionados",
            "fecha", "edad", "periodo_intervencion", "terapias_recibidas",
            "faltas", "objetivos_iniciales", "avance_objetivos", "nuevos_objetivos",
            "observaciones", "tratamiento", "sugerencias_casa", "elaborado_por", "cedula"
        ]

        # Crear una fila para cada campo
        for idx, campo in enumerate(campos):
            # Etiqueta para el nombre del campo
            etiqueta = tk.Label(
                scrollable_frame, 
                text=campo.replace("_", " ").title(),  # Formatear el nombre del campo
                bg="#FFFFFF",
                anchor="e",
                justify="right",
                width=20
            )
            etiqueta.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

            # Campo de entrada para el valor
            entry = tk.Entry(scrollable_frame, width=40)
            if campo == "Programas Seleccionados":
                # Convertir la lista de programas a una cadena
                programas = ", ".join(self.expedientes.get(campo, []))
                entry.insert(0, programas)
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
            "objetivos_iniciales": datos_plan.get("objetivos_iniciales", ""),
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
