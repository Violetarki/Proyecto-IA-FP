from models import Documento

doc = Documento(
    nombre="marketing.pdf",
    ruta="documents/marketing.pdf",
    texto="Todo el contenido del PDF...",
    paginas=58
)

print(doc)
    