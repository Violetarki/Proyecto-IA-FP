from pathlib import Path
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from werkzeug.utils import secure_filename

from src.ingestion.indexador import indexar_documentos

from web.services.auth import login_requerido

from web.services.documentos import (
    es_pdf,
    mostrar_nombre_metodologia,
    obtener_carpeta_metodologia,
    obtener_documentos,
    obtener_metodologias,
)

profesor_bp = Blueprint(
    "profesor",
    __name__,
    url_prefix="/profesor",
)


@profesor_bp.route("/documentos")
@login_requerido
def gestionar_documentos():
    """
    Muestra las metodologías disponibles y los documentos
    de la metodología seleccionada.
    """

    metodologias = obtener_metodologias()

    metodologia_seleccionada = request.args.get("metodologia")

    documentos = []

    if metodologia_seleccionada in metodologias:
        documentos = obtener_documentos(metodologia_seleccionada)

    return render_template(
        "gestion_documentos.html",
        metodologias=metodologias,
        metodologia_seleccionada=(metodologia_seleccionada),
        documentos=documentos,
        mostrar_nombre_metodologia=(mostrar_nombre_metodologia),
    )


@profesor_bp.route(
    "/documentos/subir",
    methods=["POST"],
)
@login_requerido
def subir_documento():
    """
    Sube un archivo PDF a la metodología seleccionada.
    """

    metodologia = request.form.get("metodologia")

    archivo = request.files.get("archivo")

    carpeta_metodologia = obtener_carpeta_metodologia(metodologia)

    if carpeta_metodologia is None:
        flash(
            ("La metodología seleccionada " "no es válida."),
            "error",
        )

        return redirect(url_for("profesor.gestionar_documentos"))

    if archivo is None or archivo.filename is None or archivo.filename == "":
        flash(
            ("Debes seleccionar " "un archivo."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    nombre_seguro = secure_filename(archivo.filename)

    if not nombre_seguro:
        flash(
            ("El nombre del archivo " "no es válido."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    if not es_pdf(nombre_seguro):
        flash(
            ("Solo se permiten " "archivos PDF."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_destino = carpeta_metodologia / nombre_seguro

    if ruta_destino.exists():
        flash(
            ("Ya existe un documento " "con ese nombre."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    archivo.save(ruta_destino)

    flash(
        ("Documento subido " "correctamente."),
        "exito",
    )

    return redirect(
        url_for(
            "profesor.gestionar_documentos",
            metodologia=metodologia,
        )
    )


@profesor_bp.route(
    "/documentos/eliminar",
    methods=["POST"],
)
@login_requerido
def eliminar_documento():
    """
    Elimina un archivo PDF de la metodología seleccionada.
    """

    metodologia = request.form.get("metodologia")

    nombre_documento = request.form.get("documento")

    carpeta_metodologia = obtener_carpeta_metodologia(metodologia)

    if carpeta_metodologia is None:
        flash(
            ("La metodología seleccionada " "no es válida."),
            "error",
        )

        return redirect(url_for("profesor.gestionar_documentos"))

    if not nombre_documento:
        flash(
            ("No se ha indicado " "ningún documento."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    nombre_seguro = secure_filename(nombre_documento)

    if nombre_seguro != nombre_documento:
        flash(
            ("El nombre del documento " "no es válido."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_documento = carpeta_metodologia / nombre_seguro

    if not ruta_documento.exists():
        flash(
            "El documento no existe.",
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    if not ruta_documento.is_file() or not es_pdf(nombre_seguro):
        flash(
            ("El archivo seleccionado " "no es un PDF válido."),
            "error",
        )

        return redirect(
            url_for(
                "profesor.gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_documento.unlink()

    flash(
        ("Documento eliminado " "correctamente."),
        "exito",
    )

    return redirect(
        url_for(
            "profesor.gestionar_documentos",
            metodologia=metodologia,
        )
    )


@profesor_bp.route(
    "/documentos/reconstruir",
    methods=["POST"],
)
@login_requerido
def reconstruir_base_vectorial():
    """
    Actualiza la base de conocimiento ejecutando
    el proceso completo de indexación.
    """

    metodologia = request.form.get("metodologia")

    carpeta_metodologia = obtener_carpeta_metodologia(metodologia)

    if carpeta_metodologia is None:
        flash(
            ("La metodología seleccionada " "no es válida."),
            "error",
        )

        return redirect(url_for("profesor.gestionar_documentos"))

    try:
        indexar_documentos()

        flash(
            ("Base de conocimiento " "actualizada correctamente."),
            "exito",
        )

    except Exception as error:
        flash(
            ("No se ha podido actualizar " "la base de conocimiento: " f"{error}"),
            "error",
        )

    return redirect(
        url_for(
            "profesor.gestionar_documentos",
            metodologia=metodologia,
        )
    )
