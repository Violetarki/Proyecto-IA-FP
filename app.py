"""
Punto de entrada de la aplicación web.

Este módulo únicamente crea y configura la aplicación Flask,
registra los Blueprints y establece la configuración global.
"""

import os
import logging
from pathlib import Path
from flask import Flask

print("ANTES DE IMPORTAR PUBLIC", flush=True)
from web.public import public_bp
print("PUBLIC IMPORTADO", flush=True)

print("ANTES DE IMPORTAR AUTH", flush=True)
#from web.auth import auth_bp
print("AUTH IMPORTADO", flush=True)

print("ANTES DE IMPORTAR PROFESOR", flush=True)
#from web.profesor import profesor_bp
print("PROFESOR IMPORTADO", flush=True)

Path("data/logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="data/logs/rag.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    encoding="utf-8",
)

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.propagate = False
werkzeug_logger.addHandler(logging.StreamHandler())
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


app = Flask(
    __name__,
    template_folder="web/templates",
    static_folder="web/static",
)

# Registro de los Blueprints de la aplicación.
app.register_blueprint(public_bp)
print("REGISTRADO public")

#app.register_blueprint(auth_bp)
print("REGISTRADO auth")

#app.register_blueprint(profesor_bp)
print("REGISTRADO profesor")

# La clave secreta permite que Flask gestione las sesiones.
#
# Primero intenta leerla desde una variable de entorno.
# Si no existe, utiliza una clave provisional para desarrollo local.
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "clave-provisional-desarrollo",
)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"ARRANCANDO FLASK EN EL PUERTO {port}", flush=True)
    app.run(host="0.0.0.0", port=port)