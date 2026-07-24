from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

CARPETA_DOCUMENTOS = RAIZ_PROYECTO / "documents"
CARPETA_DATA = RAIZ_PROYECTO / "data" 
CARPETA_MARKDOWN_RAW = CARPETA_DATA / "markdown_raw"
CARPETA_MARKDOWN_CLEAN = CARPETA_DATA / "markdown_clean"
CARPETA_VECTOR_STORE = CARPETA_DATA / "vector_store"
