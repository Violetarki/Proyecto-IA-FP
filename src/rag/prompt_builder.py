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
    "No añadas sangrías al inicio de las líneas."
    "Responde en texto plano, sin usar elementos Markdown como **negrita** u otros. Y usa numeración para listas."
    # Posible mejorado prompt:
    # El contexto proporcionado contiene la información que debes utilizar para responder.
    # El historial solo sirve para entender posibles referencias a preguntas anteriores.
    # Prioriza siempre la pregunta actual y el contexto recuperado.
    # No utilices información del historial para responder si no está respaldada por el contexto actual.
    # Modo preguntas: Responde de forma clara y suficiente. La respuesta debe tener aproximadamente entre 80 y 180 palabras,
    # adaptándose a la complejidad de la pregunta. No alargues la respuesta innecesariamente.
    # Modo guía: Explica únicamente lo necesario para ayudar al alumno con el paso seleccionado.
    # Responde aproximadamente entre 80 y 200 palabras. Si el paso requiere una explicación más breve, no rellenes artificialmente.
)

INSTRUCCIONES_GUIADO = (
    "Eres un profesor de Formación Profesional y estás guiando al alumno "
    "paso a paso por un proceso.\n"
    "Trabaja únicamente con la información proporcionada en el contexto.\n"
    "Explica el paso actual de forma clara y adecuada al nivel del alumno.\n"
    "Ten en cuenta el progreso anterior del alumno para mantener la continuidad.\n"
    "Céntrate únicamente en el paso actual.\n"
    "Después de explicar el paso, formula una pregunta o actividad breve "
    "para que el alumno participe.\n"
    "Si el contexto no contiene información suficiente para explicar el paso, indícalo.\n"
    "No inventes información.\n"
    "No copies grandes fragmentos del contexto.\n"
    "Explica la información con tus propias palabras."
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

            encabezado = " > ".join(chunk.jerarquia_limpia()) or "Sin contexto"
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
        historial_formateado = self._formatear_historial(historial)

        return f"""
        {INSTRUCCIONES}

        Contexto:
        {contexto}

        Pregunta:
        {pregunta}

        Historial:
        {historial_formateado}

        """.strip()


    def construir_prompt_guiado(
            self,
            historial: list[Mensaje],
            pregunta: str,
            contexto: dict,
        ) -> str:
        """
        Construye el prompt para el modo de aprendizaje guiado.
        """

        if not contexto:
            raise ValueError(
                "No se ha proporcionado contexto guiado."
            )

        if not pregunta or not pregunta.strip():
            raise ValueError(
                "La pregunta no puede estar vacía."
            )

        contexto_chunks = self._formatear_contexto(
            contexto["chunks"]
        )

        historial_formateado = self._formatear_historial(
            historial
        )

        progreso_formateado = self._formatear_progreso(
            contexto["progreso"]
        )

        return f"""
        {INSTRUCCIONES_GUIADO}

        Paso actual:
        {contexto["titulo"]}

        Ruta del proceso:
        {" > ".join(contexto["ruta"])}

        Paso padre:
        {contexto["padre"]}

        Información del paso:
        {contexto_chunks}

        Progreso anterior del alumno:
        {progreso_formateado}

        Pregunta del alumno:
        {pregunta}

        Historial de la conversación:
        {historial_formateado}
        """.strip()


    def _formatear_progreso(
            self,
            progreso: list[dict],
        ) -> str:
        """
        Formatea el progreso anterior del alumno para incluirlo en el prompt.

        Args:
            progreso: Lista de pasos trabajados y respuestas del alumno.

        Returns:
            Una cadena con el progreso formateado.
        """

        if not progreso:
            return "(sin progreso previo)"

        lineas = [f"- {titulo}" for titulo in progreso]
        return "\n".join(lineas)


if __name__ == "__main__":
    logger.info("Módulo encargado de construir el prompt para el LLM.")
