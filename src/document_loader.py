"""Buscar documentos en una carpeta 
y utilizar leer_pdf() para convertirlos en objetos Documento"""

from pathlib import Path
from models import Documento
from pdf_loader import leer_pdf

def leer_documentos(carpeta: str) -> list[Documento]:

    # Recibir la carpeta

    # Comprobar que existe

    # Buscar todos los PDFs
    # Posibilidad de usar ruta.glob("*.pdf") --> "Búscame todos los archivos que cumplan un patrón."

    # Crear una lista vacía
    documentos = []

    # Para cada PDF

        # llamar a leer_pdf()

        # guardar el Documento en la lista

    # Devolver la lista
