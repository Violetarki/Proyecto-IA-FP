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

        resultado = self.vector_store._crear_id(self.chunk1)

        esperado = f"{self.documento.ruta}:{self.chunk1.indice}"

        self.assertEqual(resultado, esperado)



    def test_preparar_registro_con_toda_la_jerarquia(self):

        id_, texto, vector, metadata = (
            self.vector_store._preparar_registro(
                self.chunk1,
                self.embeddings[0],
            )
        )

        self.assertEqual(
            id_,
            f"{self.documento.ruta}:{self.chunk1.indice}",
        )

        self.assertEqual(
            texto,
            self.chunk1.texto,
        )

        self.assertEqual(
            vector,
            self.embeddings[0].tolist(),
        )

        esperado = {
            "metodologia": self.documento.metodologia.nombre,
            "documento": self.documento.nombre,
            "ruta": self.documento.ruta,
            "indice": self.chunk1.indice,
            "titulo": self.chunk1.titulo,
            "subtitulo": self.chunk1.subtitulo,
        }

        self.assertEqual(
            metadata,
            esperado,
        )



    def test_preparar_registro_sin_jerarquia(self):

        chunk = Chunk(
            documento=self.documento,
            indice=2,
            texto="Texto sin jerarquia.",
        )

        metadata = self.vector_store._preparar_registro(
            chunk,
            self.embeddings[0],
        )

        esperado = {
            "metodologia": self.documento.metodologia.nombre,
            "documento": self.documento.nombre,
            "ruta": self.documento.ruta,
            "indice": chunk.indice,
        }

        self.assertEqual(
            metadata,
            esperado,
        )



    def test_chunk_desde_resultado(self):

        metadata = {
            "metodologia": self.documento.metodologia.nombre,
            "documento": self.documento.nombre,
            "ruta": self.documento.ruta,
            "indice": self.chunk1.indice,
            "titulo": self.chunk1.titulo,
            "subtitulo": self.chunk1.subtitulo,
        }

        resultado = self.vector_store._chunk_desde_resultado(
            self.chunk1.texto,
            metadata,
        )

        self.assertEqual(
            resultado.documento.metodologia.nombre,
            self.documento.metodologia.nombre,
        )

        self.assertEqual(
            resultado.documento.nombre,
            self.documento.nombre,
        )

        self.assertEqual(
            resultado.documento.ruta,
            self.documento.ruta,
        )

        self.assertEqual(
            resultado.indice,
            self.chunk1.indice,
        )

        self.assertEqual(
            resultado.texto,
            self.chunk1.texto,
        )

        self.assertEqual(
            resultado.titulo,
            self.chunk1.titulo,
        )

        self.assertEqual(
            resultado.subtitulo,
            self.chunk1.subtitulo,
        )

        self.assertIsNone(resultado.seccion)
        self.assertIsNone(resultado.subseccion)



    def test_filtrar_chunks_excelentes(self):

        documentos = [
            "Texto excelente 1",
            "Texto excelente 2",
        ]

        metadatos = [
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": 0,
            },
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": 1,
            },
        ]

        distancias = [
            0.2,
            0.3,
        ]

        resultado = self.vector_store._filtrar_chunks(
            documentos,
            metadatos,
            distancias,
        )

        self.assertEqual(len(resultado), 2)

        self.assertEqual(
            resultado[0].texto,
            "Texto excelente 1",
        )

        self.assertEqual(
            resultado[1].texto,
            "Texto excelente 2",
        )



    def test_filtrar_chunks_buenos(self):

        documentos = [
            "Texto excelente insuficiente",
            "Texto bueno 1",
            "Texto bueno 2",
        ]

        metadatos = [
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": 0,
            },
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": 1,
            },
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": 2,
            },
        ]

        distancias = [
            0.3,
            0.5,
            0.6,
        ]

        resultado = self.vector_store._filtrar_chunks(
            documentos,
            metadatos,
            distancias,
        )

        self.assertEqual(len(resultado), 2)

        self.assertEqual(
            resultado[0].texto,
            "Texto bueno 1",
        )

        self.assertEqual(
            resultado[1].texto,
            "Texto bueno 2",
        )



    def test_filtrar_chunks_aceptables(self):

        documentos = [
            "Excelente",
            "Bueno",
            "Aceptable 1",
            "Aceptable 2",
        ]

        metadatos = [
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": i,
            }
            for i in range(4)
        ]

        distancias = [
            0.3,
            0.5,
            0.7,
            0.8,
        ]

        resultado = self.vector_store._filtrar_chunks(
            documentos,
            metadatos,
            distancias,
        )

        self.assertEqual(len(resultado), 2)

        self.assertEqual(
            resultado[0].texto,
            "Aceptable 1",
        )

        self.assertEqual(
            resultado[1].texto,
            "Aceptable 2",
        )



    def test_filtrar_chunks_limite_maximo(self):

        documentos = [
            "Chunk 1",
            "Chunk 2",
            "Chunk 3",
            "Chunk 4",
            "Chunk 5",
        ]

        metadatos = [
            {
                "metodologia": "metodologia_test",
                "documento": "documento_test.pdf",
                "ruta": self.documento.ruta,
                "indice": i,
            }
            for i in range(5)
        ]

        distancias = [
            0.1,
            0.2,
            0.3,
            0.35,
            0.4,
        ]

        resultado = self.vector_store._filtrar_chunks(
            documentos,
            metadatos,
            distancias,
        )

        self.assertEqual(
            len(resultado),
            MAXIMO_CHUNKS,
        )


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