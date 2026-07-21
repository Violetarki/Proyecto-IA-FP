"""Módulo de limpieza de archivos Markdown."""

import re
from pathlib import Path


CABECERAS_PIES_RUIDO = {
    "Lean Startup en Educación",
    "Lean Startup en Educacion",
    'porque "emprender no es una opción"',
    'porque "emprender no es una opcion"',
    "www.pablopenalver.com",
}


SIMBOLOS_OCR = {
    "",
    "口",
    "司",
    "！",
}


def limpiar_texto(texto: str) -> str:
    """
    Limpia y normaliza el contenido de un documento Markdown.
    """

    texto = eliminar_marcadores_imagen(texto)
    texto = eliminar_cabeceras_y_pies(texto)
    texto = eliminar_numeros_pagina(texto)
    texto = eliminar_simbolos_ocr(texto)
    texto = eliminar_isbn(texto)
    texto = unir_palabras_partidas(texto)
    texto = unir_parrafos_partidos(texto)
    texto = normalizar_formato(texto)
    texto = eliminar_lineas_vacias(texto)

    return texto.strip()


def eliminar_marcadores_imagen(texto: str) -> str:
    """
    Elimina los marcadores de imagen generados al convertir el PDF.
    """

    return texto.replace("<!-- image -->", "")


def eliminar_cabeceras_y_pies(texto: str) -> str:
    """
    Elimina cabeceras y pies de página repetidos.
    """

    lineas_limpias = []

    for linea in texto.splitlines():
        contenido = linea.strip()

        if contenido in CABECERAS_PIES_RUIDO:
            continue

        lineas_limpias.append(linea)

    return "\n".join(lineas_limpias)


def eliminar_numeros_pagina(texto: str) -> str:
    """
    Elimina líneas que contienen únicamente un número de página.
    """

    lineas_limpias = []

    for linea in texto.splitlines():
        contenido = linea.strip()

        if contenido.isdigit():
            continue

        lineas_limpias.append(linea)

    return "\n".join(lineas_limpias)


def eliminar_simbolos_ocr(texto: str) -> str:
    """
    Elimina símbolos extraños introducidos durante la extracción OCR.
    """

    for simbolo in SIMBOLOS_OCR:
        texto = texto.replace(simbolo, "")

    return texto


def eliminar_isbn(texto: str) -> str:
    """
    Elimina las líneas que contienen códigos ISBN.
    """

    patron_isbn = re.compile(
        r"\bISBN(?:-1[03])?\s*:?\s*[\dXx\- ]{10,20}\b",
        re.IGNORECASE,
    )

    lineas_limpias = []

    for linea in texto.splitlines():

        if patron_isbn.search(linea):
            continue

        lineas_limpias.append(linea)

    return "\n".join(lineas_limpias)


def unir_palabras_partidas(texto: str) -> str:
    """
    Une palabras cortadas mediante un guion y un salto de línea.

    Ejemplo:
        emprendi-
        miento

    Resultado:
        emprendimiento
    """

    return re.sub(
        r"([a-záéíóúüñ])-\s*\n\s*([a-záéíóúüñ])",
        r"\1\2",
        texto,
        flags=re.IGNORECASE,
    )


def unir_parrafos_partidos(texto: str) -> str:
    """
    Une líneas consecutivas que parecen pertenecer al mismo párrafo.

    Conserva títulos, listas, tablas y bloques Markdown.
    """

    lineas = texto.splitlines()
    resultado = []
    parrafo_actual = ""

    for linea in lineas:
        contenido = linea.strip()

        if not contenido:

            if parrafo_actual:
                resultado.append(parrafo_actual)
                parrafo_actual = ""

            resultado.append("")
            continue

        if es_elemento_markdown(contenido):

            if parrafo_actual:
                resultado.append(parrafo_actual)
                parrafo_actual = ""

            resultado.append(contenido)
            continue

        if not parrafo_actual:
            parrafo_actual = contenido
        else:
            parrafo_actual += " " + contenido

    if parrafo_actual:
        resultado.append(parrafo_actual)

    return "\n".join(resultado)


def es_elemento_markdown(linea: str) -> bool:
    """
    Comprueba si una línea es un elemento Markdown que no debe unirse
    con otros párrafos.
    """

    patrones_markdown = (
        "#",
        "- ",
        "* ",
        "+ ",
        "> ",
        "|",
        "```",
    )

    if linea.startswith(patrones_markdown):
        return True

    if re.match(r"^\d+[.)]\s+", linea):
        return True

    return False


def normalizar_formato(texto: str) -> str:
    """
    Normaliza espacios y caracteres especiales sin destruir el Markdown.
    """

    texto = texto.replace("\u2003", " ")
    texto = texto.replace("\u00a0", " ")
    texto = texto.replace("\t", " ")

    texto = re.sub(r"[ ]{2,}", " ", texto)

    texto = "\n".join(
        linea.strip()
        for linea in texto.splitlines()
    )

    return texto


def eliminar_lineas_vacias(texto: str) -> str:
    """
    Conserva como máximo una línea vacía entre bloques.
    """

    return re.sub(r"\n{3,}", "\n\n", texto)


def limpiar_archivo_markdown(
    ruta_entrada: Path,
    ruta_salida: Path,
) -> None:
    """
    Lee un archivo Markdown, limpia su contenido y guarda el resultado.
    """

    if not ruta_entrada.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta_entrada}"
        )

    if ruta_entrada.suffix.lower() != ".md":
        raise ValueError(
            f"El archivo no es Markdown: {ruta_entrada}"
        )

    texto_original = ruta_entrada.read_text(
        encoding="utf-8"
    )

    texto_limpio = limpiar_texto(
        texto_original
    )

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta_salida.write_text(
        texto_limpio,
        encoding="utf-8",
    )

    print(
        f"Archivo limpio creado: {ruta_salida}"
    )


def limpiar_carpeta_markdown(
    carpeta_raw: str = "data/markdown_raw",
    carpeta_clean: str = "data/markdown_clean",
) -> None:
    """
    Recorre todos los Markdown de markdown_raw y guarda los archivos
    limpios en markdown_clean, conservando la estructura de carpetas.
    """

    ruta_raw = Path(carpeta_raw)
    ruta_clean = Path(carpeta_clean)

    if not ruta_raw.exists():
        raise FileNotFoundError(
            f"No existe la carpeta: {ruta_raw}"
        )

    if not ruta_raw.is_dir():
        raise NotADirectoryError(
            f"La ruta no es una carpeta: {ruta_raw}"
        )

    archivos_md = list(
        ruta_raw.rglob("*.md")
    )

    if not archivos_md:
        print(
            f"No se encontraron archivos Markdown en {ruta_raw}"
        )
        return

    for ruta_entrada in archivos_md:

        ruta_relativa = ruta_entrada.relative_to(
            ruta_raw
        )

        ruta_salida = ruta_clean / ruta_relativa

        limpiar_archivo_markdown(
            ruta_entrada=ruta_entrada,
            ruta_salida=ruta_salida,
        )

    print(
        f"\nSe han limpiado {len(archivos_md)} archivos Markdown."
    )


if __name__ == "__main__":

    limpiar_carpeta_markdown()