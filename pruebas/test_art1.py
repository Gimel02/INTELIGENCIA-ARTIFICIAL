import unittest

from Redes_Neuronales.ART.art1 import ART1


class PruebasART1(unittest.TestCase):

    # ======================================
    # EJEMPLO DE CLASE
    # ======================================

    def test_resonancia_con_vigilancia_05(self):

        art = ART1(
            numero_entradas=4,
            vigilancia=0.5,
            max_categorias=2
        )


        # Prototipo C1

        art.aprender(
            [1, 1, 0, 0]
        )


        # Prototipo C2

        art.aprender(
            [0, 0, 1, 1]
        )


        # Patrón E3

        resultado = art.aprender(
            [1, 1, 1, 0]
        )


        # ----------------------------------
        # Rs = 2 / 3 = 0.666...
        #
        # 0.666 > rho 0.5
        #
        # Debe reconocer C1.
        # ----------------------------------

        self.assertEqual(
            resultado["estado"],
            "RESONANCIA"
        )


        self.assertEqual(
            resultado["categoria"],
            1
        )


        self.assertAlmostEqual(
            resultado["similitud"],
            2 / 3
        )


        self.assertEqual(
            resultado["prototipo"],
            [1, 1, 0, 0]
        )


    # ======================================
    # VIGILANCIA ALTA
    # ======================================

    def test_vigilancia_08_rechaza_patron(self):

        art = ART1(
            numero_entradas=4,
            vigilancia=0.8,
            max_categorias=3
        )


        art.aprender(
            [1, 1, 0, 0]
        )


        art.aprender(
            [0, 0, 1, 1]
        )


        resultado = art.aprender(
            [1, 1, 1, 0]
        )


        # Rs = 0.666...
        #
        # 0.666 < rho 0.8
        #
        # Se crea C3.

        self.assertEqual(
            resultado["estado"],
            "NUEVA_CATEGORIA"
        )


        self.assertEqual(
            resultado["categoria"],
            3
        )


        self.assertEqual(
            art.prototipos[2],
            [1, 1, 1, 0]
        )


    # ======================================
    # SATURACIÓN
    # ======================================

    def test_saturacion_con_dos_salidas(self):

        art = ART1(
            numero_entradas=4,
            vigilancia=0.8,
            max_categorias=2
        )


        art.aprender(
            [1, 1, 0, 0]
        )


        art.aprender(
            [0, 0, 1, 1]
        )


        resultado = art.aprender(
            [1, 1, 1, 0]
        )


        # Necesitaría C3, pero solo
        # existen dos salidas disponibles.

        self.assertEqual(
            resultado["estado"],
            "SATURADA"
        )


        self.assertTrue(
            resultado["saturada"]
        )


        self.assertEqual(
            len(art.prototipos),
            2
        )

    def test_reset_prueba_otra_categoria(self):

        art = ART1(
            numero_entradas=4,
            vigilancia=0.6,
            max_categorias=4
        )


        # Ponemos directamente dos categorías
        # para comprobar el mecanismo RESET.

        art.prototipos = [

            # C1
            [1, 0, 0, 0],

            # C2
            [1, 1, 0, 1],

        ]


        entrada = [
            1,
            1,
            1,
            0
        ]


        resultado = art.aprender(
            entrada
        )


        # C1 compite primero pero no cumple
        # suficientemente la vigilancia.
        #
        # ART hace RESET y prueba C2.

        self.assertIn(
            1,
            resultado[
                "categorias_reseteadas"
            ]
        )


        # C2 sí alcanza:
        #
        # coincidencias = 2
        # activos entrada = 3
        #
        # Rs = 2/3 = 0.666...
        #
        # 0.666 >= rho 0.6

        self.assertEqual(
            resultado["estado"],
            "RESONANCIA"
        )


        self.assertEqual(
            resultado["categoria"],
            2
        )


        self.assertAlmostEqual(
            resultado["similitud"],
            2 / 3
        )

    def test_pesos_w_del_ejemplo_de_clase(
        self
    ):

        art = ART1(
            numero_entradas=4,
            vigilancia=0.5,
            gamma=0.5
        )


        prototipo = [
            1,
            1,
            0,
            0
        ]


        pesos = art.pesos_feedforward(
            prototipo
        )


        self.assertEqual(
            pesos,
            [
                0.4,
                0.4,
                0.0,
                0.0
            ]
        )

    def test_competencia_del_ejemplo_de_clase(
        self
    ):

        art = ART1(
            numero_entradas=4,
            vigilancia=0.5,
            gamma=0.5
        )


        # Categoría 1
        art.prototipos.append(
            [1, 1, 0, 0]
        )


        # Categoría 2
        art.prototipos.append(
            [0, 0, 1, 1]
        )


        entrada = [
            1,
            1,
            1,
            0
        ]


        categorias = (
            art.categorias_por_competencia(
                entrada
            )
        )


        # Según el ejemplo:
        #
        # C1 = 0.8
        # C2 = 0.4

        self.assertEqual(
            categorias[0]["indice"],
            0
        )


        self.assertAlmostEqual(
            categorias[0]["activacion"],
            0.8
        )


        self.assertAlmostEqual(
            categorias[1]["activacion"],
            0.4
        )
if __name__ == "__main__":

    unittest.main()