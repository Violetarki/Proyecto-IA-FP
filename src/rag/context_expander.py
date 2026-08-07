

from src.core.models import ResultadoBusqueda, Chunk
from src.core.config import UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MAXIMO_CHUNKS, MINIMO_CHUNKS
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



    def expandir(
        self,
        candidatos: list[ResultadoBusqueda],
    ) -> list[Chunk]:

        chunks = self._aplicar_umbrales(candidatos)

        chunks = self._enriquecer_con_padres(chunks)

        chunks = self._eliminar_duplicados(chunks)

        chunks = self._ordenar_por_jerarquia(chunks)

        return chunks



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
        if nodo.id == node_id:
            return nodo

        for hijo in nodo.hijos:
            encontrado = self._buscar_nodo(hijo, node_id)
            if encontrado is not None:
                return encontrado

        return None


# comentario de la chati: Con la restricción de "no traer chunks nuevos", esta función aporta muy poco valor. Por eso quizá la función que más valor tenga en esta primera versión no sea la de padres, sino la de ordenación por jerarquía.
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

    def _enriquecer_con_hermanos(self):
        """
        Añade los nodos que comparten el mismo padre. 
        Si preguntan por Fortalezas, puede ser útil que el modelo vea también las demás categorías.
        """

    def _enriquecer_con_hijos(self):
        """
        Añade los subapartados del chunk recuperado. 
        Permite ampliar una explicación general con detalles concretos.
        """

    def _eliminar_duplicados(self):
        """
        Evita que un mismo chunk aparezca varias veces. 
        Al añadir padres y hermanos es fácil repetir información.
        """


    def _ordenar_por_jerarquia(self, chunks):
        """
        Ordena los chunks antes de enviarlos al LLM. El modelo entiende mejor un documento cuando mantiene el orden original.
        """



    def _aplicar_umbrales(
        self,
        resultados: list[ResultadoBusqueda],
    ) -> list[Chunk]:
        """
        Filtra los chunks recuperados según su relevancia.

        Se priorizan los chunks con mejor similitud.
        Si no hay suficientes resultados excelentes,
        se amplía progresivamente el umbral de aceptación.
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