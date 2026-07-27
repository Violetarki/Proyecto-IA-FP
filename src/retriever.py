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

# Pregunta
#     │
#     ▼
# crear_embedding_texto()

#     │
#     ▼
# VectorStore()

#     │
#     ▼
# buscar()

#     │
#     ▼
# Chunks

# PSEUDOCODIGO

def recuperar_contexto(
    pregunta,
    metodologia,
    k=5,
):
    """De esta forma, recuperar_contexto() queda muy limpia: 
    valida la entrada, 
    crea el embedding de la pregunta, 
    consulta el VectorStore y 
    devuelve la lista de Chunk."""


# función privada para validar los parámetros
def _validar_consulta(
    pregunta,
    metodologia,
    k,
):
    pass
    

    if not pregunta.strip():
        raise ValueError(...)

    if not metodologia.strip():
        raise ValueError(...)

    if k <= 0:
        raise ValueError(...)

    embedding = crear_embedding_texto(pregunta)

    vector_store = VectorStore()

    chunks = vector_store.buscar(
        embedding,
        metodologia,
        k,
    )

    return chunks
