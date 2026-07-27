"""
Módulo encargado de gestionar la base de datos vectorial del proyecto.

Este módulo encapsula completamente el acceso a ChromaDB para que el
resto de la aplicación no dependa de una tecnología concreta.

Responsabilidades:
- Crear o abrir la colección vectorial.
- Indexar chunks junto con sus embeddings.
- Recuperar los chunks más similares a una consulta.
- Eliminar los chunks asociados a un documento.
- Vaciar la colección.

Si en el futuro se sustituye ChromaDB por otra base vectorial
(Azure AI Search, Pinecone, Weaviate, etc.), únicamente será
necesario modificar este módulo.
"""

import chromadb
import numpy as np
from pathlib import Path
from src.models import Chunk, Documento, Metodologia
from src.config import CARPETA_VECTOR_STORE

class VectorStore:
    """
    Gestiona el almacenamiento y recuperación de embeddings mediante
    una base de datos vectorial.

    Actualmente utiliza ChromaDB como implementación, aunque el resto
    de la aplicación no necesita conocer este detalle.
    """

    def __init__(
        self,
        collection_name: str = "chunks",
        persist_directory: str | Path = CARPETA_VECTOR_STORE,
    ) -> None:
        """
        Inicializa la conexión con la base vectorial.

        Si la colección no existe, se crea automáticamente.

        Args:
            collection_name: Nombre de la colección.
            persist_directory: Directorio donde se almacenan los datos.
        """

        self.client = chromadb.PersistentClient(path=persist_directory)

        self.collection = self.client.get_or_create_collection(name=collection_name)

    def _crear_id(
    self,
    chunk: Chunk,
    ) -> str:
        """
        Genera un identificador único para un chunk.
        """

        return f"{chunk.documento.ruta}:{chunk.indice}"

    def _preparar_registro(
        self,
        chunk: Chunk,
        embedding: np.ndarray,
    ) -> tuple[str, str, list[float], dict]:
        """
        Convierte un Chunk en un registro compatible con ChromaDB.

        Args:
            chunk: Chunk que se va a indexar.
            embedding: Embedding asociado al chunk.

        Returns:
            Una tupla con:
                - id único.
                - texto del chunk.
                - embedding como lista.
                - metadatos.
        """

        metadata = {
            "metodologia": chunk.documento.metodologia.nombre,
            "documento": chunk.documento.nombre,
            "ruta": chunk.documento.ruta,
            "indice": chunk.indice,
        }

        if chunk.titulo:
            metadata["titulo"] = chunk.titulo

        if chunk.subtitulo:
            metadata["subtitulo"] = chunk.subtitulo

        return (
            self._crear_id(chunk),
            chunk.texto,
            embedding.tolist(),
            metadata,
        )

    def _chunk_desde_resultado(
        self,
        texto: str,
        metadata: dict[str, str | int],
    ) -> Chunk:
        """
        Reconstruye un objeto Chunk a partir de un resultado de ChromaDB.

        Args:
            texto: Texto almacenado.
            metadata: Metadatos asociados al chunk.

        Returns:
            Chunk reconstruido.
        """

        documento = Documento(
            metodologia=Metodologia(nombre=metadata.get("metodologia", "")),
            nombre=metadata.get("documento", ""),
            texto=texto,
            ruta=metadata.get("ruta", ""),
        )

        return Chunk(
            documento=documento,
            indice=int(metadata.get("indice", 0)),
            texto=texto,
            titulo=metadata.get("titulo"),
            subtitulo=metadata.get("subtitulo"),
        )

    def indexar_chunks(
        self,
        chunks: list[Chunk],
        embeddings: np.ndarray,
    ) -> None:
        """
        Indexa una lista de chunks junto con sus embeddings.

        El orden de los embeddings debe coincidir con el orden de los
        chunks.

        Args:
            chunks: Chunks que se desean indexar.
            embeddings: Matriz de embeddings correspondiente.

        Raises:
            ValueError: Si el número de chunks y embeddings no coincide.
        """

        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError("El número de chunks y embeddings debe coincidir.")

        ids = []
        documentos = []
        vectores = []
        metadatos = []

        for chunk, embedding in zip(chunks, embeddings):

            (
                id_,
                texto,
                vector,
                metadata,
            ) = self._preparar_registro(
                chunk,
                embedding,
            )

            ids.append(id_)
            documentos.append(texto)
            vectores.append(vector)
            metadatos.append(metadata)

        self.collection.add(
            ids=ids,
            documents=documentos,
            embeddings=vectores,
            metadatas=metadatos,
        )

    def buscar(
        self,
        embedding: np.ndarray,
        metodologia,
        k,
    ) -> list[Chunk]:
        """
        Recupera los chunks más similares a un embedding.

        Args:
            embedding: Embedding de la consulta.
            k: Número máximo de resultados.

        Returns:
            Lista de chunks ordenados por similitud.
        """

        if embedding.size == 0:
            return []

        if k <= 0:
            raise ValueError("El número de resultados debe ser mayor que cero.")

        resultado = self.collection.query(
            query_embeddings=[embedding.tolist()],
            where={"metadatas.metodologia": metodologia},
            n_results=k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        distancias = resultado["distances"][0]
        documentos = resultado["documents"][0]
        metadatos = resultado["metadatas"][0]

        return [
            self._chunk_desde_resultado(
                texto,
                metadata,
                distancia,
            )
            for texto, metadata, distancia in zip(
                documentos,
                metadatos,
                distancias,
            )
        ]

    def eliminar_documento(
        self,
        documento: Documento,
    ) -> None:
        """
        Elimina todos los chunks pertenecientes a un documento.

        Args:
            documento: Documento que se desea eliminar.
        """

        self.collection.delete(
            where={
                "$and": [
                    {"documento": documento.nombre},
                    {"ruta": documento.ruta},
                ]
            }
        )

    def vaciar(self) -> None:
        """
        Elimina todos los registros de la colección.
        """

        total = self.collection.count()

        if total == 0:
            return

        resultado = self.collection.get()

        ids = resultado["ids"]

        if ids:
            self.collection.delete(ids=ids)


if __name__ == "__main__":

    print("VectorStore: módulo de acceso a la base de datos vectorial.")
