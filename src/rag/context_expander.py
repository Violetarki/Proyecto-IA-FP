"""
Módulo encargado de expandir y organizar el contexto recuperado.

A partir de los resultados de la búsqueda, selecciona los chunks
según sus umbrales de relevancia y puede enriquecer el contexto
utilizando las relaciones jerárquicas del KnowledgeTree.

También elimina duplicados y ordena los chunks según su posición
dentro de la jerarquía de conocimiento.
"""

from src.core.models import IntentResult, ResultadoBusqueda, Chunk
from src.core.config import UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MAXIMO_CHUNKS, MINIMO_CHUNKS
from src.rag.historial import Historial
from src.knowledge.models import KnowledgeNode, KnowledgeTree


class ContextExpander:

    """
    Expande y organiza los chunks recuperados utilizando
    la estructura jerárquica del KnowledgeTree.
    """

    def __init__(
        self, 
        arboles: dict[str, KnowledgeTree], 
        historial: Historial,
        ):
        """
        Inicializa el expandidor de contexto con los árboles de conocimiento y el historial.
        """
        self.arboles = arboles
        self.historial = historial

    def expandir(
        self,
        resultados: list[ResultadoBusqueda],
        intencion: IntentResult,
    ) -> list[Chunk]:

        candidatos = self._aplicar_umbrales(resultados)

        candidatos = self._enriquecer_con_padres(candidatos)

        candidatos = self._enriquecer_con_hermanos(candidatos)

        candidatos = self._enriquecer_con_hijos(candidatos)

        candidatos = self._eliminar_duplicados(candidatos)

        return self._ordenar_por_jerarquia(candidatos)

    def _aplicar_umbrales(
        self,
        resultados: list[ResultadoBusqueda],
    ) -> list[Chunk]:
        """
        Filtra los chunks recuperados según su relevancia.

        Prioriza chunks excelentes. Si no hay suficientes,
        amplía progresivamente el umbral de aceptación.
        """

        excelentes = [
            resultado.chunk
            for resultado in resultados
                if resultado.distancia <= UMBRAL_EXCELENTE
        ]

        if len(excelentes) >= MINIMO_CHUNKS:
            return excelentes[:MAXIMO_CHUNKS]

        buenos = [
            resultado.chunk
            for resultado in resultados
                if resultado.distancia <= UMBRAL_BUENO
        ]

        if len(buenos) >= MINIMO_CHUNKS:
            return buenos[:MAXIMO_CHUNKS]

        aceptables = [
            resultado.chunk
            for resultado in resultados
                if resultado.distancia <= UMBRAL_ACEPTABLE
        ]

        return aceptables[:MAXIMO_CHUNKS]

    def _obtener_arbol(
        self,
        chunk: Chunk,
    ) -> KnowledgeTree | None:

        return self.arboles.get(
            chunk.documento.nombre
        )

    def _clave_chunk(
        self, 
        chunk: Chunk,
        ) -> tuple[str, int]:
        
        return (
            chunk.documento.ruta,
            chunk.indice,
        )
        

    def _clave_chunk_id(
        self,
        chunk: Chunk,
        chunk_id: int,
    ) -> tuple[str, int]:

        return (
            chunk.documento.ruta,
            chunk_id,
        )
        

    def _obtener_nodo(
        self,
        chunk: Chunk,
    ) -> KnowledgeNode | None:

        arbol = self._obtener_arbol(chunk)

        if arbol is None or chunk.node_id is None:
            return None

        return self._buscar_nodo(
            arbol.raiz,
            chunk.node_id,
        )
        

    def _buscar_nodo(
        self,
        nodo: KnowledgeNode,
        node_id: str,
    ) -> KnowledgeNode | None:
        """
        Busca recursivamente un nodo del árbol a partir de su identificador.

        Recorre el nodo actual y sus descendientes hasta encontrar
        el nodo con el `node_id` indicado. Devuelve None si no existe.
        """

        if nodo.id == node_id:
            return nodo

        for hijo in nodo.hijos:
            encontrado = self._buscar_nodo(hijo, node_id)
            if encontrado is not None:
                return encontrado

        return None

    def _enriquecer_con_padres(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Enriquece el contexto con los chunks del nodo padre que ya hayan sido
        recuperados por el Retriever.
        """

        resultado = chunks.copy()

        chunks_por_clave = {self._clave_chunk(chunk): chunk for chunk in chunks}

        for chunk in chunks:

            nodo = self._obtener_nodo(chunk)

            if nodo is None or nodo.padre is None:
                continue

            for chunk_id in nodo.padre.chunk_ids:

                clave = self._clave_chunk_id(
                    chunk,
                    chunk_id,
                )

                chunk_padre = chunks_por_clave.get(clave)

                if chunk_padre is not None:
                    resultado.append(chunk_padre)

        return resultado

    def _enriquecer_con_hermanos(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Enriquece el contexto con los chunks hermanos que ya hayan sido
        recuperados por el Retriever.
        """

        resultado = chunks.copy()

        chunks_por_clave = {self._clave_chunk(chunk): chunk for chunk in chunks}

        for chunk in chunks:
            nodo = self._obtener_nodo(chunk)
            if nodo is None or nodo.padre is None:
                continue

            for chunk_id in nodo.padre.chunk_ids:
                if chunk_id == chunk.indice:
                    continue

                clave = self._clave_chunk_id(chunk, chunk_id)

                chunk_hermano = chunks_por_clave.get(clave)

                if chunk_hermano is not None:
                    resultado.append(chunk_hermano)

        return resultado

    def _enriquecer_con_hijos(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Enriquece el contexto con los chunks hijos que ya hayan sido
        recuperados por el Retriever.
        """

        resultado = chunks.copy()

        chunks_por_clave = {self._clave_chunk(chunk): chunk for chunk in chunks}

        for chunk in chunks:
            nodo = self._obtener_nodo(chunk)
            if nodo is None:
                continue

            for hijo in nodo.hijos:
                for chunk_id in hijo.chunk_ids:
                    if chunk_id == chunk.indice:
                        continue

                    clave = self._clave_chunk_id(chunk, chunk_id)

                    chunk_hijo = chunks_por_clave.get(clave)

                    if chunk_hijo is not None:
                        resultado.append(chunk_hijo)

        return resultado

    def _eliminar_duplicados(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Elimina los chunks duplicados conservando el orden original.
        """

        vistos = set()
        resultado = []

        for chunk in chunks:

            clave = (
                chunk.documento.ruta,
                chunk.indice,
            )

            if clave in vistos:
                continue

            vistos.add(clave)
            resultado.append(chunk)

        return resultado

    def _ruta_nodo(
        self,
        nodo: KnowledgeNode,
    ) -> tuple[int, ...]:

        ruta = []

        while nodo.padre is not None:
            posicion = nodo.padre.hijos.index(nodo)
            ruta.append(posicion)
            nodo = nodo.padre

        ruta.append(0)

        return tuple(reversed(ruta))
    
    
    def _ordenar_por_jerarquia(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        def clave(chunk: Chunk):
            nodo = self._obtener_nodo(chunk)

            if nodo is None:
                return (float("inf"),)

            return self._ruta_nodo(nodo)

        return sorted(chunks, key=clave)
