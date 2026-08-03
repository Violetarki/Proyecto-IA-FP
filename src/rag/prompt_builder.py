"""
Módulo encargado de construir el prompt que se enviará al modelo
de lenguaje.

Responsabilidades:
- Formatear el contexto recuperado por el retriever.
- Añadir las instrucciones para el modelo.
- Incorporar la pregunta del usuario.

Este módulo desacopla la construcción del prompt del resto del
pipeline RAG, facilitando modificar las instrucciones o el formato
sin afectar al chatbot ni al retriever.
"""

from src.core.models import Chunk, Mensaje
import logging

INSTRUCCIONES = (
    "Eres un profesor de Formación Profesional.\n"
    "Responde únicamente con la información del contexto.\n"
    "Si el contexto no contiene la respuesta, indícalo.\n"
    "No inventes información.\n"
    "No copies grandes fragmentos del contexto.\n"
    "Explica la respuesta con tus propias palabras.\n"
    "Combina la información de varios fragmentos cuando sea necesario.\n"
    "Limita la respuesta a lo necesario para responder la pregunta."
)

logger = logging.getLogger(__name__)

class ConstructorPrompts:
    """Construye los prompts que se envían al modelo."""

    def _formatear_contexto(
            self,
            chunks: list[Chunk],
        ) -> str:
        """
        Convierte una lista de chunks en un único bloque de contexto para el prompt.
        """

        partes: list[str] = []

        for chunk in chunks:

            encabezado = " > ".join(chunk.jerarquia()) or "Sin contexto"
            partes.append(f"[{encabezado}]\n{chunk.texto}")

        return "\n\n".join(partes)


    def _formatear_historial(
            self,
            mensajes: list[Mensaje]
        ) -> str:
        """
        Formatea una lista de mensajes para el prompt.

        Convierte cada objeto Mensaje en una línea del historial con el formato:
        - <rol>: <contenido>

        Args:
            mensajes: Lista de objetos Mensaje que representan el historial.

        Returns:
            Una cadena con el historial formateado para incluir en el prompt.
        """

        if not mensajes:
            logger.warning("(sin historial previo)")
            return "(sin historial previo)"

        lineas: list[str] = []

        for mensaje in mensajes:
            lineas.append(f"- {mensaje.rol}: {mensaje.contenido}")

        return "\n".join(lineas)
        

    def construir_prompt(self, historial: list[Mensaje], pregunta: str, chunks: list[Chunk]) -> str:
        """
        Une cuatro partes:

        1. Instrucciones para el modelo.
        2. Contexto recuperado.
        3. Pregunta del usuario.
        4. Historial de la conversación.
        """

        if not chunks:
            raise ValueError(
                "No se han proporcionado chunks para construir el prompt."
            )

        if not pregunta or not pregunta.strip():
            raise ValueError(
                "La pregunta no puede estar vacía."
            )
        
        contexto = self._formatear_contexto(chunks)
        historial = self._formatear_historial(historial)

        return f"""
        {INSTRUCCIONES}

        Contexto:
        {contexto}

        Pregunta:
        {pregunta}

        Historial:
        {historial}

        """.strip()


if __name__ == "__main__":
    logger.info("Módulo encargado de construir el prompt para el LLM.")
