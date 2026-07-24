import chromadb
from models import Chunk, Documento, Metodologia



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
        Inicializa la conexión con ChromaDB y crea la colección si no existe.

        Args:
            collection_name: Nombre de la colección vectorial.
            persist_directory: Ruta donde se almacenará la base de datos.
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

        # Preparar las listas necesarias para insertar los registros en batch.
        ids: list[str] = []
        textos: list[str] = []
        embeddings: list[list[float]] = []
        metadatos: list[dict] = []

        for chunk in chunks:
            if not hasattr(chunk, "embedding"):
                raise AttributeError(
                    "Cada chunk debe tener el atributo 'embedding'."
                )

            # Extraer la información relevante de cada chunk.
            ids.append(
                f"{chunk.documento.ruta}:{chunk.indice}"
            )
            textos.append(chunk.texto)
            embeddings.append(chunk.embedding)

            metadata = {
                "documento": chunk.documento.nombre,
                "ruta": chunk.documento.ruta,
                "indice": chunk.indice,
            }

            if chunk.titulo is not None:
                metadata["titulo"] = chunk.titulo
            if chunk.subtitulo is not None:
                metadata["subtitulo"] = chunk.subtitulo

            metadatos.append(metadata)

        # Insertar todos los registros de una sola vez en la colección.
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

        Args:
            documento: Documento cuyos chunks se quieren borrar.
        """

        if documento is None:
            return

        # Eliminar los registros cuyo metadato coincide con el documento.
        self.collection.delete(
            where={
                "$and": [
                    {"documento": documento.nombre},
                    {"ruta": documento.ruta},
                ]
            }
        )



    def vaciar(self):
        """
        Elimina todos los registros de la colección.
        """

        total = self.collection.count()
        if total == 0:
            return

        # Recuperar los ids de todos los elementos de la colección.
        resultado = self.collection.get(
            limit=total,
            include=["metadatas"],
        )

        ids = resultado.get("ids", [])
        if not ids:
            return

        self.collection.delete(ids=ids)


if __name__ == "__main__":
    vector_store = VectorStore(collection_name="prueba_vector_store")

    metodologia = Metodologia(nombre="lean_startup")
    documento = Documento(
        metodologia=metodologia,
        nombre="documento_prueba.md",
        texto="Texto de prueba para vector store.",
        ruta="/tmp/documento_prueba.md",
    )

    chunk_1 = Chunk(
        documento=documento,
        indice=0,
        texto="Lean startup es una metodología para validar ideas.",
        titulo="Introducción",
        subtitulo="Concepto",
    )
    chunk_1.embedding = [0.1, 0.2, 0.3, 0.4]

    chunk_2 = Chunk(
        documento=documento,
        indice=1,
        texto="Los experimentos ayudan a aprender con el cliente.",
        titulo="Experimentos",
        subtitulo="Validación",
    )
    chunk_2.embedding = [0.2, 0.3, 0.4, 0.5]

    vector_store.guardar_chunks([chunk_1, chunk_2])

    resultados = vector_store.buscar([0.1, 0.2, 0.3, 0.4], k=2)
    print(f"Resultados encontrados: {len(resultados)}")
    for chunk in resultados:
        print(chunk.texto)

    vector_store.eliminar_documento(documento)
    print("Documento eliminado del vector store.")

    vector_store.vaciar()
    print("Colección vaciada.")