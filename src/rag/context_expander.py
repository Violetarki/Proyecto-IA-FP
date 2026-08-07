

from src.core.models import ResultadoBusqueda, Chunk
from src.core.config import UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MAXIMO_CHUNKS, MINIMO_CHUNKS
from src.rag.historial import Historial
from src.knowledge.loader import cargar_arbol
from src.knowledge.models import KnowledgeTree


STOPWORDS = {
    "que",
    "qué",
    "como",
    "cómo",
    "es",
    "son",
    "el",
    "la",
    "los",
    "las",
    "un",
    "una",
    "de",
    "del",
    "y",
    "o",
    "en",
    "con",
    "para",
    "por",
    "cuál",
    "cuáles",
    "cual",
    "cuales",
    "se",
    "al",
    "a",
}

# recibe esto de vector_Store:
resultados: list[ResultadoBusqueda]


class ContextExpander:

    def __init__(
        self,
        arbol: KnowledgeTree,
        historial: Historial
    ):
        self.arbol = arbol
        self.historial = historial



    def expandir(self, chunks):

        chunks = self._aplicar_umbrales(chunks)

        chunks = self._añadir_padres(chunks)

        chunks = self._añadir_hermanos(chunks)

        chunks = self._añadir_contexto_historial(chunks)

        return self._ordenar(chunks)



    def _buscar_padre(self, nodo):
        ...


    def _buscar_hermanos(self, nodo):
        ...



    def _obtener_nodo(self, node_id):
        ...



    def _ordenar_por_jerarquia(self, chunks):
        ...



    def _filtrar_chunks(
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