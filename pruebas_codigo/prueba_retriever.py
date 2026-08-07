from src.rag.retriever import Retriever

retriever = Retriever()

resultados = retriever.recuperar_candidatos(
    pregunta="¿Qué es un DAFO?",
    metodologia="lean_startup",
)

for resultado in resultados:
    print(f"Distancia: {resultado.distancia:.3f}")
    print(resultado.chunk.texto[:150])
    print("-" * 50)
