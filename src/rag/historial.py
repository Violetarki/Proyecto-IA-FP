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

    def añadir_mensaje_usuario():
        ...

    def añadir_respuesta():
        ...

    def limpiar_historial():
        ...