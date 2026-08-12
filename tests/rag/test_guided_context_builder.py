import unittest

from src.core.models import Chunk, Documento, Metodologia
from src.knowledge.models import KnowledgeNode, KnowledgeTree
from src.rag.guided_context_builder import GuidedContextBuilder

class TestGuidedContextBuilder(unittest.TestCase):


    def setUp(self):
        self.metodologia = Metodologia(
            nombre="MetodologiaTest",
        )

        self.documento = Documento(
            metodologia=self.metodologia,
            nombre="DocumentoTest",
            texto="Texto del documento",
            ruta="documentos/test.md",
        )

        self.raiz = KnowledgeNode(
            id="raiz",
            titulo="Proceso",
            nivel=0,
        )

        self.fase = KnowledgeNode(
            id="fase",
            titulo="Fase 1",
            nivel=1,
            padre=self.raiz,
        )

        self.paso = KnowledgeNode(
            id="paso",
            titulo="Paso 1",
            nivel=2,
            padre=self.fase,
        )

        self.raiz.hijos = [self.fase]
        self.fase.hijos = [self.paso]

        self.chunk_paso = Chunk(
            documento=self.documento,
            indice=0,
            texto="Contenido del paso",
            node_id="paso",
        )

        self.chunks = [self.chunk_paso]

        self.progreso = [
            {
                "paso": "Paso anterior",
                "respuesta": "Respuesta del alumno",
            }
        ]

        self.arbol = KnowledgeTree(
            metodologia=self.metodologia,
            raiz=self.raiz,
        )

        self.builder = GuidedContextBuilder(self.arbol)


    def test_construir_contexto_paso(self):
        """Construye correctamente el contexto del paso actual."""

        contexto = self.builder.construir(
            paso=self.paso,
            chunks=self.chunks,
            progreso=self.progreso,
        )

        assert contexto["titulo"] == "Paso 1"
        assert contexto["padre"] == "Fase 1"
        assert contexto["ruta"] == [
            "Proceso",
            "Fase 1",
            "Paso 1",
        ]
        assert contexto["chunks"] == [self.chunk_paso]
        assert contexto["progreso"] == self.progreso

    def test_construir_solo_incluye_chunks_del_paso(self):
        """Solo incluye los chunks pertenecientes al paso actual."""

        chunk_otro_paso = Chunk(
            documento=self.documento,
            indice=1,
            texto="Contenido de otro paso",
            node_id="otro_paso",
        )

        chunks = [
            self.chunk_paso,
            chunk_otro_paso,
        ]

        contexto = self.builder.construir(
            paso=self.paso,
            chunks=chunks,
            progreso=self.progreso,
        )

        self.assertEqual(
            contexto["chunks"],
            [self.chunk_paso],
        )

    def test_construir_paso_sin_padre(self):
        """Construye correctamente el contexto de un nodo sin padre."""

        paso = KnowledgeNode(
            id="paso_sin_padre",
            titulo="Paso raíz",
            nivel=0,
        )

        contexto = self.builder.construir(
            paso=paso,
            chunks=[],
            progreso=[],
        )

        self.assertIsNone(contexto["padre"])
        self.assertEqual(
            contexto["ruta"],
            ["Paso raíz"],
        )

    
if __name__ == "__main__":
    unittest.main()