"""Módulo de limpieza de los textos obtenidos de los manuales PDF"""

import re
from models import Documento

def limpiar_texto(texto: str) -> str:
    """
    Limpia y normaliza el texto de un documento.

    Aplica las distintas etapas de limpieza para eliminar ruido y dejar
    el texto preparado para su posterior procesamiento.
    """

    texto = normalizar_formato(texto)

    texto = eliminar_lineas_vacias(texto)

    texto = eliminar_numeros_pagina(texto)

    texto = eliminar_urls(texto)

    texto = eliminar_elementos_boe(texto)

    return texto


PATRONES_RUIDO_BOE = {
    "BOLETÍN OFICIAL DEL ESTADO",
    "Núm.",
    "Sec. I.",
    "cve:",
}



def eliminar_lineas_vacias(texto: str) -> str:
    """
    Elimina líneas vacías repetidas conservando una única línea
    en blanco entre bloques de texto.
    """

    texto = re.sub(r"\n{3,}", "\n\n", texto)

    return texto

def eliminar_numeros_pagina(texto: str) -> str:
    """
    Elimina líneas que únicamente contienen un número
    (habitualmente números de página).
    """

    lineas_limpias = []

    for linea in texto.splitlines():

        if linea.isdigit():
            continue

        lineas_limpias.append(linea)

    return "\n".join(lineas_limpias)

def eliminar_urls(texto: str) -> str:
    """
    Elimina líneas que contienen URLs.
    """

    lineas_limpias = []

    for linea in texto.splitlines():

        if "http://" in linea or "https://" in linea or "www." in linea:
            continue

        lineas_limpias.append(linea)

    return "\n".join(lineas_limpias)

def eliminar_elementos_boe(texto: str) -> str:
    """
    Elimina encabezados y pies de página repetitivos que no aportan información.
    """

    lineas_limpias = []

    for linea in texto.splitlines():

        es_elemento_pagina = False

        for patron in PATRONES_RUIDO_BOE:
            if patron in linea:
                es_elemento_pagina = True
                break

        if not es_elemento_pagina:
            lineas_limpias.append(linea)

    return "\n".join(lineas_limpias)


def normalizar_formato(texto: str) -> str:
    """
    Normaliza espacios, caracteres especiales y saltos de línea para obtener
    un texto limpio y uniforme.
    """
    # Sustituir el carácter de espacio em por un espacio normal.
    texto = texto.replace("\u2003", " ")

    # Sustituir las tabulaciones por espacios normales.
    texto = texto.replace("\t", " ")

    # Reducir múltiples espacios consecutivos a uno, sin modificar los saltos de línea.
    texto = re.sub(r" {2,}", " ", texto)

    # Eliminar espacios al principio y final de cada línea
    texto = "\n".join(
        linea.strip()
        for linea in texto.splitlines()
    )

    return texto



def limpiar_documentos(documentos: list[Documento]) -> list[Documento]:
    """
        Limpia el texto de una lista de documentos.

        Modifica el atributo 'texto' de cada Documento utilizando
        la función limpiar_texto() y devuelve la misma lista.
    """

    for documento in documentos:
        documento.texto = limpiar_texto(documento.texto)

    return documentos

