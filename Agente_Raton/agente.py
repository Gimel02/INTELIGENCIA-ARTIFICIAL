
import math
import random


class AgenteRaton:

    def __init__(self, mundo, identificador, casilla):

        self.mundo = mundo
        self.id = identificador
        self.vivo = True

        # ==========================================
        # POSICIÓN DEL RATÓN
        # ==========================================

        # El ratón comienza en el centro de su casilla
        self.x = casilla[1] + 0.5
        self.y = casilla[0] + 0.5

        self.vx = 0.0
        self.vy = 0.0

        # ==========================================
        # DIRECCIÓN
        # ==========================================

        self.direccion = random.choice([
            "arriba",
            "abajo",
            "izquierda",
            "derecha"
        ])

        self.rumbo = 0.0

        # ==========================================
        # PARÁMETROS DE MOVIMIENTO
        # ==========================================

        self.velocidad_merodeo = 0.5
        self.velocidad_huida = 0.95

        self.agilidad = 4.0
        self.rango_percepcion = 3.0

        self.estado = "Merodeando"

        self.tiempo_cambio = random.uniform(0.8, 2.0)
        self.tiempo_bloqueo = 0.0

        # ==========================================
        # MARGEN DE SEGURIDAD
        # ==========================================

        # 0.30 celdas equivalen a 15 píxeles
        # cuando cada celda mide 50 píxeles.
        self.margen_borde = 0.30

    # ==========================================
    # POSICIÓN EN EL MAPA
    # ==========================================

    @property
    def posicion(self):
        """Devuelve la posición como (fila, columna)."""
        return (
            int(math.floor(self.y)),
            int(math.floor(self.x))
        )

    def posicion_visual(self):
        """Posición utilizada para dibujar el ratón."""
        return (
            self.y - 0.5,
            self.x - 0.5
        )

    # ==========================================
    # COMPROBAR POSICIÓN LIBRE
    # ==========================================

    def punto_libre(self, x, y):
        """
        Comprueba que el ratón permanezca dentro del mapa
        y que no entre en una casilla con un árbol.
        """

        filas = self.mundo.filas
        columnas = self.mundo.columnas

        margen = self.margen_borde

        # Evitar que el ratón se salga por los bordes
        if x < margen or x >= columnas - margen:
            return False

        if y < margen or y >= filas - margen:
            return False

        # Convertir las coordenadas a (fila, columna)
        casilla = (
            int(math.floor(y)),
            int(math.floor(x))
        )

        # Comprobar si la casilla es transitable
        return self.mundo.es_transitable(casilla)

    # ==========================================
    # COMPROBAR SI PUEDE AVANZAR
    # ==========================================

    def puede_avanzar(self, direccion, paso=0.2):

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

    # ==========================================
    # BUSCAR UNA DIRECCIÓN LIBRE
    # ==========================================

    def buscar_direccion_libre(self, rapidez, dt):

        opciones = [
            ("arriba", 0, -1),
            ("abajo", 0, 1),
            ("izquierda", -1, 0),
            ("derecha", 1, 0)
        ]

        # Distancia de prueba
        paso = max(rapidez * dt, 0.2)

        libres = []

        for direccion, dx, dy in opciones:

            prueba_x = self.x + dx * paso
            prueba_y = self.y + dy * paso

            if self.punto_libre(prueba_x, prueba_y):
                libres.append(direccion)

        # Direcciones opuestas
        opuestas = {
            "arriba": "abajo",
            "abajo": "arriba",
            "izquierda": "derecha",
            "derecha": "izquierda"
        }

        # Intentar no regresar inmediatamente
        alternativas = [
            direccion
            for direccion in libres
            if direccion != opuestas[self.direccion]
        ]

        if alternativas:
            libres = alternativas

        # Conservar la dirección si sigue disponible
        if self.direccion in libres:
            return self.direccion

        # Elegir otra dirección disponible
        if libres:
            return random.choice(libres)

        # No existe ninguna dirección libre
        return None

    # ==========================================
    # ACTUALIZAR MOVIMIENTO DEL RATÓN
    # ==========================================

    def actualizar(self, dt, posicion_jaguar):

        if not self.vivo:
            return

        # Limitar dt para evitar saltos grandes
        dt = min(max(dt, 0.0), 0.05)

        self.tiempo_bloqueo = max(
            0.0,
            self.tiempo_bloqueo - dt
        )

        # ==========================================
        # 1. DETECTAR AL JAGUAR
        # ==========================================

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

        # ==========================================
        # 2. ELEGIR DIRECCIÓN
        # ==========================================

        if huir_de is not None:

            dx_jaguar = self.x - huir_de[0]
            dy_jaguar = self.y - huir_de[1]

            # Huir por el eje que más los separa
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

            if self.puede_avanzar(direccion_huida):

                self.direccion = direccion_huida

            else:

                nueva_direccion = self.buscar_direccion_libre(
                    self.velocidad_huida,
                    dt
                )

                if nueva_direccion is not None:
                    self.direccion = nueva_direccion

            self.estado = "Huyendo"
            rapidez = self.velocidad_huida

        else:

            self.estado = "Merodeando"
            rapidez = self.velocidad_merodeo

            self.tiempo_cambio -= dt

            if self.tiempo_cambio <= 0:

                self.direccion = random.choice([
                    "arriba",
                    "abajo",
                    "izquierda",
                    "derecha"
                ])

                self.tiempo_cambio = random.uniform(
                    0.8,
                    2.0
                )

        # ==========================================
        # 3. MOVIMIENTO EN CUATRO DIRECCIONES
        # ==========================================

        self.vx = 0.0
        self.vy = 0.0

        if self.direccion == "derecha":

            self.vx = rapidez
            self.rumbo = 0.0

        elif self.direccion == "izquierda":

            self.vx = -rapidez
            self.rumbo = math.pi

        elif self.direccion == "abajo":

            self.vy = rapidez
            self.rumbo = math.pi / 2

        elif self.direccion == "arriba":

            self.vy = -rapidez
            self.rumbo = 3 * math.pi / 2

        # ==========================================
        # 4. CALCULAR NUEVA POSICIÓN
        # ==========================================

        nueva_x = self.x + self.vx * dt
        nueva_y = self.y + self.vy * dt

        # ==========================================
        # 5. VALIDAR MOVIMIENTO
        # ==========================================

        if self.punto_libre(nueva_x, nueva_y):

            self.x = nueva_x
            self.y = nueva_y

            self.tiempo_bloqueo = 0.0

        else:

            # Detener el movimiento ante un obstáculo
            self.vx = 0.0
            self.vy = 0.0

            if self.tiempo_bloqueo <= 0.0:

                nueva_direccion = self.buscar_direccion_libre(
                    rapidez,
                    dt
                )

                if nueva_direccion is not None:

                    self.direccion = nueva_direccion

                else:

                    # Si está encerrado, intentar otra dirección
                    self.direccion = random.choice([
                        "arriba",
                        "abajo",
                        "izquierda",
                        "derecha"
                    ])

                self.tiempo_bloqueo = 0.1
                self.tiempo_cambio = 0.5
