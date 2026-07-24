from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

CARPETA_DOCUMENTOS = RAIZ_PROYECTO / "documents"
CARPETA_DATA = RAIZ_PROYECTO / "data" 
CARPETA_MARKDOWN_RAW = RAIZ_PROYECTO / "data" / "markdown_raw"
CARPETA_MARKDOWN_CLEAN = RAIZ_PROYECTO / "data" / "markdown_clean"
CARPETA_VECTOR_STORE = RAIZ_PROYECTO / "data" / "vector_store"