import unittest

from src.core.limpiar_encabezados import limpiar_encabezado


class TestLimpiarEncabezados(unittest.TestCase):

    def test_sin_numeracion(self):
        self.assertEqual(
            limpiar_encabezado("Lean Startup"),
            "Lean Startup",
        )

    def test_numero_simple(self):
        self.assertEqual(
            limpiar_encabezado("4. PROTOTIPAR"),
            "PROTOTIPAR",
        )

    def test_numero_decimal(self):
        self.assertEqual(
            limpiar_encabezado("3.2. EL MAPA DE EMPATÍA"),
            "EL MAPA DE EMPATÍA",
        )

    def test_varios_niveles(self):
        self.assertEqual(
            limpiar_encabezado("2.4.1. Brainstorming"),
            "Brainstorming",
        )

    def test_numero_parte_del_titulo(self):
        self.assertEqual(
            limpiar_encabezado("7 SECRETOS PARA EMPRENDER"),
            "7 SECRETOS PARA EMPRENDER",
        )
    
    def test_numero_en_medio(self):
        self.assertEqual(
            limpiar_encabezado("Las 4 Cs del emprendimiento"),
            "Las 4 Cs del emprendimiento",
        )
        
    def test_no_modifica_numero_no_inicial(self):
        self.assertEqual(
            limpiar_encabezado("Tema 4: Prototipar"),
            "Tema 4: Prototipar",
        )

    def test_cadena_vacia(self):
        self.assertEqual(
            limpiar_encabezado(""),
            "",
        )


if __name__ == "__main__":
    unittest.main()
