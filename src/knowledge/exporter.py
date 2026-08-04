import argparse
import json
from importlib import import_module
from pathlib import Path
from typing import Any

from src.ingestion.markdown_parser import parsear_markdown
from src.knowledge.models import KnowledgeNode, KnowledgeTree


def _obtener_atributos(obj: Any) -> dict[str, Any]:
    """Recoge los atributos públicos del objeto, incluyendo los de __slots__."""
    datos: dict[str, Any] = {}

    if hasattr(obj, "__dict__"):
        datos.update(vars(obj))

    slots = getattr(obj, "__slots__", ())
    if isinstance(slots, str):
        slots = [slots]

    for slot in slots:
        if slot.startswith("_"):
            continue
        if slot in datos:
            continue
        try:
            if hasattr(obj, slot):
                datos[slot] = getattr(obj, slot)
        except AttributeError:
            pass

    return datos


def _serializar_valor(valor: Any, seen: set[int] | None = None) -> Any:
    """Convierte valores complejos a tipos serializables por JSON."""
    if valor is None:
        return None

    if isinstance(valor, Path):
        return str(valor)

    if isinstance(valor, dict):
        return {str(k): _serializar_valor(v, seen) for k, v in valor.items()}

    if isinstance(valor, (list, tuple, set)):
        return [_serializar_valor(v, seen) for v in valor]

    if isinstance(valor, (str, int, float, bool)):
        return valor

    if isinstance(valor, (KnowledgeTree, KnowledgeNode)) or hasattr(valor, "__dict__") or getattr(valor, "__slots__", None):
        return arbol_a_dict(valor, seen)

    return str(valor)


def arbol_a_dict(
    tree: KnowledgeTree | KnowledgeNode | None,
    seen: set[int] | None = None
) -> dict[str, Any]:
    """Convierte un KnowledgeTree/KnowledgeNode a un diccionario de forma recursiva."""
    if tree is None:
        return {}

    if isinstance(tree, (str, int, float, bool)):
        return tree

    if isinstance(tree, dict):
        return {str(k): _serializar_valor(v, seen) for k, v in tree.items()}

    if isinstance(tree, (list, tuple, set)):
        return [arbol_a_dict(item, seen) for item in tree]

    if seen is None:
        seen = set()

    obj_id = id(tree)
    if obj_id in seen:
        return {"$ref": obj_id}

    seen.add(obj_id)
    try:
        datos: dict[str, Any] = {}

        for nombre, valor in _obtener_atributos(tree).items():
            if nombre.startswith("_") or callable(valor):
                continue
            datos[nombre] = _serializar_valor(valor, seen)

        return datos
    finally:
        seen.discard(obj_id)


def guardar_json(tree: KnowledgeTree | KnowledgeNode, ruta: str | Path) -> None:
    """Guarda un árbol de conocimiento como JSON."""
    ruta_path = Path(ruta)

    if not ruta_path.is_absolute():
        ruta_path = (Path(__file__).resolve().parents[2] / ruta_path).resolve()

    if ruta_path.suffix != ".json":
        ruta_path = ruta_path.with_suffix(".json")

    ruta_path.parent.mkdir(parents=True, exist_ok=True)

    contenido = arbol_a_dict(tree)
    with ruta_path.open("w", encoding="utf-8") as f:
        json.dump(contenido, f, ensure_ascii=False, indent=2)


def _listar_markdown(input_dir: Path) -> list[Path]:
    """Devuelve todos los archivos .md de forma recursiva dentro del directorio."""
    md_files = sorted(input_dir.rglob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No se encontraron archivos .md en {input_dir}")
    return md_files


def _construir_arboles(input_dir: Path) -> list[Any]:
    """Intenta construir los árboles con builder.py; si no existe, usa el parser Markdown."""
    md_files = _listar_markdown(input_dir)

    for module_name in ("src.knowledge.builder", "knowledge.builder", "builder"):
        try:
            modulo = import_module(module_name)
        except ImportError:
            continue

        for func_name in (
            "build_knowledge_trees",
            "construir_arboles",
            "crear_knowledge_trees",
            "build_trees",
        ):
            func = getattr(modulo, func_name, None)
            if callable(func):
                try:
                    resultado = func(md_files)
                except TypeError:
                    resultado = func(input_dir)

                if isinstance(resultado, (list, tuple)):
                    return list(resultado)
                if resultado is not None:
                    return [resultado]

    return [parsear_markdown(path.read_text(encoding="utf-8")) for path in md_files]


def main() -> None:
    parser = argparse.ArgumentParser(description="Exporta árboles de conocimiento a JSON")
    parser.add_argument("--input-dir", type=Path, default=None, help="Directorio con los archivos .md")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directorio donde guardar los JSON")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    input_dir = (args.input_dir or (project_root / "data" / "markdown_clean")).resolve()
    output_dir = (args.output_dir or (project_root / "data" / "knowledge")).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    md_files = _listar_markdown(input_dir)
    arboles = _construir_arboles(input_dir)

    for idx, arbol in enumerate(arboles):
        if idx >= len(md_files):
            break

        nombre_salida = f"{md_files[idx].stem}.json"
        ruta_salida = output_dir / nombre_salida
        guardar_json(arbol, ruta_salida)
        print(f"JSON guardado en: {ruta_salida}")


if __name__ == "__main__":
    main()
