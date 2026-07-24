"""
Orquesta el proceso completo de indexación de documentos.

El indexador coordina las distintas etapas del pipeline sin contener
la lógica específica de ninguna de ellas.

Flujo:

PDF
↓
Docling (si es necesario)
↓
Markdown limpio (si es necesario)
↓
Documento
↓
Chunk
↓
Embeddings
↓
Base vectorial
"""


def indexar_documentos():
    """FC ppal"""

    print("Iniciando indexación...")

    markdowns = _obtener_markdowns()

    documentos = cargar_documentos(markdowns)

    chunks = crear_chunks_documentos(documentos)

    embeddings = crear_embeddings_chunks(chunks)

    vector_store = VectorStore()

    vector_store.indexar_chunks(
        chunks,
        embeddings,
    )

    print("Indexación finalizada.")


def _obtener_markdowns():
    """documents/

    ↓

    ¿Existe markdown_clean?

    ↓

    Sí

    ↓

    usar markdown limpio

    ↓

    No

    ↓

    ¿Existe markdown_raw?

    ↓

    Sí

    ↓

    limpiar

    ↓

    No

    ↓

    Docling

    return list[Path]
    
    """

    pass
# FCs privadas

# │
# ├── obtener_markdowns()
# │
# ├── limpiar_markdowns()
# │
# ├── cargar_documentos()
# │
# ├── crear_chunks()
# │
# ├── crear_embeddings()
# │
# └── guardar_vectores()


# FLUJO TIPO NARRACIÓN
# ===== Inicio de la indexación =====

# Comprobando Markdown limpio...
# ✔ Se reutilizarán 2 archivos.

# Comprobando Markdown sin limpiar...
# ✔ Se reutilizará 1 archivo.

# Convirtiendo PDFs restantes...
# ✔ 1 PDF convertido.

# Limpiando Markdown...
# ✔ 1 archivo limpiado.

# Cargando documentos...
# ✔ 3 documentos.

# Creando chunks...
# ✔ 156 chunks.

# Generando embeddings...
# ✔ 156 embeddings.

# Guardando en la base vectorial...
# ✔ Indexación completada.

# ===== Fin =====
