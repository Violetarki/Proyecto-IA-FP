import json, re
from groq import Groq
from sympy import python

from src.rag.context_expander import ContextExpander


client = Groq()

INTENT_PROMPT = """Clasifica la pregunta del usuario en una de estas categorías:
- "factual": pregunta directa sobre un concepto o dato concreto
- "comparacion": pide diferencias o similitudes entre dos o más términos
- "pasos": pide un proceso o guía paso a paso
- "estructura": pregunta qué contiene un tema, capítulo o sección (subtemas, índice)

Responde SOLO con JSON, sin texto adicional, con este formato:
{"intent": "...", "terminos": ["..."]}

Donde "terminos" son los conceptos clave a buscar (1 para factual/pasos, 2+ para comparacion, o el nombre de la sección para estructura).

Pregunta: {pregunta}"""


PATRONES = {
    "comparacion": [
        r"\bdiferencia(s)?\b", r"\bvs\b", r"\bversus\b", 
        r"\bcompar", r"\bmejor que\b", r"\bo\s+\w+\?"
    ],
    "pasos": [
        r"\bc[oó]mo\b", r"\bpasos\b", r"\bproceso\b", 
        r"\bgu[ií]a\b", r"\bqu[eé] hago\b"
    ],
    "estructura": [
        r"\bsubtemas\b", r"\bqu[eé] contiene\b", r"\bcap[ií]tulos\b",
        r"\b[ií]ndice\b", r"\bsecciones\b", r"\bde qu[eé] trata\b"
    ]
}

ESTRATEGIAS_POR_INTENT = {
    "factual": {
        "umbral": 0.7,
        "incluir_padres": True,
        "incluir_hermanos": False,
        "incluir_hijos": False
    },

    "pasos": {
        "umbral": 0.6,
        "incluir_padres": True,
        "incluir_hermanos": False,
        "incluir_hijos": True
    },

    "comparacion": {
        "umbral": 0.65,
        "incluir_padres": True,
        "incluir_hermanos": True,
        "incluir_hijos": False
    }
}

class IntentClassifier():
    ...


def clasificar_intencion(pregunta: str) -> dict:

    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": INTENT_PROMPT.format(pregunta=pregunta)}],
        temperature=0
    )

    contenido = respuesta.choices[0].message.content.strip()
    contenido = contenido.replace("```json", "").replace("```", "").strip()
    resultado = json.loads(contenido)
    
    if not resultado.get("terminos"):
        resultado["terminos"] = [pregunta]  # fallback: usa la pregunta completa
    
    return resultado


def responder(pregunta: str, coleccion_chroma, arbol_nodos, expander: ContextExpander):
    clasificacion = clasificar_intencion(pregunta)
    intent = clasificacion["intent"]
    terminos = clasificacion["terminos"]

    if intent == "estructura":
        return responder_estructura(terminos[0], arbol_nodos)

    estrategia = obtener_estrategia(intent)

    if intent == "comparacion":
        resultados = []
        for termino in terminos:
            resultados += retrieval_semantico(termino, coleccion_chroma, top_k=4)
    else:
        resultados = retrieval_semantico(terminos[0], coleccion_chroma, top_k=6)

    chunks_expandidos = expander.expandir(resultados, estrategia)
    return generar_respuesta(pregunta, chunks_expandidos, intent)


def responder_estructura(nombre_seccion: str, arbol_nodos):
    nodo = buscar_nodo_por_nombre(arbol_nodos, nombre_seccion)
    if nodo is None:
        return f"No encontré una sección llamada '{nombre_seccion}'."
    
    subtemas = [hijo.titulo for hijo in nodo.hijos]
    if not subtemas:
        return f"'{nombre_seccion}' no tiene subsecciones."
    
    return f"'{nombre_seccion}' contiene: " + ", ".join(subtemas)


def sintetizar_comparacion(pregunta: str, contextos: list[str]) -> str:
    prompt = f"""Usando el siguiente contexto, responde comparando los conceptos.
        Estructura la respuesta señalando similitudes y diferencias claramente.

        Contexto:
        {chr(10).join(contextos)}

        Pregunta: {pregunta}"""
    respuesta = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content


def clasificar_por_reglas(pregunta: str) -> str:
    pregunta_lower = pregunta.lower()
    for intent, patrones in PATRONES.items():
        for patron in patrones:
            if re.search(patron, pregunta_lower):
                return intent
    return "factual"  # default si no matchea nada


def clasificar_intencion_hibrido(pregunta: str) -> dict:
    intent_reglas = clasificar_por_reglas(pregunta)
    
    if intent_reglas != "factual":
        return {"intent": intent_reglas, "terminos": extraer_terminos_simple(pregunta)}
    
    # fallback al LLM solo si las reglas no encontraron nada claro
    return clasificar_intencion(pregunta)


def obtener_estrategia(intent: str) -> dict:
    return ESTRATEGIAS_POR_INTENT.get(intent, ESTRATEGIAS_POR_INTENT["factual"])



def retrieval_semantico(self):
    ...

def generar_respuesta_pasos(self):
    ...

def generar_respuesta_simple(self):
    ...

def buscar_nodo_por_nombre(self):
    ...

def extraer_terminos_simple(self):
    ...

def generar_respuesta(self):
    ...