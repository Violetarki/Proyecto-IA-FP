from pathlib import Path

from pdf_loader import leer_pdf
from text_cleaner import limpiar_texto


ruta = Path("documents/simulacion_empresarial.pdf")

documento = leer_pdf(ruta)

texto_limpio = limpiar_texto(documento.texto)

with open("simulacion_empresarial_limpio.txt", "w", encoding="utf-8") as f:
    f.write(texto_limpio)