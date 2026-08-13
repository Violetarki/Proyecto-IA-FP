"""
Módulo encargado de gestionar el modo de aprendizaje guiado.

GuidedMode ya no guarda estado en self: recibe y devuelve el estado
como un diccionario serializable (para poder guardarlo en flask.session).

GuidedMode → estado/progreso → obtención del paso → construcción del contexto 
→ interacción con el LLM → procesamiento de la respuesta → avance o permanencia en el paso.
"""



class GuidedMode:
    """Gestiona la lógica de una sesión de aprendizaje guiada paso a paso."""

    def estado_inicial(self, nodo_proceso) -> dict:
        """Crea el estado inicial de una guía a partir del nodo raíz del proceso."""
        pasos_ids = [hijo.id for hijo in nodo_proceso.hijos]

        return {
            "activo": True,
            "pasos_ids": pasos_ids,
            "paso_actual": 0,
            "progreso": [],
        }

    def obtener_paso_actual(self, estado: dict, arbol):
        """Devuelve el KnowledgeNode del paso actual, o None si no hay guía activa."""
        if not estado.get("activo"):
            return None

        pasos_ids = estado["pasos_ids"]
        paso_actual = estado["paso_actual"]

        id_nodo_actual = pasos_ids[paso_actual]
        return arbol.buscar_por_id(id_nodo_actual)

    def procesar_respuesta(self, estado: dict, respuesta_alumno: str, arbol) -> dict:
        """Registra la respuesta del alumno y avanza el estado al siguiente paso."""
        if not estado.get("activo"):
            return estado

        pasos_ids = estado["pasos_ids"]
        paso_actual = estado["paso_actual"]

        nodo_actual = arbol.buscar_por_id(pasos_ids[paso_actual])

        estado["progreso"].append(
            {
                "paso": nodo_actual.titulo,
                "respuesta": respuesta_alumno,
            }
        )

        estado["paso_actual"] += 1

        if estado["paso_actual"] >= len(pasos_ids):
            estado["activo"] = False

        return estado

    def esta_activo(self, estado: dict) -> bool:
        return estado.get("activo", False)
