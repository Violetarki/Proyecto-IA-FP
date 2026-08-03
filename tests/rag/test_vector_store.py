import unittest
import shutil
import uuid
import chromadb 

from pathlib import Path
import numpy as np

from src.rag.vector_store import VectorStore
from src.core.models import Documento, Metodologia, Chunk
from src.core.config import CARPETA_VECTOR_STORE, K_BUSQUEDA, UMBRAL_ACEPTABLE, UMBRAL_BUENO, UMBRAL_EXCELENTE, MINIMO_CHUNKS, MAXIMO_CHUNKS

class TestVectorStore(unittest.TestCase):

    def setUp(self):
        """Configura un entorno de prueba: cliente ChromaDB y datos de ejemplo."""

        self.carpeta_test = Path("tests/test_vector_store")

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
        """Limpia los artefactos generados durante el test."""

        shutil.rmtree(
            self.carpeta_test,
            ignore_errors=True
        )


    #
    # TEST UNITARIOS
    #


    def test_crear_id(self):
        """Comprueba que el identificador de un chunk se genera correctamente."""

        resultado = self.vector_store._crear_id(self.chunk1)

        esperado = f"{self.documento.ruta}:{self.chunk1.indice}"

        self.assertEqual(resultado, esperado)



    def test_preparar_registro_con_toda_la_jerarquia(self):
        """Verifica que se construye el registro con toda la jerarquía de metadatos."""

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
        """Comprueba la preparación de metadatos cuando no hay jerarquía."""

        chunk = Chunk(
            documento=self.documento,
            indice=2,
            texto="Texto sin jerarquia.",
        )

        resultado = self.vector_store._preparar_registro(
            chunk,
            self.embeddings[0],
        )

        metadata = resultado[3]

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
        """Reconstruye un Chunk a partir de metadatos y texto devueltos por ChromaDB."""

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
        """Filtra correctamente chunks calificados como excelentes por distancia."""

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
        """Filtra correctamente cuando los primeros resultados no son suficientes pero los buenos sí."""

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
            0.61,
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
        """Devuelve los chunks aceptables cuando ni excelentes ni buenos alcanzan el mínimo."""

        documentos = [
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
            0.7,
            0.75,
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
        """Asegura que el número máximo de chunks devueltos respeta `MAXIMO_CHUNKS`."""

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

    """
    Para mantener el test limpio podríamos añadir en el setUp() una función auxiliar tipo _crear_metadata(indice),
    para pensar más tarde
    """

    #
    # TEST DE INTEGRACIÓN CHROMADB
    #


    def test_inicializar_vector_store(self):
        """Comprueba que la inicialización crea cliente y colección en ChromaDB."""

        vector_store = VectorStore(
            collection_name="coleccion_prueba",
            persist_directory=self.carpeta_test,
        )

        self.assertIsNotNone(
            vector_store.client
        )

        self.assertIsNotNone(
            vector_store.collection
        )

        self.assertEqual(
            vector_store.collection.name,
            "coleccion_prueba",
        )



    def test_indexar_chunks(self):
        """Indexa dos chunks y comprueba que aparecen en la colección."""

        chunks = [
            self.chunk1,
            self.chunk2,
        ]

        self.vector_store.indexar_chunks(
            chunks,
            self.embeddings,
        )

        self.assertEqual(
            self.vector_store.collection.count(),
            2,
        )

        resultado = self.vector_store.collection.get()

        self.assertIn(
            self.chunk1.texto,
            resultado["documents"],
        )

        self.assertIn(
            self.chunk2.texto,
            resultado["documents"],
        )



    def test_indexar_chunks_lista_vacia(self):
        """Indexar una lista vacía no debe añadir nada a la colección."""

        self.vector_store.indexar_chunks(
            [],
            np.array([]),
        )

        self.assertEqual(
            self.vector_store.collection.count(),
            0,
        )



    def test_indexar_chunks_embeddings_incorrectos(self):
        """Lanza ValueError si la cantidad de embeddings no coincide con los chunks."""

        chunks = [self.chunk1, self.chunk2]

        # Solo un embedding para dos chunks -> error
        embeddings_malos = np.array([
            [0.1, 0.2, 0.3],
        ])

        with self.assertRaises(ValueError):
            self.vector_store.indexar_chunks(chunks, embeddings_malos)



    def test_buscar(self):
        """Indexa chunks y busca por embedding para obtener resultados ordenados."""

        chunks = [self.chunk1, self.chunk2]

        self.vector_store.indexar_chunks(chunks, self.embeddings)

        # Buscar usando el embedding del primer chunk
        resultados = self.vector_store.buscar(
            embedding=self.embeddings[0],
            metodologia=self.documento.metodologia.nombre,
            k=2,
        )

        self.assertTrue(isinstance(resultados, list))
        self.assertGreaterEqual(len(resultados), 1)
        self.assertEqual(resultados[0].texto, self.chunk1.texto)



    def test_buscar_embedding_vacio(self):
        """Buscar con un embedding vacío devuelve lista vacía."""

        resultado = self.vector_store.buscar(
            embedding=np.array([]),
            metodologia=self.documento.metodologia.nombre,
            k=3,
        )

        self.assertEqual(resultado, [])



    def test_buscar_k_invalido(self):
        """Buscar con un valor de k inválido debe lanzar ValueError."""

        with self.assertRaises(ValueError):
            self.vector_store.buscar(
                embedding=self.embeddings[0],
                metodologia=self.documento.metodologia.nombre,
                k=0,
            )



    def test_eliminar_documento(self):
        """Elimina todos los chunks asociados a un documento."""

        chunks = [self.chunk1, self.chunk2]

        self.vector_store.indexar_chunks(chunks, self.embeddings)

        # Comprobación previa
        self.assertEqual(self.vector_store.collection.count(), 2)

        self.vector_store.eliminar_documento(self.documento)

        # Tras eliminar el documento no debe haber registros
        self.assertEqual(self.vector_store.collection.count(), 0)



    def test_vaciar(self):
        """Vacía la colección eliminando todos los registros existentes."""

        chunks = [self.chunk1, self.chunk2]

        self.vector_store.indexar_chunks(chunks, self.embeddings)

        self.assertEqual(self.vector_store.collection.count(), 2)

        self.vector_store.vaciar()

        self.assertEqual(self.vector_store.collection.count(), 0)



    def test_vaciar_coleccion_vacia(self):
        """Llamar a vaciar() en una colección ya vacía no debe fallar."""

        # Asegurar que inicialmente está vacía
        self.assertEqual(self.vector_store.collection.count(), 0)

        # No debe lanzar
        self.vector_store.vaciar()

        self.assertEqual(self.vector_store.collection.count(), 0)


if __name__ == "__main__":
    unittest.main()