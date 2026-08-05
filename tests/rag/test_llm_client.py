import unittest
from unittest.mock import MagicMock

from src.rag.llm_client import LLMClient

class TestLLMClient(unittest.TestCase):

    def setUp(self):
        self.llm = LLMClient()
        self.prompt = "¿Qué es Python?" 


    def test_consultar_modelo(self):
        """Prueba que la consulta al modelo se realice con los parámetros esperados."""

        respuesta_esperada = MagicMock()

        self.llm.client.chat.completions.create = MagicMock(
            return_value=respuesta_esperada,
        )

        respuesta = self.llm._consultar_modelo(
            self.prompt,
        )

        self.assertEqual(
            respuesta,
            respuesta_esperada,
        )

        self.llm.client.chat.completions.create.assert_called_once_with(
            model=self.llm.modelo,
            messages=[
                {
                    "role": "user",
                    "content": self.prompt,
                }
            ],
            temperature=0,
            reasoning_effort="none",
            reasoning_format="hidden",
            max_completion_tokens=300,
        )


    def test_generar_respuesta(self):
        """Prueba que la respuesta del modelo se devuelva correctamente."""

        respuesta_modelo = MagicMock()

        respuesta_modelo.choices = [
            MagicMock(
                message=MagicMock(
                    content="Python es un lenguaje de programación."
                )
            )
        ]

        respuesta_modelo.usage = MagicMock(
            prompt_tokens=10,
            completion_tokens=8,
            total_tokens=18,
        )

        self.llm._consultar_modelo = MagicMock(
            return_value=respuesta_modelo,
        )

        respuesta = self.llm.generar_respuesta(
            self.prompt,
        )

        self.assertEqual(
            respuesta,
            "Python es un lenguaje de programación.",
        )

        self.llm._consultar_modelo.assert_called_once_with(
            self.prompt,
        )

    def test_generar_respuesta_elimina_bloques_think(self):
        """Prueba que los bloques de razonamiento internos se eliminen de la respuesta."""

        contenido = """
        <think>
        Este es el razonamiento interno del modelo.
        </think>

        Python es un lenguaje de programación.
        """

        respuesta_modelo = MagicMock()

        respuesta_modelo.choices = [
            MagicMock(
                message=MagicMock(
                    content=contenido
                )
            )
        ]

        respuesta_modelo.usage = MagicMock(
            prompt_tokens=10,
            completion_tokens=15,
            total_tokens=25,
        )

        self.llm._consultar_modelo = MagicMock(
            return_value=respuesta_modelo,
        )

        respuesta = self.llm.generar_respuesta(
            self.prompt,
        )

        self.assertEqual(
            respuesta,
            "Python es un lenguaje de programación.",
        )


    def test_generar_respuesta_prompt_vacio(self):
        """Prueba que un prompt vacío produzca un error de validación."""

        with self.assertRaises(ValueError):
            self.llm.generar_respuesta("")


    def test_generar_respuesta_error_modelo(self):
        """Prueba que un error del modelo se convierta en una excepción de runtime."""

        self.llm._consultar_modelo = MagicMock(
            side_effect=Exception("Error de conexión"),
        )

        with self.assertRaises(RuntimeError):
            self.llm.generar_respuesta(
                self.prompt,
            )


if __name__ == "__main__":
    unittest.main()
