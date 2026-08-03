import unittest
from unittest.mock import Mock, patch

from src.rag.rag_pipeline import RAG


class TestRAG(unittest.TestCase):

    @patch("src.rag.rag_pipeline.Historial")
    @patch("src.rag.rag_pipeline.LLMClient")
    @patch("src.rag.rag_pipeline.ConstructorPrompts")
    @patch("src.rag.rag_pipeline.Retriever")
    def test_responder(
        self,
        mock_retriever_cls,
        mock_prompt_cls,
        mock_llm_cls,
        mock_historial_cls,
    ):
        """Comprueba que ejecuta correctamente el flujo RAG."""

        retriever = mock_retriever_cls.return_value
        prompt_builder = mock_prompt_cls.return_value
        llm = mock_llm_cls.return_value
        historial = mock_historial_cls.return_value

        historial.obtener_contexto.return_value = [
            Mock(),
        ]

        chunks = [Mock(), Mock()]
        retriever.recuperar_contexto.return_value = chunks

        prompt_builder.construir_prompt.return_value = "PROMPT"

        llm.generar_respuesta.return_value = "RESPUESTA"

        rag = RAG()

        respuesta = rag.responder(
            "¿Qué es DAFO?",
            "lean_startup",
        )

        historial.obtener_contexto.assert_called_once_with(
            rag.id_conversacion,
        )

        retriever.recuperar_contexto.assert_called_once_with(
            "¿Qué es DAFO?",
            "lean_startup",
        )

        prompt_builder.construir_prompt.assert_called_once_with(
            historial.obtener_contexto.return_value,
            "¿Qué es DAFO?",
            chunks,
        )

        llm.generar_respuesta.assert_called_once_with(
            "PROMPT",
        )

        self.assertEqual(
            respuesta,
            "RESPUESTA",
        )

    @patch("src.rag.rag_pipeline.Historial")
    @patch("src.rag.rag_pipeline.LLMClient")
    @patch("src.rag.rag_pipeline.ConstructorPrompts")
    @patch("src.rag.rag_pipeline.Retriever")
    def test_guarda_historial(
        self,
        mock_retriever_cls,
        mock_prompt_cls,
        mock_llm_cls,
        mock_historial_cls,
    ):
        """Comprueba que guarda pregunta y respuesta."""

        retriever = mock_retriever_cls.return_value
        prompt_builder = mock_prompt_cls.return_value
        llm = mock_llm_cls.return_value
        historial = mock_historial_cls.return_value

        historial.obtener_contexto.return_value = []

        retriever.recuperar_contexto.return_value = []

        prompt_builder.construir_prompt.return_value = "PROMPT"

        llm.generar_respuesta.return_value = "RESPUESTA"

        rag = RAG()

        rag.responder(
            "hola",
            "lean",
        )

        self.assertEqual(
            historial.agregar_mensaje.call_count,
            2,
        )

        primera = historial.agregar_mensaje.call_args_list[0]
        segunda = historial.agregar_mensaje.call_args_list[1]

        self.assertEqual(
            primera.args[1].rol,
            "user",
        )

        self.assertEqual(
            primera.args[1].contenido,
            "hola",
        )

        self.assertEqual(
            segunda.args[1].rol,
            "bot",
        )

        self.assertEqual(
            segunda.args[1].contenido,
            "RESPUESTA",
        )
        
    @patch("src.rag.rag_pipeline.Historial")
    @patch("src.rag.rag_pipeline.LLMClient")
    @patch("src.rag.rag_pipeline.ConstructorPrompts")
    @patch("src.rag.rag_pipeline.Retriever")
    def test_constructor(
        self,
        mock_retriever,
        mock_prompt,
        mock_llm,
        mock_historial,
    ):
        """Comprueba que inicializa los componentes."""

        rag = RAG()

        mock_retriever.assert_called_once()
        mock_prompt.assert_called_once()
        mock_llm.assert_called_once()
        mock_historial.assert_called_once()

        self.assertIsInstance(
            rag.id_conversacion,
            str,
        )

        self.assertTrue(
            len(rag.id_conversacion) > 0,
        )
        
if __name__ == "__main__":
    unittest.main()
    