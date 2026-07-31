from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent

CARPETA_DOCUMENTOS = RAIZ_PROYECTO / "documents"
CARPETA_DATA = RAIZ_PROYECTO / "data" 
CARPETA_MARKDOWN_RAW = CARPETA_DATA / "markdown_raw"
CARPETA_MARKDOWN_CLEAN = CARPETA_DATA / "markdown_clean"
CARPETA_VECTOR_STORE = CARPETA_DATA / "vector_store"
CARPETA_HISTORIAL = CARPETA_DATA / "historial_conversaciones"

# Constantes RAG
K_BUSQUEDA = 8

UMBRAL_EXCELENTE = 0.4
UMBRAL_BUENO = 0.6
UMBRAL_ACEPTABLE = 0.8

MINIMO_CHUNKS = 2
MAXIMO_CHUNKS = 3

# LLM
MODELO_LLM = "qwen/qwen3.6-27b"
