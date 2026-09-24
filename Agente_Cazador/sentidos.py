class Sentidos:

    def __init__(self, mundo):

        self.mundo = mundo


        # ==========================================
        # VISTA
        # ==========================================

        self.rango_vista = 1

        self.ve_puma = False


        # ==========================================
        # OÍDO
        # ==========================================

        self.rango_oido = 2

        self.escucha_puma = False

        self.direccion_sonido = None

        self.objetivo_sonido = None


        # ==========================================
        # TACTO
        # ==========================================

        self.sensacion_tacto = (
            "Suelo firme"
        )


        # ==========================================
        # GUSTO
        # ==========================================

        self.sensacion_gusto = (
            "Sin alimento"
        )


        # ==========================================
        # OLFATO
        # ==========================================

        self.rango_olfato = 4

        self.huele_puma = False

        self.intensidad_olor = None

        self.objetivo_olor = None


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


                distancia = (
                    self.distancia(

                        posicion_agente,

                        posicion

                    )
                )


                # ======================================
                # DENTRO DEL RANGO DE VISTA
                # ======================================

                if (
                    distancia
                    <=
                    self.rango_vista
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
                # 1. Fuera del rango de vista
                # 2. Dentro del rango de oído
                # ======================================

                if (

                    distancia
                    >
                    self.rango_vista

                    and

                    distancia
                    <=
                    self.rango_oido

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


        return {

            "detectado":
                self.ve_puma,

            "celdas_visibles":
                visibles

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
        # ======================================

        if (
            distancia
            >
            self.rango_oido
        ):

            self.escucha_puma = False

            self.direccion_sonido = None

            self.objetivo_sonido = None

            return False


        # ======================================
        # SI LO VE, NO NECESITA USAR EL OÍDO
        # ======================================

        if (
            distancia
            <=
            self.rango_vista
        ):

            self.escucha_puma = False

            self.direccion_sonido = None

            self.objetivo_sonido = None

            return False


        # ======================================
        # ESCUCHA AL PUMA
        # ======================================

        self.escucha_puma = True


        cazador_f, cazador_c = (
            posicion_agente
        )

        puma_f, puma_c = (
            posicion_puma
        )


        diferencia_filas = (
            puma_f
            -
            cazador_f
        )

        diferencia_columnas = (
            puma_c
            -
            cazador_c
        )


        # ======================================
        # DETERMINAR DIRECCIÓN DEL SONIDO
        # ======================================

        if (
            abs(
                diferencia_filas
            )
            >=
            abs(
                diferencia_columnas
            )
        ):

            # Puma arriba

            if diferencia_filas < 0:

                self.direccion_sonido = (
                    "NORTE"
                )


            # Puma abajo

            else:

                self.direccion_sonido = (
                    "SUR"
                )


        else:

            # Puma a la izquierda

            if diferencia_columnas < 0:

                self.direccion_sonido = (
                    "OESTE"
                )


            # Puma a la derecha

            else:

                self.direccion_sonido = (
                    "ESTE"
                )


        # ======================================
        # CREAR OBJETIVO APROXIMADO
        # ======================================

        self.objetivo_sonido = (
            self.crear_objetivo_sonido(
                posicion_agente
            )
        )


        return True


    # ==========================================
    # CREAR OBJETIVO DEL SONIDO
    # ==========================================

    def crear_objetivo_sonido(
        self,
        posicion_agente
    ):

        fila, columna = (
            posicion_agente
        )


        direcciones = {

            "NORTE":
                (-1, 0),

            "SUR":
                (1, 0),

            "ESTE":
                (0, 1),

            "OESTE":
                (0, -1)

        }


        # ======================================
        # DIRECCIÓN NO VÁLIDA
        # ======================================

        if (
            self.direccion_sonido
            not in direcciones
        ):

            return None


        df, dc = (
            direcciones[
                self.direccion_sonido
            ]
        )


        # ======================================
        # BUSCAR HASTA 3 CASILLAS
        #
        # Primero intenta 3,
        # después 2,
        # después 1.
        # ======================================

        for distancia in range(
            3,
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

            return "arena"


        # ======================================
        # TERRENO NORMAL
        # ======================================

        self.sensacion_tacto = (
            "Suelo firme"
        )

        return "normal"


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
    # USAR OLFATO
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
        # ======================================

        if (
            distancia
            >
            self.rango_olfato
        ):

            self.huele_puma = False

            self.intensidad_olor = None

            self.objetivo_olor = None

            return False


        # ======================================
        # SI LO VE O LO ESCUCHA,
        # NO NECESITA USAR EL OLFATO
        # ======================================

        if (
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
    # CREAR OBJETIVO DEL OLOR
    # ==========================================

    def crear_objetivo_olor(
        self,
        posicion_agente,
        posicion_puma
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
                posicion_puma
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
                    posicion_puma
                )

                <

                distancia_actual

            ):

                return vecino


        return None
