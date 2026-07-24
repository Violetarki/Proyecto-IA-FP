"""
Orquesta el proceso completo de indexación de documentos.

El indexador coordina las distintas etapas del pipeline sin contener
la lógica específica de ninguna de ellas.

Flujo:

PDF
↓
Docling (si es necesario)
↓
Markdown limpio (si es necesario)
↓
Documento
↓
Chunk
↓
Embeddings
↓
Base vectorial
"""

from pathlib import Path
from docling_converter import convertir_pdf_a_markdown
from text_cleaner import limpiar_archivo_markdown
from document_loader import cargar_documentos
from chunker import crear_chunks_documentos
from embeddings import crear_embeddings_chunks
from vector_store import VectorStore

CARPETA_DOCUMENTOS = Path("documents")
CARPETA_MARKDOWN_RAW = Path("data/markdown_raw")
CARPETA_MARKDOWN_CLEAN = Path("data/markdown_clean")


def indexar_documentos():
    """FC ppal"""

    try:
        
        print("Iniciando indexación...")

        markdowns = _obtener_markdowns_limpios()
        print("Markdowns obtenidos")
        print("----------------------------------")

        documentos = cargar_documentos(markdowns)
        print("Documentos creados")
        print("----------------------------------")

        chunks = crear_chunks_documentos(documentos)
        print("Chunks de los documentos creados")
        print("----------------------------------")

        embeddings = crear_embeddings_chunks(chunks)
        print("Embeddings creados")
        print("----------------------------------")

        vector_store = VectorStore()

        vector_store.indexar_chunks(
            chunks,
            embeddings,
        )
        print("Vectores indexados")

        print("Indexación finalizada.")
        print("----------------------------------")
    
    except Exception as error:
        print(f"[ERROR] La indexación ha fallado: {error}")
        raise


def _obtener_markdowns_limpios() -> list[Path]:
    """
    Obtiene los Markdown limpios necesarios para continuar el pipeline.

    Para cada PDF:

    - reutiliza el Markdown limpio si existe;
    - si solo existe el Markdown raw, lo limpia;
    - si no existe ninguno, convierte el PDF y lo limpia.

    Returns:
        Lista con las rutas de los Markdown limpios.
    """

    markdowns_limpios: list[Path] = []

    pdfs = sorted(CARPETA_DOCUMENTOS.rglob("*.pdf"))

    if not pdfs:
        raise FileNotFoundError(
            "No se han encontrado archivos PDF en la carpeta documents."
        )

    for ruta_pdf in pdfs:

        metodologia = ruta_pdf.parent.name

        nombre = ruta_pdf.stem

        ruta_raw = CARPETA_MARKDOWN_RAW / metodologia / f"{nombre}.md"

        ruta_clean = CARPETA_MARKDOWN_CLEAN / metodologia / f"{nombre}.md"

        # Existe el MD limpio
        if ruta_clean.exists():
            print(f"[OK] Markdown limpio encontrado: " f"{ruta_clean.name}")

            markdowns_limpios.append(ruta_clean)

            continue

        # NO existe el MD limpio pero SI el raw
        if ruta_raw.exists():
            print(f"[INFO] Limpiando Markdown: " f"{ruta_raw.name}")

            ruta_clean = limpiar_archivo_markdown(ruta_raw, ruta_clean)

            markdowns_limpios.append(ruta_clean)

            continue

        # NO existen los MD limpios/raw solo PDF
        print(f"[INFO] Convirtiendo PDF: " f"{ruta_pdf.name}")

        ruta_raw = convertir_pdf_a_markdown(ruta_pdf)

        ruta_clean = limpiar_archivo_markdown(
            ruta_raw,
            ruta_clean,
        )

        markdowns_limpios.append(ruta_clean)

    print(f"[OK] Markdown limpio generado: " f"{ruta_clean.name}")
    return markdowns_limpios

