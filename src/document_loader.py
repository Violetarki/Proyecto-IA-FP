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
    if not ruta.exists() or not ruta.is_dir():
        raise FileNotFoundError(f"La carpeta no existe: {carpeta}")
    
    if not ruta.is_dir():
        raise NotADirectoryError(f"La ruta no es una carpeta: {ruta}")

    # Buscar todos los PDFs
    # Posibilidad de usar ruta.glob("*.pdf") --> "Búscame todos los archivos que cumplan un patrón."
    pdf_paths = list(ruta.glob("*.pdf"))

    # Crear una lista vacía
    documentos = []

    # Para cada PDF:
    for pdf_path in pdf_paths:
        # 1. llamar a leer_pdf()
        doc = leer_pdf(str(pdf_path))

        # 2. guardar el Documento en la lista
        documentos.append(doc)

    # Devolver la lista
    return documentos

if __name__ == "__main__":
    ruta_docs = "documents"
    leer_documentos(ruta_docs)