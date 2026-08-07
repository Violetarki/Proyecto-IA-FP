

from src.core.models import ResultadoBusqueda, Chunk
from src.core.config import UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MAXIMO_CHUNKS, MINIMO_CHUNKS
from src.rag.historial import Historial
from src.knowledge.loader import cargar_arbol
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

        chunks = self._añadir_padres(chunks)

        chunks = self._eliminar_duplicados(chunks)

        chunks = self._ordenar(chunks)

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

    def _añadir_padres(self):
        """
        Añade el nodo padre de cada chunk recuperado. El padre aporta contexto general. 
        Ej.: Si recuperamos Fortalezas(hijo), añadimos también DAFO(padre).
        """

    def _añadir_hermanos(self):
        """
        Añade los nodos que comparten el mismo padre. 
        Si preguntan por Fortalezas, puede ser útil que el modelo vea también las demás categorías.
        """

    def _añadir_hijos(self):
        """
        Añade los subapartados del chunk recuperado. 
        Permite ampliar una explicación general con detalles concretos.
        """

    def _eliminar_duplicados(self):
        """
        Evita que un mismo chunk aparezca varias veces. 
        Al añadir padres y hermanos es fácil repetir información.
        """


    def _obtener_nodo(self, node_id):
        """
        Obtiene un nodo del árbol a partir de su node_id. 
        Todos los demás métodos necesitan acceder al árbol. Es una función auxiliar para no repetir código.
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