import chromadb

print(chromadb.__version__)



class VectorStore:

    def __init__(
        self,
        collection_name: str = "chunks",
        persist_directory: str = "./data/vector_store"
        ):

        cliente = chromadb.PersistentClient(path="data/vector_store")
        self.collection = collection_name

    

    def guardar_chunks(self, chunks) -> None:
        """

         Recibir lista de chunks
                │
                ▼
        Recorrer cada chunk
                │
                ▼
        Extraer:
            - id
            - texto
            - embedding
            - metadatos
                │
                ▼
        Insertarlos en la colección

        """
        self.collection.add("chunks")


    def buscar(self, pregunta):
        """

        Embedding de la pregunta
                │
                ▼
        Consultar ChromaDB
                │
                ▼
        Obtener los x resultados más similares
                │
                ▼
        Convertir cada resultado en un Chunk
                │
                ▼
        Devolver list[Chunk]

        """

    def eliminar_documento(self, documento):
        ...

    def vaciar(self):
        ...