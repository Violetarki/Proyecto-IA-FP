"""
Módulo encargado de gestionar el modo de aprendizaje guiado.

Mantiene el estado de una sesión guiada, controla el paso actual,
registra las respuestas del alumno y gestiona el avance entre
los pasos definidos en un proceso.
"""

class GuidedMode:
    """Gestiona una sesión de aprendizaje guiada paso a paso."""

    def __init__(self):
        self.activo = False
        self.pasos = []
        self.paso_actual = 0
        self.progreso = []


   
    def iniciar(self, nodo_proceso):
        """Inicia una nueva sesión guiada."""
        self.pasos = nodo_proceso.hijos
        self.paso_actual = 0
        self.progreso = []
        self.activo = True

     
    def procesar_respuesta(self, respuesta_alumno):
        """Procesa la respuesta del alumno y avanza al siguiente paso."""

        if not self.activo:
            return

        self.progreso.append({
            "paso": self.pasos[self.paso_actual].titulo,
            "respuesta": respuesta_alumno,
        })

        self.paso_actual += 1

        if self.paso_actual >= len(self.pasos):
            self.finalizar()


    def esta_activo(self):
        return self.activo

    def finalizar(self):
        """Finaliza la sesión guiada."""
        self.activo = False
