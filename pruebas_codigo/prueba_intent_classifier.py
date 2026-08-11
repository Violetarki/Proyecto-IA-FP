"""Modulo de pruebas para el clasificador de intenciones.
Puede servir como referencia para crear nuevas pruebas unitarias."""

from src.rag.intent_classifier import IntentClassifier


def test_clasificar_intenciones_basicas():
    classifier = IntentClassifier()

    preguntas = [
        "Explícame el marketing.",
        "¿Para qué sirve el análisis DAFO?",
        "¿Cómo se realiza un análisis DAFO?",
        "Ponme un ejemplo de segmentación de mercado.",
        "¿Cuál es la diferencia entre marketing estratégico y operativo?",
        "¿Qué elementos forman el microentorno?",
    ]

    for pregunta in preguntas:
        resultado = classifier.clasificar(pregunta)
        print(pregunta)
        print(resultado)
        print()

if __name__ == "__main__":
    test_clasificar_intenciones_basicas()
