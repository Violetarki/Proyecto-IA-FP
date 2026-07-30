#!/usr/bin/env python3
"""
Cuenta palabras por sección en un archivo Markdown, usando los headers (#, ##, ###...) como divisores.
Uso: python3 contar_secciones.py archivo.md [umbral_palabras]
"""

import sys
import re


def contar_secciones(ruta, umbral=400):
    with open(ruta, encoding="utf-8") as f:
        lineas = f.readlines()

    secciones = []  # (nivel, titulo, num_linea, contenido)
    actual_nivel = 0
    actual_titulo = "(antes del primer header)"
    actual_linea = 0
    buffer = []

    header_re = re.compile(r"^(#{1,6})\s+(.*)")

    for i, linea in enumerate(lineas, start=1):
        m = header_re.match(linea)
        if m:
            # cerrar sección anterior
            secciones.append(
                (actual_nivel, actual_titulo, actual_linea, "".join(buffer))
            )
            actual_nivel = len(m.group(1))
            actual_titulo = m.group(2).strip()
            actual_linea = i
            buffer = []
        else:
            buffer.append(linea)
    secciones.append((actual_nivel, actual_titulo, actual_linea, "".join(buffer)))

    print(f"{'Nivel':<6} {'Línea':<7} {'Palabras':<9} Título")
    print("-" * 70)
    largas = []
    for nivel, titulo, num_linea, contenido in secciones:
        palabras = len(contenido.split())
        marca = "⚠️ " if palabras >= umbral else ""
        prefijo = "#" * nivel if nivel > 0 else "-"
        print(f"{prefijo:<6} {num_linea:<7} {palabras:<9} {marca}{titulo}")
        if palabras >= umbral:
            largas.append((titulo, palabras))

    if largas:
        print("\nSecciones que superan el umbral de {} palabras:".format(umbral))
        for titulo, palabras in largas:
            print(f"  - {titulo}: {palabras} palabras")
    else:
        print(f"\nNinguna sección supera el umbral de {umbral} palabras.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 contar_secciones.py archivo.md [umbral_palabras]")
        sys.exit(1)
    ruta = sys.argv[1]
    umbral = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    contar_secciones(ruta, umbral)
