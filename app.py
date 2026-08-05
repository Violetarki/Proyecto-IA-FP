"""
Punto de entrada de la aplicación web.

Este módulo únicamente crea y configura la aplicación Flask,
registra los Blueprints y establece la configuración global.
"""

import os
from flask import Flask

from web.public import public_bp
from web.auth import auth_bp
from web.profesor import profesor_bp


app = Flask(
    __name__,
    template_folder="web/templates",
    static_folder="web/static",
)

# Registro de los Blueprints de la aplicación.
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profesor_bp)


# La clave secreta permite que Flask gestione las sesiones.
#
# Primero intenta leerla desde una variable de entorno.
# Si no existe, utiliza una clave provisional para desarrollo local.
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "clave-provisional-desarrollo",
)


if __name__ == "__main__":
    app.run(
        debug=True
    )
