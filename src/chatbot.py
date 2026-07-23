

class Chatbot:

    def __init__(self, pregunta:str):

        # Generar embedding de la pregunta
        self.embedder = ...

        # Buscar chunks relevantes
        self.vector_store = ...

        # Construir el prompt


        # Enviar el prompt al LLM
        self.llm = ...


    def responder():
        pass


    def _generar_contexto():
        ...

    def _construir_prompt():
        ...

    def _consultar_llm():
        ...