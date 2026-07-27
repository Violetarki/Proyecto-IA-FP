from src.retriever import Retriever
from src.prompt_builder import ConstructorPrompts
from src.llm_client import LLMClient


class RAG:

    def __init__(self):
        self.retriever = Retriever()
        self.prompt_builder = ConstructorPrompts()
        self.llm = LLMClient()

    def responder(
        self,
        pregunta: str,
        metodologia: str,
    ) -> str:

        chunks = self.retriever.recuperar_contexto(
            pregunta,
            metodologia,
        )

        prompt = self.prompt_builder.construir_prompt(
            pregunta,
            chunks,
        )

        respuesta = self.llm.generar_respuesta(prompt)

        return respuesta
