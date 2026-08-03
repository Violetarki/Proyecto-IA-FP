import unittest
from pathlib import Path

from src.rag.prompt_builder import ConstructorPrompts, INSTRUCCIONES
from src.core.models import Chunk, Mensaje, Documento

class TestConstruirPrompt(unittest.TestCase):

    def setUp(self):
        self.constructor = ConstructorPrompts()

        self.documento = Documento(
            nombre="documento_prueba.pdf",
            ruta="documento_prueba.pdf",
            texto="Texto del documento de prueba.",
            paginas=10
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
        resultado = self.constructor._formatear_contexto([self.chunk1])

        esperado = (
            "[Tema 1 > Apartado A]\n"
            "Texto del primer chunk."
        )

        self.assertEqual(resultado, esperado)




    def test_formatear_contexto_varios_chunks(self):
        resultado = self.constructor._formatear_contexto(
            [self.chunk1, self.chunk2]
        )

        esperado = (
            "[Tema 1 > Apartado A]\n"
            "Texto del primer chunk.\n\n"
            "[Tema 2]\n"
            "Texto del segundo chunk."
        )

        self.assertEqual(resultado, esperado)

        

    def test_formatear_contexto_sin_jerarquia(self):
        ...



    def test_formatear_contexto_lista_vacia(self):
        ...



    def test_formatear_historial_varios_mensajes(self):
        ...



    def test_formatear_historial_vacio(self):
        ...



    def test_construir_prompt_correcto(self):
        ...



    def test_construir_prompt_sin_chunks(self):
        ...



    def test_construir_prompt_pregunta_vacia(self):
        ...



    def test_construir_prompt_pregunta_con_espacios(self):
        ...

        