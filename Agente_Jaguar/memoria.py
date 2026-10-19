class MemoriaJaguar:

    def __init__(self):
        self.posiciones_recientes = []
        self.max_posiciones_recientes = 4

        self.memoria_bayas = set()  # Coordenadas de bayas descubiertas (tipo 5 o 6)
        self.memoria_arena = set()  # Coordenadas de arena movediza (tipo 4)
        
        self.visitas = {}

    def recordar_posicion(self, posicion):
        if not self.posiciones_recientes or self.posiciones_recientes[-1] != posicion:
            self.posiciones_recientes.append(posicion)
        
        self.posiciones_recientes = self.posiciones_recientes[-self.max_posiciones_recientes:]
        self.visitas[posicion] = self.visitas.get(posicion, 0) + 1

    def registrar_terreno(self, posicion, tipo):
        if tipo in (5, 6):
            self.memoria_bayas.add(posicion)
        elif tipo == 4:
            self.memoria_arena.add(posicion)

    def olvidar_baya(self, posicion):
        self.memoria_bayas.discard(posicion)