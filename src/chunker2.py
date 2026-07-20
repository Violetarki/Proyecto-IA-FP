from models import Document, Chunk


MAX_CHUNK_SIZE = 1000


def chunk_document(document: Document) -> list[Chunk]:
    """
    Divide un Documento en una lista de Chunk procurando que cada uno
    represente una unidad coherente de conocimiento.
    """

    chunks = []

    seccion_actual = None
    texto_actual = []
    pagina_inicio = None
    pagina_fin = None

    for elemento in document.content:

        # Si encontramos un título, actualizamos la sección
        if es_titulo(elemento):
            seccion_actual = elemento.text
            continue

        # Si es el primer párrafo del chunk
        if pagina_inicio is None:
            pagina_inicio = elemento.page

        texto_actual.append(elemento.text)
        pagina_fin = elemento.page

        # Si el chunk ha alcanzado el tamaño máximo,
        # lo cerramos y comenzamos uno nuevo.
        if supera_tamano(texto_actual):

            chunks.append(
                crear_chunk(
                    texto_actual,
                    pagina_inicio,
                    pagina_fin,
                    seccion_actual,
                )
            )

            texto_actual = []
            pagina_inicio = None
            pagina_fin = None

    # Añadir el último chunk si queda texto pendiente
    if texto_actual:
        chunks.append(
            crear_chunk(
                texto_actual,
                pagina_inicio,
                pagina_fin,
                seccion_actual,
            )
        )

    return chunks


def crear_chunk(
    texto: list[str],
    pagina_inicio: int,
    pagina_fin: int,
    seccion: str | None,
) -> Chunk:

    return Chunk(
        text="\n".join(texto),
        page_start=pagina_inicio,
        page_end=pagina_fin,
        section=seccion,
    )

def es_titulo(elemento) -> bool:
    """
    Determina si un elemento corresponde a un título.
    """
    ...


def supera_tamano(texto: list[str]) -> bool:
    """
    Comprueba si el texto acumulado supera el tamaño máximo.
    """
    return len("\n".join(texto)) >= MAX_CHUNK_SIZE



"""

seccion_actual = None

↓

Leo un elemento

↓

¿Es un título?

Sí
    seccion_actual = ese título
    sigo leyendo

No
    lo añado al chunk actual

↓

¿El chunk ya es suficientemente grande?

No
    sigo leyendo

Sí
    creo el Chunk usando la sección_actual
    empiezo otro

"""