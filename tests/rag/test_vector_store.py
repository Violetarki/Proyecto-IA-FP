import unittest
import numpy as np

from src.rag.vector_store import VectorStore
from src.core.models import Documento, Metodologia, Chunk


class TestVectorStore(unittest.TestCase):

    def setUp(self):

        self.carpeta_test = "test_vector_store"

        self.vector_store = VectorStore(
            collection_name="test_chunks",
            persist_directory=self.carpeta_test
        )

        self.documento = Documento(
            metodologia=Metodologia(nombre="metodologia_test"),
            nombre="documento_test.pdf",
            texto="Texto del documento de prueba.",
            ruta="documentos/documento_test.pdf"
        )

        self.chunk1 = Chunk(
            documento=self.documento,
            indice=0,
            texto="Texto del primer chunk.",
            titulo="Tema 1",
            subtitulo="Apartado A"
        )

        self.chunk2 = Chunk(
            documento=self.documento,
            indice=1,
            texto="Texto del segundo chunk.",
            titulo="Tema 2"
        )

        self.embeddings = np.array([
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ])



"""
Así que haremos:

    Tests unitarios de lógica interna:
        _crear_id
        _preparar_registro
        _chunk_desde_resultado
        _filtrar_chunks
    Tests de integración con ChromaDB real:
        __init__
        indexar_chunks
        buscar
        eliminar_documento
        vaciar


"""