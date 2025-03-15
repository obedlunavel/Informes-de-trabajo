import os
import json
import tkinter as tk
from tkinter import messagebox, ttk
from Crear_informe import DetallesExpediente

class ExpedientesApp:
    def __init__(self, body_frame):
        self.body_frame = body_frame
        self.expedientes = self.cargar_expedientes()  # Cargar expedientes al inicializar

    def cargar_expedientes(self):
        """
        Carga los expedientes desde el archivo JSON.
        """
        archivo_planes = "expedientes.json"  # Usamos el archivo centralizado

        if not os.path.exists(archivo_planes):
            messagebox.showinfo("Error", "No se han encontrado expedientes guardados.")
            return []

        try:
            with open(archivo_planes, "r", encoding="utf-8") as f:
                expedientes = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showinfo("Error", f"Error al leer el archivo: {e}")
            return []

        return expedientes

    def clear_body_frame(self):
        # Limpiar el frame eliminando todos los widgets
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def lista_expedientes(self):
        """
        Muestra una lista de expedientes cargados desde un archivo JSON.
        """
        if not self.expedientes:
            messagebox.showinfo("Error", "No hay expedientes disponibles.")
            return

        self.clear_body_frame()

        # Título
        tk.Label(
            self.body_frame,
            text="Lista de Expedientes",
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

        # Crear el Treeview con columnas adicionales
        columnas = (
            "Unidad", "Número de Expediente", "Nombre del Paciente",
            "Fecha de Nacimiento", "Diagnóstico", "Área de Intervención",
            "Observaciones Clínicas", "Objetivos Iniciales"
        )
        self.tree = ttk.Treeview(revisar_frame, columns=columnas, show="headings", height=10)

        # Configurar las columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=120)  # Ajustar el ancho según sea necesario

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Crear la Scrollbar
        scrollbar = tk.Scrollbar(revisar_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Llenar el Treeview con los datos de los expedientes
        for expediente in self.expedientes:
            # Convertir la lista de programas seleccionados a una cadena
            programas = ", ".join(map(str, expediente["Objetivos Iniciales"]))
            # Insertar una fila en el Treeview
            self.tree.insert("", "end", values=(
                expediente["Unidad"],
                expediente["Número de Expediente"],
                expediente["Nombre del Paciente"],
                expediente["Fecha de Nacimiento"],
                expediente["Diagnóstico"],
                expediente["Área de Intervención"],
                expediente["Observaciones Clínicas"],
                programas
            ))

        # Botón para ver detalles
        boton_detalles = tk.Button(
            self.body_frame,
            text="Ver Detalles",
            command=self.ver_detalles,
            bg="#A52A2A",
            fg="white",
            font=("Arial", 12),
            relief="flat",
            activebackground="#800000",
            activeforeground="white"
        )
        boton_detalles.grid(row=2, column=0, pady=10, sticky="ew")

    def ver_detalles(self):
        """
        Muestra los detalles del expediente seleccionado.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Error", "Por favor, seleccione un expediente.")
            return

        # Obtener los valores del expediente seleccionado
        expediente_seleccionado = self.tree.item(seleccion, "values")
        expediente_numero = expediente_seleccionado[1]  # Número de expediente

        # Buscar el expediente en la lista de expedientes
        expediente = next((e for e in self.expedientes if e["Número de Expediente"] == expediente_numero), None)

        if not expediente:
            messagebox.showinfo("Error", "Expediente no encontrado.")
            return

        # Definir todos los campos necesarios para el informe
        campos_necesarios = [
            "fecha", "Unidad", "Número de Expediente", "Nombre del Paciente",
            "edad", "Fecha de Nacimiento", "Diagnóstico", "Área de Intervención",
            "periodo_intervencion", "terapias_recibidas",
            "faltas", "Objetivos Iniciales", "avance_objetivos", "nuevos_objetivos",
            "Observaciones Clínicas", "tratamiento", "sugerencias_casa", "elaborado_por", "cedula"
        ]

        # Agregar campos faltantes con valores vacíos
        for campo in campos_necesarios:
            if campo not in expediente:
                expediente[campo] = ""  # Asignar un valor vacío si el campo no existe

        # Crear una instancia de DetallesExpediente y mostrar los detalles
        detalles_expediente = DetallesExpediente(
            self.body_frame,
            expediente,  # Pasar el expediente actualizado (con todos los campos)
            programas={},  # Aquí deberías pasar los programas si los tienes
            planes_trabajo={},  # Aquí deberías pasar los planes de trabajo si los tienes
            guardar_planes_trabajo=lambda x: None,  # Función dummy para guardar planes
            generar_documento_word=lambda x, y: None  # Función dummy para generar documentos
        )
        detalles_expediente.crear_informe()
# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    body_frame = tk.Frame(root)
    body_frame.pack(fill="both", expand=True)
    app = ExpedientesApp(body_frame)
    app.lista_expedientes()
    root.mainloop()
