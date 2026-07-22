import chromadb
from models import Chunk, Documento, Metodologia


print(chromadb.__version__)



class VectorStore:
    """
     Gestiona la base vectorial mediante ChromaDB.
    """

    def __init__(
        self,
        collection_name: str = "chunks",
        persist_directory: str = "./data/vector_store"
        ):
        """
        Conecta con Chroma y crea la colección si no existe.
        """

        cliente = chromadb.PersistentClient(path=persist_directory)
        self.collection = cliente.create_collection(
            name=collection_name,
            get_or_create=True,
        )



    def guardar_chunks(self, chunks: list[Chunk]) -> None:
        """
        Guarda una lista de chunks en la colección de ChromaDB.

        Cada chunk se convierte en un elemento del vector store con:
            - ids
            - textos
            - embeddings
            - metadatos
        """

        if not chunks:
            return

        ids: list[str] = []
        textos: list[str] = []
        embeddings: list[list[float]] = []
        metadatos: list[dict] = []

        for chunk in chunks:
            if not hasattr(chunk, "embedding"):
                raise AttributeError(
                    "Cada chunk debe tener el atributo 'embedding'."
                )

            ids.append(
                f"{chunk.document.ruta}:{chunk.indice}"
            )
            textos.append(chunk.texto)
            embeddings.append(chunk.embedding)

            metadata = {
                "documento": chunk.document.nombre,
                "ruta": chunk.document.ruta,
                "indice": chunk.indice,
            }

            if chunk.titulo is not None:
                metadata["titulo"] = chunk.titulo
            if chunk.subtitulo is not None:
                metadata["subtitulo"] = chunk.subtitulo

            metadatos.append(metadata)

        self.collection.add(
            ids=ids,
            documents=textos,
            embeddings=embeddings,
            metadatas=metadatos,
        )



    def buscar(
            self,
            embedding: list[float],
            k: int = 5
        ) -> list[Chunk]:

        """
        Busca los chunks más similares en la colección ChromaDB.

        Args:
            embedding: Embedding de la consulta.
            k: Número de resultados a devolver.

        Returns:
            Lista de chunks ordenada por similitud.
        """

        if not embedding:
            return []

        resultado = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["documents", "metadatas"],
        )

        documentos = resultado.get("documents", [[]])[0]
        metadatas = resultado.get("metadatas", [[]])[0]

        chunks: list[Chunk] = []

        for texto, metadata in zip(documentos, metadatas):
            metodologia_nombre = metadata.get("metodologia", "")
            documento = Documento(
                metodologia=Metodologia(nombre=metodologia_nombre),
                nombre=metadata.get("documento", ""),
                texto=texto,
                ruta=metadata.get("ruta", ""),
            )

            chunks.append(
                Chunk(
                    documento=documento,
                    indice=int(metadata.get("indice", 0)),
                    texto=texto,
                    titulo=metadata.get("titulo"),
                    subtitulo=metadata.get("subtitulo"),
                )
            )

        return chunks



    def eliminar_documento(self, documento: Documento) -> None:
        """
        Elimina todos los chunks asociados a un documento de la colección.
        """

        if documento is None:
            return

        self.collection.delete(
            where={
                "documento": documento.nombre,
                "ruta": documento.ruta,
            }
        )



    def vaciar(self):
        """
        Eliminar todos los registros
        de la colección. útil durante el desarrollo y las pruebas
        """