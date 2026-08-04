"""
Módulo que se encarga de construir un KnowledgeTree a partir de un documento Markdown.

Recibirá un Documento: def crear_arbol(documento: Documento) -> KnowledgeTree:

Y devolverá: KnowledgeTree
"""

from src.core.models import Documento, Metodologia
from src.ingestion.markdown_parser import MarkdownNode, parsear_markdown
from src.knowledge.models import KnowledgeNode, KnowledgeTree


def crear_arbol(
    raiz_markdown: MarkdownNode,
    metodologia: Metodologia,
) -> KnowledgeTree:
    """
    Construye un árbol de conocimiento a partir del árbol de
    encabezados Markdown.
    """

    raiz_knowledge = _convertir_nodo(raiz_markdown, padre=None)
    return KnowledgeTree(raiz=raiz_knowledge, metodologia=metodologia)


def _convertir_nodo(
    nodo_markdown: MarkdownNode,
    padre: KnowledgeNode | None,
) -> KnowledgeNode:
    """
    Convierte recursivamente un MarkdownNode en un KnowledgeNode.
    """

    nodo_knowledge = KnowledgeNode(
        titulo=nodo_markdown.titulo,
        contenido=nodo_markdown.texto,
        padre=padre,
    )

    for hijo_markdown in nodo_markdown.hijos:
        hijo_knowledge = _convertir_nodo(hijo_markdown, padre=nodo_knowledge)
        nodo_knowledge.hijos.append(hijo_knowledge)

    return nodo_knowledge