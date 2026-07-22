import chromadb
from models import Chunk, Documento


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
            embedding: list[float],
            k: int = 5
        ) -> list[Chunk]:

        """

        Embedding de la pregunta
                │
                ▼
        Consultar ChromaDB
                │
                ▼
        Obtener los k resultados más similares
                │
                ▼
        Convertir cada resultado en un Chunk
                │
                ▼
        Devolver list[Chunk]

        
        k es el número de chunks que queremos devolver, así es dinámico, se puede cambiar
        """



    def eliminar_documento(documento: Documento) -> None:        
        """
        eliminar_documento(nombre_documento)
                │
                ▼
        Buscar todos los registros
        cuyo metadato
        documento = nombre_documento
                │
                ▼
        Eliminar esos registros
        de la colección
                │
                ▼
         Documento eliminado
         """


    def vaciar(self):
        """
        Eliminar todos los registros
        de la colección. útil durante el desarrollo y las pruebas
        """