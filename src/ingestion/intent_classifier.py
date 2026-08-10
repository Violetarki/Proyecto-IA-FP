# 1. Clasificación previa con el propio LLM (query classification)

# Antes de hacer retrieval, se le pasa la pregunta del usuario a un LLM (puede ser uno chiquito y rápido) con un prompt 
# tipo "clasifica esta pregunta en: factual_simple, step_by_step, comparación, categorización, exploración_de_subtemas".
#  El LLM devuelve una etiqueta (a veces en JSON) y según esa etiqueta el sistema decide:

# Pregunta simple → retrieval normal, top-k chunks, respuesta directa
# Step-by-step → puede activar un prompt distinto que fuerce salida estructurada, o incluso recuperar chunks en orden secuencial 
#   si tu estructura lo permite
# Comparación → aquí muchos sistemas hacen retrieval múltiple: una query por cada término a comparar, 
#   para asegurarse de traer contexto de ambos lados en vez de que el embedding "promedie" la pregunta y traiga solo lo de uno
# Categorización/subtemas → esto normalmente no es retrieval semántico puro, sino que se apoya en metadata 
#   (como tu seccion/subseccion en el chunker que hiciste)

# 2. 2. Metadata-driven retrieval

# Aquí es donde tu estructura de chunking con _Nodo tipo árbol te da una ventaja enorme. 
# Si el usuario pregunta "¿qué subtemas tiene el capítulo 3?", no necesitas retrieval semántico — puedes responder 
# consultando directamente la jerarquía de tu árbol de nodos y devolver los títulos de las secciones hijas. 
# Esto es más rápido, más preciso, y no depende de que el embedding "entienda" que es una pregunta estructural.

# 3. Query rewriting / decomposition

# Para preguntas de comparación tipo "diferencia entre X e Y", muchos sistemas parten la query en dos sub-queries
#  ("¿qué es X?", "¿qué es Y?"), hacen retrieval separado para cada una, y luego el LLM sintetiza la comparación con
#  ambos contextos ya recuperados.

# 4. Routing basado en intención + retrieval híbrido

# Sistemas más maduros combinan:

# retrieval semántico (embeddings) para preguntas abiertas/conceptuales
# retrieval estructural (metadata/árbol) para preguntas de navegación ("qué contiene X")
# a veces incluso un agente que decide qué herramienta usar (buscar en vector store vs. consultar índice de tabla de contenidos)

# Paso 1: Clasificador de intención (rápido y barato)

import json
from groq import Groq
from sympy import python

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

def clasificar_intencion(pregunta: str) -> dict:
    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": INTENT_PROMPT.format(pregunta=pregunta)}],
        temperature=0
    )
    contenido = respuesta.choices[0].message.content.strip()
    contenido = contenido.replace("```json", "").replace("```", "").strip()
    return json.loads(contenido)

# Paso 2: Router que decide qué hacer con cada intención

def responder(pregunta: str, coleccion_chroma, arbol_nodos):
    clasificacion = clasificar_intencion(pregunta)
    intent = clasificacion["intent"]
    terminos = clasificacion["terminos"]

    if intent == "estructura":
        return responder_estructura(terminos[0], arbol_nodos)

    elif intent == "comparacion":
        contextos = [retrieval_semantico(t, coleccion_chroma) for t in terminos]
        return sintetizar_comparacion(pregunta, contextos)

    elif intent == "pasos":
        contexto = retrieval_semantico(terminos[0], coleccion_chroma, top_k=8)
        return generar_respuesta_pasos(pregunta, contexto)

    else:  # factual
        contexto = retrieval_semantico(terminos[0], coleccion_chroma, top_k=4)
        return generar_respuesta_simple(pregunta, contexto)
    
# Paso 3: La rama "estructura" no toca ChromaDB, va directo al árbol
# Esta es la parte donde tu chunker con _Nodo te ahorra retrieval innecesario:
    
def responder_estructura(nombre_seccion: str, arbol_nodos):
    nodo = buscar_nodo_por_nombre(arbol_nodos, nombre_seccion)
    if nodo is None:
        return f"No encontré una sección llamada '{nombre_seccion}'."
    
    subtemas = [hijo.titulo for hijo in nodo.hijos]
    if not subtemas:
        return f"'{nombre_seccion}' no tiene subsecciones."
    
    return f"'{nombre_seccion}' contiene: " + ", ".join(subtemas)

# Paso 4: Comparación con retrieval múltiple + prompt específico

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

# Para "pasos", si el libro de Lean Startup tiene contenido secuencial (como el ciclo Build-Measure-Learn), 
# podrías incluso detectar si la pregunta cae dentro de una sección que ya tiene orden natural en tu árbol, 
# y priorizar chunks consecutivos en vez de solo los más similares semánticamente.

# La idea es usar reglas simples: buscar palabras clave o patrones en la pregunta.

# Ejemplo básico con keywords:
# Lo que hace la gente en producción normalmente es un híbrido:

# Primero pasa por reglas (rápido, gratis, cero latencia)
# Si las reglas no matchean nada con confianza (caso "factual" por defecto, o si matchea más de una categoría a la vez), 
# ahí sí se manda al LLM clasificador como fallback

# Esto te da lo mejor de los dos mundos: la mayoría de preguntas "obvias" 
# (con "cómo", "diferencia", "subtemas") se resuelven gratis sin tocar el LLM, y solo las ambiguas pagan el coste de una llamada extra.

# Lo que las reglas NO pueden hacer bien es extraer los terminos — o sea, saber que en "diferencia entre MVP y prototipo"
# los conceptos a buscar son "MVP" y "prototipo". 
# Ahí sí necesitas algo más que regex (spaCy para NER, o simplemente el LLM), 
# porque identificar entidades dentro de una frase libre es justo el tipo de tarea donde el regex se rompe rápido.
    
import re

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

# El clasificador usa muy pocos tokens
# Tu prompt de clasificación (el INTENT_PROMPT) son ~80-100 tokens fijos, más la pregunta del usuario (normalmente 10-30 tokens)
# La respuesta es un JSON cortito tipo {"intent": "comparacion", "terminos": ["MVP", "prototipo"]} → unos 15-20 tokens de salida
# Con clasificación, cuando detectas intent: comparacion y extraes terminos: ["MVP", "prototipo"], 
# haces dos retrievals separados y limpios, cada uno con un top_k bajo (3-4 chunks) porque cada query es específica. 
# Total: menos chunks, más relevantes, mismo o mejor resultado.
# Ahorro por evitar retrieval innecesario del todo
# Este es el ahorro más grande en realidad. Cuando el intent es estructura ("¿qué subtemas tiene el capítulo 3?"), 
# con tu router no llamas a ChromaDB en absoluto — vas directo al árbol de nodos
# La única llamada al LLM grande es para formatear bonito la respuesta (o ni eso, si simplemente devuelves la lista directamente)

# Esquema final de flujo:
# Pregunta usuario
#       │
#       ▼
# [Intent Classifier] ──────────► decide: intent + terminos + estrategia
#       │
#       ▼
# [Retriever] (uno o varios calls, según intent)
#       │  → list[ResultadoBusqueda]
#       ▼
# [ContextExpander.expandir()] ──► list[Chunk] enriquecidos
#       │
#       ▼
# [Prompt builder] → LLM síntesis

# El intent classifier no le habla directamente al expander. Le habla al retriever (decide cuántas queries, con qué top_k) 
# y opcionalmente le pasa parámetros de expansión al expander (por ejemplo, para intent: pasos quizás quieres _añadir_hijos 
# más agresivo porque necesitas el detalle secuencial completo; para intent: factual simple quizás ni añades hermanos porque no aporta).

# Así que una extensión natural de tu diseño sería que expandir() acepte un parámetro de configuración:

def expandir(self, resultados: list[ResultadoBusqueda], estrategia: dict = None) -> list[Chunk]:
    estrategia = estrategia or self.ESTRATEGIA_DEFAULT
    candidatos = self._aplicar_umbrales(resultados, estrategia["umbral"])
    if estrategia.get("incluir_padres", True):
        candidatos = self._añadir_padres(candidatos)
    if estrategia.get("incluir_hermanos", False):
        candidatos = self._añadir_hermanos(candidatos)
    if estrategia.get("incluir_hijos", False):
        candidatos = self._añadir_hijos(candidatos)
    candidatos = self._eliminar_duplicados(candidatos)
    return self._ordenar(candidatos)

# Y el intent classifier simplemente decide qué estrategia dict pasarle. Por ejemplo: 
# (** Las categorías de intent deben ser las mismas que las keys de ESTRATEGIAS_POR_INTENT)
ESTRATEGIAS_POR_INTENT = {
    "factual": {"umbral": 0.7, "incluir_padres": True, "incluir_hermanos": False, "incluir_hijos": False},
    "pasos": {"umbral": 0.6, "incluir_padres": True, "incluir_hermanos": False, "incluir_hijos": True},
    "comparacion": {"umbral": 0.65, "incluir_padres": True, "incluir_hermanos": True, "incluir_hijos": False},
}

# Falta el fallback si la key de intent no existe en ESTRATEGIAS_POR_INTENT
# El LLM a veces puede devolver algo inesperado (aunque le fuerces el prompt), así que conviene un .get() 
# con default en vez de acceso directo:

def obtener_estrategia(intent: str) -> dict:
    return ESTRATEGIAS_POR_INTENT.get(intent, ESTRATEGIAS_POR_INTENT["factual"])

# 3. La función clasificar_intencion original no distinguía estructura de forma especial en el router — ahora sí importa
# Recuerda que para intent == "estructura" NO quieres pasar por ContextExpander en absoluto 
# (vas directo al árbol, como vimos). Así que tu función responder() necesita ese caso aparte, antes de siquiera llamar al retriever:
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

# 4. Un detalle de robustez en el prompt del clasificador
# Como vas a depender de que terminos siempre tenga al menos un elemento (lo usas con terminos[0] en varios sitios), 
# vale la pena reforzar en el prompt que nunca devuelva la lista vacía, y añadir una validación defensiva en tu código:

def clasificar_intencion(pregunta: str) -> dict:
    respuesta = client.chat.completions.create(...)
    contenido = respuesta.choices[0].message.content.strip()
    contenido = contenido.replace("```json", "").replace("```", "").strip()
    resultado = json.loads(contenido)
    
    if not resultado.get("terminos"):
        resultado["terminos"] = [pregunta]  # fallback: usa la pregunta completa
    
    return resultado