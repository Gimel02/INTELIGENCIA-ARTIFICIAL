from Algoritmos.a_Estrella import AEstrella


class Persecucion:

    # ==========================================
    # PUNTO DE INTERCEPCIÓN
    #
    # Si el jaguar se está moviendo, ir a donde
    # está ahora no sirve: cuando el cazador
    # llegue, ya se habrá ido.
    #
    # Con las dos últimas posiciones donde lo
    # vio, calcula hacia dónde se mueve y
    # apunta un poco más adelante.
    #
    # Entre más lejos esté, más adelante
    # apunta (hasta 2 casillas).
    # ==========================================

    @staticmethod
    def punto_intercepcion(
        posicion_cazador,
        posicion_presa,
        posicion_presa_anterior,
        mundo,
        adelanto=None
    ):

        # Sin dirección conocida: ir directo

        if (
            posicion_presa_anterior is None
            or
            posicion_presa_anterior == posicion_presa
        ):

            return posicion_presa


        # ======================================
        # DIRECCIÓN DE LA PRESA
        # ======================================

        df = (
            posicion_presa[0]
            -
            posicion_presa_anterior[0]
        )

        dc = (
            posicion_presa[1]
            -
            posicion_presa_anterior[1]
        )

        df = (df > 0) - (df < 0)

        dc = (dc > 0) - (dc < 0)


        # ======================================
        # CUÁNTO ADELANTARSE
        # ======================================

        if adelanto is None:

            distancia = (
                AEstrella.heuristica(
                    posicion_cazador,
                    posicion_presa
                )
            )

            adelanto = min(
                2,
                distancia // 2
            )


        # ======================================
        # BUSCAR UNA CASILLA VÁLIDA,
        # DE LA MÁS ADELANTADA A LA PRESA
        # ======================================

        for pasos in range(
            adelanto,
            0,
            -1
        ):

            punto = (

                posicion_presa[0]
                +
                df * pasos,

                posicion_presa[1]
                +
                dc * pasos

            )


            if mundo.es_transitable(
                punto
            ):

                return punto


        return posicion_presa
