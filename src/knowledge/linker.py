from src.core.limpiar_encabezados import limpiar_encabezado
from src.knowledge.models import KnowledgeTree, KnowledgeNode
from src.core.models import Chunk


def enlazar(arbol: KnowledgeTree, chunks: list[Chunk]) -> None:
    """
    Enlaza los chunks con los nodos del árbol de conocimiento.

    Para cada chunk, localiza el KnowledgeNode al que pertenece según
    su ruta jerárquica (titulo, subtitulo, seccion, etc.) y establece
    la relación entre ambos.

    Args:
        arbol: Árbol de conocimiento del documento.
        chunks: Lista de chunks generados a partir del mismo documento.
    """

    for chunk in chunks:
        nodo = _buscar_nodo(arbol, chunk)
        _enlazar_chunk_nodo(chunk, nodo)


def _obtener_ruta(chunk: Chunk) -> list[str]:
    """
    Obtiene la ruta jerárquica asociada a un chunk.

    La ruta está formada por los encabezados del documento, desde el
    título principal hasta el nivel más específico al que pertenezca
    el chunk, omitiendo los niveles inexistentes.

    Args:
        chunk: Chunk del que se desea obtener la ruta.

    Returns:
        Lista con la ruta jerárquica del chunk.
    """

    return [
        nivel
        for nivel in (
            chunk.titulo,
            chunk.subtitulo,
            chunk.seccion,
            chunk.subseccion,
            chunk.apartado,
        )
        if nivel is not None
    ]


def _buscar_nodo(
    arbol: KnowledgeTree,
    chunk: Chunk,
) -> KnowledgeNode:

    nodo = arbol.raiz

    for nombre in _obtener_ruta(chunk):
        nodo = _buscar_hijo(nodo, nombre)

        if nodo is None:
            raise ValueError(
                f"No se encontró el nodo '{nombre}' "
                f"para el chunk {chunk.indice}"
            )

    return nodo


def _buscar_hijo(
    nodo: KnowledgeNode,
    titulo: str,
) -> KnowledgeNode | None:
    """
    Devuelve el hijo cuyo título coincide con el indicado.
    """

    for hijo in nodo.hijos:
        if limpiar_encabezado(hijo.titulo) == limpiar_encabezado(titulo):
            return hijo

    return None


def _enlazar_chunk_nodo(
    chunk: Chunk,
    nodo: KnowledgeNode,
) -> None:
    """
    Establece la relación entre un chunk y un nodo del árbol.

    Actualiza el chunk con el identificador del nodo y registra el chunk
    dentro del nodo correspondiente.

    Args:
        chunk: Chunk que se desea enlazar.
        nodo: Nodo del árbol al que pertenece el chunk.
    """

    chunk.node_id = nodo.id
    nodo.chunk_ids.append(chunk.indice)
