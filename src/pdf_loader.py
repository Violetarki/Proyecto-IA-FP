"""Recibe la ruta de un PDF, lo abre con PyMuPDF,
recorre todas las páginas, extrae el texto, cuenta el número de páginas
y construye un objeto Documento."""

import fitz
from models import Documento
from pathlib import Path

def leer_pdf(ruta_pdf: str) -> Documento:
    """
    Lee un archivo PDF y devuelve un objeto Documento.
    """
    ruta = Path(ruta_pdf)

    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    
    if ruta.suffix.lower() != ".pdf":
        raise ValueError(f"El archivo no tiene la extensión PDF")

    # Abrir el PDF
    with fitz.open(ruta) as pdf:

        # Extraer texto
        texto_completo = ""

        for pagina in pdf: 
            texto_completo += pagina.get_text() + "\n"

        # Obtener número de páginas
        paginas = len(pdf)

        # Obtener nombre del archivo
        nombre = ruta.name

    # Crear Documento
    documento = Documento(
        nombre=nombre, 
        ruta=ruta_pdf, 
        texto=texto_completo, 
        paginas=paginas
    )

    # Devolver Documento
    return documento

if __name__ == "__main__":
    ruta_pdf = "documents/boe.pdf"
    documento = leer_pdf(ruta_pdf)
    print(documento)
    
    
# A IMPLEMENTAR DIA SIGUIENTE:
    # pdf_loader.py

# Solo habría que hacer dos cambios.

# Primero, importar Metodologia:

# from models import Documento, Metodologia

# Después, cambiar la firma de la función:

# def leer_pdf(ruta_pdf: str, metodologia: Metodologia) -> Documento:

# Y al crear el documento:

# documento = Documento(
#     metodologia=metodologia,
#     nombre=nombre,
#     ruta=ruta_pdf,
#     texto=texto_completo,
#     paginas=paginas
# )

# El resto del archivo quedaría exactamente igual.