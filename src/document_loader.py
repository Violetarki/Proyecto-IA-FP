"""Recorre una carpeta, lee todos los archivos PDF utilizando pdf_loader --> leer_pdf()
y devuelve una lista de objetos Documento."""

from pathlib import Path
from models import Documento
from pdf_loader import leer_pdf

def leer_documentos(carpeta: str) -> list[Documento]:
    """
    Lee todos los archivos PDF de una carpeta y devuelve una lista
    de objetos Documento.
    """

    # Recibir la carpeta

    # Comprobar que la carpeta existe

    # Buscar todos los PDFs
    # Posibilidad de usar ruta.glob("*.pdf") --> "Búscame todos los archivos que cumplan un patrón."

    # Crear una lista vacía
    documentos = []

    # Para cada PDF:

    # 1. llamar a leer_pdf()

    # 2. guardar el Documento en la lista

    # Devolver la lista
