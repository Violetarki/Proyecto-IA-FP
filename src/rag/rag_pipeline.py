"""
Coordina el flujo principal del sistema RAG.

Este módulo actúa como punto de entrada al sistema de recuperación
aumentada por generación (RAG), coordinando las distintas etapas
del proceso:

- Recuperar candidatos mediante el Retriever.
- Obtener el contexto reciente de la conversación.
- Construir el prompt con la pregunta, el historial y los resultados recuperados.
- Enviar el prompt al modelo de lenguaje.
- Guardar la conversación en el historial.
- Devolver la respuesta generada.

El resto de la aplicación, como el chatbot web, interactúa con
el sistema RAG a través de esta clase.
"""

import uuid

from src.rag.retriever import Retriever
from src.rag.prompt_builder import ConstructorPrompts
from src.rag.llm_client import LLMClient
from src.rag.historial import Historial
from src.rag.context_expander import ContextExpander
from src.rag.intent_classifier import IntentClassifier
from src.rag.guided_mode import GuidedMode
from src.rag.guided_context_builder import GuidedContextBuilder
from src.core.models import Mensaje
from src.knowledge.models import KnowledgeTree

import logging

logger = logging.getLogger(__name__)

class RAG:
    """
    Orquesta las etapas principales del sistema RAG.

    Coordina la recuperación de candidatos, el historial de la
    conversación, la construcción del prompt y la generación
    de respuestas mediante el modelo de lenguaje.
    """

    def __init__(self, arboles: dict[str, KnowledgeTree]):
        """
        Inicializa el sistema RAG con los árboles de conocimiento
        """

        self.retriever = Retriever()
        self.prompt_builder = ConstructorPrompts()
        self.llm = LLMClient()
        self.historial = Historial()
        self.id_conversacion = str(uuid.uuid4())
        self.intent_classifier = IntentClassifier()

        self.context_expander = ContextExpander(
            arboles,
            self.historial,
        )

        self.guided_mode = GuidedMode()
        self.guided_context_builder = GuidedContextBuilder(arboles)

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

        intencion = self.intent_classifier.clasificar(pregunta)

        logger.debug(
            "Intención: %s | Keywords: %s | Método: %s",
            intencion.intencion,
            intencion.palabras_clave,
            intencion.metodo,
        )

        candidatos = self.retriever.recuperar_candidatos(
            pregunta,
            metodologia,
        )       

        logger.info(
            "Consulta RAG | metodología=%s | candidatos=%d",
            metodologia,
            len(candidatos),
        )

        for candidato in candidatos:
            logger.debug(
                "Chunk recuperado | documento=%s | ruta=%s | "
                "título=%s | node_id=%s | índice=%d | distancia=%.3f",
                candidato.chunk.documento.nombre,
                candidato.chunk.documento.ruta,
                candidato.chunk.titulo,
                candidato.chunk.node_id,
                candidato.chunk.indice,
                candidato.distancia,
            )

        candidatos_expandidos = self.context_expander.expandir(candidatos, intencion)

        logger.info("Construyendo prompt...")

        if self.guided_mode.esta_activo():
            paso = self.guided_mode.obtener_paso_actual()

            contexto_guiado = self.guided_context_builder.construir(
                paso=paso,
                chunks=candidatos_expandidos,
                progreso=self.guided_mode.progreso,
            )

            prompt = self.prompt_builder.construir_prompt_guiado(
                historial,
                pregunta,
                contexto_guiado,
            )
        else:
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
