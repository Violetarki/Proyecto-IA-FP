"""Su único trabajo es transformar una pregunta con sus chunks relevantes en un prompt"""

INSTRUCCIONES = (
    "Eres un profesor de Formación Profesional. "
    "Responde únicamente utilizando la información proporcionada en el contexto. "
    "No inventes información ni completes la respuesta con conocimientos externos. "
    "Si la respuesta no aparece en el contexto, indica que no dispones de suficiente información."
)


class ConstructorPrompts:
    """Construye los prompts que se envían al modelo."""

    def construir_prompt(self, pregunta: str, contexto: str) -> str:
        """
        Une tres partes:

        1. Instrucciones para el modelo.
        2. Contexto recuperado.
        3. Pregunta del usuario.
        """
        return f"{INSTRUCCIONES} Contexto: {contexto} Pregunta: {pregunta}"
