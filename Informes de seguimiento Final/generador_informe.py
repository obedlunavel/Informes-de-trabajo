# generador_informe.py
from generar_documento import generar_documento_word

class GeneradorInforme:
    def __init__(self, datos, nombre_archivo, generar_documento_word):
        """
        Inicializa la clase con los datos, el nombre del archivo y la función generar_documento_word.
        """
        self.datos = datos
        self.nombre_archivo = nombre_archivo
        self.generar_documento_word = generar_documento_word

    def generar_informe(self):
        """
        Genera el documento Word utilizando la función generar_documento_word.
        """
        try:
            self.generar_documento_word(self.datos, self.nombre_archivo)
            return True  # Indica que el documento se generó correctamente
        except Exception as e:
            print(f"Error al generar el documento: {e}")  # Mensaje de depuración
            return False  # Indica que hubo un error


def crear_informe(datos, nombre_archivo):
    """
    Función de conveniencia para crear un informe.
    """
    generador = GeneradorInforme(datos, nombre_archivo, generar_documento_word)
    return generador.generar_informe()
