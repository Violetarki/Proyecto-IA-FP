"""
Módulo encargado de recuperar los chunks más relevantes para una consulta.

El retriever representa la fase de recuperación de información del sistema
RAG.

Responsabilidades:
- Convertir la pregunta del usuario en un embedding.
- Consultar la base vectorial.
- Recuperar los chunks más similares.
- Aplicar los filtros necesarios (por ejemplo, metodología).

Este módulo desacopla el chatbot del sistema de almacenamiento vectorial.
"""
import re
import logging

from src.core.config import MINIMO_CHUNKS
from src.rag.embeddings import crear_embedding_texto
from src.rag.vector_store import VectorStore
from src.core.models import Chunk

logger = logging.getLogger(__name__)

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

class Retriever:
    """
    Recupera los chunks más relevantes para una consulta dada.
    """

    def __init__(self):
        self.vector_store = VectorStore()


    def _extraer_palabras_clave(
        self,
        pregunta: str,
    ) -> list[str]:

        """
        Extrae palabras clave de la pregunta del usuario.
        """
        palabras = re.findall(r"\w+", pregunta.lower())

        return [
            palabra
            for palabra in palabras
            if palabra not in STOPWORDS
        ]


    def _coincidencias(
        self,
        chunk: Chunk,
        palabras: list[str],
    ) -> int:
        """
        Cuenta cuántas palabras clave de la pregunta aparecen en el chunk.
        """
        texto = (" ".join(chunk.jerarquia_limpia()) + " " + chunk.texto).lower()

        return sum(
            bool(
                re.search(
                    rf"\b{re.escape(palabra)}\b",
                    texto,
                )
            )
            for palabra in palabras
        )


    def _filtrar_por_palabras_clave(
        self,
        pregunta: str,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        """
        Conserva únicamente los chunks que contienen suficientes palabras
        clave de la pregunta.

        Si el filtrado deja muy pocos resultados, se devuelven los originales.
        """

        palabras = self._extraer_palabras_clave(pregunta)

        if not palabras:
            return chunks

        if len(palabras) <= 3:
            minimo = len(palabras)
        else:
            minimo = 3

        filtrados = [
            chunk
            for chunk in chunks
            if self._coincidencias(chunk, palabras) >= minimo
        ]

        if len(filtrados) >= MINIMO_CHUNKS:
            return filtrados

        return chunks


    def recuperar_contexto(self,
        pregunta,
        metodologia,
        k=5,) -> list[Chunk]:
        """Recupera el contexto relevante para una pregunta dada.

        Esta función genera el embedding de la pregunta, consulta el almacén
        vectorial para obtener los chunks más relevantes y concatena sus
        textos en un solo bloque de contexto.

        Args:
            pregunta (str): Consulta del usuario cuya información de apoyo se desea recuperar.

        Returns:
            str: Texto combinado de los chunks recuperados, separado por saltos de línea.
        """

        chunks = self.recuperar_chunks(pregunta,metodologia, k)

        return chunks


    # función privada para validar los parámetros
    def recuperar_chunks(self,
        pregunta,
        metodologia,
        k):
        """Obtiene los chunks más relevantes para una consulta.

        Primero valida que la pregunta no esté vacía, luego crea el embedding de
        la pregunta y finalmente consulta el VectorStore para recuperar los chunks
        similares.

        Args:
            pregunta (str): Texto de la consulta del usuario.
            metodologia (): 
            k (int): Número de chunks a recuperar

        Returns:
            list: Lista de objetos chunk ordenados por relevancia.

        Raises:
            ValueError: Si la pregunta está vacía o contiene sólo espacios.
        """

        if not pregunta.strip():
            raise ValueError("La pregunta no puede estar vacía.")

        if k <= 0:
            raise ValueError(...)

        if not metodologia.strip():
            raise ValueError(...)

        embedding = crear_embedding_texto(pregunta)

        chunks = self.vector_store.buscar(embedding, metodologia, k)

        chunks = self._filtrar_por_palabras_clave(
            pregunta,
            chunks,
        )

        return chunks
