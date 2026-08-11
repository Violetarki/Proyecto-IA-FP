"""
Prueba manual para generar los árboles de conocimiento de cada metodología.
"""

import logging

from src.core.config import CARPETA_KNOWLEDGE, CARPETA_MARKDOWN_CLEAN
from src.ingestion.document_loader import cargar_documentos
from src.ingestion.markdown_parser import parsear_markdown
from src.knowledge.builder import crear_arbol
from src.knowledge.exporter import guardar_json

logger = logging.getLogger(__name__)


def main() -> None:
    """Genera un KnowledgeTree por cada metodología."""

    markdowns = list(CARPETA_MARKDOWN_CLEAN.rglob("*.md"))

    documentos = cargar_documentos(markdowns)

    for documento in documentos:

        raiz_markdown = parsear_markdown(documento.texto)

        arbol = crear_arbol(
            raiz_markdown,
            documento.metodologia,
        )

        ruta = CARPETA_KNOWLEDGE / f"{documento.metodologia.nombre}.json"

        guardar_json(arbol, ruta)

        logger.info(
            "Árbol generado: %s",
            ruta.name,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
