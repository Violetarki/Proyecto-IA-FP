"""
Módulo encargado de dividir documentos en fragmentos de texto.

El chunker recibe objetos Documento y devuelve objetos Chunk.
Cada chunk conserva:

- El texto del fragmento.
- El documento del que procede.
- La sección en la que aparece.
"""

import re

from models import Chunk, Documento


TAMANIO_MAXIMO_CHUNK = 1800
SOLAPAMIENTO_CHUNK = 200
SECCION_SIN_TITULO = "Sin sección"


def es_titulo(linea: str) -> bool:
    """
    Comprueba si una línea corresponde a un título Markdown.

    Ejemplos válidos:

        # Introducción
        ## Lean Startup
        ### Conceptos básicos
    """

    linea = linea.strip()

    return bool(
        re.match(r"^#{1,6}\s+\S+", linea)
    )


def limpiar_titulo(linea: str) -> str:
    """
    Elimina los símbolos Markdown de un título.

    Ejemplo:

        ## Lean Startup

    Resultado:

        Lean Startup
    """

    return re.sub(
        r"^#{1,6}\s*",
        "",
        linea.strip(),
    ).strip()


def obtener_bloques(documento: Documento) -> list[str]:
    """
    Divide el texto de un Documento en bloques.

    Cada bloque contiene líneas consecutivas no vacías.
    Una o más líneas vacías marcan el final de un bloque.
    """

    bloques: list[str] = []
    bloque_actual: list[str] = []

    for linea in documento.texto.splitlines():

        if not linea.strip():

            if bloque_actual:
                bloque = "\n".join(
                    bloque_actual
                ).strip()

                bloques.append(bloque)
                bloque_actual = []

        else:
            bloque_actual.append(linea)

    if bloque_actual:
        bloque = "\n".join(
            bloque_actual
        ).strip()

        bloques.append(bloque)

    return bloques


def dividir_texto_largo(
    texto: str,
    tamanio_maximo: int,
    solapamiento: int,
) -> list[str]:
    """
    Divide un texto demasiado largo en fragmentos más pequeños.

    La división se realiza por palabras para evitar cortar palabras
    por la mitad.

    El solapamiento permite repetir una pequeña parte del fragmento
    anterior para no perder contexto entre chunks consecutivos.
    """

    if len(texto) <= tamanio_maximo:
        return [texto]

    palabras = texto.split()
    fragmentos: list[str] = []
    fragmento_actual: list[str] = []

    for palabra in palabras:

        texto_provisional = " ".join(
            fragmento_actual + [palabra]
        )

        if (
            len(texto_provisional) <= tamanio_maximo
            or not fragmento_actual
        ):
            fragmento_actual.append(palabra)
            continue

        fragmento = " ".join(
            fragmento_actual
        ).strip()

        fragmentos.append(fragmento)

        palabras_solapadas: list[str] = []
        caracteres_solapados = 0

        for palabra_anterior in reversed(
            fragmento_actual
        ):
            longitud_palabra = len(
                palabra_anterior
            ) + 1

            if (
                caracteres_solapados + longitud_palabra
                > solapamiento
            ):
                break

            palabras_solapadas.insert(
                0,
                palabra_anterior,
            )

            caracteres_solapados += longitud_palabra

        fragmento_actual = (
            palabras_solapadas + [palabra]
        )

    if fragmento_actual:
        fragmentos.append(
            " ".join(fragmento_actual).strip()
        )

    return fragmentos


def crear_chunks(
    documento: Documento,
    tamanio_maximo: int = TAMANIO_MAXIMO_CHUNK,
    solapamiento: int = SOLAPAMIENTO_CHUNK,
) -> list[Chunk]:
    """
    Convierte un Documento en una lista de objetos Chunk.

    El algoritmo:

    1. Divide el documento en bloques.
    2. Detecta los títulos Markdown.
    3. Guarda el título como sección actual.
    4. Agrupa bloques hasta alcanzar el tamaño máximo.
    5. Crea los objetos Chunk.
    """

    if tamanio_maximo <= 0:
        raise ValueError(
            "El tamaño máximo debe ser mayor que cero."
        )

    if solapamiento < 0:
        raise ValueError(
            "El solapamiento no puede ser negativo."
        )

    if solapamiento >= tamanio_maximo:
        raise ValueError(
            "El solapamiento debe ser menor "
            "que el tamaño máximo."
        )

    bloques = obtener_bloques(documento)

    chunks: list[Chunk] = []
    seccion_actual = SECCION_SIN_TITULO
    texto_acumulado = ""

    def guardar_texto_acumulado() -> None:
        """
        Crea uno o varios chunks con el texto acumulado.
        """

        nonlocal texto_acumulado

        if not texto_acumulado.strip():
            return

        fragmentos = dividir_texto_largo(
            texto=texto_acumulado.strip(),
            tamanio_maximo=tamanio_maximo,
            solapamiento=solapamiento,
        )

        for fragmento in fragmentos:
            chunks.append(
                Chunk(
                    texto=fragmento,
                    documento_origen=documento,
                    seccion=seccion_actual,
                )
            )

        texto_acumulado = ""

    for bloque in bloques:

        lineas = bloque.splitlines()
        primera_linea = lineas[0].strip()

        if es_titulo(primera_linea):

            guardar_texto_acumulado()

            seccion_actual = limpiar_titulo(
                primera_linea
            )

            contenido_restante = "\n".join(
                lineas[1:]
            ).strip()

            if contenido_restante:
                texto_acumulado = contenido_restante

            continue

        if not texto_acumulado:
            texto_acumulado = bloque
            continue

        texto_provisional = (
            texto_acumulado
            + "\n\n"
            + bloque
        )

        if len(texto_provisional) <= tamanio_maximo:
            texto_acumulado = texto_provisional
        else:
            guardar_texto_acumulado()
            texto_acumulado = bloque

    guardar_texto_acumulado()

    return chunks


def crear_chunks_documentos(
    documentos: list[Documento],
    tamanio_maximo: int = TAMANIO_MAXIMO_CHUNK,
    solapamiento: int = SOLAPAMIENTO_CHUNK,
) -> list[Chunk]:
    """
    Crea chunks para una lista completa de documentos.
    """

    todos_los_chunks: list[Chunk] = []

    for documento in documentos:

        chunks_documento = crear_chunks(
            documento=documento,
            tamanio_maximo=tamanio_maximo,
            solapamiento=solapamiento,
        )

        todos_los_chunks.extend(
            chunks_documento
        )

    return todos_los_chunks


if __name__ == "__main__":
    from document_loader import leer_documentos

    documentos = leer_documentos(
        "data/markdown_clean"
    )

    if not documentos:
        print(
            "No se han encontrado documentos Markdown limpios."
        )

    else:
        chunks = crear_chunks_documentos(
            documentos
        )

        print(
            f"\nSe han cargado {len(documentos)} documentos."
        )

        print(
            f"Se han creado {len(chunks)} chunks.\n"
        )

        for indice, chunk in enumerate(
            chunks[:10],
            start=1,
        ):
            print(
                f"--- Chunk {indice} ---"
            )

            print(
                f"Documento: "
                f"{chunk.documento_origen.nombre}"
            )

            print(
                f"Metodología: "
                f"{chunk.documento_origen.metodologia.nombre}"
            )

            print(
                f"Sección: {chunk.seccion}"
            )

            print(
                f"Tamaño: {len(chunk.texto)} caracteres"
            )

            print(
                chunk.texto[:300]
            )

            print("=" * 80)