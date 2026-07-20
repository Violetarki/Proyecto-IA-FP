from pathlib import Path

from docling.document_converter import DocumentConverter

from models import Documento


# Creamos una única instancia del convertidor
converter = DocumentConverter()


def leer_pdf(ruta_pdf, metodologia):
    """
    Lee un PDF utilizando Docling y devuelve un objeto Documento.
    """

    # Convertir el PDF
    resultado = converter.convert(Path(ruta_pdf))

    # Exportar el contenido como Markdown
    texto = resultado.document.export_to_markdown()

    # Crear nuestro objeto Documento
    documento = Documento(
        metodologia=metodologia,
        nombre=Path(ruta_pdf).name,
        texto=texto,
        ruta=str(ruta_pdf),
        paginas=0,  # Ya veremos cómo obtenerlas con Docling
    )

    return documento
