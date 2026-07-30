from src.rag.retriever import Retriever
from src.rag.prompt_builder import ConstructorPrompts


def main():

    retriever = Retriever()
    prompt_builder = ConstructorPrompts()

    metodologia = "lean_startup"

    pregunta = input("Pregunta: ")

    chunks = retriever.recuperar_contexto(
        pregunta=pregunta,
        metodologia=metodologia,
        k=8,
    )

    print(f"\nSe han recuperado {len(chunks)} chunks.")

    if not chunks:
        print("No se ha encontrado contexto relevante.")
        return

    for i, chunk in enumerate(chunks, start=1):

        print(f"\n----- Chunk {i} -----")
        print(f"Título: {chunk.titulo}")
        print(f"Subtítulo: {chunk.subtitulo}")
        print(f"Sección: {chunk.seccion}")
        print(f"Subsección: {chunk.subseccion}")
        print(chunk.texto[:400])
        print("...")

    prompt = prompt_builder.construir_prompt(
        [],
        pregunta=pregunta,
        chunks=chunks,
    )

    print("\n")
    print("=" * 80)
    print("PROMPT GENERADO")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()
