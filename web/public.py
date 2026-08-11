from pathlib import Path
from flask import Blueprint, render_template, request, flash

from src.rag.rag_pipeline import RAG
from src.knowledge.loader import cargar_arbol
from web.services.documentos import (
    obtener_metodologias,
    mostrar_nombre_metodologia,
)

# Árboles de conocimiento disponibles.
RUTA_ARBOL_LEAN = Path( "data/knowledge/lean_startup.json" ) 
RUTA_ARBOL_SIMULACION = Path( "data/knowledge/simulacion_empresarial.json" ) 
RUTA_ARBOL_COMPLEMENTARIO = Path( "data/knowledge/se_material_complementario.json" )

arboles = {
    "lean_startup": cargar_arbol(RUTA_ARBOL_LEAN),
    "simulacion_empresarial": cargar_arbol(RUTA_ARBOL_SIMULACION),
    "se_material_complementario": cargar_arbol(RUTA_ARBOL_COMPLEMENTARIO),
}

rag = RAG(arboles)

public_bp = Blueprint(
    "public",
    __name__,
)


@public_bp.route("/")
def inicio():
    """
    Muestra la portada principal de la aplicación.
    """

    return render_template("inicio.html")


@public_bp.route(
    "/chat",
    methods=["GET", "POST"],
)
def chat():
    """
    Muestra la interfaz pública del chatbot y procesa
    las preguntas realizadas por el alumnado.

    El alumno puede elegir la metodología sobre la que
    desea realizar la consulta. Además, se recupera el
    historial completo para mostrar toda la conversación.
    """

    metodologias = obtener_metodologias()

    metodologia_seleccionada = request.form.get(
        "metodologia",
        "simulacion_empresarial",
    )

    if metodologia_seleccionada not in metodologias:
        metodologia_seleccionada = metodologias[0] if metodologias else ""

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
                ("Debes seleccionar una " "metodología válida."),
                "error",
            )

        else:
            try:
                rag.responder(
                    pregunta=pregunta,
                    metodologia=(metodologia_seleccionada),
                )

            except Exception as error:
                flash(
                    ("No se ha podido generar " f"la respuesta: {error}"),
                    "error",
                )

    conversacion = rag.historial.obtener_historial(rag.id_conversacion)

    return render_template(
        "chatbot.html",
        conversacion=conversacion,
        metodologias=metodologias,
        metodologia_seleccionada=metodologia_seleccionada,
        mostrar_nombre_metodologia=mostrar_nombre_metodologia,
    )
