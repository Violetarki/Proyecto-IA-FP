import re


PATRONES_PASOS = [
    r"\bqué pasos\b",
    r"\bcómo\s+(?:hacer|realizar|seguir|llevar a cabo)\b",
    r"\bqué\s+(?:tengo\s+que|debo)\s+hacer\b",
    r"\bguíame\b",
]


class IntentClassifier:
    """Clasifica la intención de una pregunta."""

    def es_peticion_de_pasos(self, pregunta: str) -> bool:
        """Indica si la pregunta solicita una guía paso a paso."""

        pregunta = pregunta.lower().strip()

        return any(
            re.search(patron, pregunta)
            for patron in PATRONES_PASOS
        )