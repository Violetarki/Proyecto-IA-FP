"""Dado un PDF, genera un archivo Markdown"""

from pathlib import Path
from docling.document_converter import DocumentConverter

converter = DocumentConverter()


def convertir_pdf_a_markdown(ruta_pdf: str) -> Path:
    """
    Convierte un PDF a Markdown y lo guarda junto al PDF.

    Args:
        ruta_pdf: Ruta del archivo PDF.

    Returns:
        Ruta del archivo Markdown generado.
    """

    ruta_pdf = Path(ruta_pdf)
    ruta_md = ruta_pdf.with_suffix(".md")

    print(f"Convirtiendo: {ruta_pdf.name}")

    print("Iniciando conversión...")

    # Convertir el PDF
    resultado = converter.convert(ruta_pdf)

    # Exportar el contenido como Markdown
    texto_markdown = resultado.document.export_to_markdown()

    ruta_md.write_text(texto_markdown, encoding="utf-8")

    print("Conversión terminada.")
    print(f"Markdown guardado en: {ruta_md}")

    return ruta_md
