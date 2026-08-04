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

import uuid

from src.rag.retriever import Retriever
from src.rag.prompt_builder import ConstructorPrompts
from src.rag.llm_client import LLMClient
from src.rag.historial import Historial
from src.core.models import Mensaje

import logging

logger = logging.getLogger(__name__)

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
        self.historial = Historial()
        self.id_conversacion = str(uuid.uuid4())

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

        logger.info("Recuperando contexto...")

        historial = self.historial.obtener_contexto(self.id_conversacion)

        chunks = self.retriever.recuperar_contexto(
            pregunta,
            metodologia,
        )

        # Si la pregunta nueva no recupera contexto, se combina con
        # la última pregunta del alumno para mantener el tema.
        if not chunks and historial:
            ultima_pregunta = next(
                (
                    mensaje.contenido
                    for mensaje in reversed(historial)
                    if mensaje.rol == "user"
                ),
                None,
            )

            if ultima_pregunta:
                pregunta_contextualizada = (
                    f"{ultima_pregunta}. {pregunta}"
                )

                logger.info(
                    "Reintentando la búsqueda con el contexto anterior."
                )

                chunks = self.retriever.recuperar_contexto(
                    pregunta_contextualizada,
                    metodologia,
                )

        logger.debug("Se han recuperado %d chunks.", len(chunks))

        logger.info("Construyendo prompt...")

        prompt = self.prompt_builder.construir_prompt(
            historial,
            pregunta,
            chunks,
        )

        logger.debug("\n========== PROMPT ==========\n")
        logger.debug("%s", prompt)
        logger.debug("\n============================\n")

        logger.info("Consultando el modelo...")

        respuesta = self.llm.generar_respuesta(prompt)

        # Guardar la pregunta en historial
        self.historial.agregar_mensaje(
            self.id_conversacion,
            Mensaje("user", pregunta)
        )

        # Guardar la respuesta en historial
        self.historial.agregar_mensaje(
            self.id_conversacion,
            Mensaje("bot", respuesta)
        )

        logger.info("Respuesta recibida.")
        return respuesta
