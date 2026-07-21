"""
Orquestador encargado de leer los archivos Markdown limpios.

Recorre la carpeta data/markdown_clean, detecta la metodología
mediante el nombre de cada subcarpeta y devuelve una lista
de objetos Documento.
"""

from pathlib import Path

from models import Documento, Metodologia


def leer_markdown(
    ruta_md: Path,
    metodologia: Metodologia,
) -> Documento:
    """
    Lee un archivo Markdown y lo convierte en un objeto Documento.

    Args:
        ruta_md: Ruta del archivo Markdown.
        metodologia: Metodología asociada al documento.

    Returns:
        Un objeto Documento con el contenido del archivo.
    """

    if not ruta_md.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta_md}"
        )

    if not ruta_md.is_file():
        raise ValueError(
            f"La ruta no corresponde a un archivo: {ruta_md}"
        )

    if ruta_md.suffix.lower() != ".md":
        raise ValueError(
            f"El archivo no tiene extensión Markdown: {ruta_md}"
        )

    texto = ruta_md.read_text(encoding="utf-8")

    documento = Documento(
        metodologia=metodologia,
        nombre=ruta_md.stem,
        texto=texto,
        ruta=str(ruta_md),
    )

    return documento


def leer_documentos(
    carpeta: str = "data/markdown_clean",
) -> list[Documento]:
    """
    Recorre las subcarpetas de markdown_clean y carga todos
    los archivos Markdown como objetos Documento.

    La metodología se obtiene a partir del nombre de la
    subcarpeta en la que se encuentra cada archivo.

    Args:
        carpeta: Carpeta raíz de los Markdown limpios.

    Returns:
        Lista de objetos Documento.
    """

    ruta_carpeta = Path(carpeta)

    if not ruta_carpeta.exists():
        raise FileNotFoundError(
            f"No existe la carpeta: {ruta_carpeta}"
        )

    if not ruta_carpeta.is_dir():
        raise NotADirectoryError(
            f"La ruta no es una carpeta: {ruta_carpeta}"
        )

    documentos = []

    for carpeta_metodologia in sorted(
        ruta_carpeta.iterdir()
    ):
        if not carpeta_metodologia.is_dir():
            continue

        metodologia = Metodologia(
            carpeta_metodologia.name
        )

        archivos_markdown = sorted(
            carpeta_metodologia.glob("*.md")
        )

        for archivo_md in archivos_markdown:
            documento = leer_markdown(
                ruta_md=archivo_md,
                metodologia=metodologia,
            )

            documentos.append(documento)

    return documentos


if __name__ == "__main__":
    documentos = leer_documentos()

    print(
        f"\nSe han cargado {len(documentos)} documentos:\n"
    )

    for documento in documentos:
        print(
            f"- {documento.nombre} "
            f"({documento.metodologia})"
        )