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

from src.embeddings import crear_embedding_texto
from src.vector_store import VectorStore
from src.models import Chunk


class Retriever:
    """
    Recupera los chunks más relevantes para una consulta dada.
    """

    def __init__(self):
        self.vector_store = VectorStore()


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

        return chunks

