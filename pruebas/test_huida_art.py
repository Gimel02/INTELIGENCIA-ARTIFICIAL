import random
import unittest

from Algoritmos.huida import Huida


# ==========================================
# MUNDO FALSO PARA PROBAR LA HUIDA
# 0 = libre, 1 = árbol, 4 = arena
# ==========================================

class MundoFalso:

    def __init__(self, filas=5, columnas=5, arboles=()):

        self.filas = filas
        self.columnas = columnas

        self.grid = {
            (f, c): 0
            for f in range(filas)
            for c in range(columnas)
        }

        for posicion in arboles:
            self.grid[posicion] = 1


    def dentro_limites(self, posicion):

        return posicion in self.grid


    def vecinos_validos(self, posicion):

        fila, columna = posicion

        vecinos = []

        for df, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):

            vecino = (fila + df, columna + dc)

            if vecino in self.grid and self.grid[vecino] != 1:

                vecinos.append(vecino)

        return vecinos


class PruebasHuidaConART(unittest.TestCase):

    # Presa en (2, 2) y jaguar en (2, 0):
    # (1, 2), (3, 2) y (2, 3) quedan igual de
    # lejos (3 casillas) y con 4 salidas cada
    # una: son rutas igual de buenas.

    def test_sin_informacion_es_igual_que_antes(self):

        mundo = MundoFalso()

        antes = Huida.elegir_escape((2, 2), (2, 0), mundo)

        con_art = Huida.elegir_escape(
            (2, 2), (2, 0), mundo,
            preferencia=lambda casilla: None
        )

        self.assertEqual(con_art, antes)


    def test_art_elige_entre_dos_rutas_validas(self):

        mundo = MundoFalso()

        experiencia = {(1, 2): -0.8, (3, 2): 0.6, (2, 3): -0.8}

        escape = Huida.elegir_escape(
            (2, 2), (2, 0), mundo,
            preferencia=experiencia.get
        )

        self.assertEqual(escape, (3, 2))

        # Si cambia la experiencia, cambia la ruta
        experiencia = {(1, 2): 0.6, (3, 2): -0.8, (2, 3): -0.8}

        escape = Huida.elegir_escape(
            (2, 2), (2, 0), mundo,
            preferencia=experiencia.get
        )

        self.assertEqual(escape, (1, 2))


    def test_art_nunca_lo_acerca_al_jaguar(self):

        mundo = MundoFalso()

        # (2, 1) está pegada al jaguar; aunque
        # ART la prefiera al máximo, no se elige
        experiencia = {(2, 1): 1.0, (1, 2): -1.0, (3, 2): -1.0, (2, 3): -1.0}

        escape = Huida.elegir_escape(
            (2, 2), (2, 0), mundo,
            preferencia=experiencia.get
        )

        self.assertNotEqual(escape, (2, 1))
        self.assertIsNotNone(escape)


    def test_todas_malas_igual_hay_salida(self):

        mundo = MundoFalso()

        escape = Huida.elegir_escape(
            (2, 2), (2, 0), mundo,
            preferencia=lambda casilla: -1.0
        )

        self.assertIsNotNone(escape)


    def test_no_quita_la_unica_salida(self):

        # Solo puede huir a la derecha
        mundo = MundoFalso(arboles=((1, 2), (3, 2)))

        escape = Huida.elegir_escape(
            (2, 2), (2, 0), mundo,
            preferencia=lambda casilla: -1.0
        )

        self.assertEqual(escape, (2, 3))


    def test_sin_informacion_igual_en_muchos_mapas(self):

        generador = random.Random(3)

        for _ in range(300):

            arboles = {
                (generador.randrange(7), generador.randrange(7))
                for _ in range(12)
            }

            mundo = MundoFalso(7, 7, arboles)

            libres = [p for p, t in mundo.grid.items() if t == 0]

            presa, jaguar = generador.sample(libres, 2)

            self.assertEqual(
                Huida.elegir_escape(
                    presa, jaguar, mundo,
                    preferencia=lambda casilla: None
                ),
                Huida.elegir_escape(presa, jaguar, mundo)
            )


    def test_art_no_empeora_la_distancia(self):

        generador = random.Random(5)

        for _ in range(300):

            arboles = {
                (generador.randrange(7), generador.randrange(7))
                for _ in range(12)
            }

            mundo = MundoFalso(7, 7, arboles)

            libres = [p for p, t in mundo.grid.items() if t == 0]

            presa, jaguar = generador.sample(libres, 2)

            experiencia = {
                p: generador.uniform(-1, 1) for p in libres
            }

            sin_art = Huida.elegir_escape(presa, jaguar, mundo)

            con_art = Huida.elegir_escape(
                presa, jaguar, mundo,
                preferencia=experiencia.get
            )

            # Si había escape sin ART, con ART
            # también, y nunca más cerca
            if sin_art is None:

                self.assertIsNone(con_art)

            else:

                distancia = lambda p: abs(p[0] - jaguar[0]) + abs(p[1] - jaguar[1])

                self.assertIsNotNone(con_art)
                self.assertGreaterEqual(distancia(con_art), distancia(sin_art))


if __name__ == "__main__":
    unittest.main()


# ==========================================
# REFUERZOS DE LA HUIDA (PARTE B)
#
# Se usa un cazador "vacío" con solo lo que
# necesitan estos métodos, para no armar una
# partida completa.
# ==========================================

from Agente_Cazador.agente import AgenteCazador
from Redes_Neuronales.ART.memoria_art import MemoriaART


class MundoConJaguar(MundoFalso):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.jaguar_vivo = True
        self.posicion_jaguar = None


class AgenteFalso:

    def __init__(self, mundo, posicion):

        self.mundo = mundo
        self.posicion = posicion


def cazador_de_prueba(mundo, posicion):

    cazador = AgenteCazador.__new__(AgenteCazador)

    cazador.nombre = "Rodrigo"
    cazador.mundo = mundo
    cazador.posicion = posicion
    cazador.memoria_art = MemoriaART("Rodrigo")

    # Como DIOS: ART observa el lugar actual
    cazador.memoria_art.observar(AgenteFalso(mundo, posicion))

    return cazador


class PruebasRefuerzosHuidaART(unittest.TestCase):

    def test_logro_alejarse_premia(self):

        mundo = MundoConJaguar()

        cazador = cazador_de_prueba(mundo, (2, 3))

        cazador.huida_pendiente_art = {
            "casilla": (2, 3),
            "distancia_antes": 2,
        }

        mundo.posicion_jaguar = (2, 0)   # ahora está a 3

        cazador.evaluar_huida_art()

        self.assertAlmostEqual(cazador.memoria_art.experiencia_de(1), 0.1)


    def test_piso_arena_castiga(self):

        mundo = MundoConJaguar()

        mundo.grid[(2, 3)] = 4

        cazador = cazador_de_prueba(mundo, (2, 3))

        cazador.huida_pendiente_art = {
            "casilla": (2, 3),
            "distancia_antes": 2,
        }

        mundo.posicion_jaguar = (2, 0)

        cazador.evaluar_huida_art()

        self.assertAlmostEqual(cazador.memoria_art.experiencia_de(1), -0.2)


    def test_sin_huida_pendiente_no_cambia(self):

        mundo = MundoConJaguar()

        cazador = cazador_de_prueba(mundo, (2, 3))

        cazador.huida_pendiente_art = None

        cazador.evaluar_huida_art()

        self.assertEqual(cazador.memoria_art.experiencia, {})


    def test_no_se_alejo_no_premia(self):

        mundo = MundoConJaguar()

        cazador = cazador_de_prueba(mundo, (2, 3))

        cazador.huida_pendiente_art = {
            "casilla": (2, 3),
            "distancia_antes": 3,
        }

        mundo.posicion_jaguar = (2, 1)   # ahora está a 2

        cazador.evaluar_huida_art()

        self.assertEqual(cazador.memoria_art.experiencia, {})


    def test_acorralado_castiga(self):

        # Rodeado de árboles salvo por donde
        # viene el jaguar
        mundo = MundoConJaguar(arboles=((1, 2), (3, 2), (2, 3)))

        mundo.posicion_jaguar = (2, 0)

        cazador = cazador_de_prueba(mundo, (2, 2))

        escape = cazador.elegir_escape_con_art((2, 0))

        self.assertIsNone(escape)
        self.assertAlmostEqual(cazador.memoria_art.experiencia_de(1), -0.2)


    def test_huida_normal_deja_pendiente(self):

        mundo = MundoConJaguar()

        mundo.posicion_jaguar = (2, 0)

        cazador = cazador_de_prueba(mundo, (2, 2))

        escape = cazador.elegir_escape_con_art((2, 0))

        self.assertIsNotNone(escape)
        self.assertEqual(cazador.huida_pendiente_art["casilla"], escape)
        self.assertEqual(cazador.huida_pendiente_art["distancia_antes"], 2)
