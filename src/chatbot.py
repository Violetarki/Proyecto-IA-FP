import embeddings
from vector_store import VectorStore
from llm import LLM

class Chatbot:

    def __init__(
        self,
        embedder: embeddings,
        vector_store: VectorStore,
        llm: LLM
    ):
        
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm



    def responder():
        """
        1. Generar embedding

        ↓

        2. Buscar los mejores chunks

        ↓

        3. Construir el contexto

        ↓

        4. Crear el prompt

        ↓

        5. Llamar al LLM

        ↓

        6. Devolver la respuesta
        """



    def _generar_contexto():
        ...

    def _construir_prompt():
        ...

    def _consultar_llm():
        ...