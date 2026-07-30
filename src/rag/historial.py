
"""
    Gestiona el historial de conversaciones guardado en un archivo JSON.
    Permite recuperar los mensajes de una conversación por su identificador
    y preparar la estructura para futuras operaciones de almacenamiento,
    limpieza o actualización del historial.
"""

import json
from src.core.config import CARPETA_HISTORIAL
from pathlib import Path


class Historial:

    def __init__(self, ruta_historial: str = CARPETA_HISTORIAL):
        self.ruta = Path(ruta_historial)

    def obtener_historial(self, id_conversacion: str) -> list:
        """
        Devuelve el historial de una conversación.

        Si el archivo no existe o la conversación no está registrada,
        devuelve una lista vacía.

        Args:
            id_conversacion: Identificador único de la conversación.

        Returns:
            Lista de mensajes de la conversación.
        """

        if not self.ruta.exists():
            return []

        with self.ruta.open("r", encoding="utf-8") as f:
            conversaciones = json.load(f)

        return conversaciones.get(id_conversacion, [])



    def obtener_contexto(
    self,
    id_conversacion: str,
    max_mensajes: int = 6
) -> list:
        """
        Devuelve los últimos mensajes de una conversación para utilizarlos
        como contexto del LLM.

        Args:
            id_conversacion: Identificador de la conversación.
            max_mensajes: Número máximo de mensajes a devolver.

        Returns:
            Lista con los últimos mensajes de la conversación.
        """

        historial = self.obtener_historial(id_conversacion)

        return historial[-max_mensajes:]




    def agregar_mensaje(
        self,
        id_conversacion: str,
        rol: str,
        contenido: str
    ) -> None:
        """
        Agrega un mensaje al historial de una conversación.

        Args:
            id_conversacion: Identificador de la conversación.
            rol: Rol del emisor del mensaje.
            contenido: Texto del mensaje.
        """

        if self.ruta.exists():
            with self.ruta.open("r", encoding="utf-8") as f:
                conversaciones = json.load(f)
        else:
            conversaciones = {}

        if id_conversacion not in conversaciones:
            conversaciones[id_conversacion] = []

        conversaciones[id_conversacion].append({
            "rol": rol,
            "contenido": contenido
        })

        with self.ruta.open("w", encoding="utf-8") as f:
            json.dump(conversaciones, f, ensure_ascii=False, indent=4)



    def eliminar_conversacion(self, id_conversacion: str) -> None:
        """
        Elimina una conversación completa del historial.

        Args:
            id_conversacion: Identificador de la conversación a borrar.
        """

        if not self.ruta.exists():
            return

        with self.ruta.open("r", encoding="utf-8") as f:
            conversaciones = json.load(f)

        if id_conversacion in conversaciones:
            del conversaciones[id_conversacion]

            with self.ruta.open("w", encoding="utf-8") as f:
                json.dump(conversaciones, f, ensure_ascii=False, indent=4)



# MEJORAS PARA MÁS TARDE 

def _cargar_historial():
    ...


def _guardar_historial():
    ...


"""
    Una pequeña mejora que haría

    En lugar de devolver diccionarios, yo devolvería objetos de una clase Mensaje (como ya hacéis con Documento y Chunk).

    Algo como:

    @dataclass
    class Mensaje:
        rol: str
        contenido: str

"""