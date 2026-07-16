from dataclasses import dataclass

@dataclass
class Documento:
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
