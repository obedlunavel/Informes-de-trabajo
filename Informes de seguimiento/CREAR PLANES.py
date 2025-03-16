import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from docx.shared import RGBColor
from docx.shared import Pt, RGBColor
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
import os
import tkinter.simpledialog as simpledialog
import sys
from PT_Word import GeneradorDocumento
from Crear_informe import DetallesExpediente
from Lista_expedientes import ExpedientesApp  # Importar la clase, no la función
from RevisarPlanes import RevisarPlanesTrabajo



# © 2025, Obed Luna Velázquez. Todos los derechos reservados.
# Este programa y su código fuente están protegidos por las leyes de derechos de autor.
# Prohibida su distribución y/o modificación sin autorización expresa del autor.
def resource_path(relative_path):
    """Obtiene la ruta correcta de un archivo, incluso dentro del ejecutable."""
    try:
        # PyInstaller usa este directorio temporal
        base_path = sys._MEIPASS
    except AttributeError:
        # Ruta normal si no está empaquetado
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
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


# Función para seleccionar programas
def seleccionar_programas_plan(entry_programas_seleccionados):
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

    # Función que se ejecuta cuando se confirman los programas seleccionados
    def confirmar_seleccion():
        seleccion_final = [str(id) for id, var in seleccionados if var.get() == 1]

        # Actualizar el campo "Programas Seleccionados" en la entrada principal
        entry_programas_seleccionados.delete(0, tk.END)  # Limpiar la entrada
        entry_programas_seleccionados.insert(0, ','.join(seleccion_final))  # Insertar la selección

        # Cerrar la ventana de selección
        ventana_seleccion.destroy()

    # Botón para confirmar la selección
    boton_confirmar = tk.Button(ventana_seleccion, text="Confirmar", command=confirmar_seleccion)
    boton_confirmar.grid(row=1, column=0, pady=10)  # Usar grid para colocar el botón





# Función para guardar la información en un archivo JSON
def guardar_informacion(expediente, datos):
    archivo_planes = 'planes_trabajo.json'
    
    if os.path.exists(archivo_planes):
        with open(archivo_planes, 'r') as file:
            informacion = json.load(file)
    else:
        informacion = {}
    
    # Actualizar los datos de acuerdo al número de expediente
    informacion[expediente] = datos  # Aquí asignamos los datos bajo el número de expediente
    
    with open(archivo_planes, 'w') as file:
        json.dump(informacion, file, indent=4)
    print(f"Información del expediente {expediente} guardada correctamente.")
    messagebox.showinfo("Guardado", f"Los cambios en el expediente {expediente} se han guardado correctamente.")



def recuperar_datos(expediente):
    # Cargar los datos desde el archivo JSON
    with open("planes_trabajo.json", "r") as file:
        planes_trabajo = json.load(file)
    
    # Verificar si el expediente existe
    if expediente in planes_trabajo:
        return planes_trabajo[expediente]
    else:
        raise ValueError(f"No se encontró el expediente {expediente}.")



    
# Función para cargar las sesiones de un expediente
def cargar_sesiones(expediente_num):
    if os.path.exists('sesiones.json'):
        with open('sesiones.json', 'r') as archivo:
            sesiones = json.load(archivo)
        return sesiones.get(expediente_num, [])
    else:
        return []



# Función para calcular la edad en años y meses a partir de la fecha de nacimiento
def calcular_edad(fecha_nacimiento):
    formatos = ['%d/%m/%Y', '%Y-%m-%d']  # Agrega los formatos posibles
    for formato in formatos:
        try:
            nacimiento = datetime.strptime(fecha_nacimiento, formato)
            hoy = datetime.now()
            edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
            return edad
        except ValueError:
            continue  # Intenta con el siguiente formato

    raise ValueError("El formato de la fecha no es válido.")
def usar_crear_documento(expediente):
    try:
        datos = recuperar_datos(expediente)
        generador.crear_documento(datos)
        messagebox.showinfo("Éxito", f"Documento creado para el expediente {expediente}.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Función para guardar los planes de trabajo modificados
def guardar_planes_trabajo(planes_trabajo):
    archivo_planes = "planes_trabajo.json"
    with open(archivo_planes, "w") as f:
        json.dump(planes_trabajo, f, indent=4)

# Función para cargar la configuración actual
def cargar_configuracion():
    if os.path.exists('configuracion.json'):
        with open('configuracion.json', 'r') as archivo:
            configuracion = json.load(archivo)
        return configuracion
    else:
        # Si no existe el archivo de configuración, devolver un diccionario vacío
        return {"unidad": "", "nombre_terapeuta": "", "cedula_profesional": ""}



# Función para guardar los datos de configuración
def guardar_configuracion(unidad, nombre_terapeuta, cedula_profesional):
    configuracion = {
        "unidad": unidad,
        "nombre_terapeuta": nombre_terapeuta,
        "cedula_profesional": cedula_profesional
    }
    with open('configuracion.json', 'w') as archivo:
        json.dump(configuracion, archivo)
    messagebox.showinfo("Configuración", "Datos guardados correctamente.")

class ModernMainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Planes de Trabajo")
        self.root.geometry("1024x600")
        self.root.minsize(800, 400)
        self.root.configure(bg="#F5F5DC")

        # Estilos personalizados
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.style.configure(
            "TButton",
            font=("Arial", 12),
            padding=10,
            relief="flat",
            background="#800000",  # Guinda oscuro
            foreground="white"
        )
        self.style.map(
            "TButton",
            background=[("active", "#A52A2A")],  # Guinda más claro al interactuar
            foreground=[("active", "white")]
        )

        # Dividir ventana principal en menú lateral y cuerpo principal
        self.menu_frame = tk.Frame(self.root, bg="#800000", width=250)
        self.menu_frame.pack(side="left", fill="y")

        self.body_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.body_frame.pack(side="right", expand=True, fill="both")

        # Inicializar revisar_planes
        self.revisar_planes = RevisarPlanesTrabajo(
            self.body_frame, guardar_planes_trabajo, usar_crear_documento, programas, generador
        )
        # Encabezado del menú lateral
        header_label = tk.Label(
            self.menu_frame,
            text="Menú",
            font=("Arial", 18, "bold"),
            bg="#800000",
            fg="white"
        )
        header_label.pack(fill="x", pady=(10, 20))

        # Botones del menú lateral
        self.create_menu_button("Crear Plan", self.crear_plan_trabajo)
        self.create_menu_button("Revisar Planes", self.revisar_planes.revisar_planes_trabajo)
        self.create_menu_button("Directorio", self.abrir_directorio_programas)
        self.create_menu_button("Configuración", self.abrir_configuracion)
        self.create_menu_button("Informe de trabajo", self.mostrar_expedientes)


        # Área inicial en el cuerpo principal
        self.body_label = tk.Label(
            self.body_frame,
            text="Bienvenido al Sistema de Planes de Trabajo",
            font=("Arial", 16),
            bg="#FFFFFF",
            fg="#000000"
        )
        self.body_label.pack(expand=True)

    def create_menu_button(self, text, command):
        button = tk.Button(
            self.menu_frame,
            text=text,
            command=command,  # Llamar directamente a la función
            font=("Arial", 12),
            bg="#A52A2A",
            fg="white",
            relief="flat",
            activebackground="#800000",
            activeforeground="white"
        )
        button.pack(fill="x", pady=5, padx=10)
    def mostrar_expedientes(self):
        """
        Método para mostrar la lista de expedientes.
        """
        # Limpiar el body_frame antes de mostrar la lista
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        # Crear una instancia de ExpedientesApp y pasarle el body_frame
        expedientes_app = ExpedientesApp(self.body_frame)
        expedientes_app.lista_expedientes()  # Llamar al método lista_expedientes

        
        
    

    def clear_body_frame(self):
        """Limpia el contenido actual del área del cuerpo principal."""
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        
   

    def crear_plan_trabajo(self):
        
    # Verificar si el archivo 'configuracion.json' existe
        if not os.path.exists("configuracion.json"):
            messagebox.showerror(
                "Configuración faltante",
                "El archivo 'configuracion.json' no existe. Por favor, llene la configuración antes de continuar."
            )
            return  # No continuar con la ejecución de la función
        """Muestra el formulario completo en el área principal (body_frame) para crear un nuevo plan de trabajo."""
        self.clear_body_frame()  # Limpiar el área principal antes de mostrar el formulario

        # Título del formulario
        tk.Label(
            self.body_frame,
            text="Crear Nuevo Plan de Trabajo",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#800000"
        ).pack(pady=10)

        # Contenedor para organizar los campos del formulario
        form_frame = tk.Frame(self.body_frame, bg="#FFFFFF")
        form_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Campos del formulario
        tk.Label(form_frame, text="Fecha (dd-mm-yyyy):", bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=5)
        fecha = tk.Entry(form_frame)
        fecha.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Unidad:", bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=5)
        unidad = tk.Entry(form_frame)
        unidad.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Número de Expediente:", bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=5)
        expediente = tk.Entry(form_frame)
        expediente.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Nombre del paciente:", bg="#FFFFFF").grid(row=3, column=0, sticky="w", pady=5)
        nombre = tk.Entry(form_frame)
        nombre.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Edad:", bg="#FFFFFF").grid(row=4, column=0, sticky="w", pady=5)
        edad = tk.Entry(form_frame)
        edad.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Sexo (M/F):", bg="#FFFFFF").grid(row=5, column=0, sticky="w", pady=5)
        sexo = tk.Entry(form_frame)
        sexo.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Fecha de Nacimiento (dd-mm-yyyy):", bg="#FFFFFF").grid(row=6, column=0, sticky="w", pady=5)
        nacimiento = tk.Entry(form_frame)
        nacimiento.grid(row=6, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Diagnóstico:", bg="#FFFFFF").grid(row=7, column=0, sticky="w", pady=5)
        diagnostico = tk.Entry(form_frame)
        diagnostico.grid(row=7, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Área de Intervención:", bg="#FFFFFF").grid(row=8, column=0, sticky="w", pady=5)
        area_intervencion = tk.Entry(form_frame)
        area_intervencion.grid(row=8, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Número de sesiones por semana:", bg="#FFFFFF").grid(row=9, column=0, sticky="w", pady=5)
        sesiones = tk.Entry(form_frame)
        sesiones.grid(row=9, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Reforzadores Comestibles:", bg="#FFFFFF").grid(row=10, column=0, sticky="w", pady=5)
        reforzadores_comestibles = tk.Entry(form_frame)
        reforzadores_comestibles.grid(row=10, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Reforzadores Tangibles:", bg="#FFFFFF").grid(row=11, column=0, sticky="w", pady=5)
        reforzadores_tangibles = tk.Entry(form_frame)
        reforzadores_tangibles.grid(row=11, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Reforzadores Sociales:", bg="#FFFFFF").grid(row=12, column=0, sticky="w", pady=5)
        reforzadores_sociales = tk.Entry(form_frame)
        reforzadores_sociales.grid(row=12, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Observaciones clínicas:", bg="#FFFFFF").grid(row=13, column=0, sticky="w", pady=5)
        observaciones = tk.Entry(form_frame)
        observaciones.grid(row=13, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Programas seleccionados (1,2,5,10...):", bg="#FFFFFF").grid(row=14, column=0, sticky="w", pady=5)
        programas_seleccionados = tk.Entry(form_frame)
        programas_seleccionados.grid(row=14, column=1, pady=5, padx=10)
        

        # Botón de Directorio para abrir la función F3
        boton_directorio = tk.Button(
            form_frame,
            text="Directorio",
            command=lambda: seleccionar_programas_plan(programas_seleccionados),
            bg="#A52A2A",
            fg="white",
            relief="flat",
            activebackground="#800000",
            activeforeground="white"
        )
        boton_directorio.grid(row=14, column=2, pady=5, padx=10)
        def guardar_plan():
            datos = {
                "Fecha": fecha.get(),
                "Unidad": unidad.get(),
                "Número de Expediente": expediente.get(),
                "Nombre del Paciente": nombre.get(),
                "Edad": edad.get(),
                "Sexo": sexo.get(),
                "Fecha de Nacimiento": nacimiento.get(),
                "Diagnóstico": diagnostico.get(),
                "Área de Intervención": area_intervencion.get(),
                "Sesiones por Semana": sesiones.get(),
                "Reforzadores Comestibles": reforzadores_comestibles.get(),
                "Reforzadores Tangibles": reforzadores_tangibles.get(),
                "Reforzadores Sociales": reforzadores_sociales.get(),
                "Observaciones Clínicas": observaciones.get(),
                "Programas Seleccionados": [int(p) for p in programas_seleccionados.get().split(",")]
            }
            guardar_informacion(expediente.get(), datos)
            generador.crear_documento(datos)
            messagebox.showinfo("Guardado", "El plan de trabajo ha sido guardado correctamente.")
            self.clear_body_frame()     
        # Botón de Guardar
        boton_guardar = tk.Button(
            form_frame,
            text="Guardar plan",
            command= guardar_plan,  # Ejecutar guardar_plan cuando se presione el botón
            bg="#A52A2A",
            fg="white",
            relief="flat",
            activebackground="#800000",
            activeforeground="white"
        )
        boton_guardar.grid(row=16, column=2, pady=5, padx=10)     

        # Configurar las columnas del formulario para que se ajusten
        form_frame.columnconfigure(1, weight=1)

    
    # Función para borrar un programa y actualizar el archivo JSON
    def borrar_programa(self):
        """Borra el programa seleccionado en el Treeview y actualiza el archivo JSON."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Seleccione un programa para borrar.")
            return
    
        programa_id = int(self.tree.item(selected_item, "values")[0])
        confirmar = tk.messagebox.askyesno("Confirmar", f"¿Está seguro de que desea borrar el programa {programa_id}?")
        if confirmar:
            # Eliminar el programa del diccionario
            programas.pop(programa_id, None)
    
            # Guardar los cambios en el archivo JSON después de borrar
            with open("programas.json", "w") as file:
                json.dump(programas, file, indent=4)
    
            # Actualizar la lista de programas en la interfaz
            self.actualizar_lista_programas()
    
            # Mostrar mensaje de confirmación
            tk.messagebox.showinfo("Éxito", f"El programa {programa_id} ha sido borrado.")

    def abrir_directorio_programas(self):
        """Muestra el directorio de programas en el área principal."""
        self.clear_body_frame()
        
        # Encabezado estilizado
        header_label = tk.Label(
            self.body_frame,
            text="Directorio",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#800000"
        )
        header_label.pack(pady=10)
    
        # Marco para contener el Treeview y la barra de desplazamiento
        frame_tree = tk.Frame(self.body_frame, bg="#FFFFFF")
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Crear Treeview para mostrar programas
        self.tree = ttk.Treeview(
            frame_tree,
            columns=("ID", "Nombre", "Objetivo"),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set,
        )
        self.tree.heading("ID", text="ID Programa")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Objetivo", text="Objetivo (Resumen)")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.column("Objetivo", width=600, anchor="w")
        self.tree.pack(fill="both", expand=True)
        
        scrollbar.config(command=self.tree.yview)
        
        # Llenar Treeview con datos
        self.actualizar_lista_programas()
    
        # Vincular tecla Enter para mostrar detalles
        self.tree.bind("<Return>", lambda event: self.mostrar_detalles(self.tree))
        self.tree.bind("<Double-1>", lambda event: self.mostrar_detalles(self.tree))  # Abrir con doble clic también
        
        # Botón para abrir detalles
        boton_abrir = tk.Button(
            self.body_frame,
            text="Abrir detalles",
            command=lambda: self.mostrar_detalles(self.tree),
            font=("Arial", 12),
            bg="#8B0000",
            fg="white",
            relief="flat",
            activebackground="#A52A2A",
            activeforeground="white",
        )
        boton_abrir.pack(pady=5)
    
        # Botón para agregar nuevos programas
        boton_agregar = tk.Button(
            self.body_frame,
            text="Agregar nuevo programa",
            command=self.agregar_programa,
            font=("Arial", 12),
            bg="#8B0000",
            fg="white",
            relief="flat",
            activebackground="#A52A2A",
            activeforeground="white",
        )
        boton_agregar.pack(pady=5)
    
        # Botón para borrar programas
        boton_borrar = tk.Button(
            self.body_frame,
            text="Borrar programa seleccionado",
            command=self.borrar_programa,
            font=("Arial", 12),
            bg="#8B0000",
            fg="white",
            relief="flat",
            activebackground="#A52A2A",
            activeforeground="white",
        )
        boton_borrar.pack(pady=5)
    
    def actualizar_lista_programas(self):
        """Actualiza la lista de programas en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for programa_id, detalles in programas.items():
            nombre_programa = detalles.get("Nombre", "Sin nombre")
            objetivo_resumen = detalles.get("Objetivo", "Sin objetivo")[:50] + "..."
            self.tree.insert("", tk.END, values=(programa_id, nombre_programa, objetivo_resumen))
    
    def agregar_programa(self):
        """Abre una ventana para agregar un nuevo programa."""
        agregar_window = tk.Toplevel(self.root)
        agregar_window.title("Agregar Nuevo Programa")
        agregar_window.geometry("600x600")
        agregar_window.configure(bg="#FFFFFF")

        # Títulos
        tk.Label(
            agregar_window,
            text="Agregar Nuevo Programa",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        ).pack(pady=10)

        # Campo: Nombre
        tk.Label(
            agregar_window,
            text="Nombre:",
            font=("Arial", 14),
            bg="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        entry_nombre = tk.Entry(agregar_window, font=("Arial", 12))
        entry_nombre.pack(fill="x", padx=10, pady=5)

        # Campo: Objetivo
        tk.Label(
            agregar_window,
            text="Objetivo:",
            font=("Arial", 14),
            bg="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        text_objetivo = tk.Text(agregar_window, font=("Arial", 12), height=4)
        text_objetivo.pack(fill="x", padx=10, pady=5)

        # Campo: Procedimiento
        tk.Label(
            agregar_window,
            text="Procedimiento:",
            font=("Arial", 14),
            bg="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        text_procedimiento = tk.Text(agregar_window, font=("Arial", 12), height=6)
        text_procedimiento.pack(fill="x", padx=10, pady=5)

        # Campo: Ayudas
        tk.Label(
            agregar_window,
            text="Ayudas:",
            font=("Arial", 14),
            bg="#FFFFFF"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        text_ayudas = tk.Text(agregar_window, font=("Arial", 12), height=4)
        text_ayudas.pack(fill="x", padx=10, pady=5)

        def guardar_nuevo_programa():
            nuevo_id = len(programas) + 1  # Generar nuevo ID
            programas[nuevo_id] = {
                "Nombre": entry_nombre.get(),
                "Objetivo": text_objetivo.get("1.0", "end").strip(),
                "Procedimiento": text_procedimiento.get("1.0", "end").strip(),
                "Ayudas": text_ayudas.get("1.0", "end").strip(),
            }

            # Guardar en el archivo JSON
            with open("programas.json", "w") as file:
                json.dump(programas, file, indent=4)

            agregar_window.destroy()
            tk.messagebox.showinfo("Éxito", f"El programa {nuevo_id} ha sido agregado.")
                # Llamar a la función para actualizar la lista
            self.actualizar_lista_programas()
            # Botón para guardar el programa
        tk.Button(
            agregar_window,
            text="Guardar Programa",
            command=guardar_nuevo_programa,
            bg="#A52A2A",
            fg="white",
            font=("Arial", 12),
        ).pack(pady=10)

        # Botón para cancelar
        tk.Button(
            agregar_window,
            text="Cancelar",
            command=agregar_window.destroy,
            bg="#A52A2A",
            fg="white",
            font=("Arial", 12),
        ).pack(pady=10)
    
    def borrar_programa(self):
        """Borra el programa seleccionado en el Treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Seleccione un programa para borrar.")
            return
    
        programa_id = int(self.tree.item(selected_item, "values")[0])
        confirmar = tk.messagebox.askyesno("Confirmar", f"¿Está seguro de que desea borrar el programa {programa_id}?")
        if confirmar:
            programas.pop(programa_id, None)
            self.actualizar_lista_programas()
            tk.messagebox.showinfo("Éxito", f"El programa {programa_id} ha sido borrado.")
        
    def mostrar_detalles(self, tree):
        """Muestra y permite modificar los detalles del programa seleccionado."""
        item = tree.selection()
        if item:
            programa_id = tree.item(item)["values"][0]
            detalles = programas.get(programa_id, {})
            
            # Obtener los datos del programa
            nombre = detalles.get("Nombre", "Sin nombre")
            objetivo = detalles.get("Objetivo", "Sin objetivo")
            procedimiento = detalles.get("Procedimiento", "Sin procedimiento definido")
            ayudas = detalles.get("Ayudas", "Sin ayudas disponibles")
    
            # Crear ventana emergente para mostrar detalles
            detalles_window = tk.Toplevel(self.root)
            detalles_window.title(f"Detalles del Programa {programa_id}")
            detalles_window.geometry("600x600")
            detalles_window.configure(bg="#FFFFFF")
    
            # Encabezado: Nombre del programa
            tk.Label(
                detalles_window,
                text=nombre,
                font=("Arial", 16, "bold"),
                bg="#FFFFFF",
                fg="#000000"
            ).pack(pady=10)
    
            # Sección: Objetivo
            tk.Label(
                detalles_window,
                text="Objetivo:",
                font=("Arial", 14, "bold"),
                bg="#FFFFFF",
                fg="#800000"
            ).pack(anchor="w", padx=10, pady=(10, 0))
            text_objetivo = tk.Text(
                detalles_window,
                wrap="word",
                font=("Arial", 12),
                bg="#F5F5F5",
                fg="#000000",
                height=4
            )
            text_objetivo.insert("1.0", objetivo)
            text_objetivo.pack(fill="x", padx=10, pady=5)
    
            # Sección: Procedimiento
            tk.Label(
                detalles_window,
                text="Procedimiento:",
                font=("Arial", 14, "bold"),
                bg="#FFFFFF",
                fg="#800000"
            ).pack(anchor="w", padx=10, pady=(10, 0))
            text_procedimiento = tk.Text(
                detalles_window,
                wrap="word",
                font=("Arial", 12),
                bg="#F5F5F5",
                fg="#000000",
                height=6
            )
            text_procedimiento.insert("1.0", procedimiento)
            text_procedimiento.pack(fill="x", padx=10, pady=5)
    
            # Sección: Ayudas
            tk.Label(
                detalles_window,
                text="Ayudas:",
                font=("Arial", 14, "bold"),
                bg="#FFFFFF",
                fg="#800000"
            ).pack(anchor="w", padx=10, pady=(10, 0))
            text_ayudas = tk.Text(
                detalles_window,
                wrap="word",
                font=("Arial", 12),
                bg="#F5F5F5",
                fg="#000000",
                height=4
            )
            text_ayudas.insert("1.0", ayudas)
            text_ayudas.pack(fill="x", padx=10, pady=5)
    
            # Función para guardar los cambios en el archivo JSON
            def guardar_cambios():
                # Actualizar el diccionario con los cambios
                programas[programa_id]["Objetivo"] = text_objetivo.get("1.0", "end").strip()
                programas[programa_id]["Procedimiento"] = text_procedimiento.get("1.0", "end").strip()
                programas[programa_id]["Ayudas"] = text_ayudas.get("1.0", "end").strip()
            
                # Guardar los cambios en el archivo programas.json
                with open("programas.json", "w") as file:
                    json.dump(programas, file, indent=4)
            
                # Cerrar la ventana de detalles
                detalles_window.destroy()
                
                # Mostrar mensaje de confirmación
                messagebox.showinfo("Guardado", f"Los cambios en el programa {programa_id} se han guardado.")
            
            # Botón para guardar cambios
            tk.Button(
                detalles_window,
                text="Guardar Cambios",
                command=guardar_cambios,
                bg="#800000",
                fg="white",
                font=("Arial", 12),
            ).pack(pady=10)
            
            # Botón para cerrar la ventana
            tk.Button(
                detalles_window,
                text="Cerrar",
                command=detalles_window.destroy,
                bg="#800000",
                fg="white",
                font=("Arial", 12),
            ).pack(pady=10)
    
    # Función para borrar un programa y actualizar el archivo JSON
    def borrar_programa(self):
        """Borra el programa seleccionado en el Treeview y actualiza el archivo JSON."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Seleccione un programa para borrar.")
            return
    
        programa_id = int(self.tree.item(selected_item, "values")[0])
        confirmar = tk.messagebox.askyesno("Confirmar", f"¿Está seguro de que desea borrar el programa {programa_id}?")
        if confirmar:
            # Eliminar el programa del diccionario
            programas.pop(programa_id, None)
    
            # Guardar los cambios en el archivo JSON después de borrar
            with open("programas.json", "w") as file:
                json.dump(programas, file, indent=4)
    
            # Actualizar la lista de programas en la interfaz
            self.actualizar_lista_programas()
    
            # Mostrar mensaje de confirmación
            tk.messagebox.showinfo("Éxito", f"El programa {programa_id} ha sido borrado.")
        
            
    def abrir_configuracion(self):
        """Muestra el formulario de configuración en el área principal."""
        self.clear_body_frame()  # Limpiar el área principal
        configuracion_actual = cargar_configuracion()
    
        # Encabezado estilizado
        header_label = tk.Label(
            self.body_frame,
            text="Configuración del Sistema",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#800000"
        )
        header_label.pack(pady=10)
    
        # Marco para contener los campos
        form_frame = tk.Frame(self.body_frame, bg="#F5F5F5", padx=20, pady=20)
        form_frame.pack(pady=20, padx=10, fill="both", expand=True)
    
        # Campo: Unidad
        tk.Label(form_frame, text="Unidad:", font=("Arial", 12), bg="#F5F5F5").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        entrada_unidad = tk.Entry(form_frame, font=("Arial", 12), width=30)
        entrada_unidad.grid(row=0, column=1, pady=5, padx=5)
        entrada_unidad.insert(0, configuracion_actual.get("unidad", ""))
    
        # Campo: Nombre del Terapeuta
        tk.Label(form_frame, text="Nombre del Terapeuta:", font=("Arial", 12), bg="#F5F5F5").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        entrada_nombre_terapeuta = tk.Entry(form_frame, font=("Arial", 12), width=30)
        entrada_nombre_terapeuta.grid(row=1, column=1, pady=5, padx=5)
        entrada_nombre_terapeuta.insert(0, configuracion_actual.get("nombre_terapeuta", ""))
    
        # Campo: Cédula Profesional
        tk.Label(form_frame, text="Cédula Profesional:", font=("Arial", 12), bg="#F5F5F5").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        entrada_cedula_profesional = tk.Entry(form_frame, font=("Arial", 12), width=30)
        entrada_cedula_profesional.grid(row=2, column=1, pady=5, padx=5)
        entrada_cedula_profesional.insert(0, configuracion_actual.get("cedula_profesional", ""))
    
        # Botón para guardar la configuración
        boton_guardar = tk.Button(
            self.body_frame,
            text="Guardar Configuración",
            font=("Arial", 12),
            bg="#A52A2A",
            fg="white",
            command=lambda: guardar_configuracion(
                entrada_unidad.get(),
                entrada_nombre_terapeuta.get(),
                entrada_cedula_profesional.get()
            )
        )
        boton_guardar.pack(pady=20)
    
        # Agregar marco de separación visual
        separator = tk.Frame(self.body_frame, height=2, bd=1, relief="sunken", bg="#D3D3D3")
        separator.pack(fill="x", pady=10)
    

    def run(self):
        self.root.mainloop()

# Ejecutar el menú principal
if __name__ == "__main__":
    menu = ModernMainMenu()
    menu.run()
