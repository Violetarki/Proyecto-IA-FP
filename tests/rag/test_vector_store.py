import unittest
import shutil
import uuid
from pathlib import Path
import numpy as np

from src.rag.vector_store import VectorStore
from src.core.models import Documento, Metodologia, Chunk
from src.core.config import CARPETA_VECTOR_STORE, K_BUSQUEDA, UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MINIMO_CHUNKS, MAXIMO_CHUNKS

class TestVectorStore(unittest.TestCase):

    def setUp(self):

        self.carpeta_test = Path("test_vector_store")

        self.vector_store = VectorStore(
            collection_name=f"test_chunks_{uuid.uuid4().hex}",
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

    def tearDown(self):

        shutil.rmtree(
            self.carpeta_test,
            ignore_errors=True
        )


    #
    # TEST UNITARIOS
    #


    def test_crear_id(self):
        ...



    def test_preparar_registro_con_toda_la_jerarquia(self):
        ...



    def test_preparar_registro_sin_jerarquia(self):
        ...



    def test_chunk_desde_resultado(self):
        ...



    def test_filtrar_chunks_excelentes(self):
        ...



    def test_filtrar_chunks_buenos(self):
        ...



    def test_filtrar_chunks_aceptables(self):
        ...



    def test_filtrar_chunks_limite_maximo(self):
        ...



    #
    # TEST DE INTEGRACIÓN CHROMADB
    #


    def test_inicializar_vector_store(self):
        ...



    def test_indexar_chunks(self):
        ...



    def test_indexar_chunks_lista_vacia(self):
        ...



    def test_indexar_chunks_embeddings_incorrectos(self):
        ...



    def test_buscar(self):
        ...



    def test_buscar_embedding_vacio(self):
        ...



    def test_buscar_k_invalido(self):
        ...



    def test_eliminar_documento(self):
        ...



    def test_vaciar(self):
        ...



    def test_vaciar_coleccion_vacia(self):
        ...


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