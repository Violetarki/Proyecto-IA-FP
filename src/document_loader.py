"""Recorre una carpeta, lee todos los archivos PDF utilizando pdf_loader --> leer_pdf()
y devuelve una lista de objetos Documento."""

from pathlib import Path
from models import Documento, Metodologia
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

    # Crear una lista vacía
    documentos = []

   # Recorrer cada subcarpeta (cada metodología)
    for carpeta_metodologia in ruta.iterdir():


        if not carpeta_metodologia.is_dir():
            continue

        metodologia = Metodologia(
            nombre=carpeta_metodologia.name
        )

        # Buscar PDFs dentro de esa metodología
        pdf_paths = carpeta_metodologia.glob("*.pdf")

        for pdf_path in pdf_paths:

            documento = leer_pdf(str(pdf_path), metodologia)

            documentos.append(documento)


    # Devolver la lista
    return documentos

if __name__ == "__main__":
    
    # Prueba
    documentos = leer_documentos("documents")

    for documento in documentos:
        print("-------------------------")
        print(documento.metodologia.nombre)
        print(documento.nombre)
        print(documento.paginas)
