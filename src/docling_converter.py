"""Dado un PDF, genera un archivo Markdown"""

from pathlib import Path
from docling.document_converter import DocumentConverter

converter = DocumentConverter()


def convertir_pdf_a_markdown(ruta_pdf: str) -> Path:
    """
    Convierte un PDF a Markdown y lo guarda en data/markdown_docling.

    Devuelve la ruta del archivo Markdown generado.
    """

    ruta_pdf = Path(ruta_pdf)
    
    # usa el nombre de la carpeta para construir una ruta
    carpeta_metodologia = ruta_pdf.parent.name

    ruta_md = Path("data") / "markdown_docling" / carpeta_metodologia / f"{ruta_pdf.stem}.md"

    # Crear carpetas si no existen
    ruta_md.parent.mkdir(parents=True, exist_ok=True)

    print(f"Convirtiendo: {ruta_pdf.name}")

    # Convertir el PDF
    resultado = converter.convert(ruta_pdf)

    # Exportar el contenido como Markdown
    texto_markdown = resultado.document.export_to_markdown()

    ruta_md.write_text(texto_markdown, encoding="utf-8")

    print("Conversión terminada.")
    print(f"Markdown guardado en: {ruta_md}")

    return ruta_md
