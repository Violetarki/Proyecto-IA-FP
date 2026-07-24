from src.indexador import indexar_documentos


def boton_actualizar_base_datos():
    indexar_documentos()


if __name__ == "__main__":

    # Simulación de pulsar botón
    boton_actualizar_base_datos()
