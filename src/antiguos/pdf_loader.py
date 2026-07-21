"""Recibe la ruta de un PDF, lo abre con PyMuPDF,
recorre todas las páginas, extrae el texto, cuenta el número de páginas
y construye un objeto Documento."""

import fitz
from models import Documento, Metodologia
from pathlib import Path

def leer_pdf(ruta_pdf: str, metodologia: Metodologia) -> Documento:
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
        metodologia=metodologia,
        nombre=nombre, 
        ruta=ruta_pdf, 
        texto=texto_completo, 
        paginas=paginas
    )

    # Devolver Documento
    return documento

if __name__ == "__main__":
    metodologia = Metodologia("lean_startup")

    documento = leer_pdf("documents/lean_startup/lean_startup.pdf", metodologia)

    print(documento)


