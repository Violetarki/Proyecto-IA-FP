


class Documento:
    def __init__(self, id, titulo, contenido):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido

    def __repr__(self):
        return f"<Documento {self.id}: {self.titulo}>"
    
