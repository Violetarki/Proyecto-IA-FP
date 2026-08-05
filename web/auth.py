from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

auth_bp = Blueprint(
    "auth",
    __name__,
)

from src.core.config import USUARIO_PROFESOR, CONTRASENA_PROFESOR
from web.services.auth import profesor_autenticado

@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    """
    Muestra y procesa el formulario de acceso
    para profesores.
    """

    if profesor_autenticado():
        return redirect(url_for("profesor.gestionar_documentos"))

    if request.method == "POST":
        usuario = request.form.get(
            "usuario",
            "",
        ).strip()

        contrasena = request.form.get(
            "contrasena",
            "",
        )

        credenciales_correctas = (
            usuario == USUARIO_PROFESOR and contrasena == CONTRASENA_PROFESOR
        )

        if credenciales_correctas:
            session["profesor_autenticado"] = True

            session["usuario_profesor"] = usuario

            flash(
                ("Has iniciado sesión " "correctamente."),
                "exito",
            )

            return redirect(url_for("profesor.gestionar_documentos"))

        flash(
            ("El usuario o la contraseña " "no son correctos."),
            "error",
        )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """
    Cierra la sesión del profesor.
    """

    session.clear()

    flash(
        ("Has cerrado sesión " "correctamente."),
        "informacion",
    )

    return redirect(url_for("public.inicio"))
