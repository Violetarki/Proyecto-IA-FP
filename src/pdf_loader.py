"""Recibe la ruta de un PDF, lo abre con PyMuPDF,
recorre todas las páginas, extrae el texto, cuenta el número de páginas
y construye un objeto Documento."""

from models import Documento

doc = Documento(
    nombre="marketing.pdf",
    ruta="documents/marketing.pdf",
    texto="Todo el contenido del PDF...",
    paginas=58
)

print(doc)
