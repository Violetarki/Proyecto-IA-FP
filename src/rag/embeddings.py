"""
Módulo encargado de convertir textos y chunks en vectores numéricos.

Los embeddings permiten representar el significado de un texto mediante
una lista de números. Después podremos comparar esos vectores para
encontrar los chunks más relacionados con una pregunta.
"""

from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer
from src.core.models import Chunk


NOMBRE_MODELO = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


@lru_cache(maxsize=1)
def cargar_modelo() -> SentenceTransformer:
    """
    Carga el modelo de embeddings.

    El decorador lru_cache evita cargar el modelo varias veces durante
    una misma ejecución del programa.
    """

    print(
        "Cargando modelo de embeddings:\n"
        f"{NOMBRE_MODELO}"
    )

    modelo = SentenceTransformer(
        NOMBRE_MODELO
    )

    print("Modelo cargado correctamente.\n")

    return modelo


def crear_embedding_texto(
    texto: str,
) -> np.ndarray:
    """
    Convierte un único texto en un vector NumPy.

    El vector se normaliza para facilitar después el cálculo
    de similitud entre textos.
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
    Convierte una lista de textos en una matriz de embeddings.

    Cada fila de la matriz corresponde a un texto.
    """

    if not textos:
        return np.empty(
            shape=(0, 0),
            dtype=np.float32,
        )

        # Esto en vez de empty si lo consideras mejor
        # raise ValueError(
        # "La lista de textos está vacía."

    textos_limpios: list[str] = []

    for texto in textos:

        if not texto or not texto.strip():
            raise ValueError(
                "La lista contiene un texto vacío."
            )

        textos_limpios.append(
            texto.strip().lower()
        )

    if tamanio_lote <= 0:
        raise ValueError(
            "El tamaño del lote debe ser "
            "mayor que cero."
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


def crear_embeddings_chunks(
    chunks: list[Chunk],
    tamanio_lote: int = 16,
) -> np.ndarray:
    """
    Convierte una lista de objetos Chunk en una matriz de embeddings.

    El orden de los vectores será el mismo que el orden de los chunks.
    Se usa texto_embedding() para incluir el contexto jerárquico
    (titulo, subtitulo, seccion, subseccion) junto con el texto del chunk.
    """

    textos = [chunk.texto_embedding() for chunk in chunks]

    return crear_embeddings_textos(
        textos=textos,
        tamanio_lote=tamanio_lote,
    )


if __name__ == "__main__":

    print("Este módulo proporciona funciones para generar embeddings.")
