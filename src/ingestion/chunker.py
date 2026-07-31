"""Version mas nueva de chunker.py

Se encarga de dividir un Documento en una lista de Chunk,
procurando que cada uno represente una unidad coherente de conocimiento.
 
Reglas de división:
- El nivel 1 (#) nunca genera un chunk propio; únicamente identifica el
  módulo o unidad y se almacena como contexto del resto de chunks.
- Los niveles 2, 3 y 4 (##, ###, ####) generan un chunk únicamente cuando
  contienen texto propio (con independencia de que además tengan hijos,
  que generarán sus propios chunks por separado).
- Si un encabezado no contiene texto propio, actúa únicamente como nodo
  de la jerarquía y proporciona contexto a sus descendientes, sin generar
  chunk.
- Cada chunk guarda, según hasta qué nivel llegue su ruta:
    titulo      -> header de nivel 1 (módulo)
    subtitulo   -> header de nivel 2, si existe en la ruta
    seccion     -> header de nivel 3, si existe en la ruta
    subseccion  -> header de nivel 4, si existe en la ruta
"""

import re
import logging

from src.core.models import Chunk, Documento

_HEADER_RE = re.compile(r"^(#{1,4})\s+(.*)")

logger = logging.getLogger(__name__)

# Relación entre el nivel del encabezado Markdown y el atributo
# correspondiente del modelo Chunk.
_CAMPO_POR_NIVEL = {
    1: "titulo",
    2: "subtitulo",
    3: "seccion",
    4: "subseccion",
}


class _Nodo:
    """Nodo interno del árbol de encabezados. No se expone fuera del módulo."""

    __slots__ = ("nivel", "titulo", "lineas", "hijos")

    def __init__(self, nivel: int, titulo: str | None):
        self.nivel = nivel
        self.titulo = titulo
        self.lineas: list[str] = []
        self.hijos: list["_Nodo"] = []
        
    @property
    def texto(self) -> str:
        """Devuelve el contenido del nodo como un único texto."""
        return "\n".join(self.lineas).strip()


def _parsear_arbol(texto: str) -> _Nodo:
    """Construye el árbol de encabezados a partir del texto de un Documento."""

    raiz = _Nodo(nivel=0, titulo=None)
    pila: list[_Nodo] = [raiz]

    for linea in texto.splitlines():
        linea_limpia = linea.strip()
        match = _HEADER_RE.match(linea_limpia)

        if match:
            nivel = len(match.group(1))
            titulo = match.group(2).strip()

            # Desapilar hasta encontrar el padre correcto (nivel estrictamente menor)
            while pila[-1].nivel >= nivel:
                pila.pop()

            nuevo = _Nodo(nivel=nivel, titulo=titulo)
            pila[-1].hijos.append(nuevo)
            pila.append(nuevo)
        else:
            if linea_limpia:
                pila[-1].lineas.append(linea_limpia)
            elif pila[-1].lineas:
                pila[-1].lineas.append("")

    return raiz


def _guardar_chunk(
    chunks: list[Chunk],
    documento: Documento,
    indice: int,
    contexto: dict[str, str | None],
    texto: str,
) -> int:
    """
    Crea un Chunk a partir del texto del nodo y lo añade a la lista,
    si contiene contenido.

    Args:
        chunks: Lista donde se almacenan los chunks generados.
        documento: Documento al que pertenece el chunk.
        indice: Posición del chunk dentro del documento.
        contexto: Diccionario con titulo/subtitulo/seccion/subseccion ya resueltos.
        texto: Texto del nodo (ya venido de la property nodo.texto).

    Returns:
        El siguiente índice disponible.
    """

    if texto:
        chunks.append(
            Chunk(
                documento=documento,
                indice=indice,
                texto=texto,
                titulo=contexto.get("titulo"),
                subtitulo=contexto.get("subtitulo"),
                seccion=contexto.get("seccion"),
                subseccion=contexto.get("subseccion"),
            )
        )
        indice += 1

    return indice


def _generar_chunks(
    nodo: _Nodo,
    documento: Documento,
    contexto: dict[str, str | None],
    chunks: list[Chunk],
    indice: int,
) -> int:
    """
    Recorre el árbol de encabezados generando un Chunk para cada nodo
    de nivel 2 o superior que contenga texto propio, propagando el
    contexto jerárquico (titulo, subtitulo, seccion y subseccion).
    """

    nuevo_contexto = contexto
    campo = _CAMPO_POR_NIVEL.get(nodo.nivel)

    if campo is not None and nodo.titulo is not None:
        nuevo_contexto = contexto.copy()
        nuevo_contexto[campo] = nodo.titulo

        # Si este nodo es, p.ej., un nuevo subtitulo (##), los niveles más
        # profundos que aún no se han visto (seccion, subseccion) deben
        # limpiarse para no arrastrar los de una rama anterior del árbol.
        for nivel_mayor, campo_mayor in _CAMPO_POR_NIVEL.items():
            if nivel_mayor > nodo.nivel:
                nuevo_contexto[campo_mayor] = None

    # Texto suelto antes de cualquier header (nivel 0): siempre se guarda aparte
    if nodo.nivel == 0:
        indice = _guardar_chunk(chunks, documento, indice, {}, nodo.texto)

    # Nivel 1: nunca genera chunk propio, solo aporta contexto (ya hecho arriba)
    elif nodo.nivel == 1:
        pass

    # Niveles 2, 3 y 4: generan chunk solo si tienen texto propio
    else:
        indice = _guardar_chunk(chunks, documento, indice, nuevo_contexto, nodo.texto)

    # Los hijos siempre se procesan aparte, generen o no chunk propio el padre
    for hijo in nodo.hijos:
        indice = _generar_chunks(hijo, documento, nuevo_contexto, chunks, indice)

    return indice


def crear_chunks_documento(documento: Documento) -> list[Chunk]:
    """
    Divide un Documento en una lista de Chunk utilizando los encabezados
    Markdown como separadores de secciones, respetando la jerarquía:
    el nivel 1 se guarda como módulo/contexto y los headers (a partir del nivel 2) generan chunks si tienen texto propio.

    Args:
        documento: Documento que se desea fragmentar.

    Returns:
        Lista de chunks pertenecientes al documento.
    """

    arbol = _parsear_arbol(documento.texto)

    chunks: list[Chunk] = []
    contexto_inicial: dict[str, str | None] = {
        "titulo": None,
        "subtitulo": None,
        "seccion": None,
        "subseccion": None,
    }

    _generar_chunks(
        arbol,
        documento=documento,
        contexto=contexto_inicial,
        chunks=chunks,
        indice=0,
    )

    return chunks


def crear_chunks_documentos(documentos: list[Documento]) -> list[Chunk]:
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

    logger.info("Este módulo proporciona funciones para dividir " "Documentos en Chunks.")

    from pathlib import Path

    from src.core.models import Documento, Metodologia

    ruta = Path("data/markdown_clean/lean_startup/lean_startup.md")

    documento = Documento(
        metodologia=Metodologia(nombre="Lean Startup"),
        nombre="lean_startup",
        texto=ruta.read_text(encoding="utf-8"),
        ruta=ruta,
    )

    chunks = crear_chunks_documento(documento)

    logger.debug("Se han generado %d chunks.\n", len(chunks))

    for chunk in chunks[:20]:  # Mostrar solo los 20 primeros

        logger.debug("%s", "=" * 80)
        logger.debug("Chunk %s", chunk.indice)
        logger.debug("Título:      %s", chunk.titulo)
        logger.debug("Subtítulo:   %s", chunk.subtitulo)
        logger.debug("Sección:     %s", chunk.seccion)
        logger.debug("Subsección:  %s", chunk.subseccion)
        logger.debug("%s", "-" * 80)
        logger.debug("%s", chunk.texto)
        logger.debug("")
