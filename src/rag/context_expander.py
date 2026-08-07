

from src.core.models import ResultadoBusqueda
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




    # fc opcional por si queremos filtrar los chunks por metodología, por ejemplo, 
    # para que solo se devuelvan chunks de la metodología de la pregunta
    def _filtrar_chunks(
            self,
            documentos,
            metadatos,
            distancias,
        ):
            resultados = []

            for texto, metadata, distancia in zip(
                documentos,
                metadatos,
                distancias
            ):

                resultados.append(
                    (
                        self._chunk_desde_resultado(
                            texto,
                            metadata,
                        ),
                        distancia,
                    )
                )

            excelentes = [
                chunk
                for chunk, distancia in resultados
                if distancia <= UMBRAL_EXCELENTE
            ]

            if len(excelentes) >= MINIMO_CHUNKS:
                return excelentes[:MAXIMO_CHUNKS]

            buenos = [
                chunk for chunk, distancia in resultados if distancia <= UMBRAL_BUENO
            ]

            if len(buenos) >= MINIMO_CHUNKS:
                return buenos[:MAXIMO_CHUNKS]

            aceptables = [
                chunk
                for chunk, distancia in resultados
                if distancia <= UMBRAL_ACEPTABLE
            ]

            return aceptables[:MAXIMO_CHUNKS]
