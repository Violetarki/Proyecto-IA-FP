"""
Convierte un archivo PDF a Markdown mediante Docling.

El archivo Markdown generado se guarda dentro de:

data/markdown_raw/<metodologia>/<nombre_documento>.md

La metodología se obtiene automáticamente a partir del nombre
de la carpeta donde se encuentra el PDF.
"""

from pathlib import Path

from docling.document_converter import DocumentConverter


converter = DocumentConverter()


def convertir_pdf_a_markdown(ruta_pdf: str | Path) -> Path:
    """
    Convierte un archivo PDF a Markdown mediante Docling.

    La metodología se detecta por el nombre de la carpeta
    que contiene el PDF.

    Ejemplo:

        documents/lean_startup/manual.pdf

    Generará:

        data/markdown_raw/lean_startup/manual.md

    Args:
        ruta_pdf: Ruta del archivo PDF que se va a convertir.

    Returns:
        Ruta del archivo Markdown generado.
    """

    ruta_pdf = Path(ruta_pdf)

    if not ruta_pdf.exists():
        raise FileNotFoundError(
            f"No existe el archivo PDF: {ruta_pdf}"
        )

    if not ruta_pdf.is_file():
        raise ValueError(
            f"La ruta no corresponde a un archivo: {ruta_pdf}"
        )

    if ruta_pdf.suffix.lower() != ".pdf":
        raise ValueError(
            f"El archivo no tiene extensión PDF: {ruta_pdf}"
        )

    metodologia = ruta_pdf.parent.name

    ruta_markdown = (
        Path("data")
        / "markdown_raw"
        / metodologia
        / f"{ruta_pdf.stem}.md"
    )

    ruta_markdown.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Convirtiendo PDF: {ruta_pdf}")
    print(f"Metodología detectada: {metodologia}")

    resultado = converter.convert(ruta_pdf)

    texto_markdown = (
        resultado.document.export_to_markdown()
    )

    ruta_markdown.write_text(
        texto_markdown,
        encoding="utf-8",
    )

    print("Conversión terminada correctamente.")
    print(f"Markdown guardado en: {ruta_markdown}")

    return ruta_markdown


if __name__ == "__main__":
    print(
        "Este módulo debe utilizarse llamando a "
        "convertir_pdf_a_markdown(ruta_pdf)."
    )