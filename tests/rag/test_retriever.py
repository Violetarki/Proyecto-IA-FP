import unittest
from unittest.mock import Mock, patch

from src.rag.retriever import Retriever


class TestRetriever(unittest.TestCase):
    
    def test_extraer_palabras_clave(self):
        """Comprueba que elimina las stopwords."""

        retriever = Retriever()

        resultado = retriever._extraer_palabras_clave(
            "¿Qué es el análisis DAFO?"
        )

        self.assertEqual(
            resultado,
            ["análisis", "dafo"],
        )
        
    def test_extraer_palabras_clave_solo_stopwords(self):
        """Comprueba que devuelve una lista vacía."""

        retriever = Retriever()

        resultado = retriever._extraer_palabras_clave(
            "qué es el de la"
        )

        self.assertEqual(
            resultado,
            [],
        )
        
    def test_coincidencias(self):
        """Comprueba que cuenta las palabras presentes."""

        retriever = Retriever()

        chunk = Mock()
        chunk.jerarquia.return_value = [
            "Análisis",
            "DAFO",
        ]
        chunk.texto = "Fortalezas y debilidades."

        coincidencias = retriever._coincidencias(
            chunk,
            ["dafo", "fortalezas", "cadena"],
        )

        self.assertEqual(
            coincidencias,
            2,
        )
    
    def test_coincidencias_cero(self):
        """Comprueba que devuelve cero cuando no hay coincidencias."""

        retriever = Retriever()

        chunk = Mock()
        chunk.jerarquia.return_value = ["Marketing"]
        chunk.texto = "Producto precio plaza."

        coincidencias = retriever._coincidencias(
            chunk,
            ["dafo"],
        )

        self.assertEqual(
            coincidencias,
            0,
        )
    
    @patch.object(Retriever, "_coincidencias")
    def test_filtrar_palabras_clave(
        self,
        mock_coincidencias,
    ):
        """Comprueba que filtra correctamente."""

        retriever = Retriever()

        chunk1 = Mock()
        chunk2 = Mock()
        chunk3 = Mock()

        mock_coincidencias.side_effect = [
            3,
            3,
            1,
        ]

        resultado = retriever._filtrar_por_palabras_clave(
            "fortalezas debilidades oportunidades amenazas",
            [
                chunk1,
                chunk2,
                chunk3,
            ],
        )

        self.assertEqual(
            resultado,
            [chunk1, chunk2],
        )


    @patch.object(Retriever, "_coincidencias")
    def test_filtrar_palabras_clave_minimo(
        self,
        mock_coincidencias,
    ):
        """Comprueba que devuelve los originales si el filtrado deja pocos."""

        retriever = Retriever()

        chunk1 = Mock()
        chunk2 = Mock()

        mock_coincidencias.side_effect = [
            3,
            1,
        ]

        resultado = retriever._filtrar_por_palabras_clave(
            "fortalezas debilidades oportunidades amenazas",
            [
                chunk1,
                chunk2,
            ],
        )

        self.assertEqual(
            resultado,
            [
                chunk1,
                chunk2,
            ],
        )
        
    def test_filtrar_palabras_clave_sin_palabras(self):
        """Comprueba que devuelve los chunks originales."""

        retriever = Retriever()

        chunks = [Mock(), Mock()]

        resultado = retriever._filtrar_por_palabras_clave(
            "qué es el de la",
            chunks,
        )

        self.assertEqual(
            resultado,
            chunks,
        )
    
    
    @patch.object(Retriever, "recuperar_chunks")
    def test_recuperar_contexto(
        self,
        mock_recuperar,
    ):
        """Comprueba que delega en recuperar_chunks."""

        retriever = Retriever()

        mock_recuperar.return_value = ["chunk"]

        resultado = retriever.recuperar_contexto(
            "pregunta",
            "lean",
            5,
        )

        mock_recuperar.assert_called_once_with(
            "pregunta",
            "lean",
            5,
        )

        self.assertEqual(
            resultado,
            ["chunk"],
        )
        
    def test_recuperar_chunks_pregunta_vacia(self):
        """Comprueba que valida la pregunta."""

        retriever = Retriever()

        with self.assertRaises(ValueError):
            retriever.recuperar_chunks(
                "",
                "lean",
                5,
            )
            
            
    def test_recuperar_chunks_k_invalido(self):
        """Comprueba que valida k."""

        retriever = Retriever()

        with self.assertRaises(ValueError):
            retriever.recuperar_chunks(
                "hola",
                "lean",
                0,
            )
            
    def test_recuperar_chunks_metodologia_vacia(self):
        """Comprueba que valida la metodología."""

        retriever = Retriever()

        with self.assertRaises(ValueError):
            retriever.recuperar_chunks(
                "hola",
                "",
                5,
            )
            
    @patch("src.rag.retriever.crear_embedding_texto")
    @patch.object(Retriever, "_filtrar_por_palabras_clave")
    def test_recuperar_chunks(
        self,
        mock_filtrar,
        mock_embedding,
    ):
        """Comprueba la recuperación completa."""

        retriever = Retriever()

        embedding = Mock()
        mock_embedding.return_value = embedding

        encontrados = [Mock(), Mock()]
        retriever.vector_store.buscar = Mock(
            return_value=encontrados
        )

        mock_filtrar.return_value = ["final"]

        resultado = retriever.recuperar_chunks(
            "pregunta",
            "lean",
            5,
        )

        mock_embedding.assert_called_once_with(
            "pregunta",
        )

        retriever.vector_store.buscar.assert_called_once_with(
            embedding,
            "lean",
            5,
        )

        mock_filtrar.assert_called_once_with(
            "pregunta",
            encontrados,
        )

        self.assertEqual(
            resultado,
            ["final"],
        )
        
        
if __name__ == "__main__":
    unittest.main()
