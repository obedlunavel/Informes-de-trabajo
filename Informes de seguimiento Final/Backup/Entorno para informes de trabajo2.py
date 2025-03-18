# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
from generar_documento import generar_documento_word  # Importar la función externa

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

        # Encabezado del menú lateral
        header_label = tk.Label(
            self.menu_frame,
            text="Menú",
            font=("Arial", 18, "bold"),
            bg="#800000",
            fg="white"
        )
        header_label.pack(fill="x", pady=(10, 20))

        # Botón para abrir el informe de trabajo
        self.create_menu_button("Informe de trabajo", self.informe_de_trabajo)

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
        button = ttk.Button(
            self.menu_frame,
            text=text,
            style="TButton",
            command=command
        )
        button.pack(fill="x", padx=10, pady=5)

    def informe_de_trabajo(self):
        # Limpiar el body_frame
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        # Cargar expedientes
        expedientes = self.cargar_expedientes()

        if not expedientes:
            return

        # Mostrar lista de expedientes en el body_frame
        tk.Label(
            self.body_frame,
            text="Seleccione un número de expediente:",
            font=("Arial", 14),
            bg="#FFFFFF",
            fg="#000000"
        ).pack(pady=10)

        for exp in expedientes:
            expediente = exp["Número de Expediente"]
            btn = tk.Button(
                self.body_frame,
                text=expediente,
                font=("Arial", 12),
                bg="#800000",
                fg="white",
                relief="flat",
                command=lambda e=expediente: self.mostrar_formulario(e, expedientes)
            )
            btn.pack(pady=5)

    def cargar_expedientes(self):
        try:
            with open("expedientes.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo expedientes.json no existe.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo expedientes.json está mal formado.")
            return []

    def mostrar_formulario(self, expediente, expedientes):
        # Limpiar el body_frame
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        # Buscar el expediente seleccionado
        datos_expediente = None
        for exp in expedientes:
            if exp["Número de Expediente"] == expediente:
                datos_expediente = exp
                break

        if not datos_expediente:
            messagebox.showerror("Error", "Expediente no encontrado.")
            return

        # Crear el formulario en el body_frame
        tk.Label(self.body_frame, text="Fecha:", bg="#FFFFFF", fg="#000000").grid(row=0, column=0, padx=10, pady=5)
        self.fecha_entry = tk.Entry(self.body_frame)
        self.fecha_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Unidad:", bg="#FFFFFF", fg="#000000").grid(row=1, column=0, padx=10, pady=5)
        self.unidad_entry = tk.Entry(self.body_frame)
        self.unidad_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Número de Expediente:", bg="#FFFFFF", fg="#000000").grid(row=2, column=0, padx=10, pady=5)
        self.expediente_entry = tk.Entry(self.body_frame)
        self.expediente_entry.insert(0, expediente)
        self.expediente_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Nombre del Paciente:", bg="#FFFFFF", fg="#000000").grid(row=3, column=0, padx=10, pady=5)
        self.nombre_entry = tk.Entry(self.body_frame)
        self.nombre_entry.insert(0, datos_expediente["Nombre del Paciente"])
        self.nombre_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Edad:", bg="#FFFFFF", fg="#000000").grid(row=4, column=0, padx=10, pady=5)
        self.edad_entry = tk.Entry(self.body_frame)
        self.edad_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Fecha de Nacimiento:", bg="#FFFFFF", fg="#000000").grid(row=5, column=0, padx=10, pady=5)
        self.fecha_nacimiento_entry = tk.Entry(self.body_frame)
        self.fecha_nacimiento_entry.insert(0, datos_expediente["Fecha de Nacimiento"])
        self.fecha_nacimiento_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Diagnóstico:", bg="#FFFFFF", fg="#000000").grid(row=6, column=0, padx=10, pady=5)
        self.diagnostico_entry = tk.Entry(self.body_frame)
        self.diagnostico_entry.insert(0, datos_expediente["Diagnóstico"])
        self.diagnostico_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Área de Intervención:", bg="#FFFFFF", fg="#000000").grid(row=7, column=0, padx=10, pady=5)
        self.area_intervencion_entry = tk.Entry(self.body_frame)
        self.area_intervencion_entry.insert(0, datos_expediente["Área de Intervención"])
        self.area_intervencion_entry.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Período de Intervención:", bg="#FFFFFF", fg="#000000").grid(row=8, column=0, padx=10, pady=5)
        self.periodo_intervencion_entry = tk.Entry(self.body_frame)
        self.periodo_intervencion_entry.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Número de Terapias Recibidas:", bg="#FFFFFF", fg="#000000").grid(row=9, column=0, padx=10, pady=5)
        self.terapias_recibidas_entry = tk.Entry(self.body_frame)
        self.terapias_recibidas_entry.grid(row=9, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Número de Faltas:", bg="#FFFFFF", fg="#000000").grid(row=10, column=0, padx=10, pady=5)
        self.faltas_entry = tk.Entry(self.body_frame)
        self.faltas_entry.grid(row=10, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Objetivos Iniciales (uno por línea):", bg="#FFFFFF", fg="#000000").grid(row=11, column=0, padx=10, pady=5)
        self.objetivos_iniciales_entry = tk.Text(self.body_frame, height=5, width=30)
        self.objetivos_iniciales_entry.grid(row=11, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Avance de los Objetivos:", bg="#FFFFFF", fg="#000000").grid(row=12, column=0, padx=10, pady=5)
        self.avance_objetivos_entry = tk.Text(self.body_frame, height=5, width=30)
        self.avance_objetivos_entry.grid(row=12, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Nuevos Objetivos (uno por línea):", bg="#FFFFFF", fg="#000000").grid(row=13, column=0, padx=10, pady=5)
        self.nuevos_objetivos_entry = tk.Text(self.body_frame, height=5, width=30)
        self.nuevos_objetivos_entry.grid(row=13, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Seguimiento:", bg="#FFFFFF", fg="#000000").grid(row=14, column=0, padx=10, pady=5)
        self.seguimiento_entry = tk.Text(self.body_frame, height=5, width=30)
        self.seguimiento_entry.grid(row=14, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Elaborado por:", bg="#FFFFFF", fg="#000000").grid(row=15, column=0, padx=10, pady=5)
        self.elaborado_por_entry = tk.Entry(self.body_frame)
        self.elaborado_por_entry.grid(row=15, column=1, padx=10, pady=5)

        tk.Label(self.body_frame, text="Cédula:", bg="#FFFFFF", fg="#000000").grid(row=16, column=0, padx=10, pady=5)
        self.cedula_entry = tk.Entry(self.body_frame)
        self.cedula_entry.grid(row=16, column=1, padx=10, pady=5)

        # Botón para generar el documento
        submit_button = tk.Button(
            self.body_frame,
            text="Generar Documento",
            font=("Arial", 12),
            bg="#800000",
            fg="white",
            relief="flat",
            command=self.generar_documento
        )
        submit_button.grid(row=17, column=0, columnspan=2, pady=20)

    def generar_documento(self):
        datos = {
            "fecha": self.fecha_entry.get(),
            "unidad": self.unidad_entry.get(),
            "expediente": self.expediente_entry.get(),
            "nombre": self.nombre_entry.get(),
            "edad": self.edad_entry.get(),
            "fecha_nacimiento": self.fecha_nacimiento_entry.get(),
            "diagnostico": self.diagnostico_entry.get(),
            "area_intervencion": self.area_intervencion_entry.get(),
            "periodo_intervencion": self.periodo_intervencion_entry.get(),
            "terapias_recibidas": self.terapias_recibidas_entry.get(),
            "faltas": self.faltas_entry.get(),
            "objetivos_iniciales": self.objetivos_iniciales_entry.get("1.0", tk.END),
            "avance_objetivos": self.avance_objetivos_entry.get("1.0", tk.END),
            "nuevos_objetivos": self.nuevos_objetivos_entry.get("1.0", tk.END),
            "seguimiento": self.seguimiento_entry.get("1.0", tk.END),
            "elaborado_por": self.elaborado_por_entry.get(),
            "cedula": self.cedula_entry.get()
        }

        # Nombre del archivo
        nombre_archivo = f'IS_{datos["nombre"].replace(" ", "_")}_LIBERADO_Replica.docx'

        # Llamar a la función externa para generar el documento
        generar_documento_word(datos, nombre_archivo)
        messagebox.showinfo("Éxito", "Documento generado correctamente.")

    def run(self):
        self.root.mainloop()

# Ejecutar el menú principal
if __name__ == "__main__":
    menu = ModernMainMenu()
    menu.run()
