from src.knowledge.models import KnowledgeTree, KnowledgeNode
from src.core.models import Chunk


class GuidedContextBuilder:
    """Construye el contexto necesario para el modo de aprendizaje guiado."""


    def __init__(self, arboles: dict[str, KnowledgeTree]):
        self.arboles = arboles


    def construir(
        self,
        paso: KnowledgeNode,
        chunks: list[Chunk],
        progreso: list,
    ) -> dict:
        """
        Construye el contexto del paso actual.

        Incluye el título del paso, su nodo padre, su ruta jerárquica,
        los chunks recuperados pertenecientes al paso y el progreso
        anterior del alumno.
        """

        chunks_paso = [
            chunk
            for chunk in chunks
                if chunk.node_id == paso.id
        ]

        return {
            "titulo": paso.titulo,
            "padre": paso.padre.titulo if paso.padre else None,
            "ruta": self._obtener_ruta(paso),
            "chunks": chunks_paso,
            "progreso": progreso,
        }

    def _obtener_ruta(self, nodo: KnowledgeNode) -> list[str]:
        """Devuelve la ruta jerárquica desde la raíz hasta el nodo."""

        ruta = []
        actual = nodo

        while actual is not None:
            if actual.titulo is not None:
                ruta.append(actual.titulo)

            actual = actual.padre

        return list(reversed(ruta))