"""
Se encarga de dividir un Documento en una lista de Chunk,
procurando que cada uno represente una unidad coherente de conocimiento.
"""

from src.core.models import Chunk, Documento


def _guardar_chunk(
    chunks: list[Chunk],
    documento: Documento,
    indice: int,
    titulo: str | None,
    subtitulo: str | None,
    contenido: list[str],
) -> int:
    """
    Crea un Chunk a partir del contenido acumulado y lo añade a la lista.

    Args:
        chunks: Lista donde se almacenan los chunks generados.
        documento: Documento al que pertenece el chunk.
        indice: Posición del chunk dentro del documento.
        titulo: Título principal (#) del documento.
        subtitulo: Subtítulo (##) asociado al chunk.
        contenido: Líneas de texto acumuladas.

    Returns:
        El siguiente índice disponible.
    """

    texto_chunk = "\n".join(contenido).strip()

    if texto_chunk:
        chunks.append(
            Chunk(
                documento=documento,
                indice=indice,
                titulo=titulo,
                subtitulo=subtitulo,
                texto=texto_chunk,
            )
        )
        indice += 1

    return indice


def crear_chunks_documento(
    documento: Documento,
) -> list[Chunk]:
    """
    Divide un Documento en una lista de Chunk utilizando
    los encabezados Markdown como separadores de secciones.

    Args:
        documento: Documento que se desea fragmentar.

    Returns:
        Lista de chunks pertenecientes al documento.
    """

    chunks: list[Chunk] = []

    indice = 0

    titulo_actual: str | None = None
    subtitulo_actual: str | None = None
    contenido_seccion: list[str] = []

    for linea in documento.texto.splitlines():

        linea_limpia = linea.strip()

        # Título principal (#)
        if linea_limpia.startswith("# "):

            if contenido_seccion:
                indice = _guardar_chunk(
                    chunks,
                    documento,
                    indice,
                    titulo_actual,
                    subtitulo_actual,
                    contenido_seccion,
                )
                contenido_seccion = []

            titulo_actual = linea_limpia.lstrip("#").strip()
            subtitulo_actual = None

        # Subtítulo (##)
        elif linea_limpia.startswith("## "):

            if contenido_seccion:
                indice = _guardar_chunk(
                    chunks,
                    documento,
                    indice,
                    titulo_actual,
                    subtitulo_actual,
                    contenido_seccion,
                )
                contenido_seccion = []

            subtitulo_actual = linea_limpia.lstrip("#").strip()

        else:

            if linea_limpia:
                contenido_seccion.append(linea_limpia)

            elif contenido_seccion:
                contenido_seccion.append("")

    if contenido_seccion:
        _guardar_chunk(
            chunks,
            documento,
            indice,
            titulo_actual,
            subtitulo_actual,
            contenido_seccion,
        )

    return chunks


def crear_chunks_documentos(
    documentos: list[Documento],
) -> list[Chunk]:
    """
    Divide una colección de documentos en Chunk.

    Args:
        documentos: Lista de documentos.

    Returns:
        Lista con todos los chunks generados.
    """

    todos_los_chunks: list[Chunk] = []

    for documento in documentos:

        chunks_documento = crear_chunks_documento(documento)

        todos_los_chunks.extend(chunks_documento)

    return todos_los_chunks


if __name__ == "__main__":

    print("Este módulo proporciona funciones para dividir " "Documentos en Chunks.")
