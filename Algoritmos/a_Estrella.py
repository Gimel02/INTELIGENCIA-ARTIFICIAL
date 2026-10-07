import heapq


class AEstrella:

    # Costo extra por pasar por una casilla
    # que el cazador ya pisó

    COSTO_PISADA = 2


    @staticmethod
    def heuristica(a, b):

        return (
            abs(a[0] - b[0])
            +
            abs(a[1] - b[1])
        )


    # =========================================
    # COSTO DE ENTRAR A UNA CASILLA
    # =========================================

    @staticmethod
    def costo_paso(
        casilla,
        objetivo,
        mundo,
        evitar,
        pisadas
    ):

        # Bayas malas conocidas

        if (
            casilla in evitar
            and
            casilla != objetivo
        ):

            costo = 20

        # Arena movediza

        elif mundo.grid[casilla] == 4:

            costo = 8

        # Terreno normal

        else:

            costo = 2


        # Casilla que ya pisó

        if casilla in pisadas:

            costo += AEstrella.COSTO_PISADA


        return costo


    # =========================================
    # COSTO DE LLEGAR A TODAS LAS CASILLAS
    #
    # Dijkstra desde el inicio (A* sin meta).
    # Sirve para comparar muchos destinos
    # con una sola búsqueda.
    # =========================================

    @staticmethod
    def costos_desde(
        inicio,
        mundo,
        evitar=None,
        pisadas=None
    ):

        if evitar is None:

            evitar = set()

        if pisadas is None:

            pisadas = set()


        costos = {
            inicio: 0
        }

        frontera = [
            (0, inicio)
        ]

        cerrados = set()


        while frontera:

            costo, actual = heapq.heappop(
                frontera
            )


            if actual in cerrados:

                continue

            cerrados.add(
                actual
            )


            for vecino in (
                mundo.vecinos_validos(
                    actual
                )
            ):

                if vecino in cerrados:

                    continue


                nuevo = (
                    costo
                    +
                    AEstrella.costo_paso(
                        vecino,
                        None,
                        mundo,
                        evitar,
                        pisadas
                    )
                )


                if nuevo < costos.get(
                    vecino,
                    float("inf")
                ):

                    costos[vecino] = nuevo

                    heapq.heappush(
                        frontera,
                        (nuevo, vecino)
                    )


        return costos


    @staticmethod
    def buscar(
        inicio,
        objetivo,
        mundo,
        evitar=None,
        pisadas=None
    ):

        # pisadas: casillas por las que el
        # cazador ya caminó. Cuestan un poco
        # más para preferir caminos nuevos y
        # no repetir nodos.

        if pisadas is None:

            pisadas = set()


        # Casillas que el cazador prefiere no
        # pisar, como las bayas malas que recuerda.

        if evitar is None:

            evitar = set()


        if not mundo.es_transitable(
            objetivo
        ):

            return []


        frontera = []

        heapq.heappush(
            frontera,
            (0, inicio)
        )


        costo_acumulado = {

            inicio: 0

        }


        padres = {

            inicio: None

        }


        # =========================================
        # NODOS CERRADOS
        #
        # Un nodo que ya se expandió no se
        # vuelve a expandir.
        # =========================================

        cerrados = set()


        while frontera:

            _, actual = heapq.heappop(
                frontera
            )


            # Entrada vieja de un nodo que ya
            # se expandió con un costo menor

            if actual in cerrados:

                continue


            cerrados.add(
                actual
            )


            if actual == objetivo:

                break


            vecinos = (
                mundo.vecinos_validos(
                    actual
                )
            )


            for vecino in vecinos:

                if vecino in cerrados:

                    continue


                costo_movimiento = (
                    AEstrella.costo_paso(
                        vecino,
                        objetivo,
                        mundo,
                        evitar,
                        pisadas
                    )
                )


                nuevo_costo = (

                    costo_acumulado[
                        actual
                    ]

                    +

                    costo_movimiento

                )


                if (

                    vecino not in
                    costo_acumulado

                    or

                    nuevo_costo
                    <
                    costo_acumulado[
                        vecino
                    ]

                ):

                    costo_acumulado[
                        vecino
                    ] = nuevo_costo


                    prioridad = (

                        nuevo_costo

                        +

                        AEstrella.heuristica(
                            vecino,
                            objetivo
                        )

                    )


                    heapq.heappush(

                        frontera,

                        (
                            prioridad,
                            vecino
                        )

                    )


                    padres[
                        vecino
                    ] = actual


        # =========================================
        # NO HAY CAMINO
        # =========================================

        if objetivo not in padres:

            return []


        # =========================================
        # RECONSTRUIR CAMINO
        # =========================================

        camino = []

        actual = objetivo


        while actual != inicio:

            camino.append(
                actual
            )

            actual = padres[
                actual
            ]


        camino.reverse()

        return camino