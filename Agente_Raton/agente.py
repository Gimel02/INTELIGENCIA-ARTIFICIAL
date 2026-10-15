import math
import random


class AgenteRaton:

    # ==========================================
    # AGENTE CONTINUO
    #
    # A diferencia del cazador y del jaguar,
    # el ratón NO se mueve de casilla en
    # casilla: su posición es continua (con
    # decimales) y tiene un vector de
    # velocidad.
    #
    # Unidades: casillas y segundos.
    # La posición (x, y) es el centro del
    # ratón: x = columna + 0.5, y = fila + 0.5
    #
    # Comportamientos (steering):
    # - Merodear: cambia poco a poco de
    #   dirección, al azar.
    # - Huir: si percibe al jaguar, corre en
    #   la dirección contraria.
    # - Evitar obstáculos: no entra a árboles
    #   ni sale del mapa.
    # ==========================================

    def __init__(self, mundo, identificador, casilla):

        self.mundo = mundo

        self.id = identificador

        self.vivo = True


        # ==========================================
        # POSICIÓN Y VELOCIDAD CONTINUAS
        # ==========================================

        self.x = casilla[1] + 0.5

        self.y = casilla[0] + 0.5

        self.vx = 0.0

        self.vy = 0.0

        # Hacia dónde quiere ir (radianes)

        self.rumbo = random.uniform(
            0,
            2 * math.pi
        )


        # ==========================================
        # PARÁMETROS
        # ==========================================

        # Casillas por segundo

        self.velocidad_merodeo = 0.5

        self.velocidad_huida = 0.95

        # Qué tan rápido cambia su velocidad
        # hacia la deseada (aceleración)

        self.agilidad = 4.0

        # Distancia (en casillas) a la que
        # percibe al jaguar

        self.rango_percepcion = 3.0


        self.estado = "Merodeando"


    # ==========================================
    # CASILLA DONDE ESTÁ
    # ==========================================

    @property
    def posicion(self):

        return (
            int(self.y),
            int(self.x)
        )


    # ==========================================
    # POSICIÓN PARA DIBUJAR (fila, columna)
    # ==========================================

    def posicion_visual(self):

        return (
            self.y - 0.5,
            self.x - 0.5
        )


    # ==========================================
    # ¿PUEDE ESTAR EN ESE PUNTO?
    # ==========================================

    def punto_libre(self, x, y):

        casilla = (
            int(math.floor(y)),
            int(math.floor(x))
        )

        return self.mundo.es_transitable(
            casilla
        )


    # ==========================================
    # ACTUALIZAR (cada cuadro de animación)
    #
    # posicion_jaguar: (fila, columna) con
    # decimales, o None si no hay jaguar
    # ==========================================

    def actualizar(
        self,
        dt,
        posicion_jaguar
    ):

        if not self.vivo:

            return


        # ======================================
        # 1. PERCIBIR AL JAGUAR
        # ======================================

        huir_de = None

        if posicion_jaguar is not None:

            jx = posicion_jaguar[1] + 0.5

            jy = posicion_jaguar[0] + 0.5

            distancia = math.hypot(
                self.x - jx,
                self.y - jy
            )

            if distancia <= self.rango_percepcion:

                huir_de = (jx, jy)


        # ======================================
        # 2. VELOCIDAD DESEADA
        # ======================================

        if huir_de is not None:

            # Dirección contraria al jaguar

            self.rumbo = math.atan2(
                self.y - huir_de[1],
                self.x - huir_de[0]
            )

            rapidez = self.velocidad_huida

            self.estado = "Huyendo"

        else:

            # Merodear: girar un poco al azar

            self.rumbo += random.uniform(
                -1.5,
                1.5
            ) * dt

            rapidez = self.velocidad_merodeo

            self.estado = "Merodeando"


        # ======================================
        # 3. EVITAR OBSTÁCULOS
        #
        # Mira un poco adelante. Si ahí hay un
        # árbol o el borde, prueba otros rumbos
        # cercanos y toma el primero libre.
        # ======================================

        self.rumbo = self.rumbo_libre(
            self.rumbo
        )


        deseada_x = math.cos(self.rumbo) * rapidez

        deseada_y = math.sin(self.rumbo) * rapidez


        # ======================================
        # 4. ACELERAR HACIA LA VELOCIDAD DESEADA
        # ======================================

        ajuste = min(
            1.0,
            self.agilidad * dt
        )

        self.vx += (deseada_x - self.vx) * ajuste

        self.vy += (deseada_y - self.vy) * ajuste


        # ======================================
        # 5. AVANZAR
        #
        # Si el siguiente punto choca, solo
        # avanza en el eje que sí está libre.
        # ======================================

        nueva_x = self.x + self.vx * dt

        nueva_y = self.y + self.vy * dt


        if self.punto_libre(nueva_x, nueva_y):

            self.x = nueva_x

            self.y = nueva_y

        elif self.punto_libre(nueva_x, self.y):

            self.x = nueva_x

            self.vy = 0.0

        elif self.punto_libre(self.x, nueva_y):

            self.y = nueva_y

            self.vx = 0.0

        else:

            self.vx = 0.0

            self.vy = 0.0

            self.rumbo += math.pi


    # ==========================================
    # BUSCAR UN RUMBO SIN OBSTÁCULOS
    # ==========================================

    def rumbo_libre(self, rumbo):

        mirar = 0.6

        for giro in (
            0,
            0.4, -0.4,
            0.8, -0.8,
            1.3, -1.3,
            1.9, -1.9,
            math.pi
        ):

            prueba = rumbo + giro

            x = self.x + math.cos(prueba) * mirar

            y = self.y + math.sin(prueba) * mirar

            if self.punto_libre(x, y):

                return prueba


        return rumbo
