import unittest

from src.core.aplanar_tablas import aplanar_tablas


class TestAplanarTablas(unittest.TestCase):

    def test_sin_tablas(self):
        texto = "Esto es un párrafo."

        self.assertEqual(aplanar_tablas(texto), texto)

    def test_tablas_por_filas(self):
        tabla = """| ANÁLISIS DAFO | FORTALEZAS | DEBILIDADES |
|----------------|-------------|--------------|
| ANÁLISIS INTERNO | Recursos superiores | Resistencia al cambio |
"""

        esperado = (
            "ANÁLISIS DAFO - ANÁLISIS INTERNO - FORTALEZAS: Recursos superiores.\n"
            "ANÁLISIS DAFO - ANÁLISIS INTERNO - DEBILIDADES: Resistencia al cambio."
        )

        self.assertEqual(
            aplanar_tablas(tabla).strip(),
            esperado.strip(),
        )

    def test_tabla_por_columnas(self):
        tabla = """| Pensar | Contactos |
|---------|-----------|
| Brainstorming | Clientes |
| Nuevas ideas | Proveedores |
| | Empresarios |
"""

        esperado = (
            "Pensar: Brainstorming, Nuevas ideas.\n"
            "Contactos: Clientes, Proveedores, Empresarios."
        )

        self.assertEqual(
            aplanar_tablas(tabla).strip(),
            esperado.strip(),
        )


if __name__ == "__main__":
    unittest.main()
