import re

from src.core.models import IntentResult


class IntentClassifier:
    """Detecta la intención de una pregunta de usuario."""

    INTENCIONES = {
        "consulta_conceptual",
        "pasos",
        "ejemplo_actividad",
        "comparacion",
        "otra",
    }

    def clasificar(self, pregunta: str) -> IntentResult:

        texto = pregunta.lower().strip()

        intencion = self._detectar_intencion(texto)

        if intencion == "consulta_conceptual":
            palabras_clave = self._extraer_concepto(texto)

        elif intencion == "pasos":
            palabras_clave = self._extraer_proceso(texto)
            
        elif intencion == "ejemplo_actividad":
            palabras_clave = self._extraer_ejemplo_actividad(texto)

        elif intencion == "comparacion":
            palabras_clave = self._extraer_conceptos_comparacion(texto)

        else:
            palabras_clave = self._extraer_palabras_genericas(texto)

        return IntentResult(
            intencion=intencion,
            palabras_clave=palabras_clave,
            metodo="reglas",
        )

    # ------------------------------------------------------------------
    # Detección de intención
    # ------------------------------------------------------------------

    def _detectar_intencion(self, texto: str) -> str:

        if self._es_comparacion(texto):
            return "comparacion"

        if self._es_pasos(texto):
            return "pasos"

        if self._es_ejemplo_actividad(texto):
            return "ejemplo_actividad"

        if self._es_consulta_conceptual(texto):
            return "consulta_conceptual"

        return "otra"

    def _es_comparacion(self, texto: str) -> bool:
        patrones = (
            r"\bdiferencia\b",
            r"\bdiferencias\b",
            r"\bcomparar\b",
            r"\bcompara\b",
            r"\bcomparación\b",
        )

        return any(re.search(patron, texto) for patron in patrones)

    def _es_pasos(self, texto: str) -> bool:
        patrones = (
            r"\bcuáles son los pasos\b",
            r"\bqué pasos\b",
            r"\bpasos para\b",
            r"\bpasos necesarios\b",
            r"\bcómo se hace\b",
            r"\bcómo hacer\b",
            r"\bqué hay que hacer para\b",
            r"\bcómo se realiza\b",
            r"\bcómo se lleva a cabo\b",
        )

        return any(re.search(patron, texto) for patron in patrones)

    def _es_ejemplo_actividad(self, texto: str) -> bool:
        patrones = (
            r"\bejemplo\b",
            r"\bcaso práctico\b",
            r"\bactividad\b",
            r"\bforo\b",
        )

        return any(re.search(patron, texto) for patron in patrones)

    def _es_consulta_conceptual(self, texto: str) -> bool:
        patrones = (
            r"\bqué es\b",
            r"\bqué significa\b",
            r"\bdefine\b",
            r"\ben qué consiste\b",
            r"\bexplícame\b",
            r"\bpara qué sirve\b",
            r"\bqué elementos\b",
            r"\bqué características\b",
            r"\bpor qué\b",
        )

        return any(re.search(patron, texto) for patron in patrones)

    # ------------------------------------------------------------------
    # Extracción de conceptos
    # ------------------------------------------------------------------

    def _extraer_concepto(self, texto: str) -> list[str]: 

        patrones = ( 
                    "qué es", 
                    "qué significa", 
                    "define", 
                    "en qué consiste", 
                    ) 

        texto_limpio = self._quitar_patrones(texto, patrones) 

        return self._limpiar_palabras(texto_limpio)
    

    def _extraer_proceso(self, texto: str) -> list[str]: 

        patrones = ( 
                    "cuáles son los pasos para", 
                    "qué pasos hay que seguir para", 
                    "qué pasos hay que seguir", 
                    "pasos necesarios para", 
                    "pasos para", 
                    "cómo se hace", 
                    "cómo hacer", 
                    "qué hay que hacer para", 
                    ) 

        texto_limpio = self._quitar_patrones(texto, patrones)

        return self._limpiar_palabras(texto_limpio)
    

    def _extraer_conceptos_comparacion(self, texto: str) -> list[str]: 

        patrones = ( 
                    "qué diferencia hay entre", 
                    "qué diferencias hay entre", 
                    "diferencias entre", 
                    "comparación entre", 
                    ) 

        texto_limpio = self._quitar_patrones(texto, patrones)

        # De momento dejamos los conceptos como palabras.
        # Más adelante podemos mejorar esta extracción para
        # obtener grupos como "empresario individual".
        return self._limpiar_palabras(texto_limpio)
    
    def _extraer_ejemplo_actividad(self, texto: str) -> list[str]:
        patrones = (
            "ponme un ejemplo de",
            "ponme un ejemplo",
            "un ejemplo de",
            "caso práctico de",
            "actividad sobre",
        )

        texto_limpio = self._quitar_patrones(texto, patrones)

        return self._limpiar_palabras(texto_limpio)


    def _extraer_palabras_genericas(
        self,
        texto: str,
    ) -> list[str]:

        return self._limpiar_palabras(texto)

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def _quitar_patrones(self, texto: str, patrones: tuple[str, ...], ) -> str: 

        texto_limpio = texto 

        for patron in patrones:

            texto_limpio = texto_limpio.replace(patron, " ")

        return texto_limpio

    def _limpiar_palabras(self, texto: str) -> list[str]:

        palabras_ignoradas = {
            "qué",
            "que",
            "es",
            "son",
            "los",
            "las",
            "una",
            "uno",
            "para",
            "del",
            "por",
            "con",
            "entre",
            "cómo",
            "como",
            "hay",
            "se",
        }

        palabras = re.findall(r"\b[\wáéíóúüñ]+\b", texto) 

        return [ 
                palabra 
                for palabra in palabras 
                if palabra not in palabras_ignoradas and len(palabra) > 2 
                ]


# PATRONES_PASOS = [
#     r"\bqué pasos\b",
#     r"\bcómo\s+(?:hacer|realizar|seguir|llevar a cabo)\b",
#     r"\bqué\s+(?:tengo\s+que|debo)\s+hacer\b",
#     r"\bguíame\b",
# ]


#     def es_peticion_de_pasos(self, pregunta: str) -> bool:
#         """Indica si la pregunta solicita una guía paso a paso."""

#         pregunta = pregunta.lower().strip()

#         return any(
#             re.search(patron, pregunta)
#             for patron in PATRONES_PASOS
#  )
