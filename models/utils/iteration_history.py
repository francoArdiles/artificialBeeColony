class History:
    """
    Contiene la historia de búsqueda
    """
    def __init__(self, name: str = ''):
        self.sols = []
        self.name = name

    def add(self, sol, **kwargs):
        self.sols.append(sol)
