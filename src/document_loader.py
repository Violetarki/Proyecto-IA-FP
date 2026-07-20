"""orquestador: Recorre una carpeta, lee todos los archivos PDF en formato .md
y devuelve una lista de objetos Documento."""

from pathlib import Path
from models import Documento, Metodologia


def leer_documentos(carpeta):
    """
    Recorre todas las subcarpetas buscando archivos Markdown (.md)
    y crea un Documento por cada uno.
    """
    
    # Tiene q poder hacer:
        # Recorrer las metodologías.
        # Buscar los PDFs.
        # Asegurarse de que existe el .md.
        # Leer los Markdown.
        # Devolver list[Documento].
        
        
    # Replantear codigo segun nuevo pipeline con Docling
    documentos = []

    carpeta = Path(carpeta)

    for carpeta_metodologia in carpeta.iterdir():

        if not carpeta_metodologia.is_dir():
            continue

        metodologia = Metodologia(
            nombre=carpeta_metodologia.name.replace("_", " ").title()
        )

        for archivo_md in carpeta_metodologia.glob("*.md"):

            texto = archivo_md.read_text(encoding="utf-8")

            documento = Documento(
                metodologia=metodologia,
                nombre=archivo_md.stem,
                texto=texto,
                ruta=str(archivo_md), #esto tmb cambia a otra cosa
                paginas=0 # esta parte es inventada, ver como obtener nº paginas con el nuevo sistema
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
