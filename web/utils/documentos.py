"""
Funciones auxiliares para gestionar metodologías y documentos.
"""

from pathlib import Path


CARPETA_DOCUMENTOS = Path("documents")


def obtener_metodologias() -> list[str]:
    """
    Devuelve las metodologías disponibles a partir de las
    subcarpetas existentes dentro de documents.
    """

    if not CARPETA_DOCUMENTOS.exists():
        return []

    metodologias = [
        carpeta.name
        for carpeta in CARPETA_DOCUMENTOS.iterdir()
        if carpeta.is_dir()
    ]

    return sorted(metodologias)


def mostrar_nombre_metodologia(
    metodologia: str,
) -> str:
    """
    Convierte el nombre de una carpeta en un texto legible.

    Ejemplo:
        lean_startup -> Lean Startup
    """

    return metodologia.replace("_", " ").title()