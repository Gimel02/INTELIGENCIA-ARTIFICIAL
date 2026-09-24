# Lo que la vista distingue de cada tipo de casilla.
# De las bayas solo ve el color: no sabe si son
# buenas o malas hasta probarlas.

OBSERVACIONES = {

    1: "arbol",
    4: "arena",
    5: "morada",
    6: "roja"

}


class Sentidos:

    def __init__(self, mundo):

        self.mundo = mundo


        # ==========================================
        # VISTA
        # ==========================================

        # Los árboles tapan la vista

        self.rango_vista = 2

        self.ve_puma = False


        # ==========================================
        # OÍDO
        # ==========================================

        # El sonido sí pasa entre los árboles

        self.rango_oido = 3

        self.escucha_puma = False

        self.direccion_sonido = None

        self.intensidad_sonido = None

        self.objetivo_sonido = None


        # ==========================================
        # TACTO
        # ==========================================

        self.sensacion_tacto = (
            "Suelo firme"
        )

        # Direcciones de las casillas vecinas
        # donde siente arena movediza

        self.arena_cercana = []


        # ==========================================
        # GUSTO
        # ==========================================

        self.sensacion_gusto = (
            "Sin alimento"
        )


        # ==========================================
        # OLFATO
        # ==========================================

        # Olor del puma

        self.rango_olfato = 5

        self.huele_puma = False

        self.intensidad_olor = None

        self.objetivo_olor = None


        # Olor de las bayas que ya sabe
        # que son buenas

        self.rango_olfato_bayas = 3

        self.huele_bayas = False

        self.color_olor_bayas = None

        self.objetivo_olor_bayas = None


    # ==========================================
    # DISTANCIA MANHATTAN
    # ==========================================

    @staticmethod
    def distancia(
        posicion1,
        posicion2
    ):

        return (

            abs(
                posicion1[0]
                -
                posicion2[0]
            )

            +

            abs(
                posicion1[1]
                -
                posicion2[1]
            )

        )


    # ==========================================
    # NOMBRE DE UNA DIRECCIÓN
    # ==========================================

    @staticmethod
    def nombre_direccion(
        df,
        dc
    ):

        nombres = {

            (-1, 0): "NORTE",
            (1, 0): "SUR",
            (0, 1): "ESTE",
            (0, -1): "OESTE",

            (-1, 1): "NORESTE",
            (-1, -1): "NOROESTE",
            (1, 1): "SURESTE",
            (1, -1): "SUROESTE"

        }

        return nombres.get(
            (df, dc)
        )


    # ==========================================
    # LÍNEA DE VISTA
    #
    # Revisa las casillas que hay entre
    # el cazador y el destino.
    # Si un árbol está en medio, no lo puede ver.
    # ==========================================

    def hay_linea_de_vista(
        self,
        origen,
        destino
    ):

        df = destino[0] - origen[0]

        dc = destino[1] - origen[1]


        pasos = (
            abs(df)
            +
            abs(dc)
        )


        for i in range(
            1,
            pasos
        ):

            # ======================================
            # CASILLAS QUE CRUZA LA LÍNEA
            #
            # Si la línea pasa justo por la esquina
            # entre dos casillas, se revisan las dos.
            # ======================================

            filas = self.valores_en_linea(
                origen[0],
                df,
                i,
                pasos
            )

            columnas = self.valores_en_linea(
                origen[1],
                dc,
                i,
                pasos
            )


            casillas = []


            for fila in filas:

                for columna in columnas:

                    casilla = (
                        fila,
                        columna
                    )

                    if (
                        casilla != origen
                        and
                        casilla != destino
                    ):

                        casillas.append(
                            casilla
                        )


            if not casillas:

                continue


            # ======================================
            # SOLO SE TAPA SI TODAS LAS CASILLAS
            # DE ESE PUNTO SON ÁRBOLES
            # ======================================

            todas_son_arbol = all(

                self.mundo.grid.get(
                    casilla
                ) == 1

                for casilla in casillas

            )


            if todas_son_arbol:

                return False


        return True


    @staticmethod
    def valores_en_linea(
        inicio,
        diferencia,
        paso,
        pasos
    ):

        numerador = (
            diferencia
            *
            paso
        )


        # Cae exactamente en una casilla

        if numerador % pasos == 0:

            return [
                inicio
                +
                numerador // pasos
            ]


        # Cae justo entre dos casillas

        if (2 * numerador) % pasos == 0:

            abajo = (
                inicio
                +
                numerador // pasos
            )

            return [
                abajo,
                abajo + 1
            ]


        return [
            inicio
            +
            round(numerador / pasos)
        ]


    # ==========================================
    # OBSERVAR UNA CASILLA
    #
    # Devuelve lo que se ve: "arbol", "arena",
    # "morada", "roja" o "libre".
    # ==========================================

    def observar(
        self,
        posicion
    ):

        return OBSERVACIONES.get(

            self.mundo.grid[
                posicion
            ],

            "libre"

        )


    # ==========================================
    # ¿PUEDE VER ESA CASILLA?
    # ==========================================

    def puede_ver(
        self,
        posicion_agente,
        posicion
    ):

        if (
            self.distancia(
                posicion_agente,
                posicion
            )
            >
            self.rango_vista
        ):

            return False


        return self.hay_linea_de_vista(
            posicion_agente,
            posicion
        )


    # ==========================================
    # OBTENER CELDAS VISIBLES
    # ==========================================

    def obtener_celdas_visibles(
        self,
        posicion_agente
    ):

        visibles = []


        for fila in range(
            self.mundo.filas
        ):

            for columna in range(
                self.mundo.columnas
            ):

                posicion = (
                    fila,
                    columna
                )


                # ======================================
                # DENTRO DEL RANGO Y SIN ÁRBOLES
                # EN MEDIO
                # ======================================

                if self.puede_ver(
                    posicion_agente,
                    posicion
                ):

                    visibles.append(
                        posicion
                    )


        return visibles


    # ==========================================
    # OBTENER CELDAS DEL RANGO DE OÍDO
    # ==========================================

    def obtener_celdas_oido(
        self,
        posicion_agente
    ):

        celdas_oido = []


        for fila in range(
            self.mundo.filas
        ):

            for columna in range(
                self.mundo.columnas
            ):

                posicion = (
                    fila,
                    columna
                )


                distancia = (
                    self.distancia(

                        posicion_agente,

                        posicion

                    )
                )


                # ======================================
                # RANGO DEL OÍDO
                #
                # Solo se toman las celdas:
                #
                # 1. Que no puede ver
                #    (lejos o tapadas por árboles)
                # 2. Dentro del rango de oído
                # ======================================

                if (

                    distancia
                    <=
                    self.rango_oido

                    and

                    not self.puede_ver(
                        posicion_agente,
                        posicion
                    )

                ):

                    celdas_oido.append(
                        posicion
                    )


        return celdas_oido


    # ==========================================
    # USAR VISTA
    # ==========================================

    def usar_vista(
        self,
        posicion_agente,
        posicion_puma
    ):

        visibles = (
            self.obtener_celdas_visibles(
                posicion_agente
            )
        )


        # ======================================
        # ¿PUMA DENTRO DEL RANGO?
        # ======================================

        if posicion_puma in visibles:

            self.ve_puma = True

        else:

            self.ve_puma = False


        # ======================================
        # TERRENO QUE VE
        #
        # Árboles, arena y bayas (por color)
        # que tiene enfrente, para guardarlos
        # en memoria.
        # ======================================

        terreno = {

            posicion:
                self.observar(
                    posicion
                )

            for posicion in visibles

        }


        return {

            "detectado":
                self.ve_puma,

            "celdas_visibles":
                visibles,

            "terreno":
                terreno

        }


    # ==========================================
    # USAR OÍDO
    # ==========================================

    def usar_oido(
        self,
        posicion_agente,
        posicion_puma
    ):

        distancia = (
            self.distancia(

                posicion_agente,

                posicion_puma

            )
        )


        # ======================================
        # FUERA DEL RANGO DEL OÍDO
        # O LO PUEDE VER
        # ======================================

        if (

            distancia
            >
            self.rango_oido

            or

            self.puede_ver(
                posicion_agente,
                posicion_puma
            )

        ):

            self.escucha_puma = False

            self.direccion_sonido = None

            self.intensidad_sonido = None

            self.objetivo_sonido = None

            return False


        # ======================================
        # ESCUCHA AL PUMA
        # ======================================

        self.escucha_puma = True


        diferencia_filas = (
            posicion_puma[0]
            -
            posicion_agente[0]
        )

        diferencia_columnas = (
            posicion_puma[1]
            -
            posicion_agente[1]
        )


        # ======================================
        # DETERMINAR DIRECCIÓN DEL SONIDO
        #
        # Ahora también reconoce diagonales.
        # Si una diferencia es más del doble
        # que la otra, la dirección es recta.
        # ======================================

        df = (
            (diferencia_filas > 0)
            -
            (diferencia_filas < 0)
        )

        dc = (
            (diferencia_columnas > 0)
            -
            (diferencia_columnas < 0)
        )


        if (
            abs(diferencia_filas)
            >
            2 * abs(diferencia_columnas)
        ):

            dc = 0

        elif (
            abs(diferencia_columnas)
            >
            2 * abs(diferencia_filas)
        ):

            df = 0


        self.direccion_sonido = (
            self.nombre_direccion(
                df,
                dc
            )
        )


        # ======================================
        # INTENSIDAD DEL SONIDO
        #
        # Entre más cerca, más fuerte.
        # ======================================

        if (
            distancia
            <
            self.rango_oido
        ):

            self.intensidad_sonido = (
                "fuerte"
            )

        else:

            self.intensidad_sonido = (
                "débil"
            )


        # ======================================
        # CREAR OBJETIVO APROXIMADO
        # ======================================

        self.objetivo_sonido = (
            self.crear_objetivo_sonido(
                posicion_agente,
                df,
                dc
            )
        )


        return True


    # ==========================================
    # CREAR OBJETIVO DEL SONIDO
    # ==========================================

    def crear_objetivo_sonido(
        self,
        posicion_agente,
        df,
        dc
    ):

        fila, columna = (
            posicion_agente
        )


        # ======================================
        # DIRECCIÓN NO VÁLIDA
        # ======================================

        if (
            df == 0
            and
            dc == 0
        ):

            return None


        # ======================================
        # BUSCAR HASTA 3 CASILLAS
        #
        # En diagonal cada paso avanza 2
        # casillas, por eso solo intenta 2 y 1.
        # ======================================

        if df != 0 and dc != 0:

            maximo = 2

        else:

            maximo = 3


        for distancia in range(
            maximo,
            0,
            -1
        ):

            posicion = (

                fila
                +
                df
                *
                distancia,

                columna
                +
                dc
                *
                distancia

            )


            # ======================================
            # DEBE SER UNA CELDA TRANSITABLE
            # ======================================

            if self.mundo.es_transitable(
                posicion
            ):

                return posicion


        return None


    # ==========================================
    # USAR TACTO
    # ==========================================

    def usar_tacto(
        self,
        posicion
    ):

        # ======================================
        # CASILLAS VECINAS
        #
        # Siente la arena de alrededor
        # antes de pisarla.
        # ======================================

        self.arena_cercana = []

        arena_vecina = []


        fila, columna = posicion


        for df, dc in (
            (-1, 0),
            (1, 0),
            (0, 1),
            (0, -1)
        ):

            vecino = (
                fila + df,
                columna + dc
            )


            if (
                self.mundo.dentro_limites(
                    vecino
                )
                and
                self.mundo.grid[
                    vecino
                ] == 4
            ):

                self.arena_cercana.append(
                    self.nombre_direccion(
                        df,
                        dc
                    )
                )

                arena_vecina.append(
                    vecino
                )


        tipo = (
            self.mundo.grid[
                posicion
            ]
        )


        # ======================================
        # ARENA MOVEDIZA
        # ======================================

        if tipo == 4:

            self.sensacion_tacto = (
                "Arena movediza"
            )

            return (
                "arena",
                arena_vecina
            )


        # ======================================
        # TERRENO NORMAL
        # ======================================

        self.sensacion_tacto = (
            "Suelo firme"
        )

        return (
            "normal",
            arena_vecina
        )


    # ==========================================
    # USAR GUSTO
    # ==========================================

    def usar_gusto(
        self,
        posicion
    ):

        tipo = (
            self.mundo.grid[
                posicion
            ]
        )


        # ======================================
        # BAYA BUENA
        # ======================================

        if tipo == 5:

            self.sensacion_gusto = (
                "Bayas dulces"
            )

            return "baya_buena"


        # ======================================
        # BAYA MALA
        # ======================================

        elif tipo == 6:

            self.sensacion_gusto = (
                "Bayas amargas"
            )

            return "baya_mala"


        # ======================================
        # SIN ALIMENTO
        # ======================================

        self.sensacion_gusto = (
            "Sin alimento"
        )

        return None


    # ==========================================
    # USAR OLFATO (PUMA)
    # ==========================================

    def usar_olfato(
        self,
        posicion_agente,
        posicion_puma
    ):

        distancia = (
            self.distancia(

                posicion_agente,

                posicion_puma

            )
        )


        # ======================================
        # FUERA DEL RANGO DEL OLFATO
        # O YA LO ESCUCHA / LO VE
        # ======================================

        if (

            distancia
            >
            self.rango_olfato

            or

            distancia
            <=
            self.rango_oido

        ):

            self.huele_puma = False

            self.intensidad_olor = None

            self.objetivo_olor = None

            return False


        # ======================================
        # HUELE AL PUMA
        # ======================================

        self.huele_puma = True


        # ======================================
        # INTENSIDAD DEL OLOR
        #
        # Entre más cerca, más fuerte.
        # ======================================

        if (
            distancia
            <=
            self.rango_oido + 1
        ):

            self.intensidad_olor = (
                "Olor fuerte"
            )

        else:

            self.intensidad_olor = (
                "Olor débil"
            )


        # ======================================
        # SEGUIR EL RASTRO
        # ======================================

        self.objetivo_olor = (
            self.crear_objetivo_olor(
                posicion_agente,
                posicion_puma
            )
        )


        return True


    # ==========================================
    # USAR OLFATO (BAYAS)
    #
    # Distingue el olor de cada color de baya,
    # pero solo sigue el olor de los colores
    # que ya aprendió que son buenos.
    # El olor pasa entre los árboles.
    # ==========================================

    def usar_olfato_bayas(
        self,
        posicion_agente,
        colores_buenos
    ):

        mas_cercana = None

        menor_distancia = None


        for posicion, tipo in (
            self.mundo.grid.items()
        ):

            if (
                OBSERVACIONES.get(tipo)
                not in colores_buenos
            ):

                continue


            distancia = (
                self.distancia(
                    posicion_agente,
                    posicion
                )
            )


            if (
                distancia
                >
                self.rango_olfato_bayas
            ):

                continue


            if (
                menor_distancia is None
                or
                distancia < menor_distancia
            ):

                mas_cercana = posicion

                menor_distancia = distancia


        # ======================================
        # NO HUELE BAYAS
        # ======================================

        if mas_cercana is None:

            self.huele_bayas = False

            self.color_olor_bayas = None

            self.objetivo_olor_bayas = None

            return False


        # ======================================
        # HUELE BAYAS BUENAS
        # ======================================

        self.huele_bayas = True

        self.color_olor_bayas = (
            self.observar(
                mas_cercana
            )
        )


        # Si ya está encima, no necesita moverse

        if mas_cercana == posicion_agente:

            self.objetivo_olor_bayas = None

            return True


        self.objetivo_olor_bayas = (
            self.crear_objetivo_olor(
                posicion_agente,
                mas_cercana
            )
        )


        return True


    # ==========================================
    # CREAR OBJETIVO DEL OLOR
    # ==========================================

    def crear_objetivo_olor(
        self,
        posicion_agente,
        posicion_origen_olor
    ):

        # ======================================
        # EL OLOR NO DA LA POSICIÓN EXACTA.
        #
        # El cazador solo sabe hacia qué
        # casilla vecina el olor es más fuerte.
        # ======================================

        distancia_actual = (
            self.distancia(
                posicion_agente,
                posicion_origen_olor
            )
        )


        for vecino in (
            self.mundo.vecinos_validos(
                posicion_agente
            )
        ):

            if (

                self.distancia(
                    vecino,
                    posicion_origen_olor
                )

                <

                distancia_actual

            ):

                return vecino


        return None
