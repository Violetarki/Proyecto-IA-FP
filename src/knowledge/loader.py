
from pathlib import Path
import json

from src.knowledge.models import KnowledgeTree, KnowledgeNode
from src.core.models import Metodologia


def cargar_arbol(ruta: str | Path) -> KnowledgeTree:
    """
    Carga un KnowledgeTree desde un fichero JSON.
    """

    ruta = Path(ruta)

    with ruta.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    raiz = _dict_a_nodo(datos["raiz"])

    return KnowledgeTree(
        metodologia=Metodologia(datos["metodologia"]),
        raiz=raiz
    )


def _dict_a_nodo(datos: dict) -> KnowledgeNode:
    """
    Convierte recursivamente un diccionario JSON
    en un KnowledgeNode.
    """

    nodo = KnowledgeNode(
        id=datos.get("id"),
        titulo=datos.get("titulo"),
        nivel=datos.get("nivel"),
        chunk_ids=datos.get("chunk_ids", [])
    )

    nodo.hijos = [
        _dict_a_nodo(hijo)
        for hijo in datos.get("hijos", [])
    ]

    for hijo in nodo.hijos:
        hijo.padre = nodo

    return nodo