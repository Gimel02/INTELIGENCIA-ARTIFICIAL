# ==========================================
# FÍSICA CINEMÁTICA
#
# Cada personaje (cazador y jaguar) tiene un
# cuerpo con masa. Para pasar de una casilla
# a otra no "salta": acelera, alcanza una
# velocidad y recorre la distancia.
#
# Fuerzas (en la dirección del movimiento):
#
#   F_neta = F_motriz - F_rozamiento - F_arrastre
#
#   F_rozamiento = mu * m * g     (depende del suelo)
#   F_arrastre   = b * v          (resistencia al avanzar)
#
#   a = F_neta / m                (segunda ley de Newton)
#   v = v + a * dt
#   x = x + v * dt
#
# Velocidad máxima (cuando F_neta = 0):
#
#   v_max = (F_motriz - mu * m * g) / b
#
# Por eso:
# - Un cuerpo más pesado acelera más lento
#   y tiene menor velocidad máxima.
# - En arena (mu alto) todos van más lento.
# ==========================================

GRAVEDAD = 9.8

# Tamaño real de una casilla

METROS_POR_CASILLA = 2.0

# Coeficiente de rozamiento de cada suelo
# (tipo de casilla del mundo)

ROZAMIENTO_SUELO = {

    # Terreno normal
    0: 0.10,

    # Arena movediza
    4: 0.40,

    # Bayas (terreno normal)
    5: 0.10,
    6: 0.10

}

# Al cambiar de dirección se pierde velocidad

FACTOR_GIRO = 0.5

# Velocidad mínima para que nunca se quede
# atascado, aunque el suelo sea muy pesado

VELOCIDAD_MINIMA = 0.3


class CuerpoFisico:

    def __init__(
        self,
        masa,
        fuerza_motriz,
        coeficiente_arrastre,
        posicion
    ):

        # ==========================================
        # PROPIEDADES FÍSICAS
        # ==========================================

        # kg
        self.masa = masa

        # N
        self.fuerza_motriz = fuerza_motriz

        # N·s/m
        self.coeficiente_arrastre = (
            coeficiente_arrastre
        )


        # ==========================================
        # ESTADO DEL MOVIMIENTO
        # ==========================================

        # m/s
        self.velocidad = 0.0

        # m/s²
        self.aceleracion = 0.0

        # Casilla de donde sale y a donde va

        self.origen = posicion

        self.destino = posicion

        # Metros recorridos entre origen y destino

        self.recorrido = 0.0

        # Dirección del último movimiento

        self.direccion = (0, 0)

        # Tiempo que espera quieto antes
        # de volver a decidir (segundos)

        self.espera = 0.0


    # ==========================================
    # ¿ESTÁ QUIETO EN UNA CASILLA?
    # ==========================================

    def en_reposo(self):

        return (
            self.origen == self.destino
            and
            self.espera <= 0
        )


    # ==========================================
    # VELOCIDAD MÁXIMA EN UN SUELO
    # ==========================================

    def velocidad_maxima(
        self,
        tipo_suelo
    ):

        mu = ROZAMIENTO_SUELO.get(
            tipo_suelo,
            0.10
        )


        v_max = (

            (
                self.fuerza_motriz
                -
                mu * self.masa * GRAVEDAD
            )

            /

            self.coeficiente_arrastre

        )


        return max(
            VELOCIDAD_MINIMA,
            v_max
        )


    # ==========================================
    # EMPEZAR A MOVERSE HACIA UNA CASILLA
    # ==========================================

    def mover_a(
        self,
        destino
    ):

        nueva_direccion = (

            destino[0] - self.destino[0],

            destino[1] - self.destino[1]

        )


        # ======================================
        # CAMBIO DE DIRECCIÓN
        #
        # Para girar tiene que frenar: pierde
        # parte de su velocidad.
        # ======================================

        if nueva_direccion != self.direccion:

            self.velocidad *= FACTOR_GIRO


        self.direccion = nueva_direccion

        self.origen = self.destino

        self.destino = destino

        self.recorrido = 0.0


    # ==========================================
    # QUEDARSE QUIETO UN MOMENTO
    # ==========================================

    def detener(
        self,
        segundos
    ):

        self.velocidad = 0.0

        self.aceleracion = 0.0

        self.espera = segundos


    # ==========================================
    # ACTUALIZAR (cada cuadro de animación)
    #
    # tipo_suelo: casilla a la que se dirige
    # ==========================================

    def actualizar(
        self,
        dt,
        tipo_suelo
    ):

        # ======================================
        # ESPERANDO
        # ======================================

        if self.origen == self.destino:

            if self.espera > 0:

                self.espera -= dt

            return


        # ======================================
        # FUERZAS
        # ======================================

        mu = ROZAMIENTO_SUELO.get(
            tipo_suelo,
            0.10
        )


        fuerza_rozamiento = (
            mu
            *
            self.masa
            *
            GRAVEDAD
        )

        fuerza_arrastre = (
            self.coeficiente_arrastre
            *
            self.velocidad
        )

        fuerza_neta = (
            self.fuerza_motriz
            -
            fuerza_rozamiento
            -
            fuerza_arrastre
        )


        # ======================================
        # SEGUNDA LEY DE NEWTON
        # ======================================

        self.aceleracion = (
            fuerza_neta
            /
            self.masa
        )


        self.velocidad += (
            self.aceleracion
            *
            dt
        )

        self.velocidad = max(
            VELOCIDAD_MINIMA,
            self.velocidad
        )


        # ======================================
        # AVANZAR
        # ======================================

        self.recorrido += (
            self.velocidad
            *
            dt
        )


        # ======================================
        # LLEGÓ A LA CASILLA
        # ======================================

        if (
            self.recorrido
            >=
            METROS_POR_CASILLA
        ):

            self.origen = self.destino

            self.recorrido = 0.0


    # ==========================================
    # POSICIÓN PARA DIBUJAR
    #
    # Fila y columna con decimales, entre
    # la casilla de origen y la de destino.
    # ==========================================

    def posicion_visual(self):

        avance = (
            self.recorrido
            /
            METROS_POR_CASILLA
        )


        fila = (
            self.origen[0]
            +
            (self.destino[0] - self.origen[0])
            *
            avance
        )

        columna = (
            self.origen[1]
            +
            (self.destino[1] - self.origen[1])
            *
            avance
        )


        return (
            fila,
            columna
        )
