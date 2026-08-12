"""
Laboratorio para probar estrategias de enriquecimiento de contexto.

Este script NO modifica ContextExpander.

Permite probar una estrategia concreta sobre el flujo real:

    Pregunta
        ↓
    IntentClassifier
        ↓
    Retriever
        ↓
    candidatos recuperados
        ↓
    estrategia de contexto
        ↓
    chunks finales

Actualmente solo se prueba:

    consulta_conceptual

La estrategia inicial es:

    - aplicar umbrales actuales
    - añadir padres
    - no añadir hermanos
    - no añadir hijos
    - eliminar duplicados
    - ordenar por jerarquía
"""

import json
from pathlib import Path

from src.core.models import Chunk
from src.core.models import ResultadoBusqueda
from src.knowledge.models import KnowledgeNode, KnowledgeTree
from src.rag.context_expander import ContextExpander
from src.rag.historial import Historial
from src.rag.intent_classifier import IntentClassifier
from src.rag.retriever import Retriever

# ------------------------------------------------------------------
# Configuración
# ------------------------------------------------------------------

CARPETA_ARBOLES = Path("data/knowledge")

METODOLOGIA = "simulacion_empresarial"


# ------------------------------------------------------------------
# Estrategia que estamos probando
# ------------------------------------------------------------------

ESTRATEGIA_CONSULTA_CONCEPTUAL = {
    "umbrales": {
        "excelente": 0.5,
        "bueno": 0.8,
        "aceptable": 1.0,
    },
    "padres": True,
    "hermanos": False,
    "hijos": False,
}


# ------------------------------------------------------------------
# Carga de árboles
# ------------------------------------------------------------------


def cargar_nodo(
    datos: dict,
    padre: KnowledgeNode | None = None,
) -> KnowledgeNode:
    """
    Convierte recursivamente un nodo JSON en un KnowledgeNode.
    """

    nodo = KnowledgeNode(
        id=datos["id"],
        titulo=datos["titulo"],
        nivel=datos["nivel"],
        padre=padre,
        hijos=[],
        chunk_ids=datos.get("chunk_ids", []),
    )

    for datos_hijo in datos.get("hijos", []):
        hijo = cargar_nodo(
            datos_hijo,
            padre=nodo,
        )

        nodo.hijos.append(hijo)

    return nodo


def cargar_arbol(
    ruta: Path,
) -> KnowledgeTree:
    """
    Carga un KnowledgeTree desde un archivo JSON.
    """

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        datos = json.load(archivo)

    raiz = cargar_nodo(datos["raiz"])

    return KnowledgeTree(
        metodologia=datos["metodologia"],
        raiz=raiz,
    )


def cargar_arboles() -> dict[str, KnowledgeTree]:
    """
    Carga todos los árboles disponibles en data/knowledge.

    La clave del diccionario coincide con el nombre del documento
    utilizado por ContextExpander para localizar el árbol.
    """

    arboles = {}

    for ruta in CARPETA_ARBOLES.glob("*.json"):
        arbol = cargar_arbol(ruta)

        # El ContextExpander busca el árbol mediante:
        #
        #     chunk.documento.nombre
        #
        # Por eso usamos el nombre del archivo sin extensión.
        nombre_documento = ruta.stem

        arboles[nombre_documento] = arbol

    return arboles


# ------------------------------------------------------------------
# Estrategia
# ------------------------------------------------------------------


def aplicar_estrategia(
    expander: ContextExpander,
    candidatos: list[ResultadoBusqueda],
    estrategia: dict,
) -> list[Chunk]:
    """
    Aplica manualmente una estrategia utilizando
    los mecanismos existentes de ContextExpander.

    Esta función es provisional y solo sirve para experimentar.

    No pretende ser la implementación definitiva.
    """

    # 1. Selección por umbrales
    candidatos_filtrados = expander._aplicar_umbrales(candidatos)

    # 2. Expansión jerárquica según la estrategia
    if estrategia["padres"]:
        candidatos_filtrados = expander._enriquecer_con_padres(candidatos_filtrados)

    if estrategia["hermanos"]:
        candidatos_filtrados = expander._enriquecer_con_hermanos(candidatos_filtrados)

    if estrategia["hijos"]:
        candidatos_filtrados = expander._enriquecer_con_hijos(candidatos_filtrados)

    # 3. Eliminar duplicados
    candidatos_filtrados = expander._eliminar_duplicados(candidatos_filtrados)

    # 4. Ordenar según la jerarquía
    candidatos_filtrados = expander._ordenar_por_jerarquia(candidatos_filtrados)

    return candidatos_filtrados


# ------------------------------------------------------------------
# Utilidades de visualización
# ------------------------------------------------------------------


def mostrar_candidato(
    posicion: int,
    resultado: ResultadoBusqueda,
) -> None:
    """
    Muestra un resultado recuperado por el Retriever.
    """

    chunk = resultado.chunk

    print(f"{posicion}. " f"{chunk.titulo}")

    print(f"   distancia : {resultado.distancia:.3f}")

    print(f"   documento : {chunk.documento.nombre}")

    print(f"   ruta      : {chunk.documento.ruta}")

    print(f"   índice    : {chunk.indice}")

    print(f"   node_id   : {chunk.node_id}")


def mostrar_chunk(
    posicion: int,
    chunk: Chunk,
    expander: ContextExpander,
) -> None:
    """
    Muestra un chunk y su posición dentro del árbol.
    """

    print(f"{posicion}. " f"{chunk.titulo}")

    print(f"   documento : {chunk.documento.nombre}")

    print(f"   índice    : {chunk.indice}")

    print(f"   node_id   : {chunk.node_id}")

    # Buscar el nodo correspondiente en el árbol
    nodo = expander._obtener_nodo(chunk)

    if nodo is None:
        print("   nodo      : NO ENCONTRADO")
        return

    print(f"   nivel     : {nodo.nivel}")

    if nodo.padre is not None:
        print(f"   padre     : {nodo.padre.titulo}")
    else:
        print("   padre     : ninguno")

    if nodo.hijos:
        print(f"   hijos     : " f"{[hijo.titulo for hijo in nodo.hijos]}")
    else:
        print("   hijos     : ninguno")


def mostrar_estrategia(
    estrategia: dict,
) -> None:
    """
    Muestra la configuración de la estrategia.
    """

    umbrales = estrategia["umbrales"]

    print("\n" + "=" * 60)
    print("ESTRATEGIA")
    print("=" * 60)

    print(f"Umbral excelente : {umbrales['excelente']}")

    print(f"Umbral bueno     : {umbrales['bueno']}")

    print(f"Umbral aceptable : {umbrales['aceptable']}")

    print(f"Padres           : " f"{'SÍ' if estrategia['padres'] else 'NO'}")

    print(f"Hermanos         : " f"{'SÍ' if estrategia['hermanos'] else 'NO'}")

    print(f"Hijos            : " f"{'SÍ' if estrategia['hijos'] else 'NO'}")


# ------------------------------------------------------------------
# Prueba de una pregunta
# ------------------------------------------------------------------


def probar_pregunta(
    pregunta: str,
    classifier: IntentClassifier,
    retriever: Retriever,
    expander: ContextExpander,
) -> None:
    """
    Ejecuta una pregunta contra la estrategia actual.
    """

    print("\n\n")
    print("#" * 70)
    print(f"PREGUNTA: {pregunta}")
    print("#" * 70)

    # --------------------------------------------------------------
    # 1. Clasificación de intención
    # --------------------------------------------------------------

    intencion = classifier.clasificar(pregunta)

    print("\n" + "=" * 60)
    print("INTENCIÓN")
    print("=" * 60)

    print(f"Intención      : {intencion.intencion}")

    print(f"Palabras clave : {intencion.palabras_clave}")

    print(f"Método         : {intencion.metodo}")

    # --------------------------------------------------------------
    # 2. Comprobamos que corresponde a esta estrategia
    # --------------------------------------------------------------

    if intencion.intencion != "consulta_conceptual":
        print("\nLa pregunta no pertenece a " "'consulta_conceptual'.")

        return

    # --------------------------------------------------------------
    # 3. Recuperación vectorial
    # --------------------------------------------------------------

    candidatos = retriever.recuperar_candidatos(
        pregunta=pregunta,
        metodologia=METODOLOGIA,
    )

    print("\n" + "=" * 60)
    print("RECUPERACIÓN VECTORIAL")
    print("=" * 60)

    print(f"Candidatos recuperados: {len(candidatos)}")

    if not candidatos:
        print("No se han recuperado candidatos.")
        return

    for posicion, candidato in enumerate(
        candidatos,
        start=1,
    ):
        mostrar_candidato(
            posicion,
            candidato,
        )

    # --------------------------------------------------------------
    # 4. Aplicamos la estrategia
    # --------------------------------------------------------------

    contexto_final = aplicar_estrategia(
        expander=expander,
        candidatos=candidatos,
        estrategia=ESTRATEGIA_CONSULTA_CONCEPTUAL,
    )

    # --------------------------------------------------------------
    # 5. Resultado final
    # --------------------------------------------------------------

    print("\n" + "=" * 60)
    print("CONTEXTO DESPUÉS DE LA ESTRATEGIA")
    print("=" * 60)

    print(f"Chunks finales: {len(contexto_final)}")

    for posicion, chunk in enumerate(
        contexto_final,
        start=1,
    ):
        mostrar_chunk(
            posicion,
            chunk,
            expander,
        )

    # --------------------------------------------------------------
    # 6. Mostrar configuración utilizada
    # --------------------------------------------------------------

    mostrar_estrategia(ESTRATEGIA_CONSULTA_CONCEPTUAL)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------


def main() -> None:
    """
    Punto de entrada del script.
    """

    print("=" * 70)
    print("LABORATORIO DE ESTRATEGIAS DE CONTEXTO")
    print("=" * 70)

    print(f"\nMetodología: {METODOLOGIA}")

    # --------------------------------------------------------------
    # Cargar árboles
    # --------------------------------------------------------------

    arboles = cargar_arboles()

    print(f"Árboles cargados: {len(arboles)}")

    for nombre, arbol in arboles.items():
        print(f"  - {nombre} " f"({arbol.metodologia})")

    # --------------------------------------------------------------
    # Crear componentes
    # --------------------------------------------------------------

    classifier = IntentClassifier()

    retriever = Retriever()

    historial = Historial()

    expander = ContextExpander(
        arboles=arboles,
        historial=historial,
    )

    # --------------------------------------------------------------
    # Preguntas de prueba
    # --------------------------------------------------------------

    preguntas = [
        "¿Qué características tiene un emprendedor?",
    ]

    # --------------------------------------------------------------
    # Ejecutar pruebas
    # --------------------------------------------------------------

    for pregunta in preguntas:
        probar_pregunta(
            pregunta=pregunta,
            classifier=classifier,
            retriever=retriever,
            expander=expander,
        )


if __name__ == "__main__":
    main()
