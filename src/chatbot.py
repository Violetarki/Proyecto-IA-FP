import embeddings, prompts
from vector_store import VectorStore
from llm_client import LLM
from models import Chunk
import numpy as np

class Chatbot:

    def __init__(
        self,
        embedder: embeddings,
        vector_store: VectorStore,
        llm: LLM
    ):
        
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm



    def responder(self, pregunta:str) -> str:
        """

        4. Crear el prompt

        ↓

        5. Llamar al LLM

        ↓

        6. Devolver la respuesta
        """
        respuesta = ""
        
        # Generamos el contexto
        contexto = self._generar_contexto(pregunta)

        # Construimos el prompt
        prompt = prompts.construir_prompt(pregunta, contexto)

        
        return respuesta






    def _generar_contexto(self, pregunta:str) -> str:
        """
        A partir de la pregunta del usuario, obtener el texto del documento que será enviado al LLM como contexto
        """
        # Generar embedding de la pregunta
        embedding_pregunta = self.embedder.crear_embedding_texto(pregunta)

        # Buscar los chunks
        chunks_respuesta = self.vector_store.buscar(embedding_pregunta, 5)

        #Unir los textos
        texto_respuesta = ""

        for chunk in chunks_respuesta:
            f"{texto_respuesta} {chunk.texto} \n"


        return texto_respuesta



        return prompt 
    def _consultar_llm():
        ...