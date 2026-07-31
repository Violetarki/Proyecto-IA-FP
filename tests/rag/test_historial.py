import unittest
import tempfile
from pathlib import Path

from src.core.models import Mensaje
from src.rag.historial import Historial


class TestHistorial(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test."""

        self.temp_dir = tempfile.TemporaryDirectory()
        self.historial = Historial(Path(self.temp_dir.name) / "historial.json")

    def test_historial_vacio(self):

        historial = self.historial.obtener_historial("123")

        self.assertEqual(historial, [])

    def test_agregar_mensaje(self):
        # Añadir un mensaje en el historial

        # Guardar:
        # Mensaje(
        #     rol="user",
        #     contenido="Hola"
        # )
        # Después:
        # obtener_historial("123")
        # Debe devolver un mensaje con esos datos.

    def tearDown(self):
        """Se ejecuta al terminar cada test."""

        self.temp_dir.cleanup()

if __name__ == "__main__":
    unittest.main()
