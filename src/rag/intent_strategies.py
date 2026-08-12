ESTRATEGIAS = {
    "consulta_conceptual": {
        "umbrales": "...",
        "padres": True,
        "hermanos": False,
        "hijos": False,
        "maximo_chunks": "...",
    },
    "pasos": {
        "umbrales": "...",
        "padres": True,
        "hermanos": True,
        "hijos": True,
        "maximo_chunks": "...",
    },
    "ejemplo_actividad": {...},
    "comparacion": {...},
    "otra": {...},
}

MASEXPRESIONES = {
    "padres": {
        "activo": True,
        "profundidad": 2,
    },
    "hermanos": {
        "activo": True,
        "maximo": 2,
    },
    "hijos": {
        "activo": False,
    },
    "umbrales": {
        "excelente": 0.5,
        "bueno": 0.8,
        "aceptable": 1.0,
    },
}
