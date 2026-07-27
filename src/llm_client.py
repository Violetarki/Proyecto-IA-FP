"""
Módulo encargado de comunicarse con el modelo de lenguaje.

Su única responsabilidad es enviar un prompt al LLM y devolver
la respuesta generada.
"""

from ollama import chat

from src.config import MODELO_LLM


class LLMClient:
    """
    Gestiona la comunicación con el modelo de lenguaje.
    """

    def __init__(
        self,
        modelo: str = MODELO_LLM,
    ) -> None:
        """
        Inicializa el cliente del modelo.

        Args:
            modelo: Nombre del modelo disponible en Ollama.
        """

        self.modelo = modelo

    def _consultar_modelo(
        self,
        prompt: str,
    ):
        """
        Envía un prompt al modelo de lenguaje.

        Args:
            prompt: Prompt que se enviará al modelo.

        Returns:
            Respuesta completa devuelta por Ollama.
        """

        return chat(
            model=self.modelo,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    def generar_respuesta(
        self,
        prompt: str,
    ) -> str:
        """
        Genera una respuesta a partir de un prompt.

        Args:
            prompt: Prompt que se enviará al modelo.

        Returns:
            Texto generado por el modelo.
        """

        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        try:
            respuesta = self._consultar_modelo(prompt)
        except Exception as e:
            raise RuntimeError("Error al comunicarse con el modelo de lenguaje.") from e

        return respuesta.message.content


if __name__ == "__main__":

    llm = LLMClient()

    while True:

        pregunta = input("\nPregunta: ").strip()

        if not pregunta:
            break

        respuesta = llm.generar_respuesta(pregunta)

        print("\nRespuesta:\n")
        print(respuesta)
