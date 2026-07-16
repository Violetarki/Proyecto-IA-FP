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
    ruta = Path(carpeta)

    # Comprobar que la carpeta existe
    if not ruta.is_dir():
        raise NotADirectoryError(f"La ruta no es una carpeta: {ruta}")

    if not ruta.exists():
        raise FileNotFoundError(f"No existe la carpeta: {ruta}")

    # Buscar todos los PDFs
    # --> "Búscame todos los archivos que cumplan un patrón."

    # Crear una lista vacía
    documentos = []

    # Para cada PDF:
    for archivo in ruta.glob("*.pdf"):
        documento = leer_pdf(archivo)
        documentos.append(documento)
   

    # Devolver la lista
    return documentos


if __name__ == "__main__":
    ruta_docs = "documents"
    leer_documentos(ruta_docs)
