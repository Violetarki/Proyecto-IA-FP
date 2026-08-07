"""
Módulo encargado de transformar textos en embeddings.

Los embeddings representan el contenido semántico de un texto
mediante vectores numéricos.
"""

import logging
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


NOMBRE_MODELO = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


@lru_cache(maxsize=1)
def cargar_modelo() -> SentenceTransformer:
    """
    Carga el modelo utilizado para generar embeddings.

    El modelo se almacena en caché para evitar cargarlo varias
    veces durante una misma ejecución del programa.

    Returns:
        Modelo de SentenceTransformer cargado.
    """

    logger.info(
        "Cargando modelo de embeddings:\n%s",
        NOMBRE_MODELO,
    )

    modelo = SentenceTransformer(
        NOMBRE_MODELO
    )

    logger.info(
        "Modelo cargado correctamente."
    )

    return modelo


def crear_embedding_texto(
    texto: str,
) -> np.ndarray:
    """
    Convierte un único texto en un embedding.

    Args:
        texto: Texto que se quiere transformar.

    Returns:
        Vector NumPy normalizado que representa el texto.

    Raises:
        ValueError: Si el texto está vacío.
    """

    if not texto or not texto.strip():
        raise ValueError(
            "No se puede crear un embedding "
            "de un texto vacío."
        )

    modelo = cargar_modelo()

    embedding = modelo.encode(
        texto.strip().lower(),
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embedding.astype(
        np.float32
    )


def crear_embeddings_textos(
    textos: list[str],
    tamanio_lote: int = 16,
) -> np.ndarray:
    """
    Convierte una lista de textos en embeddings.

    Cada fila de la matriz resultante corresponde al embedding
    de uno de los textos recibidos.

    Args:
        textos: Lista de textos que se quieren transformar.
        tamanio_lote: Número de textos procesados en cada lote.

    Returns:
        Matriz NumPy con los embeddings generados.

    Raises:
        ValueError: Si algún texto está vacío o si el tamaño
        del lote no es válido.
    """

    if not textos:
        return np.empty(
            shape=(0, 0),
            dtype=np.float32,
        )

    if tamanio_lote <= 0:
        raise ValueError(
            "El tamaño del lote debe ser "
            "mayor que cero."
        )

    textos_limpios: list[str] = []

    for texto in textos:
        if not texto or not texto.strip():
            raise ValueError(
                "La lista contiene un texto vacío."
            )

        textos_limpios.append(
            texto.strip().lower()
        )

    modelo = cargar_modelo()

    embeddings = modelo.encode(
        textos_limpios,
        batch_size=tamanio_lote,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return embeddings.astype(
        np.float32
    )


if __name__ == "__main__":
    logger.info(
        "Este módulo proporciona funciones "
        "para generar embeddings."
    )