import unittest
from unittest.mock import Mock, patch
import numpy as np

from src.rag.embeddings import (
    crear_embedding_texto,
    crear_embeddings_textos,
    crear_embeddings_chunks,
    cargar_modelo,
)

class TestEmbeddings(unittest.TestCase):
    @patch("src.rag.embeddings.SentenceTransformer")
    def test_cargar_modelo(self, mock_modelo):
        """Comprueba que carga el modelo correcto."""

        cargar_modelo.cache_clear()

        modelo = Mock()
        mock_modelo.return_value = modelo

        resultado = cargar_modelo()

        mock_modelo.assert_called_once_with(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.assertIs(resultado, modelo)


    @patch("src.rag.embeddings.SentenceTransformer")
    def test_cargar_modelo_cache(self, mock_modelo):
        """Comprueba que el modelo solo se carga una vez."""

        cargar_modelo.cache_clear()

        modelo = Mock()
        mock_modelo.return_value = modelo

        cargar_modelo()
        cargar_modelo()

        mock_modelo.assert_called_once()


    @patch("src.rag.embeddings.cargar_modelo")
    def test_crear_embedding_texto(self, mock_cargar):
        """Comprueba que crea correctamente un embedding."""

        modelo = Mock()

        modelo.encode.return_value = np.array(
            [1.0, 2.0, 3.0],
            dtype=np.float64,
        )

        mock_cargar.return_value = modelo

        embedding = crear_embedding_texto(" Hola ")

        modelo.encode.assert_called_once_with(
            "hola",
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        np.testing.assert_array_equal(
            embedding,
            np.array([1, 2, 3], dtype=np.float32),
        )

        self.assertEqual(
            embedding.dtype,
            np.float32,
        )


    def test_crear_embedding_texto_vacio(self):
        """Comprueba que no permite textos vacíos."""

        with self.assertRaises(ValueError):
            crear_embedding_texto("")


    def test_crear_embedding_texto_espacios(self):
        """Comprueba que no permite textos con espacios."""

        with self.assertRaises(ValueError):
            crear_embedding_texto("     ")


    def test_crear_embeddings_textos_lista_vacia(self):
        """Comprueba que devuelve una matriz vacía."""

        embeddings = crear_embeddings_textos([])

        self.assertEqual(
            embeddings.shape,
            (0, 0),
        )

        self.assertEqual(
            embeddings.dtype,
            np.float32,
        )


    @patch("src.rag.embeddings.cargar_modelo")
    def test_crear_embeddings_textos(self, mock_cargar):
        """Comprueba que crea embeddings para varios textos."""

        modelo = Mock()

        modelo.encode.return_value = np.array(
            [
                [1, 2],
                [3, 4],
            ],
            dtype=np.float64,
        )

        mock_cargar.return_value = modelo

        embeddings = crear_embeddings_textos(
            [" Hola ", " Mundo "],
            tamanio_lote=8,
        )

        modelo.encode.assert_called_once_with(
            ["hola", "mundo"],
            batch_size=8,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        np.testing.assert_array_equal(
            embeddings,
            np.array(
                [
                    [1, 2],
                    [3, 4],
                ],
                dtype=np.float32,
            ),
        )


    def test_crear_embeddings_textos_texto_vacio(self):
        """Comprueba que detecta textos vacíos."""

        with self.assertRaises(ValueError):
            crear_embeddings_textos(["hola", ""])


    def test_crear_embeddings_textos_texto_espacios(self):
        """Comprueba que detecta textos con espacios."""

        with self.assertRaises(ValueError):
            crear_embeddings_textos(["hola", "   "])


    def test_crear_embeddings_textos_batch_invalido(self):
        """Comprueba que el tamaño del lote sea válido."""

        with self.assertRaises(ValueError):
            crear_embeddings_textos(
                ["hola"],
                tamanio_lote=0,
            )


    @patch("src.rag.embeddings.crear_embeddings_textos")
    def test_crear_embeddings_chunks(
        self,
        mock_crear_embeddings,
    ):
        """Comprueba que obtiene el texto de cada chunk."""

        chunk1 = Mock()
        chunk2 = Mock()

        chunk1.texto_embedding.return_value = "texto 1"
        chunk2.texto_embedding.return_value = "texto 2"

        crear_embeddings_chunks(
            [chunk1, chunk2],
            tamanio_lote=4,
        )

        chunk1.texto_embedding.assert_called_once()
        chunk2.texto_embedding.assert_called_once()

        mock_crear_embeddings.assert_called_once_with(
            textos=[
                "texto 1",
                "texto 2",
            ],
            tamanio_lote=4,
        )


if __name__ == "__main__":
    unittest.main()
