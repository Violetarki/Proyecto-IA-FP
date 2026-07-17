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

    def __init__(self, metodologia: Metodologia, nombre: str = "", texto: str = "", ruta: str = "", paginas: int = 0 ):
        self.metodologia = metodologia
        self.nombre = nombre
        self.texto = texto
        self.ruta = ruta
        self.paginas = paginas

    def __repr__(self):
        return (
            f"Documento(nombre={self.nombre!r}, texto={self.texto!r}, "
            f"ruta={self.ruta!r}, paginas={self.paginas})"
            f"metodologia={self.metodologia!r}"
        )

    def __eq__(self, other):
        if isinstance(other, Documento):
            return self.nombre == other.nombre
        return False


@dataclass
class Chunk:
    """
    Representa un fragmento de un Documento.
    """

    texto: str
    documento_origen: str
    seccion: str

    def __init__(self, texto: str, documento_origen: str, seccion: str):
        self.texto = texto
        self.documento_origen = documento_origen
        self.seccion = seccion

    def __repr__(self) -> str:
        return (
            f"Chunk(texto={self.texto!r}, documento_origen={self.documento_origen!r}, "
            f"seccion={self.seccion!r})"
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, Chunk):
            return (
                self.texto == other.texto
                and self.documento_origen == other.documento_origen
                and self.seccion == other.seccion
            )
        return False
    
@dataclass
class Metodologia:
    """
    Representa de qué carpeta viene un documento
    """

    def __init__(self, nombre: str = ""):
        self.nombre = nombre

    def __repr__(self) -> str:
        return f"Metodologia(nombre={self.nombre!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Metodologia):
            return self.nombre == other.nombre
        return False