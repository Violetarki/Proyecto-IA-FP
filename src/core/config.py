import os
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent

CARPETA_DOCUMENTOS = RAIZ_PROYECTO / "documents"
CARPETA_DATA = RAIZ_PROYECTO / "data" 
CARPETA_MARKDOWN_RAW = CARPETA_DATA / "markdown_raw"
CARPETA_MARKDOWN_CLEAN = CARPETA_DATA / "markdown_clean"
CARPETA_VECTOR_STORE = CARPETA_DATA / "vector_store"
CARPETA_HISTORIAL = CARPETA_DATA / "historial_conversaciones"
CARPETA_KNOWLEDGE = CARPETA_DATA / "knowledge"

MANUALES_CON_KNOWLEDGE = {
    "lean_startup",
    "simulacion_empresarial",
}

# Constantes RAG
K_BUSQUEDA = 15

UMBRAL_EXCELENTE = 0.4
UMBRAL_BUENO = 0.6
UMBRAL_ACEPTABLE = 0.8

MINIMO_CHUNKS = 2
MAXIMO_CHUNKS = 3

# LLM
MODELO_LLM = "qwen/qwen3.6-27b"

# Chatbot
# Credenciales provisionales para acceder al panel de profesores.
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
