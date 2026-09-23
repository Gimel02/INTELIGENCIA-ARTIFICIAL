import heapq


class AEstrella:

    @staticmethod
    def heuristica(a, b):

        return (
            abs(a[0] - b[0])
            +
            abs(a[1] - b[1])
        )


    @staticmethod
    def buscar(
        inicio,
        objetivo,
        mundo
    ):

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


        while frontera:

            _, actual = heapq.heappop(
                frontera
            )


            if actual == objetivo:

                break


            vecinos = (
                mundo.vecinos_validos(
                    actual
                )
            )


            for vecino in vecinos:

                tipo = mundo.grid[
                    vecino
                ]


                # =================================
                # COSTOS
                # =================================

                if tipo == 4:

                    costo_movimiento = 8

                else:

                    costo_movimiento = 2


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