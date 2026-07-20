"""Se encarga de dividir un Documento en una lista de Chunk, 
procurando que cada uno represente una unidad coherente de conocimiento."""

from models import Document, Chunk

# Entrada:
# Documento

# Salida:
# list[Chunk]

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

TITULOS = {
    "Conceptos básicos",
    "Simulación empresarial",
    "Síntesis",
    "Test de repaso",
    "Comprueba tu aprendizaje",
    "Resultados de aprendizaje",
    "Contenidos básicos",
}
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
