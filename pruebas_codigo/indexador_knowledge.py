from pathlib import Path

from src.knowledge.loader import cargar_arbol

arbol = cargar_arbol(Path("data/knowledge/lean_startup.json"))


def recorrer(nodo):
    if nodo.titulo:
        titulo = nodo.titulo.lower()

        if any(
            palabra in titulo
            for palabra in [
                "actividad",
                "ejercicio",
                "tarea",
            ]
        ):
            print(f"nivel {nodo.nivel}: {nodo.titulo}")

    for hijo in nodo.hijos:
        recorrer(hijo)


recorrer(arbol.raiz)


# amos a saco. La estructura queda así:

# guided_steps.py → decide qué se muestra según metodología.
# GuidedMode → solo gestiona selección/completados.
# GuidedContextBuilder → prepara el contexto de la selección y sus hijos.
# rag_pipeline.py → conecta todo.
# chatbot.html → checklist.
# Flask → guarda el estado en session.
