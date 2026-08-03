import unittest

from src.core.models import Chunk, Documento, Mensaje
from src.rag.prompt_builder import ConstructorPrompts, INSTRUCCIONES


class TestConstruirPrompt(unittest.TestCase):
    """Prueba la construcción y el formateo de prompts del módulo prompt builder."""


    def setUp(self):
        """Prepara un constructor de prompts y datos de ejemplo para cada prueba."""
        self.constructor = ConstructorPrompts()

        self.documento = Documento(
            metodologia=None,
            nombre="documento_prueba.pdf",
            ruta="documento_prueba.pdf",
            texto="Texto del documento de prueba."
        )

        self.chunk1 = Chunk(
            documento=self.documento,
            indice=0,
            texto="Texto del primer chunk.",
            titulo="1. Tema 1",
            subtitulo="1.1 Apartado A"
        )

        self.chunk2 = Chunk(
            documento=self.documento,
            indice=1,
            texto="Texto del segundo chunk.",
            titulo="2. Tema 2"
        )

        self.historial = [
            Mensaje(
                rol="user",
                contenido="¿Qué es Python?"
            ),
            Mensaje(
                rol="assistant",
                contenido="Es un lenguaje."
            )
        ]



    def test_formatear_contexto_un_chunk(self):
        """Comprueba que un único chunk se formatea con su jerarquía."""
        resultado = self.constructor._formatear_contexto([self.chunk1])

        esperado = (
            "[Tema 1 > 1.1 Apartado A]\n"
            "Texto del primer chunk."
        )

        self.assertEqual(resultado, esperado)



    def test_formatear_contexto_varios_chunks(self):
        """Comprueba que varios chunks se concatenan con separadores adecuados."""
        resultado = self.constructor._formatear_contexto(
            [self.chunk1, self.chunk2]
        )

        esperado = (
            "[Tema 1 > 1.1 Apartado A]\n"
            "Texto del primer chunk.\n\n"
            "[Tema 2]\n"
            "Texto del segundo chunk."
        )

        self.assertEqual(resultado, esperado)



    def test_formatear_contexto_sin_jerarquia(self):
        """Comprueba el formateo de un chunk sin información de jerarquía."""
        chunk = Chunk(
            documento=self.documento,
            indice=0,
            texto="Texto sin jerarquia."
        )

        resultado = self.constructor._formatear_contexto([chunk])

        esperado = (
            "[Sin contexto]\n"
            "Texto sin jerarquia."
        )

        self.assertEqual(resultado, esperado)



    def test_formatear_historial_varios_mensajes(self):
        """Comprueba que el historial de varios mensajes se formatea correctamente."""
        resultado = self.constructor._formatear_historial(
            self.historial
        )

        esperado = (
            "- user: ¿Qué es Python?\n"
            "- assistant: Es un lenguaje."
        )

        self.assertEqual(resultado, esperado)



    def test_formatear_historial_vacio(self):
        """Comprueba que el historial vacío devuelve el mensaje por defecto."""
        resultado = self.constructor._formatear_historial([])

        esperado = "(sin historial previo)"

        self.assertEqual(resultado, esperado)



    def test_construir_prompt_correcto(self):
        """Comprueba que el prompt incluye instrucciones, contexto, pregunta e historial."""
        resultado = self.constructor.construir_prompt(
            self.historial,
            "¿Qué es Python?",
            [self.chunk1, self.chunk2]
        )

        self.assertIn(INSTRUCCIONES, resultado)
        self.assertIn("Contexto:", resultado)
        self.assertIn(
            self.constructor._formatear_contexto([self.chunk1, self.chunk2]),
            resultado
        )
        self.assertIn("Pregunta:", resultado)
        self.assertIn("¿Qué es Python?", resultado)
        self.assertIn("Historial:", resultado)
        self.assertIn(self.constructor._formatear_historial(self.historial), resultado)



    def test_construir_prompt_sin_chunks(self):
        """Comprueba que se lanza un error si no hay chunks para construir el prompt."""
        with self.assertRaises(ValueError):
            self.constructor.construir_prompt(
                self.historial,
                "¿Qué es Python?",
                []
            )



    def test_construir_prompt_pregunta_vacia(self):
        """Comprueba que se lanza un error si la pregunta está vacía."""
        with self.assertRaises(ValueError):
            self.constructor.construir_prompt(
                self.historial,
                "",
                [self.chunk1]
            )



    def test_construir_prompt_pregunta_con_espacios(self):
        """Comprueba que se lanza un error si la pregunta contiene solo espacios."""
        with self.assertRaises(ValueError):
            self.constructor.construir_prompt(
                self.historial,
                "   ",
                [self.chunk1]
            )


if __name__ == "__main__":
    unittest.main()