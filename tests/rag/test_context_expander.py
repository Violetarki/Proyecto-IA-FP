import unittest
from unittest.mock import Mock

from src.core.config import (
    UMBRAL_ACEPTABLE,
    UMBRAL_BUENO,
    UMBRAL_EXCELENTE,
)
from src.core.models import (
    Chunk,
    Documento,
    Metodologia,
    ResultadoBusqueda,
)
from src.knowledge.models import KnowledgeNode, KnowledgeTree
from src.rag.context_expander import ContextExpander


class TestContextExpander(unittest.TestCase):

    def setUp(self):
        self.metodologia = Metodologia("MetodologiaTest")

        self.documento = Documento(
            metodologia=self.metodologia,
            nombre="DocumentoTest",
            texto="Texto del documento",
            ruta="documento.md",
        )

        # Construcción del árbol:
        #
        # Raíz
        # └── Proceso
        #     ├── Paso 1
        #     └── Paso 2

        self.raiz = KnowledgeNode(
            id="raiz",
            titulo="Raíz",
            nivel=0,
        )

        self.proceso = KnowledgeNode(
            id="proceso",
            titulo="Proceso",
            nivel=1,
            padre=self.raiz,
        )

        self.paso_1 = KnowledgeNode(
            id="paso-1",
            titulo="Paso 1",
            nivel=2,
            padre=self.proceso,
        )

        self.paso_2 = KnowledgeNode(
            id="paso-2",
            titulo="Paso 2",
            nivel=2,
            padre=self.proceso,
        )

        self.raiz.hijos = [self.proceso]
        self.proceso.hijos = [self.paso_1, self.paso_2]

        self.arbol = KnowledgeTree(
            metodologia=self.metodologia,
            raiz=self.raiz,
        )

        self.historial = Mock()

        self.expander = ContextExpander(
            self.arbol,
            self.historial,
        )

        self.chunk_1 = Chunk(
            documento=self.documento,
            indice=1,
            texto="Texto del paso 1",
            node_id="paso-1",
        )

        self.chunk_2 = Chunk(
            documento=self.documento,
            indice=2,
            texto="Texto del paso 2",
            node_id="paso-2",
        )

        self.chunk_proceso = Chunk(
            documento=self.documento,
            indice=3,
            texto="Texto del proceso",
            node_id="proceso",
        )

        self.paso_1.chunk_ids = [1]
        self.paso_2.chunk_ids = [2]
        self.proceso.chunk_ids = [3]

    def test_aplicar_umbrales_prioriza_excelentes(self):
        resultados = [
            ResultadoBusqueda(self.chunk_1, UMBRAL_EXCELENTE),
            ResultadoBusqueda(self.chunk_2, UMBRAL_EXCELENTE),
            ResultadoBusqueda(self.chunk_proceso, UMBRAL_BUENO),
        ]

        resultado = self.expander._aplicar_umbrales(
            resultados,
        )

        self.assertEqual(
            resultado,
            [self.chunk_1, self.chunk_2],
        )

    def test_aplicar_umbrales_usa_buenos_si_no_hay_suficientes_excelentes(
        self,
    ):
        resultados = [
            ResultadoBusqueda(self.chunk_1, UMBRAL_BUENO),
            ResultadoBusqueda(self.chunk_2, UMBRAL_BUENO),
        ]

        resultado = self.expander._aplicar_umbrales(
            resultados,
        )

        self.assertEqual(
            resultado,
            [self.chunk_1, self.chunk_2],
        )

    def test_aplicar_umbrales_usa_aceptables_si_no_hay_suficientes_buenos(
        self,
    ):
        resultados = [
            ResultadoBusqueda(
                self.chunk_1,
                UMBRAL_ACEPTABLE,
            ),
            ResultadoBusqueda(
                self.chunk_2,
                UMBRAL_ACEPTABLE,
            ),
        ]

        resultado = self.expander._aplicar_umbrales(
            resultados,
        )

        self.assertEqual(
            resultado,
            [self.chunk_1, self.chunk_2],
        )

    def test_obtener_nodo_encuentra_nodo(self):
        resultado = self.expander._obtener_nodo("paso-1")

        self.assertIs(
            resultado,
            self.paso_1,
        )

    def test_obtener_nodo_devuelve_none_si_no_existe(self):
        resultado = self.expander._obtener_nodo("no-existe")

        self.assertIsNone(resultado)

    
    def test_eliminar_duplicados_conserva_el_orden(self):
        chunks = [
            self.chunk_1,
            self.chunk_2,
            self.chunk_1,
        ]

        resultado = self.expander._eliminar_duplicados(chunks)

        self.assertEqual(
            resultado,
            [
                self.chunk_1,
                self.chunk_2,
            ],
        )

   
    def test_enriquecer_con_hijos_anade_hijo_recuperado(self):
        resultado = self.expander._enriquecer_con_hijos(
            [self.chunk_proceso, self.chunk_1]
        )

        self.assertEqual(
            resultado,
            [
                self.chunk_proceso,
                self.chunk_1,
                self.chunk_1,
            ],
        )

    def test_ordenar_por_jerarquia(self):
        chunks = [
            self.chunk_2,
            self.chunk_1,
        ]

        resultado = self.expander._ordenar_por_jerarquia(chunks)

        self.assertEqual(
            resultado,
            [
                self.chunk_1,
                self.chunk_2,
            ],
        )

    def test_expandir_elimina_duplicados_y_ordena(self):
        resultados = [
            ResultadoBusqueda(self.chunk_2, UMBRAL_EXCELENTE),
            ResultadoBusqueda(self.chunk_1, UMBRAL_EXCELENTE),
        ]

        resultado = self.expander.expandir(resultados)

        self.assertEqual(
            resultado,
            [
                self.chunk_1,
                self.chunk_2,
            ],
        )


if __name__ == "__main__":
    unittest.main()