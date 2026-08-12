import unittest
from unittest.mock import Mock, patch

from src.rag.rag_pipeline import RAG
from src.knowledge.models import KnowledgeNode, KnowledgeTree


class TestRAG(unittest.TestCase):

    def setUp(self):
        """Prepara los mocks y el árbol de conocimiento de prueba."""

        self.paso_1 = KnowledgeNode(
            id="paso-1",
            titulo="Paso 1",
            nivel=1,
        )

        self.paso_2 = KnowledgeNode(
            id="paso-2",
            titulo="Paso 2",
            nivel=1,
        )

        self.raiz = KnowledgeNode(
            id="proceso",
            titulo="Proceso",
            nivel=0,
            hijos=[self.paso_1, self.paso_2],
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

    @patch("src.rag.rag_pipeline.GuidedContextBuilder")
    @patch("src.rag.rag_pipeline.IntentClassifier")
    @patch("src.rag.rag_pipeline.ContextExpander")
    @patch("src.rag.rag_pipeline.Historial")
    @patch("src.rag.rag_pipeline.LLMClient")
    @patch("src.rag.rag_pipeline.ConstructorPrompts")
    @patch("src.rag.rag_pipeline.Retriever")
    def test_responder_inicia_guia(
        self,
        mock_retriever_cls,
        mock_prompt_cls,
        mock_llm_cls,
        mock_historial_cls,
        mock_context_expander_cls,
        mock_intent_classifier_cls,
        mock_guided_context_builder_cls,
    ):
        """Comprueba que inicia correctamente el modo guiado."""

        retriever = mock_retriever_cls.return_value
        prompt_builder = mock_prompt_cls.return_value
        llm = mock_llm_cls.return_value
        historial = mock_historial_cls.return_value
        context_expander = mock_context_expander_cls.return_value
        intent_classifier = mock_intent_classifier_cls.return_value
        guided_context_builder = mock_guided_context_builder_cls.return_value

        historial.obtener_contexto.return_value = []

        candidatos = []
        candidatos_expandidos = []
        intencion = Mock()

        retriever.recuperar_candidatos.return_value = candidatos
        context_expander.expandir.return_value = candidatos_expandidos
        intent_classifier.clasificar.return_value = intencion

        guided_context_builder.construir.return_value = "CONTEXTO GUIADO"
        prompt_builder.construir_prompt_guiado.return_value = "PROMPT GUIADO"
        llm.generar_respuesta.return_value = "RESPUESTA"

        rag = RAG(self.arboles)

        respuesta = rag.responder(
            "Quiero empezar",
            "lean_startup",
            modo_guiado=True,
        )

        self.assertTrue(
            rag.guided_mode.esta_activo(),
        )

        self.assertEqual(
            rag.guided_mode.obtener_paso_actual(),
            self.paso_1,
        )

        guided_context_builder.construir.assert_called_once_with(
            paso=self.paso_1,
            chunks=candidatos_expandidos,
            progreso=[],
        )

        prompt_builder.construir_prompt_guiado.assert_called_once_with(
            historial.obtener_contexto.return_value,
            "Quiero empezar",
            "CONTEXTO GUIADO",
        )

        llm.generar_respuesta.assert_called_once_with(
            "PROMPT GUIADO",
        )

        self.assertEqual(
            respuesta,
            "RESPUESTA",
        )


    @patch("src.rag.rag_pipeline.GuidedContextBuilder")
    @patch("src.rag.rag_pipeline.IntentClassifier")
    @patch("src.rag.rag_pipeline.ContextExpander")
    @patch("src.rag.rag_pipeline.Historial")
    @patch("src.rag.rag_pipeline.LLMClient")
    @patch("src.rag.rag_pipeline.ConstructorPrompts")
    @patch("src.rag.rag_pipeline.Retriever")
    def test_responder_procesa_respuesta_en_guia(
        self,
        mock_retriever_cls,
        mock_prompt_cls,
        mock_llm_cls,
        mock_historial_cls,
        mock_context_expander_cls,
        mock_intent_classifier_cls,
        mock_guided_context_builder_cls,
    ):
        """Comprueba que procesa una respuesta y avanza al siguiente paso."""

        retriever = mock_retriever_cls.return_value
        prompt_builder = mock_prompt_cls.return_value
        llm = mock_llm_cls.return_value
        historial = mock_historial_cls.return_value
        context_expander = mock_context_expander_cls.return_value
        intent_classifier = mock_intent_classifier_cls.return_value
        guided_context_builder = mock_guided_context_builder_cls.return_value

        historial.obtener_contexto.return_value = []

        candidatos = []
        candidatos_expandidos = []
        intencion = Mock()

        retriever.recuperar_candidatos.return_value = candidatos
        context_expander.expandir.return_value = candidatos_expandidos
        intent_classifier.clasificar.return_value = intencion

        guided_context_builder.construir.return_value = "CONTEXTO GUIADO"
        prompt_builder.construir_prompt_guiado.return_value = "PROMPT GUIADO"
        llm.generar_respuesta.return_value = "RESPUESTA"

        rag = RAG(self.arboles)

        # Simula que la guía ya estaba iniciada.
        rag.guided_mode.iniciar(self.raiz)
        
        respuesta = rag.responder(
            "Respuesta del alumno",
            "lean_startup",
            modo_guiado=True,
        )

        # La respuesta se ha registrado en el progreso.
        self.assertEqual(
            rag.guided_mode.progreso,
            [
                {
                    "paso": "Paso 1",
                    "respuesta": "Respuesta del alumno",
                }
            ],
        )

        # La guía ha avanzado al siguiente paso.
        self.assertEqual(
            rag.guided_mode.obtener_paso_actual(),
            self.paso_2,
        )

        guided_context_builder.construir.assert_called_once_with(
            paso=self.paso_2,
            chunks=candidatos_expandidos,
            progreso=rag.guided_mode.progreso,
        )

        prompt_builder.construir_prompt_guiado.assert_called_once_with(
            historial.obtener_contexto.return_value,
            "Respuesta del alumno",
            "CONTEXTO GUIADO",
        )

        llm.generar_respuesta.assert_called_once_with(
            "PROMPT GUIADO",
        )

        self.assertEqual(
            respuesta,
            "RESPUESTA",
        )


            
if __name__ == "__main__":
    unittest.main()
    