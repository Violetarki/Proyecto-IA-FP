
INSTRUCCIONES = (
    "Responde únicamente utilizando la información proporcionada en el contexto. "
    "Si la respuesta no aparece en el contexto, indícalo claramente.")


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