"""Carga los documentos Markdown limpios del proyecto.

Recorre la carpeta data/markdown_clean, detecta la metodología a partir del
nombre de cada subcarpeta y devuelve una lista de objetos Documento.
"""

from pathlib import Path
from models import Documento, Metodologia


def leer_documentos():
    """
    Recorre todos los archivos Markdown limpios y devuelve
    una lista de objetos Documento.
    """

    documentos = []

    ruta_carpeta = Path("data/markdown_clean")

    for carpeta_metodologia in ruta_carpeta.iterdir():

        if not carpeta_metodologia.is_dir():
            continue

        metodologia = Metodologia(carpeta_metodologia.name)

        for archivo_md in carpeta_metodologia.glob("*.md"):

            texto = archivo_md.read_text(encoding="utf-8")

            documento = Documento(
                metodologia=metodologia,
                nombre=archivo_md.stem,
                texto=texto,
                ruta=str(archivo_md),
            )

            documentos.append(documento)

    return documentos
