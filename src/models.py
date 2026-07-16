"""Contiene las clases que representan los documentos y otros modelos de datos del proyecto.
Define la clase Documento, utilizada para almacenar la información extraída de un PDF."""

from dataclasses import dataclass

@dataclass
class Documento:
    """
    Representa un documento leído desde un archivo PDF.

    Almacena la información básica del documento, incluyendo su nombre,
    ruta, contenido textual y número de páginas.
    """

    def __init__(self, nombre: str = "", texto: str = "", ruta: str = "", paginas: int = 0):
        self.nombre = nombre
        self.texto = texto
        self.ruta = ruta
        self.paginas = paginas

    def __repr__(self):
        return (
            f"Documento(nombre={self.nombre!r}, texto={self.texto!r}, "
            f"ruta={self.ruta!r}, paginas={self.paginas})"
        )

    def __eq__(self, other):
        if isinstance(other, Documento):
            return self.nombre == other.nombre
        return False
