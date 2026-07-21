"""
Aplicación web para gestionar los documentos utilizados por las
distintas metodologías educativas.
"""

from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Necesaria para mostrar mensajes con flash().
# Más adelante se puede guardar en una variable de entorno.
app.secret_key = "clave-provisional-desarrollo"


# Carpeta principal donde se almacenan los documentos.
CARPETA_DOCUMENTOS = Path("documents")


# Metodologías disponibles.
# La clave coincide con el nombre de la carpeta.
METODOLOGIAS = {
    "lean_startup": "Lean Startup",
    "simulacion_empresarial": "Simulación Empresarial",
}


def obtener_carpeta_metodologia(metodologia: str) -> Path | None:
    """
    Devuelve la carpeta asociada a una metodología válida.

    Si la metodología no existe, devuelve None.
    """

    if metodologia not in METODOLOGIAS:
        return None

    return CARPETA_DOCUMENTOS / metodologia


def obtener_documentos(metodologia: str) -> list[str]:
    """
    Devuelve la lista de archivos PDF de una metodología.
    """

    carpeta_metodologia = obtener_carpeta_metodologia(metodologia)

    if carpeta_metodologia is None:
        return []

    if not carpeta_metodologia.exists():
        return []

    documentos = [
        archivo.name
        for archivo in carpeta_metodologia.iterdir()
        if archivo.is_file() and archivo.suffix.lower() == ".pdf"
    ]

    return sorted(documentos)


def es_pdf(nombre_archivo: str) -> bool:
    """
    Comprueba si un archivo tiene extensión PDF.
    """

    return Path(nombre_archivo).suffix.lower() == ".pdf"


@app.route("/")
def inicio():
    """
    Redirige a la página de gestión de documentos.
    """

    return redirect(url_for("gestionar_documentos"))


@app.route("/profesor/documentos")
def gestionar_documentos():
    """
    Muestra las metodologías disponibles y los documentos
    de la metodología seleccionada.
    """

    metodologia_seleccionada = request.args.get("metodologia")

    documentos = []

    if metodologia_seleccionada in METODOLOGIAS:
        documentos = obtener_documentos(metodologia_seleccionada)

    return render_template(
        "gestion_documentos.html",
        metodologias=METODOLOGIAS,
        metodologia_seleccionada=metodologia_seleccionada,
        documentos=documentos,
    )


@app.route("/profesor/documentos/subir", methods=["POST"])
def subir_documento():
    """
    Sube un archivo PDF a la metodología seleccionada.
    """

    metodologia = request.form.get("metodologia")
    archivo = request.files.get("archivo")

    carpeta_metodologia = obtener_carpeta_metodologia(metodologia)

    if carpeta_metodologia is None:
        flash("La metodología seleccionada no es válida.", "error")
        return redirect(url_for("gestionar_documentos"))

    if archivo is None or archivo.filename == "":
        flash("Debes seleccionar un archivo.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    nombre_seguro = secure_filename(archivo.filename)

    if not nombre_seguro:
        flash("El nombre del archivo no es válido.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    if not es_pdf(nombre_seguro):
        flash("Solo se permiten archivos PDF.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    carpeta_metodologia.mkdir(parents=True, exist_ok=True)

    ruta_destino = carpeta_metodologia / nombre_seguro

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

    flash("Documento subido correctamente.", "exito")

    return redirect(
        url_for(
            "gestionar_documentos",
            metodologia=metodologia,
        )
    )


@app.route("/profesor/documentos/eliminar", methods=["POST"])
def eliminar_documento():
    """
    Elimina un archivo PDF de la metodología seleccionada.
    """

    metodologia = request.form.get("metodologia")
    nombre_documento = request.form.get("documento")

    carpeta_metodologia = obtener_carpeta_metodologia(metodologia)

    if carpeta_metodologia is None:
        flash("La metodología seleccionada no es válida.", "error")
        return redirect(url_for("gestionar_documentos"))

    if not nombre_documento:
        flash("No se ha indicado ningún documento.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    # Evita que se puedan introducir rutas manuales.
    nombre_seguro = secure_filename(nombre_documento)

    if nombre_seguro != nombre_documento:
        flash("El nombre del documento no es válido.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_documento = carpeta_metodologia / nombre_seguro

    if not ruta_documento.exists():
        flash("El documento no existe.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    if not ruta_documento.is_file() or not es_pdf(nombre_seguro):
        flash("El archivo seleccionado no es un PDF válido.", "error")
        return redirect(
            url_for(
                "gestionar_documentos",
                metodologia=metodologia,
            )
        )

    ruta_documento.unlink()

    flash("Documento eliminado correctamente.", "exito")

    return redirect(
        url_for(
            "gestionar_documentos",
            metodologia=metodologia,
        )
    )


@app.route("/profesor/documentos/reconstruir", methods=["POST"])
def reconstruir_base_vectorial():
    """
    Muestra un mensaje provisional.

    Más adelante esta ruta se conectará con el pipeline
    de lectura, limpieza, chunking y vectorización.
    """

    metodologia = request.form.get("metodologia")

    if metodologia not in METODOLOGIAS:
        flash("La metodología seleccionada no es válida.", "error")
        return redirect(url_for("gestionar_documentos"))

    flash(
        "La reconstrucción de la base vectorial se implementará próximamente.",
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