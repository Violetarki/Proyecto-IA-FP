"""
Rutas relacionadas con el chatbot público.

Este módulo se encarga de:

- Mostrar la interfaz del chatbot.
- Recibir las preguntas del alumnado.
- Enviar la metodología seleccionada al sistema RAG.
- Recuperar y mostrar el historial completo.
"""

from flask import (
    Blueprint,
    flash,
    render_template,
    request,
)

from src.rag.rag_pipeline import RAG
from web.utils.documentos import (
    mostrar_nombre_metodologia,
    obtener_metodologias,
)


chatbot_bp = Blueprint(
    "chatbot",
    __name__,
)

rag = RAG()


@chatbot_bp.route(
    "/chat",
    methods=["GET", "POST"],
)
def chat():
    """
    Muestra la interfaz pública del chatbot y procesa
    las preguntas realizadas por el alumnado.
    """

    metodologias = obtener_metodologias()

    metodologia_seleccionada = request.form.get(
        "metodologia",
        "lean_startup",
    )

    if metodologia_seleccionada not in metodologias:
        metodologia_seleccionada = (
            metodologias[0]
            if metodologias
            else ""
        )

    if request.method == "POST":
        pregunta = request.form.get(
            "pregunta",
            "",
        ).strip()

        if not pregunta:
            flash(
                "Debes escribir una pregunta.",
                "error",
            )

        elif not metodologia_seleccionada:
            flash(
                "Debes seleccionar una metodología válida.",
                "error",
            )

        else:
            try:
                rag.responder(
                    pregunta=pregunta,
                    metodologia=metodologia_seleccionada,
                )

            except Exception as error:
                flash(
                    (
                        "No se ha podido generar "
                        f"la respuesta: {error}"
                    ),
                    "error",
                )

    conversacion = rag.historial.obtener_historial(
        rag.id_conversacion
    )

    return render_template(
        "chatbot.html",
        conversacion=conversacion,
        metodologias=metodologias,
        metodologia_seleccionada=metodologia_seleccionada,
        mostrar_nombre_metodologia=(
            mostrar_nombre_metodologia
        ),
    )