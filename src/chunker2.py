from models import Document, Chunk


MAX_CHUNK_SIZE = 1000


def chunk_document(document: Document) -> list[Chunk]:
    """
    Divide un Documento en una lista de Chunk procurando que cada uno
    represente una unidad coherente de conocimiento.

    Es la función principal. Orquesta todo el proceso:

    Obtiene el texto del documento.
    Lo divide en párrafos.
    Agrupa los párrafos.
    Devuelve la lista de Chunk.

    No debería contener lógica compleja, solo coordinar el resto de funciones.

    """

def dividir_en_parrafos(texto):
    """
    Su única misión es transformar un texto grande en una lista de párrafos.

    Entrada:

    Párrafo 1

    Párrafo 2

    Párrafo 3

    Salida:

    [
        "Párrafo 1",
        "Párrafo 2",
        "Párrafo 3"
    ]
    
    """
def es_titulo(elemento) -> bool:
    """
    Decide si un párrafo corresponde a un título.

    Por ejemplo:

        1. Introducción

    → True

    Mientras que

        La inteligencia artificial permite...

    → False
    """
    
def agrupar_parrafos(parrafos):
    """
    Aquí está el verdadero algoritmo de chunking.

    Va recorriendo los párrafos:

    mantiene la sección actual;
    añade párrafos al chunk;
    cuando se alcanza el tamaño máximo, crea un nuevo Chunk.

    Es la función más importante del módulo.
    """

def supera_tamano(texto: list[str]) -> bool:
    """
    Se limita a responder una pregunta:

    ¿El texto acumulado ya es suficientemente grande?

    Por ejemplo:

    return len(texto) >= MAX_CHUNK_SIZE

    Más adelante podréis cambiar el criterio (caracteres, palabras, tokens...) sin tocar el resto del código.
    """




def crear_chunk() -> Chunk:
    """
    Construye el objeto Chunk a partir del texto y los metadatos disponibles.

    Así, si mañana añadís nuevos atributos al Chunk (por ejemplo, un identificador o la sección del documento), solo tendréis que modificar esta función.
    """








"""

                Documento
                    │
                    ▼
          documento.texto
                    │
                    ▼
      _dividir_en_parrafos()
                    │
                    ▼
      ["p1", "p2", "p3", ...]
                    │
                    ▼
      _agrupar_parrafos()
                    │
      ┌─────────────┴─────────────┐
      │                           │
¿es título?                  ¿supera tamaño?
      │                           │
actualizar sección          crear Chunk
      │                           │
      └─────────────┬─────────────┘
                    ▼
             list[Chunk]

"""