from collections.abc import Callable
from functools import wraps
from flask import flash, redirect, session, url_for


def profesor_autenticado() -> bool:
    """
    Comprueba si el profesor ha iniciado sesión.
    """

    return session.get(
        "profesor_autenticado",
        False,
    )


def login_requerido(
    funcion: Callable,
) -> Callable:
    """
    Protege una ruta para que solo pueda acceder
    un profesor autenticado.

    Si no existe una sesión válida, se redirige al login.
    """

    @wraps(funcion)
    def funcion_protegida(
        *args,
        **kwargs,
    ):
        if not profesor_autenticado():
            flash(
                ("Debes iniciar sesión para " "acceder al panel."),
                "error",
            )

            return redirect(url_for("auth.login"))

        return funcion(
            *args,
            **kwargs,
        )

    return funcion_protegida
