import unittest

from Redes_Neuronales.ART.patron_entorno import (
    patron_entorno,
    analizar_entorno,
)


# ==========================================
# MUNDO PEQUEÑO PARA PRUEBAS
# ==========================================

class MundoFalso:

    def __init__(self):

        self.filas = 3
        self.columnas = 3

        # Centro:
        #
        #       libre
        #         ↑
        # árbol ← A → arena
        #         ↓
        #        baya
        #
        self.grid = {

            (0, 0): 0,
            (0, 1): 0,
            (0, 2): 0,

            (1, 0): 1,
            (1, 1): 0,
            (1, 2): 4,

            (2, 0): 0,
            (2, 1): 5,
            (2, 2): 0,
        }


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


class AgenteFalso:

    def __init__(
        self,
        mundo,
        posicion
    ):

        self.mundo = mundo
        self.posicion = posicion


# ==========================================
# PRUEBAS
# ==========================================

class PruebasPatronEntorno(
    unittest.TestCase
):

    def test_patron_cuatro_direcciones(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (1, 1)
        )


        patron = patron_entorno(
            agente
        )


        # arriba = libre -> 1
        # abajo = baya -> 1
        # izquierda = árbol -> 0
        # derecha = arena -> 0

        self.assertEqual(
            patron,
            [1, 1, 0, 0]
        )


    def test_borde_es_cero(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (0, 0)
        )


        patron = patron_entorno(
            agente
        )


        # arriba queda fuera del mapa
        # izquierda queda fuera del mapa

        self.assertEqual(
            patron[0],
            0
        )


        self.assertEqual(
            patron[2],
            0
        )


    def test_detalle_explica_el_patron(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (1, 1)
        )


        resultado = analizar_entorno(
            agente
        )


        self.assertEqual(
            resultado[
                "detalle"
            ][
                "izquierda"
            ][
                "tipo"
            ],
            "arbol"
        )


        self.assertEqual(
            resultado[
                "detalle"
            ][
                "derecha"
            ][
                "tipo"
            ],
            "arena"
        )


        self.assertEqual(
            resultado[
                "patron"
            ],
            [1, 1, 0, 0]
        )


if __name__ == "__main__":

    unittest.main()