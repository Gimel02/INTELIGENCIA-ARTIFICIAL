from Algoritmos.a_Estrella import AEstrella


# Peso de la experiencia ART al huir.
# Alejarse una casilla vale 10 puntos; ART
# suma como máximo ±5, así que solo
# desempata entre rutas igual de buenas.
PESO_ART = 5


class Huida:

    # ==========================================
    # ELEGIR CASILLA DE ESCAPE
    #
    # El que huye (jaguar o cazador) revisa sus
    # casillas vecinas y elige la mejor para
    # alejarse del perseguidor.
    #
    # Puntaje de cada casilla:
    # + distancia al perseguidor (lo más importante)
    # + salidas que tiene (para no meterse
    #   en un callejón sin salida)
    # - si es arena movediza (lo hace lento)
    #
    # CAMBIO: nuevo parámetro opcional "prohibidas"
    # (por ejemplo, bayas malas). Esas casillas
    # nunca se eligen como escape. Si no se pasa,
    # todo funciona exactamente igual que antes.
    # ==========================================

    @staticmethod
    def elegir_escape(
        posicion_presa,
        posicion_cazador,
        mundo,
        prohibidas=(),
        preferencia=None
    ):

        # preferencia (opcional): función que
        # recibe una casilla vecina y regresa su
        # experiencia ART (-1 a 1) o None si no
        # hay información. Sin ella, todo
        # funciona exactamente igual que antes.

        candidatas = []

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
            # del perseguidor

            if vecino == posicion_cazador:

                continue


            # CAMBIO: nunca elige una casilla prohibida

            if vecino in prohibidas:

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


            candidatas.append(
                (vecino, distancia, puntaje)
            )

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


        # ======================================
        # PREFERENCIA ART
        #
        # Solo puede elegir entre casillas que
        # quedan IGUAL DE LEJOS O MÁS del
        # perseguidor que la que se elegía sin
        # ART. Así nunca se acerca por culpa de
        # ART ni se queda sin salida. Nunca quita
        # opciones: solo cambia puntajes.
        # ======================================

        if preferencia is not None:

            distancia_base = AEstrella.heuristica(
                mejor,
                posicion_cazador
            )

            mejor_art = None
            puntaje_art = None

            for vecino, distancia, puntaje in candidatas:

                if distancia < distancia_base:

                    continue

                experiencia = preferencia(vecino)

                if experiencia is not None:

                    puntaje += PESO_ART * experiencia

                if puntaje_art is None or puntaje > puntaje_art:

                    mejor_art = vecino
                    puntaje_art = puntaje

            mejor = mejor_art


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
