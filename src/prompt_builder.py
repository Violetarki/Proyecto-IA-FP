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

from src.models import Chunk

INSTRUCCIONES = (
    "Eres un profesor de Formación Profesional.\n"
    "Responde únicamente utilizando la información proporcionada en el contexto.\n"
    "No inventes información ni completes la respuesta con conocimientos externos.\n"
    "Si la respuesta no aparece en el contexto, indica que no dispones de suficiente información.\n"
    "No copies grandes fragmentos del contexto.\n"
    "Explica la información con tus propias palabras manteniendo el mismo significado.\n"
    "Si distintas partes del contexto contienen información complementaria, combínalas en una única respuesta."

)


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

            encabezado = chunk.titulo or "Sin título"

            if chunk.subtitulo:
                encabezado += f" > {chunk.subtitulo}"

            partes.append(
                f"[{encabezado}]\n{chunk.texto}"
            )

        return "\n\n".join(partes)

    def construir_prompt(self, pregunta: str, chunks: list[Chunk]) -> str:
        """
        Une tres partes:

        1. Instrucciones para el modelo.
        2. Contexto recuperado.
        3. Pregunta del usuario.
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

        return f"""
        {INSTRUCCIONES}

        Contexto:
        {contexto}

        Pregunta:
        {pregunta}
        """.strip()

if __name__ == "__main__":
    print("Módulo encargado de construir el prompt para el LLM.")
