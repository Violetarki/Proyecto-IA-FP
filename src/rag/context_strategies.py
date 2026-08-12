"""
Estrategias de selección y organización del contexto
según la intención de la pregunta.
"""

from src.core.models import EstrategiaContexto


class ContextStrategies:
    """
    Contiene las estrategias específicas de cada intención.
    """

    def consulta_conceptual(self) -> EstrategiaContexto:
        """
        Estrategia para consultas conceptuales.

        Para una consulta conceptual queremos conservar
        los chunks relevantes y su contexto jerárquico.

        La expansión jerárquica ya la realiza ContextExpander,
        por lo que esta estrategia no vuelve a buscar padres,
        hermanos o hijos.
        """
        return EstrategiaContexto(
            umbral_excelente=0.5,
            umbral_bueno=0.8,
            umbral_aceptable=1.0,
            anadir_padres=True,
            anadir_hermanos=False,
            anadir_hijos=False,
        )
        
    def pasos(self) -> EstrategiaContexto:
        """Estrategia para intención pasos"""
        return EstrategiaContexto(
            umbral_excelente=0.5,
            umbral_bueno=0.8,
            umbral_aceptable=1.0,
            anadir_padres=False,
            anadir_hermanos=False,
            anadir_hijos=False,
        )
