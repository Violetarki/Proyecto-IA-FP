"""Se encarga de dividir un Documento en una lista de Chunk, 
procurando que cada uno represente una unidad coherente de conocimiento."""

from document_loader import leer_documentos
from models import Documento, Chunk

# Entrada:
# Documento - ok

# Salida:
# list[Chunk] - ok


def crear_chunks() -> list[Chunk]:
    """Lee los documentos Markdown limpios y devuelve una lista de Chunk.

    El algoritmo recorre cada documento línea a línea, identifica las
    secciones marcadas con encabezados de Markdown y crea un chunk por
    cada sección con el texto acumulado. De esta forma, cada chunk conserva
    el contenido lógico del documento y su sección asociada.
    """

    # 1. Cargar los documentos Markdown limpios desde la carpeta markdown_clean.
    documentos = leer_documentos("data/markdown_clean")

    # 2. Preparar la lista donde guardaremos todos los chunks generados.
    chunks: list[Chunk] = []

    # 3. Recorrer cada documento y dividirlo por secciones.
    for documento in documentos:
        # Mantener el estado de la sección actual mientras recorremos el texto.
        seccion_actual = ""
        contenido_seccion: list[str] = []

        # 4. Recorrer las líneas del documento.
        for linea in documento.texto.splitlines():
            # Si la línea empieza por "##", significa que empieza una nueva
            # sección. Antes de cambiar de sección, guardamos la anterior.
            if linea.startswith("##") and linea.strip():
                if contenido_seccion:
                    texto_chunk = "\n".join(contenido_seccion).strip()
                    if texto_chunk:
                        chunks.append(
                            Chunk(
                                texto=texto_chunk,
                                documento_origen=documento,
                                seccion=seccion_actual,
                            )
                        )

                # Iniciar la nueva sección con el texto del encabezado.
                seccion_actual = linea.strip().lstrip("#").strip()
                contenido_seccion = []
            else:
                # Si no es un encabezado, se añade al contenido actual.
                if linea.strip():
                    contenido_seccion.append(linea.strip())
                elif contenido_seccion:
                    # Mantener separación entre párrafos cuando haya líneas vacías.
                    contenido_seccion.append("")

        # 5. Guardar la última sección del documento cuando termine el recorrido.
        if contenido_seccion:
            texto_chunk = "\n".join(contenido_seccion).strip()
            if texto_chunk:
                chunks.append(
                    Chunk(
                        texto=texto_chunk,
                        documento_origen=documento,
                        seccion=seccion_actual,
                    )
                )

    # 6. Devolver la lista completa de chunks generados.
    return chunks


## Esto entiendo que ya no es necesario
def obtener_bloques(documento: Documento) -> list[str]:
    """Recibir un Documento y devolver una lista de bloques de texto.

    Cada bloque agrupa líneas consecutivas no vacías. Separa los bloques
    cuando encuentra una o más líneas vacías.
    """
    bloques: list[str] = []
    bloque_actual: list[str] = []

    # Recorrer todas las líneas del texto del documento.
    for linea in documento.texto.splitlines():
        if linea.strip() == "":
            # Línea vacía: terminar el bloque actual si hay algo acumulado.
            if bloque_actual:
                bloques.append("\n".join(bloque_actual).strip())
                bloque_actual = []
        else:
            # Línea no vacía: añadirla al bloque actual.
            bloque_actual.append(linea)

    # Al terminar, guardar el último bloque si existe.
    if bloque_actual:
        bloques.append("\n".join(bloque_actual).strip())

    return bloques


if __name__ == "__main__":
    chunks = crear_chunks()

    if not chunks:
        print("No se han encontrado chunks en la carpeta 'data/markdown_clean'.")
    else:
        print(f"Se han creado {len(chunks)} chunks.\n")

        for i, chunk in enumerate(chunks[:10], start=1):
            print(f"--- Chunk {i} ---")
            print(f"Sección: {chunk.seccion}")
            print(f"Documento: {chunk.documento_origen.nombre}")
            print(chunk.texto[:400])
            print("\n" + "=" * 80)