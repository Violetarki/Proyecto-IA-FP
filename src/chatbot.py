from src.embeddings import crear_embedding_texto
from src.vector_store import VectorStore
from src.prompt_builder import ConstructorPrompts
from src.llm_client import LLMClient
from src.retriever import recuperar_contexto


class Chatbot:
    """Coordina la recuperación de contexto y la generación de respuestas."""

    def __init__(
        self,
        embedder: crear_embedding_texto,
        vector_store: VectorStore,
        llm: LLMClient
    ):
        """Inicializa el chatbot con su generador de embeddings, vector store y cliente LLM."""
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm


    def responder(self, pregunta: str, metodologia: str) -> str:
        """Devuelve una respuesta para la pregunta usando contexto recuperado."""

        # Recuperamos el contexto
        contexto = recuperar_contexto(pregunta, metodologia)

        # Construimos el prompt
        prompt = ConstructorPrompts().construir_prompt(pregunta, contexto)

        # Obtenemos la respuesta del LLM
        respuesta = self.llm.generar_respuesta(prompt)

        return respuesta



if __name__ == "__main__":
    """Prueba interactiva del chatbot con el LLM real instalado."""

    class DummyVectorStore:
        """Implementación mínima de un vector store para pruebas."""

        def buscar(self, embedding, k=5):
            return [
                type("Chunk", (), {"texto": "Lean startup valida la idea con experimentos."})(),
                type("Chunk", (), {"texto": "La simulación empresarial ayuda a anticipar riesgos."})(),
            ]

    chatbot = Chatbot(
        embedder=lambda texto: [0.1, 0.2, 0.3],
        vector_store=DummyVectorStore(),
        llm=LLMClient(),
    )

    print("Prueba interactiva del chatbot con LLM real")
    print("Escribe tu pregunta (o deja vacío para salir):")

    while True:
        pregunta = input("> ").strip()
        if not pregunta:
            print("Saliendo...")
            break

        try:
            respuesta = chatbot.responder(pregunta)
            print("\nRespuesta del modelo:\n")
            print(respuesta)
            print("\n---\n")
        except Exception as exc:
            print(f"Error al generar respuesta: {exc}")
            break
