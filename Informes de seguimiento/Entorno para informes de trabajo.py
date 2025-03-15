import tkinter as tk
from tkinter import ttk, messagebox
from Lista_expedientes import ExpedientesApp  # Importar la clase, no la función

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
        button = ttk.Button(
            self.menu_frame,
            text=text,
            style="TButton",
            command=command
        )
        button.pack(fill="x", padx=10, pady=5)

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


    

    def run(self):
        self.root.mainloop()

# Ejecutar el menú principal
if __name__ == "__main__":
    menu = ModernMainMenu()
    menu.run()
