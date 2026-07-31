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

        id_conversacion = 123
        mensaje = Mensaje(
             rol="user",
             contenido="Hola"
         )

        self.historial.agregar_mensaje(id_conversacion, mensaje)
        self.historial.obtener_historial("123")

        self.assertEqual(len(self.historial), 1)
        self.assertIsInstance(self.historial[0], Mensaje)
        self.assertEqual(self.historial[0], mensaje)

        
    def test_agregar_varios_mensajes(self):
        id_conversacion = "123"

        mensajes = [
            Mensaje("user", "Hola"),
            Mensaje("assistant", "Hola, ¿en qué puedo ayudarte?"),
            Mensaje("user", "¿Qué es Scrum?")
        ]

        for mensaje in mensajes:
            self.historial.agregar_mensaje(id_conversacion, mensaje)

        historial = self.historial.obtener_historial(id_conversacion)

        self.assertListEqual(historial, mensajes)

    
    def test_obtener_contexto(self):
        id_conversacion = "123"

        mensajes = [
            Mensaje("user", "Mensaje 1"),
            Mensaje("assistant", "Mensaje 2"),
            Mensaje("user", "Mensaje 3"),
            Mensaje("assistant", "Mensaje 4"),
            Mensaje("user", "Mensaje 5")
        ]

        for mensaje in mensajes:
            self.historial.agregar_mensaje(id_conversacion, mensaje)


        contexto = self.historial.obtener_contexto(
            id_conversacion,
            max_mensajes=3
        )

        self.assertListEqual(contexto, mensajes[-3:])


    def test_obtener_contexto_con_menos_mensajes_que_el_limite(self):

        id_conversacion = "123"

        mensajes = [
            Mensaje("user", "Hola"),
            Mensaje("assistant", "Hola, ¿en qué puedo ayudarte?")
        ]

        for mensaje in mensajes:
            self.historial.agregar_mensaje(id_conversacion, mensaje)

        contexto = self.historial.obtener_contexto(
            id_conversacion,
            max_mensajes=6
        )

        self.assertListEqual(contexto, mensajes)

    
    def test_eliminar_conversacion(self):
        
        id_conversacion = "123"
        mensaje = Mensaje(
            rol="user",
            contenido="Hola"
        )

        self.historial.agregar_mensaje(id_conversacion, mensaje)
        self.historial.eliminar_conversacion(id_conversacion)

        historial = self.historial.obtener_historial(id_conversacion)

        self.assertListEqual(historial, [])


    def test_eliminar_conversacion_inexistente(self):
        self.historial.eliminar_conversacion("123")

    
    def test_conversaciones_independientes(self):

        mensaje1 = Mensaje("user", "Hola")
        mensaje2 = Mensaje("user", "¿Qué es Scrum?")

        self.historial.agregar_mensaje("123", mensaje1)
        self.historial.agregar_mensaje("456", mensaje2)

        historial1 = self.historial.obtener_historial("123")
        historial2 = self.historial.obtener_historial("456")

        self.assertListEqual(historial1, [mensaje1])
        self.assertListEqual(historial2, [mensaje2])
            

    def test_conversacion_inexistente(self):
        
        self.historial.agregar_mensaje(
            "456",
            Mensaje("user", "Hola")
        )

        historial = self.historial.obtener_historial("123")

        self.assertEqual(historial, [])
    

    def tearDown(self):
        """Se ejecuta al terminar cada test."""

        self.temp_dir.cleanup()

if __name__ == "__main__":
    unittest.main()
