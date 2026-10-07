import random

from Algoritmos.a_Estrella import AEstrella
from Algoritmos.huida import Huida


class AgenteJaguar:

    def __init__(self, mundo):

        self.mundo = mundo


        # ==========================================
        # DETECCIÓN DEL CAZADOR
        #
        # El jaguar huele y oye al cazador a
        # esta distancia (los árboles no lo tapan).
        # ==========================================

        self.rango_deteccion = 4


        # Probabilidad de moverse cuando está
        # tranquilo (si no, descansa)

        self.probabilidad_merodear = 0.35


        self.estado = "Descansando"


    # ==========================================
    # POSICIÓN
    # ==========================================

    @property
    def posicion(self):

        return self.mundo.posicion_jaguar


    # ==========================================
    # TOMAR DECISIÓN
    #
    # Devuelve la casilla a la que se mueve,
    # o None si se queda quieto.
    # ==========================================

    def tomar_decision(
        self,
        posicion_cazador
    ):

        if not self.mundo.jaguar_vivo:

            return None


        distancia = (
            AEstrella.heuristica(
                self.posicion,
                posicion_cazador
            )
        )


        # ==========================================
        # 1. DETECTA AL CAZADOR: ESCAPAR
        # ==========================================

        if (
            distancia
            <=
            self.rango_deteccion
        ):

            destino = Huida.elegir_escape(

                self.posicion,

                posicion_cazador,

                self.mundo

            )


            if destino is None:

                self.estado = "Acorralado"

                return None


            self.estado = "Huyendo"

            self.mundo.mover_jaguar(
                destino
            )

            return destino


        # ==========================================
        # 2. TRANQUILO: MERODEAR O DESCANSAR
        # ==========================================

        if (
            random.random()
            >
            self.probabilidad_merodear
        ):

            self.estado = "Descansando"

            return None


        opciones = [

            vecino

            for vecino in self.mundo.vecinos_validos(
                self.posicion
            )

            # Evita la arena y el campamento

            if self.mundo.grid[vecino] != 4
            and vecino != self.mundo.campamento

        ]


        if not opciones:

            self.estado = "Descansando"

            return None


        destino = random.choice(
            opciones
        )


        self.estado = "Merodeando"

        self.mundo.mover_jaguar(
            destino
        )

        return destino
