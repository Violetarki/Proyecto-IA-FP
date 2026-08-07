from src.core.models import ResultadoBusqueda
from src.knowledge.loader import cargar_arbol


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

# fc opcional por si queremos filtrar los chunks por metodología, por ejemplo, para que solo se devuelvan chunks de la metodología de la pregunta
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
