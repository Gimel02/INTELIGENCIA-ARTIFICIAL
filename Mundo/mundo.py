import random


class MundoSelva:

    def __init__(self):

        # =========================================
        # CONFIGURACIÓN DEL MUNDO
        # =========================================

        self.tamano_celda = 50

        self.filas = 10
        self.columnas = 12

        self.ancho = (
            self.columnas
            * self.tamano_celda
        )

        self.alto = (
            self.filas
            * self.tamano_celda
        )


        # =========================================
        # TIPOS DE TERRENO
        # =========================================
        #
        # 0 = terreno normal
        # 1 = árbol
        # 4 = arena movediza
        # 5 = baya buena
        # 6 = baya mala
        #
        # =========================================

        self.grid = {}


        # =========================================
        # POSICIONES
        # =========================================

        self.campamento = None

        self.inicio_cazador = None
        self.posicion_cazador = None

        self.inicio_puma = None
        self.posicion_puma = None

        # Estado del puma
        self.puma_vivo = True


        # =========================================
        # GENERAR MUNDO UNA SOLA VEZ
        # =========================================

        self.generar_mundo()


    # =========================================
    # GENERAR MUNDO
    # =========================================

    def generar_mundo(self):

        for fila in range(self.filas):

            for columna in range(self.columnas):

                numero = random.random()


                if numero < 0.15:

                    self.grid[
                        (fila, columna)
                    ] = 1


                elif numero < 0.23:

                    self.grid[
                        (fila, columna)
                    ] = 4


                elif numero < 0.27:

                    self.grid[
                        (fila, columna)
                    ] = 5


                elif numero < 0.30:

                    self.grid[
                        (fila, columna)
                    ] = 6


                else:

                    self.grid[
                        (fila, columna)
                    ] = 0


        # =========================================
        # CAMPAMENTO
        # =========================================

        self.campamento = (
            self.posicion_aleatoria_valida()
        )


        # =========================================
        # CAZADOR
        # =========================================

        self.inicio_cazador = (
            self.campamento
        )

        self.posicion_cazador = (
            self.inicio_cazador
        )

    # =========================================
        # PUMA
        # =========================================

        self.puma_vivo = True

        self.inicio_puma = (
            self.posicion_aleatoria_valida(
                exclude=[
                    self.campamento
                ]
            )
        )

        self.posicion_puma = (
            self.inicio_puma
        )


    # =========================================
    # POSICIÓN ALEATORIA
    # =========================================

    def posicion_aleatoria_valida(
        self,
        exclude=None
    ):

        if exclude is None:

            exclude = []


        while True:

            posicion = (

                random.randint(
                    0,
                    self.filas - 1
                ),

                random.randint(
                    0,
                    self.columnas - 1
                )

            )


            # Para iniciar personajes queremos
            # terreno libre.

            if (

                self.grid[posicion] == 0

                and

                posicion not in exclude

            ):

                return posicion


    # =========================================
    # ¿ESTÁ DENTRO DEL TABLERO?
    # =========================================

    def dentro_limites(
        self,
        posicion
    ):

        fila, columna = posicion

        return (

            0 <= fila < self.filas

            and

            0 <= columna < self.columnas

        )


    # =========================================
    # ¿SE PUEDE CAMINAR?
    # =========================================

    def es_transitable(
        self,
        posicion
    ):

        # Primero comprobamos límites

        if not self.dentro_limites(
            posicion
        ):

            return False


        # Después comprobamos árboles

        if self.grid[posicion] == 1:

            return False


        return True


    # =========================================
    # VECINOS VÁLIDOS
    # =========================================

    def vecinos_validos(
        self,
        posicion
    ):

        fila, columna = posicion


        posibles = [

            (
                fila - 1,
                columna
            ),

            (
                fila + 1,
                columna
            ),

            (
                fila,
                columna - 1
            ),

            (
                fila,
                columna + 1
            )

        ]


        validos = []


        for vecino in posibles:

            if self.es_transitable(
                vecino
            ):

                validos.append(
                    vecino
                )


        return validos

    # =========================================
    # MOVER CAZADOR
    # =========================================

    def mover_cazador(
        self,
        nueva_posicion
    ):

        if not self.es_transitable(
            nueva_posicion
        ):

            return False


        self.posicion_cazador = (
            nueva_posicion
        )

        return True


    # =========================================
    # MOVER PUMA
    # =========================================

    

    
    # =========================================
    # CAZAR PUMA
    # =========================================

    def cazar_puma(self):

        if not self.puma_vivo:

            return False

        self.puma_vivo = False

        return True


    # =========================================
    # CONTENIDO DE CELDA
    # =========================================

    def contenido_celda(
        self,
        fila,
        columna
    ):

        posicion = (
            fila,
            columna
        )


        # =========================================
        # FUERA DEL MUNDO
        # =========================================

        if not self.dentro_limites(
            posicion
        ):

            return "borde"


        tipo = self.grid[
            posicion
        ]


        if tipo == 1:

            return "arbol"

        elif tipo == 4:

            return "arena"

        elif tipo == 5:

            return "baya_buena"

        elif tipo == 6:

            return "baya_mala"

        else:

            return "libre"


    # =========================================
    # PERCEPCIÓN INMEDIATA
    # =========================================

    def obtener_percepcion(
        self,
        agente
    ):

        fila = agente.fila
        columna = agente.columna


        return {

            "arriba":
                self.contenido_celda(
                    fila - 1,
                    columna
                ),

            "abajo":
                self.contenido_celda(
                    fila + 1,
                    columna
                ),

            "izquierda":
                self.contenido_celda(
                    fila,
                    columna - 1
                ),

            "derecha":
                self.contenido_celda(
                    fila,
                    columna + 1
                )

        }


    # =========================================
    # COMPROBAR COLISIÓN
    # =========================================

    def comprobar_colision(
        self,
        fila,
        columna
    ):

        posicion = (
            fila,
            columna
        )


        return not self.es_transitable(
            posicion
        )