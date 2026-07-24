"""
Aplicación web del Asistente IA para Formación Profesional.

La aplicación permite:

- Acceder al chatbot desde la parte pública.
- Iniciar sesión como profesor.
- Gestionar documentos desde un panel privado.
"""

import os
from functools import wraps
from pathlib import Path
from typing import Callable

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename


app = Flask(__name__)

# La clave secreta permite que Flask gestione las sesiones.
#
# Primero intenta leerla desde una variable de entorno.
# Si no existe, utiliza una clave provisional para desarrollo local.
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "clave-provisional-desarrollo",
)


# Credenciales provisionales para acceder al panel de profesores.
#
# Más adelante pueden guardarse en variables de entorno,
# una base de datos o un sistema de usuarios.
USUARIO_PROFESOR = os.getenv(
    "USUARIO_PROFESOR",
    "profesor",
)

CONTRASENA_PROFESOR = os.getenv(
    "CONTRASENA_PROFESOR",
    "profesor123",
)


# Carpeta principal donde se almacenan las metodologías
# y sus documentos.
CARPETA_DOCUMENTOS = Path("documents")


def obtener_metodologias() -> list[str]:
    """
    Devuelve las metodologías disponibles a partir de las
    subcarpetas existentes dentro de documents.
    """

    if not CARPETA_DOCUMENTOS.exists():
        return []

    metodologias = [
        carpeta.name
        for carpeta in CARPETA_DOCUMENTOS.iterdir()
        if carpeta.is_dir()
    ]

    return sorted(metodologias)


def mostrar_nombre_metodologia(metodologia: str) -> str:
    """
    Convierte el nombre de una carpeta en un texto legible.

    Ejemplo:
        lean_startup -> Lean Startup
    """

    return metodologia.replace("_", " ").title()


def obtener_carpeta_metodologia(
    metodologia: str | None,
) -> Path | None:
    """
    Devuelve la carpeta asociada a una metodología.

    Si la metodología no existe o no es válida,
    devuelve None.
    """

    if not metodologia:
        return None

    carpeta_metodologia = CARPETA_DOCUMENTOS / metodologia

    if not carpeta_metodologia.exists():
        return None

    if not carpeta_metodologia.is_dir():
        return None

    return carpeta_metodologia


def obtener_documentos(metodologia: str) -> list[str]:
    """
    Devuelve los archivos PDF de una metodología.
    """

    carpeta_metodologia = obtener_carpeta_metodologia(
        metodologia
    )

    if carpeta_metodologia is None:
        return []

    documentos = [
        archivo.name
        for archivo in carpeta_metodologia.iterdir()
        if archivo.is_file()
        and archivo.suffix.lower() == ".pdf"
    ]

    return sorted(documentos)


def es_pdf(nombre_archivo: str) -> bool:
    """
    Comprueba si un archivo tiene extensión PDF.
    """

    return Path(nombre_archivo).suffix.lower() == ".pdf"


def profesor_autenticado() -> bool:
    """
    Comprueba si el profesor ha iniciado sesión.
    """

    return session.get("profesor_autenticado", False)


def login_requerido(funcion: Callable) -> Callable:
    """
    Protege una ruta para que solo pueda acceder
    un profesor autenticado.

    Si no existe una sesión válida, se redirige al login.
    """

    @wraps(funcion)
    def funcion_protegida(*args, **kwargs):
        if not profesor_autenticado():
            flash(
                "Debes iniciar sesión para acceder al panel.",
                "error",
            )

            return redirect(url_for("login"))

        return funcion(*args, **kwargs)

    return funcion_protegida


@app.route("/")
def inicio():
    """
    Muestra la portada principal de la aplicación.
    """

    return render_template("inicio.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    """
    Muestra la interfaz pública del chatbot.

    Por ahora devuelve una respuesta provisional.
    Más adelante se conectará con src/chatbot.py.
    """

    pregunta = ""
    respuesta = ""

    if request.method == "POST":
        pregunta = request.form.get(
            "pregunta",
            "",
        ).strip()

        if pregunta:
            respuesta = (
                "La conexión con el modelo de lenguaje "
                "todavía está en desarrollo."
            )
        else:
            flash(
                "Debes escribir una pregunta.",
                "error",
            )

    return render_template(
        "chatbot.html",
        pregunta=pregunta,
        respuesta=respuesta,
    )
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Muestra y procesa el formulario de acceso
    para profesores.
    """

    if profesor_autenticado():
        return redirect(url_for("gestionar_documentos"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        credenciales_correctas = (
            usuario == USUARIO_PROFESOR
            and contrasena == CONTRASENA_PROFESOR
        )

        if credenciales_correctas:
            session["profesor_autenticado"] = True
            session["usuario_profesor"] = usuario

            flash(
                "Has iniciado sesión correctamente.",
                "exito",
            )

            return redirect(
                url_for("gestionar_documentos")
            )

        flash(
            "El usuario o la contraseña no son correctos.",
            "error",
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Cierra la sesión del profesor.
    """

    session.clear()

    flash(
        "Has cerrado sesión correctamente.",
        "informacion",
    )

    return redirect(url_for("inicio"))


@app.route("/profesor/documentos")
@login_requerido
def gestionar_documentos():
    """
    Muestra las metodologías disponibles y los documentos
    de la metodología seleccionada.
    """

    metodologias = obtener_metodologias()
    metodologia_seleccionada = request.args.get(
        "metodologia"
    )

    documentos = []

    if metodologia_seleccionada in metodologias:
        documentos = obtener_documentos(
            metodologia_seleccionada
        )

    return render_template(
        "gestion_documentos.html",
        metodologias=metodologias,
        metodologia_seleccionada=metodologia_seleccionada,
        documentos=documentos,
        mostrar_nombre_metodologia=(
            mostrar_nombre_metodologia
        ),
    )


@app.route(
    "/profesor/documentos/subir",
    methods=["POST"],
)
@login_requerido
def subir_documento():
    """
    Sube un archivo PDF a la metodología seleccionada.
    """

    metodologia = request.form.get("metodologia")
    archivo = request.files.get("archivo")

    carpeta_metodologia = obtener_carpeta_metodologia(
        metodologia
    )

    if carpeta_metodologia is None:
        flash(
            "La metodología seleccionada no es válida.",
            "error",
        )

        return redirect(
            url_for("gestionar_documentos")
        )

    if archivo is None or archivo.filename == "":
        flash(
            "Debes seleccionar un archivo.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    nombre_seguro = secure_filename(archivo.filename)

    if not nombre_seguro:
        flash(
            "El nombre del archivo no es válido.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    if not es_pdf(nombre_seguro):
        flash(
            "Solo se permiten archivos PDF.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_destino = (
        carpeta_metodologia / nombre_seguro
    )

    if ruta_destino.exists():
        flash(
            "Ya existe un documento con ese nombre.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    archivo.save(ruta_destino)

    flash(
        "Documento subido correctamente.",
        "exito",
    )

    return redirect(
        url_for(
            "gestionar_documentos",
            metodologia=metodologia,
        )
    )


@app.route(
    "/profesor/documentos/eliminar",
    methods=["POST"],
)
@login_requerido
def eliminar_documento():
    """
    Elimina un archivo PDF de la metodología seleccionada.
    """

    metodologia = request.form.get("metodologia")
    nombre_documento = request.form.get("documento")

    carpeta_metodologia = obtener_carpeta_metodologia(
        metodologia
    )

    if carpeta_metodologia is None:
        flash(
            "La metodología seleccionada no es válida.",
            "error",
        )

        return redirect(
            url_for("gestionar_documentos")
        )

    if not nombre_documento:
        flash(
            "No se ha indicado ningún documento.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    nombre_seguro = secure_filename(
        nombre_documento
    )

    if nombre_seguro != nombre_documento:
        flash(
            "El nombre del documento no es válido.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_documento = (
        carpeta_metodologia / nombre_seguro
    )

    if not ruta_documento.exists():
        flash(
            "El documento no existe.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    if (
        not ruta_documento.is_file()
        or not es_pdf(nombre_seguro)
    ):
        flash(
            "El archivo seleccionado no es un PDF válido.",
            "error",
        )

        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_documento.unlink()

    flash(
        "Documento eliminado correctamente.",
        "exito",
    )

    return redirect(
        url_for(
            "gestionar_documentos",
            metodologia=metodologia,
        )
    )


@app.route(
    "/profesor/documentos/reconstruir",
    methods=["POST"],
)
@login_requerido
def reconstruir_base_vectorial():
    """
    Muestra un mensaje provisional.

    Más adelante esta ruta se conectará con el pipeline
    de lectura, limpieza, chunking y vectorización.
    """

    metodologia = request.form.get("metodologia")

    carpeta_metodologia = obtener_carpeta_metodologia(
        metodologia
    )

    if carpeta_metodologia is None:
        flash(
            "La metodología seleccionada no es válida.",
            "error",
        )

        return redirect(
            url_for("gestionar_documentos")
        )

    flash(
        (
            "La reconstrucción de la base vectorial "
            "se implementará próximamente."
        ),
        "informacion",
    )

    return redirect(
        url_for(
            "gestionar_documentos",
            metodologia=metodologia,
        )
    )


if __name__ == "__main__":
    app.run(debug=True)