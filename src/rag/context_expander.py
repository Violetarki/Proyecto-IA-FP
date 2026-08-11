

from src.core.models import ResultadoBusqueda, Chunk
from src.core.config import UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MAXIMO_CHUNKS, MINIMO_CHUNKS, ESTRATEGIA_DEFAULT
from src.rag.historial import Historial
from src.knowledge.models import KnowledgeTree



class ContextExpander:

    def __init__(
        self,
        arbol: KnowledgeTree,
        historial: Historial
    ):
        self.arbol = arbol
        self.historial = historial



    def expandir(self, resultados: list[ResultadoBusqueda], estrategia: dict = None) -> list[Chunk]:

        estrategia = estrategia or ESTRATEGIA_DEFAULT

        candidatos = self._aplicar_umbrales(resultados, estrategia["umbral"])

        if estrategia.get("incluir_padres", True):
            candidatos = self._enriquecer_con_padres(candidatos)

        if estrategia.get("incluir_hermanos", False):
            candidatos = self._enriquecer_con_hermanos(candidatos)

        if estrategia.get("incluir_hijos", False):
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


    def _obtener_nodo(
        self,
        node_id: str,
    ):
        """
        Obtiene un nodo del árbol a partir de su node_id.

        Devuelve None si el nodo no existe.
        """

        return self._buscar_nodo(self.arbol.raiz, node_id)


    def _buscar_nodo(
        self,
        nodo,
        node_id: str,
    ):
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


# comentario de la chati: Con la restricción de "no traer chunks nuevos", esta función aporta muy poco valor. 
# Por eso quizá la función que más valor tenga en esta primera versión no sea la de padres, sino la de ordenación por jerarquía.
    def _enriquecer_con_padres(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Enriquece el contexto con los chunks del nodo padre que ya hayan sido
        recuperados por el Retriever.
        """

        resultado = chunks.copy()

        chunks_por_indice = {
            chunk.indice: chunk
            for chunk in chunks
        }

        for chunk in chunks:

            nodo = self._obtener_nodo(chunk.node_id)

            if nodo is None or nodo.padre is None:
                continue

            for chunk_id in nodo.padre.chunk_ids:

                chunk_padre = chunks_por_indice.get(chunk_id)

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

        chunks_por_indice = {
            chunk.indice: chunk
            for chunk in chunks
        }

        for chunk in chunks:
            nodo = self._obtener_nodo(chunk.node_id)

            if nodo is None or nodo.padre is None:
                continue

            for chunk_id in nodo.padre.chunk_ids:
                if chunk_id == chunk.indice:
                    continue

                chunk_hermano = chunks_por_indice.get(chunk_id)

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

        chunks_por_indice = {
            chunk.indice: chunk
            for chunk in chunks
        }

        for chunk in chunks:
            nodo = self._obtener_nodo(chunk.node_id)

            if nodo is None:
                continue

            for hijo in nodo.hijos:
                for chunk_id in hijo.chunk_ids:
                    if chunk_id == chunk.indice:
                        continue

                    chunk_hijo = chunks_por_indice.get(chunk_id)

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
            if chunk.indice in vistos:
                continue

            vistos.add(chunk.indice)
            resultado.append(chunk)

        return resultado


    def _ruta_nodo(self, nodo):
        """
        Obtiene la ruta jerárquica de un nodo dentro del árbol.
        """

        ruta = []

        while nodo is not None:
            ruta.append(nodo.nivel)
            nodo = nodo.padre

        return tuple(reversed(ruta))


    def _ordenar_por_jerarquia(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Ordena los chunks según su posición en el KnowledgeTree.
        """

        def clave(chunk: Chunk):
            nodo = self._obtener_nodo(chunk.node_id)

            if nodo is None:
                return (float("inf"),)

            ruta = []
            actual = nodo

            while actual.padre is not None:
                posicion = actual.padre.hijos.index(actual)
                ruta.append(posicion)
                actual = actual.padre

            ruta.append(0)

            return tuple(reversed(ruta))

        return sorted(chunks, key=clave)
