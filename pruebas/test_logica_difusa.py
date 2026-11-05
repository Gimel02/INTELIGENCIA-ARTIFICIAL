# ==========================================
# PRUEBAS AUTOMÁTICAS DE LA LÓGICA DIFUSA
#
# Comprueban que cada parte del sistema
# difuso hace lo que dice el reporte:
#
#   1. Funciones de membresía (con los
#      ejemplos de clase)
#   2. Operadores AND, OR, NOT
#   3. Base de conocimiento (23 y 11 reglas)
#   4. Motor Mamdani y centroide
#   5. Decisiones del cazador en casos
#      controlados
#   6. Decisiones del jaguar en casos
#      controlados
#   7. Bitácora del jaguar y escenarios
#   8. Interceptor (Agente 3, cazador rival) y DIOS
#
# Cómo correrlas (desde la carpeta del
# proyecto):
#
#   python3 -m unittest discover pruebas -v
# ==========================================

import contextlib
import io
import os
import tempfile
import unittest

from Logica_Difusa.funciones_membresia import (
    grado,
    grado_inversa,
    triangular,
    trapezoidal,
)
from Logica_Difusa.operadores import AND, OR, NOT, AGG, implicacion
from Logica_Difusa.variables import DISTANCIA, RESERVA, PELIGRO
from Logica_Difusa.base_conocimiento import (
    BaseConocimiento,
    base_equipo,
)
from Logica_Difusa.motor_mamdani import ControladorDifuso, centroide


# ==========================================
# 1. FUNCIONES DE MEMBRESÍA
# ==========================================

class PruebasMembresia(unittest.TestCase):

    def test_grado_ejemplo_adulto_de_clase(self):

        # Ejemplo de la presentación: adulto con
        # X0 = 18 y X1 = 21

        self.assertEqual(grado(12, 18, 21), 0.0)
        self.assertAlmostEqual(grado(19, 18, 21), 1 / 3)
        self.assertEqual(grado(35, 18, 21), 1.0)

    def test_grado_inversa(self):

        self.assertEqual(grado_inversa(5, 8, 18), 1.0)
        self.assertAlmostEqual(grado_inversa(13, 8, 18), 0.5)
        self.assertEqual(grado_inversa(20, 8, 18), 0.0)

    def test_triangular(self):

        self.assertEqual(triangular(1, 1, 3, 6), 0.0)
        self.assertEqual(triangular(3, 1, 3, 6), 1.0)
        self.assertAlmostEqual(triangular(4, 1, 3, 6), 2 / 3)

    def test_trapezoidal(self):

        self.assertEqual(trapezoidal(20, 8, 18, 25, 35), 1.0)
        self.assertAlmostEqual(trapezoidal(30, 8, 18, 25, 35), 0.5)
        self.assertEqual(trapezoidal(40, 8, 18, 25, 35), 0.0)

    def test_grados_siempre_entre_0_y_1(self):

        for variable in (RESERVA, DISTANCIA, PELIGRO):

            for x in range(-10, 120):

                for mu in variable.fuzzificar(x).values():

                    self.assertGreaterEqual(mu, 0.0)
                    self.assertLessEqual(mu, 1.0)

    def test_distancia_4_es_cerca_y_media(self):

        grados = DISTANCIA.fuzzificar(4)

        self.assertAlmostEqual(grados["cerca"], 2 / 3)
        self.assertAlmostEqual(grados["media"], 1 / 3)
        self.assertEqual(grados["muy_cerca"], 0.0)
        self.assertEqual(grados["lejos"], 0.0)


# ==========================================
# 2. OPERADORES
# ==========================================

class PruebasOperadores(unittest.TestCase):

    def test_and_es_el_minimo(self):

        # Ejemplo de clase: Edad 0.8 AND Curso 0.6
        self.assertEqual(AND(0.8, 0.6), 0.6)

    def test_or_es_el_maximo(self):

        self.assertEqual(OR(0.8, 0.6), 0.8)

    def test_not_es_uno_menos(self):

        self.assertAlmostEqual(NOT(0.75), 0.25)

    def test_implicacion_recorta(self):

        self.assertEqual(implicacion(0.4, 0.9), 0.4)

    def test_agregacion_sin_valores_es_cero(self):

        self.assertEqual(AGG(), 0.0)


# ==========================================
# 3. BASE DE CONOCIMIENTO
# ==========================================

class PruebasBaseConocimiento(unittest.TestCase):

    def test_numero_de_reglas(self):

        # Cazador: 4 x 5 = 20 de la matriz + 3 extra
        # Jaguar:  3 x 3 = 9 de la matriz + 2 extra

        self.assertEqual(len(base_equipo("cazador").reglas), 23)
        self.assertEqual(len(base_equipo("jaguar").reglas), 11)

    def test_guardar_y_cargar_json(self):

        base = base_equipo("cazador")

        with tempfile.TemporaryDirectory() as carpeta:

            archivo = os.path.join(carpeta, "base.json")

            base.guardar(archivo)

            cargada = BaseConocimiento.cargar(archivo)

        self.assertEqual(cargada.a_cromosoma(), base.a_cromosoma())


# ==========================================
# 4. MOTOR MAMDANI Y CENTROIDE
# ==========================================

class PruebasMotor(unittest.TestCase):

    def setUp(self):

        self.cazador = ControladorDifuso(base_equipo("cazador"))

    def test_centroide_de_un_rectangulo(self):

        xs = [0, 1, 2, 3, 4]

        self.assertAlmostEqual(centroide(xs, [1, 1, 1, 1, 1]), 2.0)

    def test_centroide_sin_area(self):

        self.assertIsNone(centroide([0, 1, 2], [0, 0, 0]))

    def decidir_con_metodo(self, metodo, entradas):

        import Logica_Difusa.motor_mamdani as motor

        anterior = motor.METODO_DEFUZZIFICACION

        motor.METODO_DEFUZZIFICACION = metodo

        try:

            return self.cazador.decidir(entradas)

        finally:

            motor.METODO_DEFUZZIFICACION = anterior

    def test_ejemplo_numerico_con_centroide(self):

        # reserva 30, distancia 4, peligro 60
        # Gana la regla R21 (huir, 0.67), pero el
        # centroide (33.3) cae en RECARGAR.

        accion, x = self.decidir_con_metodo(
            "centroide",
            {"reserva": 30, "distancia": 4, "peligro": 60}
        )

        self.assertAlmostEqual(x, 33.32, places=2)
        self.assertEqual(accion, "recargar")
        self.assertEqual(self.cazador.regla_dominante()[0], "R21")

    def test_ejemplo_numerico_con_altura_maxima(self):

        # Mismo ejemplo: con altura máxima gana la
        # regla más fuerte, R21 -> HUIR. El
        # centroide se sigue calculando igual.

        accion, x = self.decidir_con_metodo(
            "altura_maxima",
            {"reserva": 30, "distancia": 4, "peligro": 60}
        )

        self.assertAlmostEqual(x, 33.32, places=2)
        self.assertEqual(accion, "huir")

    def test_traza_guarda_cada_fase(self):

        self.cazador.decidir(
            {"reserva": 30, "distancia": 4, "peligro": 70}
        )

        traza = self.cazador.ultima_traza

        for fase in ("grados", "fuerzas", "alturas", "agregado", "x_estrella", "accion"):

            self.assertIn(fase, traza)


# ==========================================
# 5. CAZADOR EN CASOS CONTROLADOS
# ==========================================

class PruebasCazador(unittest.TestCase):

    CASOS = [
        # (reserva, distancia, peligro) -> acción
        ((5, 30, 0), "recargar"),     # reserva muy baja, tranquilo
        ((90, 1, 0), "atacar"),       # reserva alta, jaguar muy cerca
        ((90, 3, 90), "huir"),        # jaguar agresivo y cerca
        ((90, 6, 0), "perseguir"),    # reserva alta, distancia media
        ((45, 12, 0), "explorar"),    # reserva media, jaguar lejos
        ((90, 25, 0), "explorar"),    # no sabe del jaguar (muy lejos)
    ]

    def test_casos(self):

        controlador = ControladorDifuso(base_equipo("cazador"))

        for (reserva, distancia, peligro), esperada in self.CASOS:

            with self.subTest(reserva=reserva, distancia=distancia, peligro=peligro):

                accion, _ = controlador.decidir(
                    {"reserva": reserva, "distancia": distancia, "peligro": peligro}
                )

                self.assertEqual(accion, esperada)


# ==========================================
# 6. JAGUAR EN CASOS CONTROLADOS
# ==========================================

class PruebasJaguar(unittest.TestCase):

    CASOS = [
        # (hambre, distancia_cazador, energia_cazador) -> acción
        ((10, 2, 80), "huir"),         # saciado y el cazador cerca
        ((90, 2, 80), "atacar"),       # voraz y el cazador cerca
        ((57, 6, 80), "cazar_raton"),  # hambriento, cazador a media distancia
        ((10, 20, 80), "merodear"),    # saciado y el cazador lejos
        ((10, 2, 10), "atacar"),       # cazador débil y cerca
        ((50, 20, 10), "merodear"),    # cazador débil pero lejos
    ]

    def test_casos(self):

        controlador = ControladorDifuso(base_equipo("jaguar"))

        for (hambre, distancia, energia), esperada in self.CASOS:

            with self.subTest(hambre=hambre, distancia=distancia, energia=energia):

                accion, _ = controlador.decidir(
                    {
                        "hambre": hambre,
                        "distancia_cazador": distancia,
                        "energia_cazador": energia,
                    }
                )

                self.assertEqual(accion, esperada)


# ==========================================
# 7. BITÁCORA DEL JAGUAR Y ESCENARIOS
# ==========================================

class PruebasAgentes(unittest.TestCase):

    def test_bitacora_del_jaguar(self):

        import random

        from Mundo.mundo import MundoSelva
        from Agente_Cazador.agente import AgenteCazador
        from Agente_Jaguar.agente import AgenteJaguar

        random.seed(5)

        with contextlib.redirect_stdout(io.StringIO()):

            mundo = MundoSelva()
            cazador = AgenteCazador(mundo)
            jaguar = AgenteJaguar(mundo)

            for _ in range(10):

                cazador.tomar_decision(mundo.posicion_jaguar)

                if mundo.jaguar_vivo:

                    jaguar.tomar_decision(cazador.posicion, cazador.energia, mundo.ratones)

        self.assertGreater(len(jaguar.bitacora), 0)

        registro = jaguar.bitacora[-1]

        for campo in ("turno", "entradas", "regla", "accion", "movimiento", "fuente"):

            self.assertIn(campo, registro)

    def test_escenario_peligro_empieza_recargando_o_huyendo(self):

        from Mundo.escenarios import ESCENARIOS
        from Logica_Difusa.simulador import jugar_partida

        partida = jugar_partida(
            base_equipo("cazador"),
            base_equipo("jaguar"),
            0,
            max_turnos=20,
            escenario=ESCENARIOS[2],
        )

        self.assertIn(partida["secuencia"][0], ("recargar", "huir"))

    def test_escenario_caza_empieza_explorando(self):

        from Mundo.escenarios import ESCENARIOS
        from Logica_Difusa.simulador import jugar_partida

        partida = jugar_partida(
            base_equipo("cazador"),
            base_equipo("jaguar"),
            0,
            max_turnos=20,
            escenario=ESCENARIOS[1],
        )

        self.assertEqual(partida["secuencia"][0], "explorar")


# ==========================================
# 8. INTERCEPTOR (AGENTE 3, CAZADOR RIVAL) Y
#    DIOS
# ==========================================

class PruebasInterceptor(unittest.TestCase):

    def jugar_con_dios(self, con_interceptor, semilla=5, pasos=4000):

        import random

        from Logica_Difusa.dios import Dios

        random.seed(semilla)

        dios = Dios()

        dios.con_interceptor = con_interceptor

        pisadas_cueva = 0

        with contextlib.redirect_stdout(io.StringIO()):

            dios.nueva_partida()

            for _ in range(pasos):

                if not dios.paso(0.05):
                    break

                if (
                    dios.interceptor is not None
                    and dios.interceptor.posicion == dios.mundo.cueva
                ):
                    pisadas_cueva += 1

        return dios, pisadas_cueva

    def test_interceptor_es_otro_cazador(self):

        # Mismas reglas que el cazador, pero su
        # propio controlador (decide por su cuenta)

        from Agente_Cazador.agente import AgenteCazador

        dios, pisadas_cueva = self.jugar_con_dios(True)

        self.assertIsInstance(dios.interceptor, AgenteCazador)
        self.assertIsNot(dios.interceptor.controlador, dios.cazador.controlador)
        self.assertEqual(len(dios.interceptor.controlador.base.reglas), 23)
        self.assertGreater(dios.interceptor.turno, 0)
        self.assertEqual(pisadas_cueva, 0)

    def test_pelea_entre_cazadores(self):

        # Gana el que tiene más energía; el que
        # pierde muere

        dios, _ = self.jugar_con_dios(True, pasos=1)

        cazador = dios.cazador
        interceptor = dios.interceptor

        # Una casilla libre lejos de las dos cabañas
        def distancia_a_cabanas(c):
            return min(
                abs(c[0] - cabana[0]) + abs(c[1] - cabana[1])
                for cabana in dios.mundo.campamentos
            )

        lejos = max(
            (
                (fila, columna)
                for fila in range(dios.mundo.filas)
                for columna in range(dios.mundo.columnas)
                if dios.mundo.es_transitable((fila, columna))
            ),
            key=distancia_a_cabanas
        )

        def juntar(energia_cazador, energia_interceptor):

            for agente, cuerpo, energia in (
                (cazador, dios.cuerpo_cazador, energia_cazador),
                (interceptor, dios.cuerpo_interceptor, energia_interceptor),
            ):
                agente.posicion = lejos
                agente.vidas = 1
                agente.energia = energia
                cuerpo.origen = cuerpo.destino = lejos

            dios.espera_pelea = 0

            with contextlib.redirect_stdout(io.StringIO()):
                dios.pelea_entre_cazadores()

        # El interceptor tiene más energía: gana
        juntar(60, 90)

        self.assertEqual(cazador.vidas, 0)
        self.assertEqual(interceptor.vidas, 1)

        # Ahora el cazador tiene más: gana él
        juntar(80, 30)

        self.assertEqual(cazador.vidas, 1)
        self.assertEqual(interceptor.vidas, 0)

        # Empate: nadie muere, los dos pierden 10
        juntar(50, 50)

        self.assertEqual((cazador.vidas, interceptor.vidas), (1, 1))
        self.assertEqual((cazador.energia, interceptor.energia), (40, 40))

    def test_cada_cazador_tiene_su_cabana(self):

        dios, _ = self.jugar_con_dios(True, pasos=1)

        cabana = dios.mundo.campamento_interceptor

        self.assertNotEqual(cabana, dios.mundo.campamento)
        self.assertEqual(dios.interceptor.campamento, cabana)
        self.assertEqual(dios.cazador.campamento, dios.mundo.campamento)
        self.assertNotEqual(cabana, dios.mundo.cueva)

    def test_en_la_cabana_no_se_pelea(self):

        dios, _ = self.jugar_con_dios(True, pasos=1)

        campamento = dios.mundo.campamento

        dios.cazador.posicion = campamento
        dios.interceptor.posicion = campamento
        dios.cazador.energia = 30
        dios.interceptor.energia = 90
        dios.espera_pelea = 0

        with contextlib.redirect_stdout(io.StringIO()):
            dios.pelea_entre_cazadores()

        self.assertEqual(dios.cazador.energia, 30)

    def test_sin_interceptor(self):

        dios, _ = self.jugar_con_dios(False, pasos=200)

        self.assertIsNone(dios.interceptor)


if __name__ == "__main__":

    unittest.main()
