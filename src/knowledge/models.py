from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from src.core.models import Metodologia


@dataclass
class KnowledgeNode:
    """
    Representa un apartado del conocimiento.

    Cada nodo corresponde a un encabezado Markdown (#, ##, ###, #### o #####)
    y mantiene las relaciones jerárquicas con el resto de apartados del manual.
    """     
    id: str
    
    titulo: str | None = None
    
    nivel: int = 0       

    padre: KnowledgeNode | None = None

    hijos: list[KnowledgeNode] = field(default_factory=list)   
    
    chunk_ids: list[int] = field(default_factory=list)


@dataclass
class KnowledgeTree:
    """
    Representa el árbol de conocimiento de una metodología.
    """

    metodologia: Metodologia

    raiz: KnowledgeNode
