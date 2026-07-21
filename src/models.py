"""Contiene las clases que representan las entidades principales
del sistema de gestión documental."""

from dataclasses import dataclass

@dataclass
class Metodologia:
    """
    Representa una metodología educativa asociada a un conjunto de documentos.
    Se obtiene a partir del nombre de la carpeta
    """

    nombre: str


@dataclass
class Documento:
    """
    Representa un documento educativo preparado para ser procesado
    por el sistema RAG.

    Su contenido procede de un archivo Markdown generado a partir
    del documento original y posteriormente limpiado.
    """

    metodologia: Metodologia
    nombre: str
    texto: str
    ruta: str


@dataclass
class Chunk:
    """
    Representa un fragmento de un Documento.
    """

    texto: str
    documento_origen: Documento
    seccion: str
