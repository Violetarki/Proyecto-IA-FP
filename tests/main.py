"""
    Modulo de prueba para la función de indexación de documentos.
    Probar individualmente cuando se tenga q volver a indexar la base de datos con python -m tests.main
"""

from src.ingestion.indexador import indexar_documentos


def boton_actualizar_base_datos():
    indexar_documentos()


if __name__ == "__main__":

    # Simulación de pulsar botón
    boton_actualizar_base_datos()
