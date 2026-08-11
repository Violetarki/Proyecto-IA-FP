from src.rag.retriever import Retriever

retriever = Retriever()

pregunta = "¿Qué es un MVP?"

resultados = retriever.recuperar_candidatos(
    pregunta=pregunta,
    metodologia="simulacion_empresarial",
    k=15,
)

print(f"\nPREGUNTA: {pregunta}")
print("=" * 50)

for i, resultado in enumerate(resultados, start=1):
    chunk = resultado.chunk

    print(f"\n{i}. Distancia: {resultado.distancia:.4f}")
    print(f"   Manual: {chunk.documento.nombre}")
    print(f"   Título: {chunk.titulo}")
    print(f"   Subtítulo: {chunk.subtitulo}")
    print(f"   Texto: {chunk.texto[:200].replace(chr(10), ' ')}...")
