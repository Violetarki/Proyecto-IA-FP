import unittest

from src.rag.intent_classifier import IntentClassifier


class TestIntentClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = IntentClassifier()

    def test_es_peticion_de_pasos(self):
        preguntas = [
            "¿Qué pasos tengo que seguir?",
            "¿Qué pasos debo seguir?",
            "¿Cómo hacer una solicitud?",
            "¿Cómo realizar el proceso?",
            "¿Cómo seguir el procedimiento?",
            "¿Cómo llevar a cabo el proceso?",
            "¿Qué tengo que hacer?",
            "¿Qué debo hacer?",
            "Guíame",
        ]

        for pregunta in preguntas:
            with self.subTest(pregunta=pregunta):
                self.assertTrue(
                    self.classifier.es_peticion_de_pasos(pregunta)
                )

    def test_no_es_peticion_de_pasos(self):
        preguntas = [
            "¿Qué es este proceso?",
            "¿Por qué se hace este proceso?",
            "¿Cuál es el objetivo?",
            "Explícame este concepto",
            "¿Cuánto cuesta?",
            "¿Quién realiza el proceso?",
        ]

        for pregunta in preguntas:
            with self.subTest(pregunta=pregunta):
                self.assertFalse(
                    self.classifier.es_peticion_de_pasos(pregunta)
                )

    def test_ignora_mayusculas(self):
        pregunta = "¿QUÉ PASOS TENGO QUE SEGUIR?"

        resultado = self.classifier.es_peticion_de_pasos(pregunta)

        self.assertTrue(resultado)

    def test_ignora_espacios_exteriores(self):
        pregunta = "   ¿Qué pasos tengo que seguir?   "

        resultado = self.classifier.es_peticion_de_pasos(pregunta)

        self.assertTrue(resultado)


if __name__ == "__main__":
    unittest.main()