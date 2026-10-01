from Algoritmos.a_Estrella import AEstrella


class Huida:

    # ==========================================
    # ELEGIR CASILLA DE ESCAPE
    #
    # El que huye (puma) revisa sus casillas
    # vecinas y elige la mejor para alejarse
    # del cazador.
    #
    # Puntaje de cada casilla:
    # + distancia al cazador (lo más importante)
    # + salidas que tiene (para no meterse
    #   en un callejón sin salida)
    # - si es arena movediza (lo hace lento)
    # ==========================================

    @staticmethod
    def elegir_escape(
        posicion_presa,
        posicion_cazador,
        mundo
    ):

        distancia_actual = (
            AEstrella.heuristica(
                posicion_presa,
                posicion_cazador
            )
        )


        mejor = None

        mejor_puntaje = None


        for vecino in (
            mundo.vecinos_validos(
                posicion_presa
            )
        ):

            # Nunca se mete en la casilla
            # del cazador

            if vecino == posicion_cazador:

                continue


            distancia = (
                AEstrella.heuristica(
                    vecino,
                    posicion_cazador
                )
            )


            salidas = len(
                mundo.vecinos_validos(
                    vecino
                )
            )


            puntaje = (
                distancia * 10
                +
                salidas
            )


            if mundo.grid[vecino] == 4:

                puntaje -= 6


            if (
                mejor_puntaje is None
                or
                puntaje > mejor_puntaje
            ):

                mejor = vecino

                mejor_puntaje = puntaje


        # ======================================
        # SI NINGUNA CASILLA LO ALEJA,
        # SE QUEDA DONDE ESTÁ
        # ======================================

        if mejor is None:

            return None


        if (
            AEstrella.heuristica(
                mejor,
                posicion_cazador
            )
            <
            distancia_actual
        ):

            return None


        return mejor
