import tkinter as tk
from tkinter import messagebox

# Función para seleccionar programas
def seleccionar_programas(programas, campos_modificados):
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



