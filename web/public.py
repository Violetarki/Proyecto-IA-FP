from pathlib import Path
import uuid
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
import logging

logger = logging.getLogger(__name__)

from src.rag.rag_pipeline import RAG
from src.knowledge.loader import cargar_arbol
from src.rag.guided_steps import obtener_pasos, obtener_actividades_lean
from web.profesor import obtener_metodologia_activa
from web.services.documentos import (
    obtener_metodologias,
    mostrar_nombre_metodologia,
)

# Árboles de conocimiento disponibles.
RUTA_ARBOL_LEAN = Path( "data/knowledge/lean_startup.json" ) 
RUTA_ARBOL_SIMULACION = Path( "data/knowledge/simulacion_empresarial.json" ) 
RUTA_ARBOL_COMPLEMENTARIO = Path( "data/knowledge/se_material_complementario.json" )


arbol_lean = cargar_arbol(RUTA_ARBOL_LEAN)
arbol_simulacion = cargar_arbol(RUTA_ARBOL_SIMULACION)
arbol_complementario = cargar_arbol(RUTA_ARBOL_COMPLEMENTARIO)


arboles = {
    "lean_startup": arbol_lean,
    "simulacion_empresarial": arbol_simulacion,
    "se_material_complementario": arbol_complementario,
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


@public_bp.route("/chat/nueva")
def nueva_conversacion():
    """
    Inicia una nueva conversación sin modificar
    el progreso del modo guiado, pero con nuevo historial.
    """
    id_anterior = session.get("id_conversacion")

    if id_anterior:
        rag.historial.eliminar_conversacion(id_anterior)
        
    session["id_conversacion"] = str(uuid.uuid4())

    return redirect(url_for("public.chat"))


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

    metodologia_seleccionada = obtener_metodologia_activa()

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

                print(
                    "GUIAS ANTES DE PREGUNTA:",
                    session.get("guias"),
                    flush=True,
                )

                # Guardamos el progreso antes de la pregunta.
                guias_guardadas = dict(session.get("guias", {}))

                rag.responder(
                    pregunta=pregunta,
                    metodologia=metodologia_seleccionada,
                    id_conversacion=session["id_conversacion"],
                    modo_guiado=False,
                )

                # Restauramos explícitamente el progreso.
                session["guias"] = guias_guardadas
                session.modified = True

                print(
                    "GUIAS DESPUÉS DE PREGUNTA:",
                    session.get("guias"),
                    flush=True,
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

    print(
        "GUIAS EN SESION:",
        session.get("guias"),
        flush=True,
    )

    print(
        "ESTADO GUIA ACTUAL:",
        estado_guia,
        flush=True,
    )

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


@public_bp.route(
    "/chat/marcar-paso",
    methods=["POST"],
)
def marcar_paso():
    """
    Guarda el estado de completado de un paso/actividad
    para la metodología correspondiente.
    """

    metodologia = request.form.get(
        "metodologia",
        "",
    ).strip()

    paso_id = request.form.get(
        "paso_id",
        "",
    ).strip()

    completado = (
        request.form.get(
            "completado",
            "false",
        )
        == "true"
    )

    if not metodologia or not paso_id:
        return {
            "ok": False,
            "error": "Faltan datos.",
        }, 400

    if metodologia not in arboles:
        return {
            "ok": False,
            "error": "La metodología no es válida.",
        }, 400

    if "guias" not in session:
        session["guias"] = {}

    estado = session["guias"].get(metodologia)

    if estado is None:
        estado = {
            "activo": False,
            "completados": [],
            "paso_actual": None,
            "pasos_ids": [],
        }

    completados = estado.setdefault(
        "completados",
        [],
    )

    if completado:
        if paso_id not in completados:
            completados.append(paso_id)
    else:
        if paso_id in completados:
            completados.remove(paso_id)

    session["guias"][metodologia] = estado
    session.modified = True

    return {
        "ok": True,
        "completado": completado,
    }
