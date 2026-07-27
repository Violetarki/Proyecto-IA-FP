from src.retriever import Retriever
from src.prompt_builder import ConstructorPrompts


def main():

    pregunta = input("Pregunta: ")

    metodologia = "lean_startup"

    retriever = Retriever()

    chunks = retriever.recuperar_contexto(
        pregunta=pregunta,
        metodologia=metodologia,
    )

    print(f"\nSe han recuperado {len(chunks)} chunks.\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"----- Chunk {i} -----")
        print(f"Título: {chunk.titulo}")

        if chunk.subtitulo:
            print(f"Subtítulo: {chunk.subtitulo}")

        print(chunk.texto[:250])
        print()

    prompt = ConstructorPrompts().construir_prompt(
        pregunta,
        chunks,
    )

    print("=" * 80)
    print("PROMPT GENERADO")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()
