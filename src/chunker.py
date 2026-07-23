"""Se encarga de dividir un Documento en una lista de Chunk, 
procurando que cada uno represente una unidad coherente de conocimiento."""

from document_loader import leer_documentos
from models import Chunk

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
        # Mantener el estado del subtítulo actual y del título del chunk.
        subtitulo_actual: str | None = None
        contenido_seccion: list[str] = []
        titulo_actual: str | None = None

        # 4. Recorrer las líneas del documento.
        for linea in documento.texto.splitlines():
            linea_limpia = linea.strip()

            # Si la línea empieza por "###", la usamos como título del chunk.
            if linea_limpia.startswith("#"):
                # Si ya había contenido acumulado, guardamos el chunk anterior.
                if contenido_seccion:
                    texto_chunk = "\n".join(contenido_seccion).strip()
                    if texto_chunk:
                        chunks.append(
                            Chunk(
                                documento=documento,
                                indice=len(chunks),
                                titulo=titulo_actual,
                                subtitulo=subtitulo_actual,
                                texto=texto_chunk,
                            )
                        )
                    contenido_seccion = []

                # El nuevo título del siguiente chunk se toma de esta línea.
                titulo_actual = linea_limpia.lstrip("#").strip()

            # Si la línea empieza por "##", significa que empieza una nueva
            # sección. Antes de cambiar de sección, guardamos la anterior.
            elif linea_limpia.startswith("##"):
                if contenido_seccion:
                    texto_chunk = "\n".join(contenido_seccion).strip()
                    if texto_chunk:
                        chunks.append(
                            Chunk(
                                documento=documento,
                                indice=len(chunks),
                                titulo=titulo_actual,
                                subtitulo=subtitulo_actual,
                                texto=texto_chunk,
                            )
                        )
                    contenido_seccion = []

                # Iniciar el nuevo subtítulo con el texto del encabezado.
                subtitulo_actual = linea_limpia.lstrip("#").strip()
            else:
                # Si no es un encabezado, se añade al contenido actual.
                if linea_limpia:
                    contenido_seccion.append(linea_limpia)
                elif contenido_seccion:
                    # Mantener separación entre párrafos cuando haya líneas vacías.
                    contenido_seccion.append("")

        # 5. Guardar la última sección del documento cuando termine el recorrido.
        if contenido_seccion:
            texto_chunk = "\n".join(contenido_seccion).strip()
            if texto_chunk:
                chunks.append(
                    Chunk(
                        documento=documento,
                        indice=len(chunks),
                        titulo=titulo_actual,
                        subtitulo=subtitulo_actual,
                        texto=texto_chunk,
                    )
                )

    # 6. Devolver la lista completa de chunks generados.
    return chunks


if __name__ == "__main__":
    chunks = crear_chunks()

    if not chunks:
        print("No se han encontrado chunks en la carpeta 'data/markdown_clean'.")
    else:
        print(f"Se han creado {len(chunks)} chunks.\n")

        for i, chunk in enumerate(chunks[:10], start=1):
            print(f"--- Chunk {i} ---")
            print(f"Título: {chunk.titulo}")
            print(f"Subtítulo: {chunk.subtitulo}")
            print(f"Documento: {chunk.documento.nombre}")
            print(chunk.texto[:400])
            print("\n" + "=" * 80)