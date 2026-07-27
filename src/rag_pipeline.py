"""
Coordina el flujo completo del sistema RAG.

Este módulo actúa como punto de entrada al sistema de recuperación
aumentada por generación (RAG), integrando las distintas etapas del
proceso:

- Recuperar los chunks relevantes mediante el Retriever.
- Construir el prompt con el contexto recuperado.
- Enviar el prompt al modelo de lenguaje.
- Devolver la respuesta generada.

El resto de la aplicación (por ejemplo, el chatbot web) únicamente
debe interactuar con esta clase.
"""

from src.retriever import Retriever
from src.prompt_builder import ConstructorPrompts
from src.llm_client import LLMClient


class RAG:
    """
    Orquesta todas las etapas del sistema RAG.

    Esta clase constituye la puerta de entrada al sistema de preguntas
    y respuestas, coordinando la recuperación de contexto, la construcción
    del prompt y la generación de la respuesta mediante el LLM.
    """

    def __init__(self):
        self.retriever = Retriever()
        self.prompt_builder = ConstructorPrompts()
        self.llm = LLMClient()

    def responder(
        self,
        pregunta: str,
        metodologia: str,
    ) -> str:

        """
        Genera una respuesta utilizando el flujo completo del sistema RAG.

        Args:
            pregunta: Pregunta realizada por el usuario.
            metodologia: Metodología sobre la que se realizará la búsqueda.

        Returns:
            Respuesta generada por el modelo de lenguaje.
        """

        print("Recuperando contexto...")

        chunks = self.retriever.recuperar_contexto(
            pregunta,
            metodologia,
        )

        print(f"Se han recuperado {len(chunks)} chunks.")

        print("Construyendo prompt...")

        prompt = self.prompt_builder.construir_prompt(
            pregunta,
            chunks,
        )

        print("\n========== PROMPT ==========\n")
        print(prompt)
        print("\n============================\n")

        print("Consultando el modelo...")

        respuesta = self.llm.generar_respuesta(prompt)

        print("Respuesta recibida.")
        return respuesta
