"""Orquestador: Recorre la carpeta data/markdown_clean, lee todos los archivos .md
, detectar la metodología por el nombre de la carpeta y devuelve una lista de objetos Documento.
"""

from pathlib import Path
from models import Documento, Metodologia


def leer_documentos(carpeta="data/markdown_clean"):
    """
    Recorre todos los archivos Markdown limpios y devuelve
    una lista de objetos Documento.
    """

    documentos = []

    carpeta = Path(carpeta)

    for carpeta_metodologia in carpeta.iterdir():

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


if __name__ == "__main__":
    pass
# cuando hagamos la interfaz web para que los profesores suban documentos, probablemente solo hay que llamar a:

# documentos = leer_documentos("documents")

# Pipeline actual con .md:
# PDF
#  │
#  ▼
# Docling
#  │
#  ▼
# Markdown (.md)
#  │
#  ▼
# text_cleaner
#  │
#  ▼
# Documento ** Este paso va en este archivo
#  │
#  ▼
# Chunker
#  │
#  ▼
# Embeddings

# **
# leer_documentos()
#     │
#     ├── convertir_si_necesario()
    def convertir_si_necesario(pdf_path):
        pass

    # Responsabilidad:

    # Comprobar si existe el .md.
    # Si no existe (o está desactualizado), llamar a docling_converter.
#     │
#     # └── leer_markdown()
    def leer_markdown(md_path, metodologia):
        pass
