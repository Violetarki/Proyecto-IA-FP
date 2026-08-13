from pathlib import Path
import uuid
from flask import Blueprint, render_template, request, flash, session
import logging

logger = logging.getLogger(__name__)

from src.rag.rag_pipeline import RAG
from src.knowledge.loader import cargar_arbol
from src.rag.guided_steps import obtener_pasos, obtener_actividades_lean, obtener_fases_simulacion
from web.services.documentos import (
    obtener_metodologias,
    mostrar_nombre_metodologia,
)

# Árboles de conocimiento disponibles.
RUTA_ARBOL_LEAN = Path( "data/knowledge/lean_startup.json" ) 
RUTA_ARBOL_SIMULACION = Path( "data/knowledge/simulacion_empresarial.json" ) 
RUTA_ARBOL_COMPLEMENTARIO = Path( "data/knowledge/se_material_complementario.json" )

print("ANTES DE CARGAR LEAN", flush=True)
arbol_lean = cargar_arbol(RUTA_ARBOL_LEAN)
print("LEAN CARGADO", flush=True)

print("ANTES DE CARGAR SIMULACION", flush=True)
arbol_simulacion = cargar_arbol(RUTA_ARBOL_SIMULACION)
print("SIMULACION CARGADA", flush=True)

print("ANTES DE CARGAR COMPLEMENTARIO", flush=True)
arbol_complementario = cargar_arbol(RUTA_ARBOL_COMPLEMENTARIO)
print("COMPLEMENTARIO CARGADO", flush=True)

arboles = {
    "lean_startup": arbol_lean,
    "simulacion_empresarial": arbol_simulacion,
    "se_material_complementario": arbol_complementario,
}

print("ARBOLES CARGADOS", flush=True)

rag = RAG(arboles)

print("RAG CREADO", flush=True)

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

    if "id_conversacion" not in session:
        session["id_conversacion"] = str(uuid.uuid4())

    if "guias" not in session:
        session["guias"] = {}

    metodologia_seleccionada = request.values.get(
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

        modo = request.form.get(
            "modo",
            "normal",
        )

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

        elif modo == "normal":
            try:
                rag.responder(
                    pregunta=pregunta,
                    metodologia=metodologia_seleccionada,
                    id_conversacion=session["id_conversacion"],
                    modo_guiado=False,
                )

            except Exception as error:
                flash(
                    ("No se ha podido generar " f"la respuesta: {error}"),
                    "error",
                )

        elif modo == "guiado":
            try:
                estado_guiado = session["guias"].get(
                    metodologia_seleccionada
                )

                _, estado_guiado = rag.responder(
                    pregunta=pregunta,
                    metodologia=metodologia_seleccionada,
                    id_conversacion=session["id_conversacion"],
                    modo_guiado=True,
                    estado_guiado=estado_guiado,
                )

                session["guias"][metodologia_seleccionada] = estado_guiado

                # Forzamos a Flask a detectar el cambio dentro del diccionario.
                session.modified = True

            except Exception as error:
                flash(
                    ("No se ha podido generar " f"el modo guiado: {error}"),
                    "error",
                )

    conversacion = rag.historial.obtener_historial(session["id_conversacion"])

    arbol = arboles.get(metodologia_seleccionada)

    pasos = (
        obtener_pasos(
            metodologia_seleccionada,
            arbol,
        )
        if arbol
        else []
    )

    estado_guia = session["guias"].get(metodologia_seleccionada)

    actividades_por_paso = {}

    if metodologia_seleccionada == "lean_startup":
        for paso in pasos:
            actividades_por_paso[paso.id] = obtener_actividades_lean(paso)

    return render_template(
            "chatbot.html",
            conversacion=conversacion,
            metodologias=metodologias,
            metodologia_seleccionada=metodologia_seleccionada,
            mostrar_nombre_metodologia=mostrar_nombre_metodologia,
            pasos=pasos,
            estado_guia=estado_guia,
            actividades_por_paso=actividades_por_paso,
        )


@public_bp.route(
    "/chat/seleccionar-paso",
    methods=["POST"],
)
def seleccionar_paso():
    """
    Selecciona un paso del modo guiado y genera
    una primera respuesta del asistente sobre él.
    """

    metodologia = request.form.get(
        "metodologia",
        "",
    ).strip()

    paso_id = request.form.get(
        "paso_id",
        "",
    ).strip()

    if not metodologia or not paso_id:
        return {
            "ok": False,
            "error": "Faltan datos para seleccionar la actividad.",
        }, 400

    if metodologia not in arboles:
        return {
            "ok": False,
            "error": "La metodología seleccionada no es válida.",
        }, 400

    if "id_conversacion" not in session:
        session["id_conversacion"] = str(uuid.uuid4())

    if "guias" not in session:
        session["guias"] = {}

    try:

        estado_guiado = session["guias"].get(metodologia)

        respuesta, estado_guiado = rag.responder(
            pregunta="",
            metodologia=metodologia,
            id_conversacion=session["id_conversacion"],
            modo_guiado=True,
            estado_guiado=estado_guiado,
            paso_id=paso_id,
        )

        if estado_guiado.get("paso_actual") != paso_id:
            return {
                "ok": False,
                "error": "La actividad seleccionada no es válida.",
            }, 400

        session["guias"][metodologia] = estado_guiado
        session.modified = True

        return {
            "ok": True,
            "respuesta": respuesta,
            "paso_id": paso_id,
        }

    except Exception:

        logger.exception("Error al seleccionar paso guiado.")
        return {
            "ok": False,
            "error": "No se ha podido iniciar la actividad.",
        }, 500
