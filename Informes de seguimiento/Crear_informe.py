import tkinter as tk
from tkinter import messagebox
import json
from generar_documento import generar_documento_word
from SeleccionarObjetivos import seleccionar_programas
from AvanceFrame import actualizar_objetivos_iniciales, construir_avance_frame  # Importar funciones
from generador_objetivos import generar_nuevos_objetivos, construir_nuevos_objetivos_frame
from SeleccionarNuevosObjetivos import seleccionar_programas_nuevos
from Sugerencias import crear_frame_seleccion, generar_seccion_word



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
        self.categorias_seleccionadas = {}
        self.sugerencias_frame = None
                # Cargar objetivos desde el archivo JSON
        with open("objetivos.json", "r", encoding="utf-8") as file:
            self.objetivos = json.load(file)

                # Diccionario para mapear nombres de campos de la interfaz a nombres finales
        self.MAPEO_CAMPOS = {
            "fecha": "fecha",
            "Unidad": "unidad",
            "Número de Expediente": "expediente",
            "Nombre del Paciente": "nombre",
            "edad": "edad",
            "Fecha de Nacimiento": "fecha_nacimiento",
            "Diagnóstico": "diagnostico",
            "Área de Intervención": "area_intervencion",
            "periodo_intervencion": "periodo_intervencion",
            "terapias_recibidas": "terapias_recibidas",
            "faltas": "faltas",
            "Objetivos Iniciales": "objetivos_iniciales",
            "avance_objetivos": "avance_objetivos",
            "nuevos_objetivos": "nuevos_objetivos",
            "Observaciones Clínicas": "observaciones",
            "tratamiento": "tratamiento",
            "sugerencias_casa": "sugerencias_casa",
            "elaborado_por": "elaborado_por",
            "cedula": "cedula",
        }
        
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
        construir_nuevos_objetivos_frame(self.expedientes, self.nuevos_obj_frame, self.campos_modificados)
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
            self.avance_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
            self.avance_frame.grid(row=self.nuevos_objetivos_row, column=1, padx=10, pady=5, sticky="w")

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

        # Diccionario para mapear nombres de campos de la interfaz a nombres finales
        MAPEO_CAMPOS = {
            "fecha": "fecha",
            "Unidad": "unidad",
            "Número de Expediente": "expediente",
            "Nombre del Paciente": "nombre",
            "edad": "edad",
            "Fecha de Nacimiento": "fecha_nacimiento",
            "Diagnóstico": "diagnostico",
            "Área de Intervención": "area_intervencion",
            "periodo_intervencion": "periodo_intervencion",
            "terapias_recibidas": "terapias_recibidas",
            "faltas": "faltas",
            "Objetivos Iniciales": "objetivos_iniciales",
            "avance_objetivos": "avance_objetivos",
            "nuevos_objetivos": "nuevos_objetivos",
            "Observaciones Clínicas": "observaciones",
            "tratamiento": "tratamiento",
            "sugerencias_casa": "sugerencias_casa",
            "elaborado_por": "elaborado_por",
            "cedula": "cedula",
        }

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
                        self.expedientes,  # Datos del expediente
                        self.avance_frame,  # Frame a actualizar
                        self.construir_avance_frame  # Función de reconstrucción
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
                self.nuevos_obj_frame.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

                # Llamar a la función para construir el frame de nuevos objetivos
                construir_nuevos_objetivos_frame(self.expedientes, self.nuevos_obj_frame, self.campos_modificados)

                # Convertir la lista de programas a una cadena
                programas = ", ".join(self.expedientes.get(campo, []))
                entry.insert(0, programas)

                boton_generar_nuevos_objetivos = tk.Button(
                    self.scrollable_frame,  # Usar el mismo frame para que esté alineado
                    text="Generar Nuevos Objetivos",
                    command=lambda: self.actualizar_nuevos_objetivos(),
                    width=20
                )
                boton_generar_nuevos_objetivos.grid(row=idx, column=2, padx=10, pady=5, sticky="w")

                # Botón para modificar los programas (colocado en la misma fila, columna 3)
                boton_modificar_nuevos_objetivos = tk.Button(
                    self.scrollable_frame,  # Usar el mismo frame para que esté alineado
                    text="Modificar Nuevos Objetivos",
                    command=lambda: seleccionar_programas_nuevos(
                        self.campos_modificados,  # Diccionario de campos modificados
                        self.expedientes,  # Datos del expediente
                        self.nuevos_obj_frame,  # Frame de nuevos objetivos
                        construir_nuevos_objetivos_frame  # Función para construir el frame
                    ),
                    width=20
                )
                boton_modificar_nuevos_objetivos.grid(row=idx, column=3, padx=10, pady=5, sticky="w")

            elif campo == "sugerencias_casa":
                # Frame de selección de programas al lado
                self.frame_programas, self.vars_programas = crear_frame_seleccion(
                    parent=self.scrollable_frame,
                    row=idx,  # Misma fila que sugerencias_casa
                    column=1,  # Columna adyacente
                    expediente=self.expedientes,
                    campos_modificados=self.campos_modificados  # Asegúrate de que este diccionario está definido

                )

                # Configurar grid para alineación
                self.scrollable_frame.grid_columnconfigure(2, weight=1)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

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

        # Generar un nombre de archivo dinámico
        nombre_archivo = f"IS_{self.expedientes['nombre'].replace(' ', '_')}_{self.expedientes['expediente']}_LIBERADO_Replica.docx"

        # Botón para generar el documento Word
        boton_generar_documento = tk.Button(
            botones_frame,
            text="Generar Documento",
            command=lambda: self.generar_documento(self.campos_modificados, nombre_archivo),
            width=20
        )
        boton_generar_documento.grid(row=0, column=1, padx=10, pady=5)

    def guardar_todos_los_cambios(self):
        """Guarda los cambios en los campos modificados dentro de Datos del Expediente."""
        
        # Mapeo correcto de claves
        claves_correctas = {
            "fecha": "fecha",
            "Unidad": "unidad",
            "Número de Expediente": "expediente",
            "Nombre del Paciente": "nombre",
            "edad": "edad",
            "Fecha de Nacimiento": "fecha_nacimiento",
            "Diagnóstico": "diagnostico",
            "Área de Intervención": "area_intervencion",
            "periodo_intervencion": "periodo_intervencion",
            "terapias_recibidas": "terapias_recibidas",
            "faltas": "faltas",
            "Objetivos Iniciales": "objetivos_iniciales",
            "Observaciones Clínicas": "observaciones",
            "tratamiento": "tratamiento",
            "sugerencias_casa": "sugerencias_casa",
            "elaborado_por": "elaborado_por",
            "cedula": "cedula"
        }

        # Diccionario corregido
        datos_corregidos = {}

        for key, widget in self.campos_modificados.items():
            if isinstance(widget, tk.Entry):
                nuevo_valor = widget.get()
            elif isinstance(widget, tk.StringVar):
                nuevo_valor = widget.get()
            else:
                nuevo_valor = ""  # Si el widget no es reconocido, asigna una cadena vacía

            # Usar la clave correcta en datos_corregidos
            clave_corregida = claves_correctas.get(key, key)  # Si no está en el mapeo, deja el mismo nombre
            datos_corregidos[clave_corregida] = nuevo_valor

        # Unir los avances en un solo campo "avance_objetivos"
        avances = [valor for clave, valor in datos_corregidos.items() if clave.startswith("avance_objetivo_")]
        if avances:
            datos_corregidos["avance_objetivos"] = "\n".join(avances)

        # Eliminar claves individuales de avances para evitar duplicados
        for clave in list(datos_corregidos.keys()):
            if clave.startswith("avance_objetivo_"):
                del datos_corregidos[clave]

        # Guardar los datos corregidos en datos_expediente
        self.datos_expediente.update(datos_corregidos)

        messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")
        self.clear_body_frame()  # Limpiar la interfaz después de guardar

    def formatear_avance_objetivos(self, avance_objetivos):
        """Formatea los datos de avance de objetivos para que sean legibles."""
        if not avance_objetivos:
            return "No se registraron avances."

        avance_texto = "El paciente ha mostrado avances en:\n"
        for objetivo_id, avance in avance_objetivos.items():
            nombre_objetivo = self.objetivos[objetivo_id]["Nombre"]
            descripcion = self.objetivos[objetivo_id][avance["nivel"]]
            avance_texto += f"- {nombre_objetivo}: {descripcion}\n"
        return avance_texto.strip()  # Eliminar el último salto de línea
    def extraer_avance_objetivos(self):
        """Extrae los datos de avance de objetivos desde los campos modificados."""
        avance_objetivos = {}
        for key, var in self.campos_modificados.items():
            if key.startswith("avance_objetivo_"):
                # Extraer el ID del objetivo (por ejemplo, "avance_objetivo_3" -> "3")
                objetivo_id = key.replace("avance_objetivo_", "")
                # Obtener el valor seleccionado (sin_ayuda, con_ayuda, no_logra)
                nivel_avance = var.get()
                # Obtener la descripción del avance desde objetivos.json
                descripcion = self.objetivos[objetivo_id][nivel_avance]
                avance_objetivos[objetivo_id] = {
                    "nivel": nivel_avance,
                    "descripcion": descripcion
                }
        return avance_objetivos
    def extraer_nuevos_objetivos(self, nuevos_obj_frame):
        """Extrae los datos de nuevos objetivos desde el frame, incluyendo subframes de forma recursiva."""
        nuevos_objetivos = []

        if not nuevos_obj_frame.winfo_children():
            return []

        def obtener_entries(frame):
            """Función recursiva para buscar todos los Entry dentro de subframes."""
            entries = []
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Entry):  
                    widget.update_idletasks()  # Asegurar que la interfaz está actualizada
                    valor = widget.get().strip()

                    if valor:
                        entries.append(valor)

                elif isinstance(widget, tk.Frame):  
                    entries.extend(obtener_entries(widget))  # 🔥 Llamado recursivo
                    
            return entries

        # Buscar los Entry dentro de `nuevos_obj_frame`
        nuevos_objetivos = obtener_entries(nuevos_obj_frame)

        return nuevos_objetivos


        # 🔥 Llamar a la función para buscar dentro de `nuevos_obj_frame`
        nuevos_objetivos = obtener_entries(nuevos_obj_frame)

        if not nuevos_objetivos:
            print("⚠️ No se capturaron nuevos objetivos. Verifica que los Entries tengan texto o que los Frames contengan los Entry.")

        # ✅ Guardar en `campos_modificados` como lista real
        self.campos_modificados["nuevos_objetivos"] = nuevos_objetivos

        # 🔍 Depuración: Verificar qué se está guardando
        print(f"📌 Nuevos objetivos guardados en campos_modificados (como lista): {self.campos_modificados['nuevos_objetivos']}")

        return nuevos_objetivos


    def generar_documento(self, campos_modificados, nombre_archivo):
        """Genera un documento Word con los datos del expediente."""
        datos = {}

        # ✅ Extraer datos de los Entry y StringVar
        for campo_interfaz, widget in campos_modificados.items():
            campo_final = self.MAPEO_CAMPOS.get(campo_interfaz, campo_interfaz)

            if isinstance(widget, tk.Entry):
                valor = widget.get().strip()
            elif isinstance(widget, tk.StringVar):
                valor = widget.get().strip()
            elif isinstance(widget, str):  # Si ya es string (ej. sugerencias_casa)
                valor = widget.strip()
            else:
                valor = ""

            datos[campo_final] = valor

        # ✅ Leer objetivos desde objetivos.json
        try:
            with open("objetivos.json", "r", encoding="utf-8") as file:
                objetivos = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo objetivos.json no encontrado.")
            return
           # 🔥 ✅ EXTRAER NUEVOS OBJETIVOS ANTES DE USARLOS
        nuevos_obj_ids = self.extraer_nuevos_objetivos(self.nuevos_obj_frame) if self.nuevos_obj_frame else []

        # 🔍 Depuración: Ver qué devuelve extraer_nuevos_objetivos
        print(f"📌 IDs extraídos de nuevos_objetivos: {nuevos_obj_ids}")

        # ✅ Convertir los IDs a nombres de objetivos
        nuevos_obj_nombres = []
        for obj_id in nuevos_obj_ids:
            obj_id = str(obj_id)  
            if obj_id in objetivos:
                nombre = objetivos[obj_id]["Nombre"]
                nuevos_obj_nombres.append(f"{obj_id} - {nombre}")
            else:
                print(f"⚠️ Objetivo '{obj_id}' no encontrado en el archivo JSON")

        # ✅ Guardar los nuevos objetivos en `datos`
        datos["nuevos_objetivos"] = "\n".join(nuevos_obj_nombres)

        # 🔍 Depuración: Verificar si los nombres se están copiando correctamente
        print(f"📌 Nombres de nuevos objetivos en datos: {datos['nuevos_objetivos']}")


        # ✅ Convertir objetivos iniciales de IDs a nombres
        if "objetivos_iniciales" in datos and datos["objetivos_iniciales"]:
            objetivos_ids = [obj.strip() for obj in datos["objetivos_iniciales"].split(",")]
            objetivos_nombres = []

            for obj_id in objetivos_ids:
                obj_id = str(obj_id)  # Asegurar que sea string para comparación
                if obj_id in objetivos:
                    nombre = objetivos[obj_id]["Nombre"]
                    objetivos_nombres.append(f"{obj_id} - {nombre}")
                else:
                    print(f"⚠️ Objetivo '{obj_id}' no encontrado en el archivo JSON")

            datos["objetivos_iniciales"] = "\n".join(objetivos_nombres)

        # ✅ Extraer datos de avance_objetivos
        avance_objetivos = self.extraer_avance_objetivos()
        datos["avance_objetivos"] = self.formatear_avance_objetivos(avance_objetivos)

        # ✅ Eliminar claves individuales de avances para evitar duplicados
        for key in list(datos.keys()):
            if key.startswith("avance_objetivo_"):
                del datos[key]

        # ✅ Extraer nuevos objetivos correctamente
        nuevos_obj_ids = self.extraer_nuevos_objetivos(self.nuevos_obj_frame) if self.nuevos_obj_frame else []

        # ✅ Convertir los IDs a nombres de objetivos
        nuevos_obj_nombres = []
        for obj_id in nuevos_obj_ids:
            obj_id = str(obj_id)  # Asegurar que el ID sea string
            if obj_id in objetivos:
                nombre = objetivos[obj_id]["Nombre"]
                nuevos_obj_nombres.append(f"{obj_id} - {nombre}")
            else:
                print(f"⚠️ Objetivo '{obj_id}' no encontrado en el archivo JSON")

        # ✅ Guardar los nuevos objetivos en `datos`
        datos["nuevos_objetivos"] = "\n".join(nuevos_obj_nombres)

        # ✅ Copiar sugerencias de casa correctamente
        datos["sugerencias_casa"] = campos_modificados.get("sugerencias_casa", "").strip()

        # ✅ Depuración: Mostrar los datos antes de generar el documento
        for key in list(datos.keys()):
            if key.startswith("nuevo_objetivo_"):
                del datos[key]
        print(f"✅ Datos para el documento Word:\n{json.dumps(datos, indent=4, ensure_ascii=False)}")

        # ✅ Generar el documento Word
        self.generar_documento_word(datos, nombre_archivo)
