"""Modelos del dominio utilizados por el sistema RAG. 
Este módulo define las entidades principales que representan la información procesada durante el pipeline del proyecto. 
Estas clases son independientes de librerías externas como Docling, ChromaDB o el LLM 
y representan únicamente el dominio de la aplicación."""

from dataclasses import dataclass

@dataclass
class Metodologia:
    """Representa una metodología educativa.
     
    La metodología se obtiene automáticamente a partir del nombre de la carpeta donde se encuentra el documento
    """

    nombre: str


@dataclass
class Documento:
    """Representa un documento educativo preparado para el sistema RAG.

    El contenido procede de un archivo Markdown previamente generado y limpiado.
    Un documento contiene el texto completo y sirve como origen para crear los distintos chunks
    que posteriormente serán indexados.

    Contiene:
    - Metodología educativa a la que pertenece el documento.
    - Nombre del documento, sin la extensión del archivo.
    - Contenido completo del documento en formato Markdown limpio.
    - Ruta del archivo Markdown dentro del proyecto.
    """

    metodologia: Metodologia
    nombre: str
    texto: str
    ruta: str


@dataclass
class Chunk:
    """Representa un fragmento de un documento.

    Los chunks son las unidades mínimas que se indexan en la base vectorial.
    Cada uno mantiene una referencia al documento original para conservar su contexto
    y facilitar la recuperación de información.

    Contiene:
    - Documento del que procede el chunk.
    - Posición del chunk dentro del documento.
    - Contenido textual del fragmento.
    - Título de la sección a la que pertenece el chunk, si existe.
    - Subtítulo o sección de nivel inferior, si existe.
    """

    documento: Documento
    indice: int
    texto: str
    titulo: str | None = None
    subtitulo: str | None = None
    seccion: str | None = None
    subseccion: str | None = None

    def jerarquia(self) -> list[str]:
        """Devuelve los niveles de contexto disponibles (titulo, subtitulo, seccion, subseccion), sin los que sean None."""
        return [
            parte
            for parte in [self.titulo, self.subtitulo, self.seccion, self.subseccion]
            if parte
        ]

    def texto_embedding(self) -> str:
        return "\n".join(self.jerarquia() + [self.texto]).lower()
