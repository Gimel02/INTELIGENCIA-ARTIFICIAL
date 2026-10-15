
import math
import random


class AgenteRaton:

    def __init__(self, mundo, identificador, casilla):

        self.mundo = mundo
        self.id = identificador
        self.vivo = True

        # ==========================================
        # POSICION Y VELOCIDAD
        # ==========================================

        self.x = casilla[1] + 0.5
        self.y = casilla[0] + 0.5

        self.vx = 0.0
        self.vy = 0.0

        # Direccion inicial
        self.rumbo = random.choice([
            0,
            math.pi / 2,
            math.pi,
            3 * math.pi / 2
        ])

        # ==========================================
        # PARAMETROS DE MOVIMIENTO
        # ==========================================

        self.velocidad_merodeo = 0.5
        self.velocidad_huida = 0.95
        self.agilidad = 4.0
        self.rango_percepcion = 3.0

        self.estado = "Merodeando"
        self.direccion = "abajo"

        # Tiempo para cambiar de direccion
        self.tiempo_cambio = 0.0

        # Evita cambiar de direccion constantemente
        # cuando el raton encuentra un obstaculo
        self.tiempo_bloqueo = 0.0

    # ==========================================
    # POSICION EN LA CUADRICULA
    # ==========================================

    @property
    def posicion(self):
        return (
            int(self.y),
            int(self.x)
        )

    # ==========================================
    # POSICION PARA DIBUJAR
    # ==========================================

    def posicion_visual(self):
        return (
            self.y - 0.5,
            self.x - 0.5
        )

    # ==========================================
    # COMPROBAR SI UN PUNTO ES TRANSITABLE
    # ==========================================

    def punto_libre(self, x, y):

        casilla = (
            int(math.floor(y)),
            int(math.floor(x))
        )

        return self.mundo.es_transitable(casilla)

    # ==========================================
    # CONVERTIR ANGULO EN CUATRO DIRECCIONES
    # ==========================================

    def ajustar_direccion(self, rumbo):

        rumbo = rumbo % (2 * math.pi)

        if rumbo < math.pi / 4 or rumbo >= 7 * math.pi / 4:
            return "derecha"

        elif rumbo < 3 * math.pi / 4:
            return "abajo"

        elif rumbo < 5 * math.pi / 4:
            return "izquierda"

        else:
            return "arriba"

    # ==========================================
    # ACTUALIZAR MOVIMIENTO DEL RATON
    # ==========================================

    def actualizar(self, dt, posicion_jaguar):

        if not self.vivo:
            return

        self.tiempo_bloqueo = max(
            0.0,
            self.tiempo_bloqueo - dt
        )

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
        # 2. ELEGIR DIRECCION Y VELOCIDAD
        # ======================================

        if huir_de is not None:

            dx_jaguar = self.x - huir_de[0]
            dy_jaguar = self.y - huir_de[1]

            # Alejarse por el eje de mayor diferencia
            if abs(dx_jaguar) > abs(dy_jaguar):

                direccion_huida = (
                    "derecha"
                    if dx_jaguar >= 0
                    else "izquierda"
                )

            else:

                direccion_huida = (
                    "abajo"
                    if dy_jaguar >= 0
                    else "arriba"
                )

            # Solo cambiar si la direccion de huida
            # esta libre o si el raton esta bloqueado
            if (
                self.puede_avanzar(direccion_huida)
                or self.tiempo_bloqueo <= 0
            ):
                self.direccion = direccion_huida

            rapidez = self.velocidad_huida
            self.estado = "Huyendo"

        else:

            self.estado = "Merodeando"
            self.tiempo_cambio -= dt

            # Elegir otra direccion cuando corresponda
            if self.tiempo_cambio <= 0:

                self.direccion = random.choice([
                    "arriba",
                    "abajo",
                    "izquierda",
                    "derecha"
                ])

                self.tiempo_cambio = random.uniform(
                    0.8, 2.0
                )

            rapidez = self.velocidad_merodeo

        # ======================================
        # 3. PREPARAR MOVIMIENTO CARDINAL
        # ======================================

        self.vx = 0.0
        self.vy = 0.0

        if self.direccion == "derecha":
            self.vx = rapidez

        elif self.direccion == "izquierda":
            self.vx = -rapidez

        elif self.direccion == "abajo":
            self.vy = rapidez

        elif self.direccion == "arriba":
            self.vy = -rapidez

        # Actualizar rumbo
        if self.direccion == "derecha":
            self.rumbo = 0
        elif self.direccion == "abajo":
            self.rumbo = math.pi / 2
        elif self.direccion == "izquierda":
            self.rumbo = math.pi
        else:
            self.rumbo = 3 * math.pi / 2

        # ======================================
        # 4. CALCULAR NUEVA POSICION
        # ======================================

        nueva_x = self.x + self.vx * dt
        nueva_y = self.y + self.vy * dt

        if self.punto_libre(nueva_x, nueva_y):

            self.x = nueva_x
            self.y = nueva_y

            # El camino esta libre
            self.tiempo_bloqueo = 0.0

        else:

            # ==================================
            # 5. BUSCAR UNA DIRECCION LIBRE
            # ==================================

            opciones = [
                ("arriba", 0, -1),
                ("abajo", 0, 1),
                ("izquierda", -1, 0),
                ("derecha", 1, 0)
            ]

            # Comprobar un paso suficiente para
            # detectar la siguiente casilla
            paso = max(rapidez * dt, 0.1)

            libres = []

            for direccion, dx, dy in opciones:

                prueba_x = self.x + dx * paso
                prueba_y = self.y + dy * paso

                if self.punto_libre(prueba_x, prueba_y):
                    libres.append(direccion)

            # Evitar regresar inmediatamente
            # por donde venia
            opuestas = {
                "arriba": "abajo",
                "abajo": "arriba",
                "izquierda": "derecha",
                "derecha": "izquierda"
            }

            alternativas = [
                direccion
                for direccion in libres
                if direccion != opuestas.get(self.direccion)
            ]

            if alternativas:
                libres = alternativas

            if libres:

                # Priorizar continuar en linea recta
                # si esa direccion sigue disponible
                if self.direccion in libres:
                    nueva_direccion = self.direccion

                else:
                    nueva_direccion = random.choice(libres)

                self.direccion = nueva_direccion

                # Esperar brevemente antes de volver
                # a intentar cambiar por un obstaculo
                self.tiempo_bloqueo = 0.25
                self.tiempo_cambio = 0.4

            else:

                # Si no hay ninguna salida disponible,
                # detenerse temporalmente
                self.vx = 0.0
                self.vy = 0.0

                self.tiempo_bloqueo = 0.25
                self.tiempo_cambio = 0.4

    # ==========================================
    # COMPROBAR SI PUEDE AVANZAR EN UNA DIRECCION
    # ==========================================

    def puede_avanzar(self, direccion):

        paso = 0.2

        dx = 0.0
        dy = 0.0

        if direccion == "derecha":
            dx = paso

        elif direccion == "izquierda":
            dx = -paso

        elif direccion == "abajo":
            dy = paso

        elif direccion == "arriba":
            dy = -paso

        return self.punto_libre(
            self.x + dx,
            self.y + dy
        )
