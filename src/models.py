"""Contiene las clases que representan las entidades principales
del sistema de gestión documental."""

from dataclasses import dataclass
    
@dataclass
class Metodologia:
    """
    Representa una metodología educativa asociada a un conjunto de documentos.
    """

    nombre: str


@dataclass
class Documento:
    """
    Representa un documento leído desde un archivo PDF.

    Almacena la información básica del documento, incluyendo su nombre,
    ruta, contenido textual y número de páginas.
    """
    metodologia: Metodologia
    nombre: str
    texto: str
    ruta: str
    paginas: int


@dataclass
class Chunk:
    """
    Representa un fragmento de un Documento.
    """

    texto: str
    documento_origen: Documento
    seccion: str