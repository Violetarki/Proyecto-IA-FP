from ollama import chat


class LLMClient:


    def __init__(self, modelo: str = "gemma3:4b"):
        """
        inicializamos el modelo (?)
        """
        self.modelo = modelo
    

        

    def generar_respuesta(self, prompt:str) -> str:
        """
        Recibir un prompt y devolver la respuesta del modelo.
        """

        respuesta = chat(
            model=self.modelo,
            messages=[
                {
                    'role': 'user', 
                    'content': prompt
                }],)

        return respuesta.message.content




if __name__ == "__main__":
    """Prueba interactiva de LLMClient desde la línea de comandos."""
    client = LLMClient()
    print("Escribe tu prompt (o deja vacío para salir):")
    while True:
        prompt = input("> ").strip()
        if not prompt:
            print("Saliendo...")
            break

        try:
            respuesta = client.generar_respuesta(prompt)
            print("\nRespuesta del modelo:\n")
            print(respuesta)
            print("\n---\n")
        except Exception as exc:
            print(f"Error al generar respuesta: {exc}")
            break

