from src.rag.vector_store import VectorStore


def probar_vector_store():

    store = VectorStore()

    resultado = store.collection.get(
        limit=5,
        include=["metadatas"],
    )

    for metadata in resultado["metadatas"]:
        print(metadata)


if __name__ == "__main__":
    probar_vector_store()
