"""Test para probar el pipeline RAG con Ollama"""

from src.rag_pipeline import RAG


def main():

    rag = RAG()

    metodologia = "lean_startup"

    while True:

        pregunta = input("\nPregunta: ").strip()

        if not pregunta:
            break

        respuesta = rag.responder(
            pregunta,
            metodologia,
        )

        print("\nRespuesta:\n")
        print(respuesta)


if __name__ == "__main__":
    main()
