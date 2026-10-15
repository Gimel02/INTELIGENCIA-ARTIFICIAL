import random

from Algoritmos.a_Estrella import AEstrella
from Algoritmos.huida import Huida
from Algoritmos.persecucion import Persecucion


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
                # ==========================================
        # HAMBRE
        # ==========================================

        self.hambre = 0
        self.hambre_max = 100

        # Cuánto aumenta por cada decisión
        self.aumento_hambre = 2
        self.estado_hambre = "NORMAL"


        # ==========================================
        # CAZA DE RATONES
        # ==========================================

        # Distancia a la que huele a los ratones

        self.rango_olfato_ratones = 6

        # Cuánta hambre se quita al comer uno

        self.saciedad_raton = 50


        # ==========================================
        # INVERSIÓN DE PAPELES: ATACAR AL CAZADOR
        #
        # Normalmente el jaguar huye del cazador.
        # Pero se vuelve el PERSEGUIDOR si:
        # - el cazador está débil (energía < 30)
        # - o tiene HAMBRE INDOMABLE y ya no
        #   quedan ratones
        # ==========================================

        self.energia_debil_cazador = 30

        # Distancia a la que lo sigue persiguiendo
        # una vez que empezó el ataque

        self.rango_ataque = 8

        self.atacando = False

        # Decisiones que pasa huyendo después
        # de atacar (no puede volver a atacar)

        self.retirada = 0

        self.decisiones_retirada = 6

        # Última posición donde vio al cazador
        # (para cortarle el paso)

        self.cazador_anterior = None

        # El cazador revisa esto: mientras el
        # jaguar ataca o se retira, no lo puede
        # atrapar

        mundo.jaguar_peligroso = False

        # True mientras persigue al cazador
        # (el cazador lo puede percibir)

        mundo.jaguar_atacando = False


        self.estado = "Descansando"


    # ==========================================
    # POSICIÓN
    # ==========================================

    @property
    def posicion(self):

        return self.mundo.posicion_jaguar


    # ==========================================
    # ACTUALIZAR HAMBRE
    # ==========================================

    def actualizar_hambre(self):

        self.hambre += self.aumento_hambre

        self.hambre = min(
            self.hambre,
            self.hambre_max
        )

        self.actualizar_nivel_hambre()


    # ==========================================
    # NIVEL DE HAMBRE
    # ==========================================

    def actualizar_nivel_hambre(self):

        if self.hambre >= 80:

            self.estado_hambre = (
                "HAMBRE INDOMABLE"
            )

        elif self.hambre >= 40:

            self.estado_hambre = (
                "HAMBRIENTO"
            )

        else:

            self.estado_hambre = (
                "NORMAL"
            )


    # ==========================================
    # TOMAR DECISIÓN
    #
    # Prioridades:
    # 0. Retirarse después de atacar
    # 1. Atacar al cazador (inversión de papeles)
    # 2. Huir del cazador
    # 3. Cazar ratones si tiene hambre
    # 4. Descansar o merodear
    #
    # Devuelve la casilla a la que se mueve,
    # o None si se queda quieto.
    # ==========================================

    def tomar_decision(
        self,
        posicion_cazador,
        energia_cazador=100,
        ratones=None
    ):

        if not self.mundo.jaguar_vivo:

            return None


        self.actualizar_hambre()


        if ratones is None:

            ratones = []


        ratones_vivos = [
            raton
            for raton in ratones
            if raton.vivo
        ]


        distancia = (
            AEstrella.heuristica(
                self.posicion,
                posicion_cazador
            )
        )


        destino = self.decidir(
            posicion_cazador,
            energia_cazador,
            ratones_vivos,
            distancia
        )


        self.cazador_anterior = posicion_cazador

        self.mundo.jaguar_atacando = self.atacando

        self.mundo.jaguar_peligroso = (
            self.atacando
            or
            self.retirada > 0
        )


        if destino is not None:

            self.mundo.mover_jaguar(
                destino
            )


        return destino


    def decidir(
        self,
        posicion_cazador,
        energia_cazador,
        ratones_vivos,
        distancia
    ):

        # ==========================================
        # 0. RETIRADA DESPUÉS DE ATACAR
        # ==========================================

        if self.retirada > 0:

            self.retirada -= 1

            self.atacando = False

            self.estado = "Retirándose tras el ataque"

            return Huida.elegir_escape(
                self.posicion,
                posicion_cazador,
                self.mundo
            )


        # ==========================================
        # 1. INVERSIÓN DE PAPELES: ATACAR
        # ==========================================

        cazador_debil = (
            energia_cazador
            <
            self.energia_debil_cazador
        )

        # HAMBRE INDOMABLE: el hambre le quita el
        # miedo y ataca al cazador aunque todavía
        # queden ratones

        hambre_indomable = (
            self.hambre >= 80
        )

        alcance = (
            self.rango_ataque
            if self.atacando
            else self.rango_deteccion
        )


        if (
            (cazador_debil or hambre_indomable)
            and
            distancia <= alcance
        ):

            self.atacando = True


            if cazador_debil:

                self.estado = (
                    "¡Atacando al cazador débil!"
                )

            else:

                self.estado = (
                    "¡Hambre indomable! Atacando"
                )


            # Persecución: apunta a donde va a
            # estar el cazador

            meta = Persecucion.punto_intercepcion(
                self.posicion,
                posicion_cazador,
                self.cazador_anterior,
                self.mundo
            )

            return self.paso_hacia(meta)


        self.atacando = False


        # ==========================================
        # 2. DETECTA AL CAZADOR: ESCAPAR
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

                # Acorralado: si el cazador está muy
                # cerca, contraataca en vez de
                # quedarse quieto

                if distancia <= 2:

                    self.atacando = True

                    self.estado = (
                        "¡Acorralado! Contraataca"
                    )

                    return self.paso_hacia(
                        posicion_cazador
                    )


                self.estado = "Acorralado"

                return None


            self.estado = "Huyendo"

            return destino


        # ==========================================
        # 3. TIENE HAMBRE: CAZAR RATONES
        # ==========================================

        if (
            self.hambre >= 40
            and
            ratones_vivos
        ):

            cercano = min(
                ratones_vivos,
                key=lambda raton:
                AEstrella.heuristica(
                    self.posicion,
                    raton.posicion
                )
            )


            if (
                AEstrella.heuristica(
                    self.posicion,
                    cercano.posicion
                )
                <=
                self.rango_olfato_ratones
            ):

                self.estado = "Cazando ratón"

                return self.paso_hacia(
                    cercano.posicion
                )


            # No huele ninguno: los busca
            # (con hambre sí cruza la arena)

            self.estado = "Buscando ratones"

            return self.merodear(
                cruzar_arena=True
            )


        # ==========================================
        # 4. TRANQUILO: MERODEAR O DESCANSAR
        # ==========================================

        if (
            random.random()
            >
            self.probabilidad_merodear
        ):

            self.estado = "Descansando"

            return None


        self.estado = "Merodeando"

        return self.merodear()


    # ==========================================
    # DAR UN PASO HACIA UNA META (A*)
    # ==========================================

    def paso_hacia(self, meta):

        if meta == self.posicion:

            return None


        camino = AEstrella.buscar(
            self.posicion,
            meta,
            self.mundo
        )


        if not camino:

            return None


        return camino[0]


    # ==========================================
    # MERODEAR: UN PASO AL AZAR
    # ==========================================

    def merodear(self, cruzar_arena=False):

        opciones = [

            vecino

            for vecino in self.mundo.vecinos_validos(
                self.posicion
            )

            # Evita el campamento, y la arena
            # salvo que tenga hambre

            if (
                cruzar_arena
                or
                self.mundo.grid[vecino] != 4
            )
            and vecino != self.mundo.campamento

        ]


        if not opciones:

            return None


        return random.choice(
            opciones
        )


    # ==========================================
    # COMER UN RATÓN
    # ==========================================

    def comer_raton(self):

        self.hambre = max(
            0,
            self.hambre - self.saciedad_raton
        )

        self.actualizar_nivel_hambre()

        self.estado = "¡Comió un ratón!"


    # ==========================================
    # DESPUÉS DE ATACAR AL CAZADOR
    # ==========================================

    def despues_de_atacar(self):

        self.atacando = False

        self.retirada = self.decisiones_retirada

        self.hambre = max(
            0,
            self.hambre - 40
        )

        self.actualizar_nivel_hambre()

        self.mundo.jaguar_peligroso = True

        self.mundo.jaguar_atacando = False

        self.estado = "¡Atacó al cazador!"
