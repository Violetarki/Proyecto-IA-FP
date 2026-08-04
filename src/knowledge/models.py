from __future__ import annotations

from dataclasses import dataclass, field

from src.core.models import Metodologia


@dataclass
class KnowledgeNode:
    """
    Representa un apartado del conocimiento.

    Cada nodo corresponde a un encabezado Markdown (#, ##, ### o ####)
    y mantiene las relaciones jerárquicas con el resto de apartados
    del manual.
    """

    titulo: str | None

    nivel: int

    padre: KnowledgeNode | None = None

    hijos: list[KnowledgeNode] = field(default_factory=list)


@dataclass
class KnowledgeTree:
    """
    Representa el árbol de conocimiento de una metodología.
    """

    metodologia: Metodologia

    raiz: KnowledgeNode
