"""Dado un PDF, genera un archivo Markdown"""

from pathlib import Path

# Estas lineas del 6 al 18 antes de la fc se usan para crear una version de Converter mas sencilla en pdfs sin imagenes
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

pipeline_options = PdfPipelineOptions()

# Desactivar OCR - igual se puede poner en una sola fc o en dos separadas
pipeline_options.do_ocr = False

converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
)

def convertir_pdf_a_markdown(ruta_pdf: str) -> Path:
    """
    Convierte un PDF a Markdown y lo guarda junto al PDF.

    Devuelve la ruta del archivo .md generado.
    """

    ruta_pdf = Path(ruta_pdf)
    ruta_md = ruta_pdf.with_suffix(".md")

    print(f"Convirtiendo: {ruta_pdf.name}")

    print("Iniciando conversión...")

    # Convertir el PDF
    resultado = converter.convert(Path(ruta_pdf))

    # Exportar el contenido como Markdown
    markdown = resultado.document.export_to_markdown()

    ruta_md = Path(ruta_pdf).with_suffix(".md")

    ruta_md.write_text(markdown, encoding="utf-8")

    print("Conversión terminada.")
    print(f"Markdown guardado en: {ruta_md}")

    return ruta_md

if __name__ == "__main__":
    # prueba manual para convertir los pdf -- cambiar la ruta segun necesario - mejorar luego
    convertir_pdf_a_markdown("documents/simulacion_empresarial/simulacion_empresarial.pdf")
