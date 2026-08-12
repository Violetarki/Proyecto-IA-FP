# 1. definicion ⭐

"¿Qué es X?"

Ejemplos:

¿Qué es el microentorno?

¿Qué significa segmentación de mercado?

Define empresario individual.

Estrategia:

concepto recuperado +
padre

El padre aporta contexto, pero no necesitamos hijos ni hermanos.

# 4. comparacion ⭐

"Quiero comparar dos o más conceptos."

Ejemplos:

¿Qué diferencia hay entre leasing y renting?

¿Qué diferencias existen entre macroentorno y microentorno?

Compara empresario individual y sociedad limitada.

Aquí necesitamos algo que las otras intenciones no proporcionan:

concepto A

- padre A

concepto B

- padre B

Y las palabras_clave del clasificador son especialmente importantes:

{
"intencion": "comparacion",
"palabras_clave": [
"leasing",
"renting"
]
}

Así podemos intentar asegurarnos de que el contexto contiene los dos conceptos, algo que una búsqueda vectorial normal no garantiza.

También es una intención claramente diferenciada.

consulta_conceptual

Pregunta:

¿Qué es el microentorno?

Retriever encuentra:

Microentorno

ContextExpander:

Microentorno
↑
Entorno

Y listo.

pasos

Pregunta:

¿Cuáles son los pasos para crear una empresa?

Retriever encuentra algo relacionado con:

Creación de una empresa

ContextExpander mira el árbol:

Creación de una empresa
├── Paso/parte 1
├── Paso/parte 2
├── Paso/parte 3
└── ...

Y prioriza los hijos.

No necesitamos calcular ninguna complejidad.

comparacion

Pregunta:

¿Qué diferencia hay entre empresario individual y sociedad limitada?

Las keywords nos dicen:

empresario individual
sociedad limitada

Retriever busca información.

Después ContextExpander intenta localizar:

Empresario individual +
Sociedad limitada

y añadir sus padres para dar contexto.

De nuevo, no necesitamos complejidad.

ejemplo_actividad

Pregunta:

Ponme un ejemplo de análisis DAFO.

Retriever encuentra:

Análisis DAFO

ContextExpander mira alrededor:

Análisis DAFO
├── explicación
├── ejemplo
├── actividades
└── ...

y prioriza los nodos relacionados con:

ejemplo
caso práctico
actividad
Y aquí aparece algo que creo que te estaba liando

No necesitamos que el IntentClassifier determine exactamente qué nodos añadir.

Solo necesitamos que nos diga:

{
"intencion": "pasos",
"palabras_clave": [
"crear una empresa"
]
}

Después:

IntentClassifier
↓
IntentResult
↓
ContextExpander
↓
KnowledgeTree

El ContextExpander ya sabe:

Si es pasos → mira hijos.

Si es comparacion → busca los dos conceptos.

Si es ejemplo_actividad → busca ejemplos/actividades cercanos.

Si es consulta_conceptual → empieza por concepto + padre.

Eso es mucho más sencillo.

                    PREGUNTA
                       │
                       ▼
                IntentClassifier
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
        conceptual    pasos   comparación
              │        │        │
              └────────┼────────┘
                       ▼
                   Retriever
                       │
                       ▼
                ContextExpander
                       │
              ┌────────┼─────────┐
              ▼        ▼         ▼
             padre    hijos   varios nodos
                       │
                       ▼
                  PromptBuilder
                       │
                       ▼
                      LLM
