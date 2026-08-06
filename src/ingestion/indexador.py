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
parsear_markdown
    ↓
MarkdownNode
    ├──► crear_arbol
    └──► crear_chunks_documento
             ↓
          enlazar
             ↓
        guardar_json
             ↓
      añadir chunks a la lista
            Chunk
                ↓
            Embeddings
                ↓
        Base vectorial
"""

import logging
from pathlib import Path

from src.ingestion.docling_converter import convertir_pdf_a_markdown
from src.ingestion.text_cleaner import limpiar_archivo_markdown
from src.ingestion.document_loader import cargar_documentos
from src.ingestion.markdown_parser import parsear_markdown
from src.knowledge.builder import crear_arbol
from src.knowledge.linker import enlazar
from src.knowledge.exporter import guardar_json
from src.ingestion.chunker import crear_chunks_documentos
from src.rag.embeddings import crear_embeddings_chunks
from src.rag.vector_store import VectorStore

from src.core.config import (
    CARPETA_DOCUMENTOS,
    CARPETA_MARKDOWN_RAW,
    CARPETA_MARKDOWN_CLEAN,
    CARPETA_KNOWLEDGE,
)

logger = logging.getLogger(__name__)

def indexar_documentos() -> None:
    """
    Ejecuta el pipeline completo de indexación.

    Coordina todas las etapas necesarias para transformar los documentos
    en registros almacenados en la base vectorial.
    """

    try:

        logger.info("Iniciando indexación...")

        markdowns = _obtener_markdowns_limpios()
        
        if not markdowns:
            logger.warning("No hay documentos para indexar.")
            return
        
        logger.info("Markdowns obtenidos")
        logger.info("----------------------------------")

        documentos = cargar_documentos(markdowns)
        logger.info("Documentos creados")
        logger.info("----------------------------------")

        chunks = crear_chunks_documentos(documentos)
        logger.info("Chunks de los documentos creados")
        logger.info("----------------------------------")

        embeddings = crear_embeddings_chunks(chunks)
        logger.info("Embeddings creados")
        logger.info("----------------------------------")

        vector_store = VectorStore()

        vector_store.indexar_chunks(
            chunks,
            embeddings,
        )
        logger.info("Vectores indexados")

        logger.info("Indexación finalizada.")
        logger.info("----------------------------------")

    except Exception as error:
        logger.warning("La indexación ha fallado: %s", error)
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
            logger.debug(" Markdown limpio encontrado: %s", ruta_clean.name)

            markdowns_limpios.append(ruta_clean)

            continue

        # NO existe el MD limpio pero SI el raw
        if ruta_raw.exists():
            logger.info("Limpiando Markdown: %s", ruta_raw.name)

            ruta_clean = limpiar_archivo_markdown(ruta_raw, ruta_clean)

            markdowns_limpios.append(ruta_clean)

            continue

        # NO existen los MD limpios/raw solo PDF
        logger.info("Convirtiendo PDF: %s", ruta_pdf.name)

        ruta_raw = convertir_pdf_a_markdown(ruta_pdf)

        ruta_clean = limpiar_archivo_markdown(
            ruta_raw,
            ruta_clean,
        )

        markdowns_limpios.append(ruta_clean)

        logger.debug("Markdown limpio generado: %s", ruta_clean.name)
        
    return markdowns_limpios
