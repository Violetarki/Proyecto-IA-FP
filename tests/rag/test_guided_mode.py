import unittest

from src.rag.guided_mode import GuidedMode
from src.knowledge.models import KnowledgeNode


class TestGuidedMode(unittest.TestCase):

    def setUp(self):
        self.guided_mode = GuidedMode()

        self.paso_1 = KnowledgeNode(
            id="1",
            titulo="Paso 1",
            nivel=1,
        )

        self.paso_2 = KnowledgeNode(
            id="2",
            titulo="Paso 2",
            nivel=1,
        )

        self.nodo_proceso = KnowledgeNode(
            id="proceso",
            titulo="Proceso",
            nivel=0,
            hijos=[self.paso_1, self.paso_2],
        )

    def test_estado_inicial(self):
        self.assertFalse(self.guided_mode.activo)
        self.assertEqual(self.guided_mode.pasos, [])
        self.assertEqual(self.guided_mode.paso_actual, 0)
        self.assertEqual(self.guided_mode.progreso, [])

    def test_iniciar_activa_la_guia(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.assertTrue(self.guided_mode.activo)

    def test_iniciar_guarda_los_pasos(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.assertEqual(
            self.guided_mode.pasos,
            self.nodo_proceso.hijos,
        )

    def test_iniciar_comienza_por_el_primer_paso(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.assertEqual(self.guided_mode.paso_actual, 0)

    def test_iniciar_reinicia_el_progreso(self):
        self.guided_mode.iniciar(self.nodo_proceso)
        self.guided_mode.progreso.append(
            {
                "paso": "Paso anterior",
                "respuesta": "Respuesta anterior",
            }
        )

        self.guided_mode.iniciar(self.nodo_proceso)

        self.assertEqual(self.guided_mode.progreso, [])

    def test_procesar_respuesta_guarda_el_progreso(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.guided_mode.procesar_respuesta("Respuesta del alumno")

        self.assertEqual(
            self.guided_mode.progreso,
            [
                {
                    "paso": "Paso 1",
                    "respuesta": "Respuesta del alumno",
                }
            ],
        )

    def test_procesar_respuesta_avanza_al_siguiente_paso(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.guided_mode.procesar_respuesta("Respuesta del alumno")

        self.assertEqual(self.guided_mode.paso_actual, 1)

    def test_procesar_ultima_respuesta_finaliza_la_guia(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.guided_mode.procesar_respuesta("Respuesta 1")
        self.guided_mode.procesar_respuesta("Respuesta 2")

        self.assertFalse(self.guided_mode.activo)

    def test_procesar_respuestas_guarda_todo_el_progreso(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.guided_mode.procesar_respuesta("Respuesta 1")
        self.guided_mode.procesar_respuesta("Respuesta 2")

        self.assertEqual(
            self.guided_mode.progreso,
            [
                {
                    "paso": "Paso 1",
                    "respuesta": "Respuesta 1",
                },
                {
                    "paso": "Paso 2",
                    "respuesta": "Respuesta 2",
                },
            ],
        )

    def test_procesar_respuesta_sin_guia_activa_no_hace_nada(self):
        self.guided_mode.procesar_respuesta("Respuesta")

        self.assertEqual(self.guided_mode.progreso, [])
        self.assertEqual(self.guided_mode.paso_actual, 0)
        self.assertFalse(self.guided_mode.activo)

    def test_esta_activo_devuelve_el_estado(self):
        self.assertFalse(self.guided_mode.esta_activo())

        self.guided_mode.iniciar(self.nodo_proceso)

        self.assertTrue(self.guided_mode.esta_activo())


    def test_finalizar_desactiva_la_guia(self):
        self.guided_mode.iniciar(self.nodo_proceso)

        self.guided_mode.finalizar()

        self.assertFalse(self.guided_mode.activo)


if __name__ == "__main__":
    unittest.main()