from pathlib import Path

from src.knowledge.loader import cargar_arbol
from src.rag.guided_steps import (
    obtener_pasos,
    obtener_fases_simulacion,
    obtener_actividades_lean,
)

arboles = {
    "lean_startup": cargar_arbol(Path("data/knowledge/lean_startup.json")),
    "simulacion_empresarial": cargar_arbol(
        Path("data/knowledge/simulacion_empresarial.json")
    ),
}


# LEAN
arbol = arboles["lean_startup"]

print("\n" + "=" * 60)
print("LEAN STARTUP")
print("=" * 60)

modulos = obtener_pasos("lean_startup", arbol)

for modulo in modulos:
    print(f"\n{modulo.titulo}")

    actividades = obtener_actividades_lean(modulo)

    for actividad in actividades:
        print(f"    └── nivel {actividad.nivel}: " f"{actividad.titulo}")


# SIMULACIÓN
arbol = arboles["simulacion_empresarial"]

print("\n" + "=" * 60)
print("SIMULACIÓN EMPRESARIAL")
print("=" * 60)

procesos = obtener_pasos(
    "simulacion_empresarial",
    arbol,
)

for proceso in procesos:

    print(f"\n{proceso.titulo}")

    fases = obtener_fases_simulacion(proceso)

    for fase in fases:
        print(f"    └── {fase.titulo}")
