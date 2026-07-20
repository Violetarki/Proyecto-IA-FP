"""Se encarga de dividir un Documento en una lista de Chunk, 
procurando que cada uno represente una unidad coherente de conocimiento."""

from models import Documento, Chunk, Metodologia

# Entrada:
# Documento - ok

# Salida:
# list[Chunk] - ok


def crear_chunks():
    pass


def obtener_bloques(documento: Documento) -> list[str]:
    """Recibir un Documento y devolver una lista de bloques de texto.

    Cada bloque agrupa líneas consecutivas no vacías. Separa los bloques
    cuando encuentra una o más líneas vacías.
    """
    bloques: list[str] = []
    bloque_actual: list[str] = []

    # Recorrer todas las líneas del texto del documento.
    for linea in documento.texto.splitlines():
        if linea.strip() == "":
            # Línea vacía: terminar el bloque actual si hay algo acumulado.
            if bloque_actual:
                bloques.append("\n".join(bloque_actual).strip())
                bloque_actual = []
        else:
            # Línea no vacía: añadirla al bloque actual.
            bloque_actual.append(linea)

    # Al terminar, guardar el último bloque si existe.
    if bloque_actual:
        bloques.append("\n".join(bloque_actual).strip())

    return bloques


if __name__ == "__main__":
    from document_loader import leer_documentos

    documentos = leer_documentos("documents")
    if not documentos:
        print("No se han encontrado documentos en la carpeta 'documents'.")
    else:
        documento_real = documentos[0]
        bloques = obtener_bloques(documento_real)

        print(f"Documento real: {documento_real.nombre}")
        print(f"Metodología: {documento_real.metodologia.nombre}")
        print(f"Páginas: {documento_real.paginas}")
        print(f"Se han obtenido {len(bloques)} bloques:\n")

        for i, bloque in enumerate(bloques, start=1):
            print(f"--- Bloque {i} ---")
            print(bloque)
            print()


# Ej.:
# Documento
#       │
#       ▼
# chunker
#       │
#       ▼
# Chunk
# Chunk
# Chunk
# Chunk

# cómo detecta un título:
# Opción A — Detectar patrones conocidos: Síntesis, etc
# Opción B — Detectar por formato: línea corta; no acaba en punto (aunque hay excepciones); está rodeada de líneas vacías.
# Opción C — Mezcla de ambas


# Podemos tener una lista de patrones como:

# TITULOS = {
#     "Conceptos básicos",
#     "Simulación empresarial",
#     "Síntesis",
#     "Test de repaso",
#     "Comprueba tu aprendizaje",
#     "Resultados de aprendizaje",
#     "Contenidos básicos",
# }
# qué hace cuando encuentra uno,

# cómo decide que un chunk es demasiado grande.

# Propuesta de arquitectura
# chunker.py

# ├── crear_chunks() --> Coordina el algoritmo.
# ├── es_titulo() --> T/F ¿Esta línea es un título?
# ├── obtener_seccion() --> Cuando detectamos un título, devuelve el texto que guardaremos en: chunk.seccion

# Hasta ahora hablábamos de un único atributo:

# seccion: str

# Yo no lo cambiaría.
# Pero empezaría a pensar en él como una ruta.
# Estudio de mercado > Simulación empresarial > Fase 1. Decisiones sobre el producto
# Y todos los chunks que pertenezcan a esa fase llevarán esa misma ruta.
# Podéis imprimir:

# Documento:
# simulacion_empresarial.pdf

# Sección:
# Estudio de mercado > Simulación empresarial > Fase 2

# Ahora el chunker ya no solo tiene que dividir texto.

# También tiene que recordar dónde está dentro del documento.

# Es decir, durante el recorrido del texto habrá un estado interno.
# Sección actual:

# Estudio de mercado

# ↓

# Encuentra:

# Conceptos básicos

# ↓

# Actualiza:

# Estudio de mercado > Conceptos básicos

# ↓

# Empieza a leer párrafos...

# ↓

# Crea chunks con esa ruta.

# ↓

# Encuentra:

# Simulación empresarial

# ↓

# Actualiza la ruta.

# ↓

# Sigue creando chunks.


# ///////////////////////////////////////////////////

# Lo que realmente queremos

# Documento

# ↓

# Sección

# ↓

# Si la sección es pequeña

# ↓

# 1 Chunk

# ----------------------

# Si la sección es grande

# ↓

# Chunk 1

# Chunk 2

# Chunk 3

# ...
# Es decir:

# La sección marca los límites lógicos.

# El tamaño marca los límites físicos.
