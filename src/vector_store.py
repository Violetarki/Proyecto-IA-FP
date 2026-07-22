import chromadb
from models import Chunk, Documento


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