import unittest
from unittest.mock import Mock, patch

from src.rag.rag_pipeline import RAG
from src.knowledge.models import KnowledgeNode, KnowledgeTree


class TestRAG(unittest.TestCase):

    def setUp(self):
        """Prepara los mocks y el árbol de conocimiento de prueba."""

        self.paso = KnowledgeNode(
            id="paso-1",
            titulo="Paso 1",
            nivel=1,
        )

        self.raiz = KnowledgeNode(
            id="proceso",
            titulo="Proceso",
            nivel=0,
            hijos=[self.paso],
        )

        self.arboles = {
            "lean_startup": KnowledgeTree(
                raiz=self.raiz,
                metodologia="MetodologiaTest",
            ),
        }


    @patch("src.rag.rag_pipeline.IntentClassifier")
    @patch("src.rag.rag_pipeline.ContextExpander")
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
        mock_context_expander_cls,
        mock_intent_classifier_cls,
    ):
        """Comprueba que ejecuta correctamente el flujo RAG."""

        retriever = mock_retriever_cls.return_value
        prompt_builder = mock_prompt_cls.return_value
        llm = mock_llm_cls.return_value
        historial = mock_historial_cls.return_value
        context_expander = mock_context_expander_cls.return_value
        intent_classifier = mock_intent_classifier_cls.return_value

        historial.obtener_contexto.return_value = []

        candidatos = [Mock(), Mock()]
        candidatos_expandidos = [Mock()]

        retriever.recuperar_candidatos.return_value = candidatos
        context_expander.expandir.return_value = candidatos_expandidos

        intent_classifier.clasificar.return_value = Mock()

        prompt_builder.construir_prompt.return_value = "PROMPT"

        llm.generar_respuesta.return_value = "RESPUESTA"

        rag = RAG(self.arboles)

        respuesta = rag.responder(
            "¿Qué es DAFO?",
            "lean_startup",
        )

        historial.obtener_contexto.assert_called_once_with(
            rag.id_conversacion,
        )

        retriever.recuperar_candidatos.assert_called_once_with(
            "¿Qué es DAFO?",
            "lean_startup",
        )

        context_expander.expandir.assert_called_once_with(
            candidatos,
            intent_classifier.clasificar.return_value,
        )

        prompt_builder.construir_prompt.assert_called_once_with(
            historial.obtener_contexto.return_value,
            "¿Qué es DAFO?",
            candidatos_expandidos,
        )

        llm.generar_respuesta.assert_called_once_with(
            "PROMPT",
        )

        self.assertEqual(
            respuesta,
            "RESPUESTA",
        )

    @patch("src.rag.rag_pipeline.IntentClassifier")
    @patch("src.rag.rag_pipeline.ContextExpander")
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
        mock_context_expander_cls,
        mock_intent_classifier_cls,
    ):
        """Comprueba que guarda pregunta y respuesta en el historial."""

        retriever = mock_retriever_cls.return_value
        prompt_builder = mock_prompt_cls.return_value
        llm = mock_llm_cls.return_value
        historial = mock_historial_cls.return_value
        context_expander = mock_context_expander_cls.return_value
        intent_classifier = mock_intent_classifier_cls.return_value

        historial.obtener_contexto.return_value = []

        candidatos = []
        candidatos_expandidos = []

        retriever.recuperar_candidatos.return_value = candidatos
        context_expander.expandir.return_value = candidatos_expandidos
        intent_classifier.clasificar.return_value = Mock()

        prompt_builder.construir_prompt.return_value = "PROMPT"
        llm.generar_respuesta.return_value = "RESPUESTA"

        rag = RAG(self.arboles)

        rag.responder(
            "hola",
            "lean_startup",
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

        
    @patch("src.rag.rag_pipeline.GuidedContextBuilder")
    @patch("src.rag.rag_pipeline.ContextExpander")
    @patch("src.rag.rag_pipeline.IntentClassifier")
    @patch("src.rag.rag_pipeline.Historial")
    @patch("src.rag.rag_pipeline.LLMClient")
    @patch("src.rag.rag_pipeline.ConstructorPrompts")
    @patch("src.rag.rag_pipeline.Retriever")
    def test_constructor(
        self,
        mock_retriever_cls,
        mock_prompt_cls,
        mock_llm_cls,
        mock_historial_cls,
        mock_intent_classifier_cls,
        mock_context_expander_cls,
        mock_guided_context_builder_cls,
    ):
        """Comprueba que inicializa los componentes."""

        rag = RAG(self.arboles)

        mock_retriever_cls.assert_called_once()
        mock_prompt_cls.assert_called_once()
        mock_llm_cls.assert_called_once()
        mock_historial_cls.assert_called_once()
        mock_intent_classifier_cls.assert_called_once()

        mock_context_expander_cls.assert_called_once_with(
            self.arboles,
            rag.historial,
        )

        mock_guided_context_builder_cls.assert_called_once_with(
            self.arboles,
        )

        self.assertIsInstance(
            rag.id_conversacion,
            str,
        )

        self.assertTrue(
            len(rag.id_conversacion) > 0,
        )

            
if __name__ == "__main__":
    unittest.main()
    