import unittest

from Redes_Neuronales.ART.memoria_art import (
    MemoriaART,
)


# ==========================================
# MUNDO FALSO
# ==========================================

class MundoFalso:

    def __init__(
        self
    ):

        self.filas = 5
        self.columnas = 5

        self.grid = {

            (fila, columna): 0

            for fila in range(
                self.filas
            )

            for columna in range(
                self.columnas
            )
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

class PruebasMemoriaART(
    unittest.TestCase
):

    def test_aprende_primer_patron(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (2, 2)
        )


        memoria = MemoriaART(
            "Rodrigo"
        )


        resultado = memoria.observar(
            agente
        )


        # Todo alrededor es libre.

        self.assertEqual(
            memoria.ultimo_patron,
            [1, 1, 1, 1]
        )


        self.assertEqual(
            resultado["estado"],
            "NUEVA_CATEGORIA"
        )


        self.assertEqual(
            memoria.numero_categorias,
            1
        )


    # ======================================
    # MEMORIAS INDEPENDIENTES
    # ======================================

    def test_dos_agentes_no_comparten_memoria(
        self
    ):

        mundo = MundoFalso()


        rodrigo = AgenteFalso(
            mundo,
            (2, 2)
        )


        gonzalo = AgenteFalso(
            mundo,
            (2, 2)
        )


        memoria_rodrigo = MemoriaART(
            "Rodrigo"
        )


        memoria_gonzalo = MemoriaART(
            "Gonzalo"
        )


        memoria_rodrigo.observar(
            rodrigo
        )


        # Rodrigo ya aprendió.
        self.assertEqual(
            memoria_rodrigo.numero_categorias,
            1
        )


        # Gonzalo todavía no ha visto nada.
        self.assertEqual(
            memoria_gonzalo.numero_categorias,
            0
        )


    # ======================================
    # RECONOCIMIENTO
    # ======================================

    def test_reconoce_patron_conocido(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (2, 2)
        )


        memoria = MemoriaART(
            "Jaguar"
        )


        primero = memoria.observar(
            agente
        )


        segundo = memoria.observar(
            agente
        )


        self.assertEqual(
            primero["estado"],
            "NUEVA_CATEGORIA"
        )


        self.assertEqual(
            segundo["estado"],
            "RESONANCIA"
        )


        self.assertEqual(
            memoria.numero_categorias,
            1
        )


        self.assertAlmostEqual(
            segundo["similitud"],
            1.0
        )


    # ======================================
    # STM SE BORRA, LTM PERMANECE
    # ======================================

    def test_reinicio_conserva_largo_plazo(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (2, 2)
        )


        memoria = MemoriaART(
            "Rodrigo"
        )


        memoria.observar(
            agente
        )


        self.assertIsNotNone(
            memoria.ultimo_patron
        )


        self.assertEqual(
            memoria.numero_categorias,
            1
        )


        memoria.reiniciar_partida()


        # STM vacía.

        self.assertIsNone(
            memoria.ultimo_patron
        )


        # LTM sigue aprendida.

        self.assertEqual(
            memoria.numero_categorias,
            1
        )


    # ======================================
    # RESUMEN PARA EL FUTURO PANEL
    # ======================================

    def test_resumen(
        self
    ):

        mundo = MundoFalso()

        agente = AgenteFalso(
            mundo,
            (2, 2)
        )


        memoria = MemoriaART(
            "Gonzalo",
            vigilancia=0.7
        )


        memoria.observar(
            agente
        )


        resumen = memoria.resumen()


        self.assertEqual(
            resumen["agente"],
            "Gonzalo"
        )


        self.assertEqual(
            resumen["patron"],
            [1, 1, 1, 1]
        )


        self.assertEqual(
            resumen["categoria"],
            1
        )


        self.assertAlmostEqual(
            resumen["vigilancia"],
            0.7
        )

    def test_dios_asigna_memoria_a_los_tres(
        self
    ):

        from Logica_Difusa.dios import Dios


        dios = Dios()

        dios.nueva_partida()


        self.assertIsNotNone(
            dios.cazador.memoria_art
        )


        self.assertIsNotNone(
            dios.jaguar.memoria_art
        )


        self.assertIsNotNone(
            dios.interceptor.memoria_art
        )


        self.assertEqual(
            dios.cazador.memoria_art.nombre,
            "Rodrigo"
        )


        self.assertEqual(
            dios.interceptor.memoria_art.nombre,
            "Gonzalo"
        )


        self.assertEqual(
            dios.jaguar.memoria_art.nombre,
            "Jaguar"
        )


    def test_art_de_agentes_es_independiente(
        self
    ):

        from Logica_Difusa.dios import Dios


        dios = Dios()

        dios.nueva_partida()


        rodrigo = (
            dios.cazador.memoria_art
        )

        gonzalo = (
            dios.interceptor.memoria_art
        )

        jaguar = (
            dios.jaguar.memoria_art
        )


        self.assertIsNot(
            rodrigo,
            gonzalo
        )


        self.assertIsNot(
            rodrigo,
            jaguar
        )


        self.assertIsNot(
            gonzalo,
            jaguar
        )


    def test_art_conserva_ltm_entre_partidas(
        self
    ):

        from Logica_Difusa.dios import Dios


        dios = Dios()

        dios.nueva_partida()


        memoria = (
            dios.cazador.memoria_art
        )


        # Rodrigo observa su mapa actual.

        memoria.observar(
            dios.cazador
        )


        categorias_antes = (
            memoria.numero_categorias
        )


        self.assertGreater(
            categorias_antes,
            0
        )


        # Nueva partida.

        dios.nueva_partida()


        nueva_memoria = (
            dios.cazador.memoria_art
        )


        # Es exactamente la misma memoria ART.

        self.assertIs(
            memoria,
            nueva_memoria
        )


        # La memoria de largo plazo permanece.

        self.assertEqual(
            nueva_memoria.numero_categorias,
            categorias_antes
        )


        # Pero la STM fue reiniciada.

        self.assertIsNone(
            nueva_memoria.ultimo_patron
        )

if __name__ == "__main__":

    unittest.main()