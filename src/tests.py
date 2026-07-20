# Pruebas codigo
from document_loader import leer_documentos
from text_cleaner import limpiar_documentos

documentos = leer_documentos("documents")

documentos = limpiar_documentos(documentos)

for documento in documentos:

    print("=" * 70)
    print(documento.metodologia.nombre)
    print(documento.nombre)
    print("=" * 70)

    lineas = documento.texto.splitlines()

    for i, linea in enumerate(lineas[:150]):
        print(f"{i:03d}: {repr(linea)}")

    print()
