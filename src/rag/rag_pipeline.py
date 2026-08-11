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
from src.rag.context_expander import ContextExpander
from src.rag.intent_classifier import IntentClassifier
from src.rag.guided_mode import GuidedMode
from src.core.models import Mensaje
from src.knowledge.models import KnowledgeTree, KnowledgeNode

import logging

logger = logging.getLogger(__name__)

class RAG:
    """
    Orquesta todas las etapas del sistema RAG.

    Esta clase constituye la puerta de entrada al sistema de preguntas
    y respuestas, coordinando la recuperación de contexto, la construcción
    del prompt y la generación de la respuesta mediante el LLM.
    """

    def __init__(self, arbol: KnowledgeTree):
        self.retriever = Retriever()
        self.prompt_builder = ConstructorPrompts()
        self.llm = LLMClient()
        self.historial = Historial()
        self.id_conversacion = str(uuid.uuid4())

        self.context_expander = ContextExpander(
            arbol,
            self.historial,
        )

        self.intent_classifier = IntentClassifier()
        self.guided_mode = GuidedMode()

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

        candidatos = self.retriever.recuperar_candidatos(
            pregunta,
            metodologia,
        )

        logger.debug("Se han recuperado %d candidatos.", len(candidatos))

        candidatos_expandidos = self.context_expander.expandir(candidatos)

        logger.info("Construyendo prompt...")

        prompt = self.prompt_builder.construir_prompt(
            historial,
            pregunta,
            candidatos_expandidos,
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
