"""Se encarga de dividir un Documento en una lista de Chunk, 
procurando que cada uno represente una unidad coherente de conocimiento."""


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
