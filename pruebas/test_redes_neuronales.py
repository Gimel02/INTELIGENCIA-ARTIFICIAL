# ==========================================
# PRUEBAS AUTOMÁTICAS DE LA RED NEURONAL
#
#   1. Funciones de transferencia
#   2. La neurona: regla de propagación y
#      salida
#   3. Aprendizaje: el perceptrón aprende OR
#      (ejemplo del PDF) y AND; regla delta
#   4. La red "¿el jaguar va a atacar?":
#      entradas, supervisor, aprendizaje,
#      guardar y cargar
#   5. Modo observador: el juego es idéntico
#      con y sin red
#
# Cómo correrlas (desde la carpeta del
# proyecto):
#
#   python3 -m unittest discover pruebas -v
# ==========================================

import contextlib
import io
import os
import unittest

from Redes_Neuronales.funciones_transferencia import (
    escalon,
    lineal,
    lineal_mixta,
    sigmoidal,
    gaussiana,
)
from Redes_Neuronales.neurona import Neurona
from Redes_Neuronales.predictor_ataque import (
    PredictorAtaque,
    HORIZONTE,
    CARPETA_PESOS,
)


OR = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
AND = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]


def entrenar_hasta_aprender(neurona, tabla, max_epocas=50):

    for epoca in range(1, max_epocas + 1):

        errores = sum(abs(neurona.entrenar(x, d)) for x, d in tabla)

        if errores == 0:

            return epoca

    return None


# ==========================================
# 1. FUNCIONES DE TRANSFERENCIA
# ==========================================

class PruebasFuncionesTransferencia(unittest.TestCase):

    def test_escalon(self):

        # E = {0, 1} y E = {-1, 1} (pág. 45)
        self.assertEqual(escalon(0.3), 1)
        self.assertEqual(escalon(-0.3), 0)
        self.assertEqual(escalon(0.3, bipolar=True), 1)
        self.assertEqual(escalon(-0.3, bipolar=True), -1)

    def test_escalon_en_el_umbral_conserva_la_salida(self):

        # Si Net = θ, la salida es y(t), la anterior
        self.assertEqual(escalon(0, anterior=0), 0)
        self.assertEqual(escalon(0, anterior=1), 1)
        self.assertEqual(escalon(0, bipolar=True, anterior=-1), -1)

        # Sin salida anterior se toma 1
        self.assertEqual(escalon(0), 1)

    def test_lineal(self):

        # y = Net - θ (pág. 46)
        self.assertEqual(lineal(2.5), 2.5)
        self.assertEqual(lineal(-3), -3)

    def test_mixta_de_0_a_1(self):

        # 0 si x < -c; 1 si x > c; x/(2c) + 1/2 en otro caso
        self.assertEqual(lineal_mixta(-5, c=2), 0)
        self.assertEqual(lineal_mixta(5, c=2), 1)
        self.assertAlmostEqual(lineal_mixta(0, c=2), 0.5)
        self.assertAlmostEqual(lineal_mixta(1, c=2), 0.75)

    def test_mixta_con_limites_b_y_B(self):

        # Pág. 47: b si x <= b; x si b < x < B; B si x >= B
        self.assertEqual(lineal_mixta(-5, inferior=-2, superior=3), -2)
        self.assertEqual(lineal_mixta(9, inferior=-2, superior=3), 3)
        self.assertEqual(lineal_mixta(1.5, inferior=-2, superior=3), 1.5)

    def test_sigmoidal_como_en_el_pdf(self):

        # y = 1 / (1 + e^-(Net - θ)); en Net = θ vale 0.5
        import math

        self.assertAlmostEqual(sigmoidal(0), 0.5)
        self.assertAlmostEqual(sigmoidal(1.3), 1 / (1 + math.exp(-1.3)))

    def test_neurona_ficticia_del_umbral(self):

        # Pág. 49: y0 = 1 con peso w0 = -θ, así
        # f(Σ_{j=1} w·y - θ) = f(Σ_{j=0} w·y)
        neurona = Neurona(2, pesos=[0.4, 0.6], umbral=0.3)

        x = [1.0, 0.5]

        con_umbral = 0.4 * 1.0 + 0.6 * 0.5 - 0.3
        con_ficticia = sum(w * y for w, y in zip([neurona.w0, 0.4, 0.6], [1, 1.0, 0.5]))

        self.assertAlmostEqual(neurona.net(x), con_umbral)
        self.assertAlmostEqual(con_umbral, con_ficticia)

    def test_mixta_de_menos_1_a_1(self):

        # -1 si x < -c; 1 si x > c; a·x en otro caso
        self.assertEqual(lineal_mixta(-5, c=2, bipolar=True), -1)
        self.assertEqual(lineal_mixta(5, c=2, bipolar=True), 1)
        self.assertAlmostEqual(lineal_mixta(1, c=2, bipolar=True), 0.5)
        self.assertAlmostEqual(lineal_mixta(1, c=2, bipolar=True, a=0.3), 0.3)

    def test_sigmoidal(self):

        self.assertAlmostEqual(sigmoidal(0), 0.5)
        self.assertGreater(sigmoidal(5), 0.99)
        self.assertLess(sigmoidal(-5), 0.01)

    def test_gaussiana(self):

        self.assertAlmostEqual(gaussiana(0), 1.0)
        self.assertAlmostEqual(gaussiana(1), gaussiana(-1))
        self.assertLess(gaussiana(3), 0.05)


# ==========================================
# 2. LA NEURONA
# ==========================================

class PruebasNeurona(unittest.TestCase):

    def test_regla_de_propagacion(self):

        # net = Σ wi · xi − θ
        neurona = Neurona(2, pesos=[0.5, 0.5], umbral=0.5)

        self.assertAlmostEqual(neurona.net([1, 0]), 0.0)
        self.assertAlmostEqual(neurona.net([1, 1]), 0.5)
        self.assertAlmostEqual(neurona.net([0, 0]), -0.5)

    def test_salida_es_si_o_no(self):

        neurona = Neurona(2, pesos=[0.5, 0.5], umbral=0.75)

        self.assertEqual(neurona.salida([1, 1]), 1)
        self.assertEqual(neurona.salida([1, 0]), 0)

    def test_numero_de_entradas(self):

        with self.assertRaises(ValueError):

            Neurona(3).net([1, 0])


# ==========================================
# 3. APRENDIZAJE
# ==========================================

class PruebasAprendizaje(unittest.TestCase):

    def test_perceptron_aprende_or_del_pdf(self):

        neurona = Neurona(2, alfa=0.5)

        epocas = entrenar_hasta_aprender(neurona, OR)

        self.assertIsNotNone(epocas)

        for x, d in OR:

            self.assertEqual(neurona.salida(x), d)

    def test_perceptron_aprende_and(self):

        neurona = Neurona(2, alfa=0.5)

        self.assertIsNotNone(entrenar_hasta_aprender(neurona, AND))

        for x, d in AND:

            self.assertEqual(neurona.salida(x), d)

    def test_un_paso_de_la_regla(self):

        # Δwi = α · xi · (d − y)
        neurona = Neurona(2, alfa=0.5, umbral=0.5)

        # net = −0.5 -> y = 0, pero d = 1
        error = neurona.entrenar([1, 0], 1)

        self.assertEqual(error, 1)
        self.assertEqual(neurona.pesos, [0.5, 0.0])
        self.assertAlmostEqual(neurona.umbral, 0.0)

    def test_si_acierta_no_cambia(self):

        neurona = Neurona(2, pesos=[1, 1], umbral=0.5, alfa=0.5)

        neurona.entrenar([1, 1], 1)

        self.assertEqual(neurona.pesos, [1, 1])
        self.assertEqual(neurona.entrenamientos_sin_cambio, 1)

    def test_regla_delta_baja_el_error(self):

        neurona = Neurona(2, transferencia="sigmoidal", alfa=0.5)

        def error_total():
            return sum((d - neurona.salida(x)) ** 2 for x, d in OR)

        antes = error_total()

        for _ in range(200):
            for x, d in OR:
                neurona.entrenar(x, d)

        self.assertLess(error_total(), antes / 4)


# ==========================================
# 4. LA RED "¿EL JAGUAR VA A ATACAR?"
# ==========================================

class PruebasPredictorAtaque(unittest.TestCase):

    def test_entradas(self):

        red = PredictorAtaque()

        self.assertEqual(red.entradas(10, 50, 100), [0.0, 0.5, 0, 0.0])

        red.distancia_anterior = 5

        cercania, hambre, se_acerca, debilidad = red.entradas(3, 80, 40)

        self.assertAlmostEqual(cercania, 0.7)
        self.assertAlmostEqual(hambre, 0.8)
        self.assertEqual(se_acerca, 1)
        self.assertAlmostEqual(debilidad, 0.6)

    def test_sin_entrenar_dice_no_ataca(self):

        self.assertEqual(PredictorAtaque().predecir([1, 1, 1, 1]), 0)

    def test_refuerzo_negativo_si_no_anticipa_ataque(self):

        # La red predice NO ATACA.
        # Si después el Jaguar sí ataca,
        # el crítico entrega -1.

        red = PredictorAtaque()


        red.observar(
            1,
            True,
            3,
            70,
            30,
            False
        )


        red.observar(
            2,
            True,
            2,
            70,
            30,
            True
        )


        self.assertEqual(
            red.evaluadas,
            1
        )


        self.assertEqual(
            red.refuerzos_negativos,
            1
        )


        self.assertEqual(
            red.refuerzos_positivos,
            0
        )


        self.assertEqual(
            red.recompensa_acumulada,
            -1
        )


        self.assertEqual(
            red.bitacora[-1]["refuerzo"],
            -1
        )


        self.assertEqual(
            red.bitacora[-1]["motivo"],
            "no anticipó el ataque"
        )

    def test_refuerzo_positivo_si_no_hay_ataque(self):

        # La red predice NO ATACA.
        # Si transcurre el horizonte sin ataque,
        # el crítico entrega +1.

        red = PredictorAtaque()


        red.observar(
            1,
            True,
            8,
            10,
            90,
            False
        )


        for turno in range(
            2,
            2 + HORIZONTE
        ):

            red.observar(
                turno,
                False,
                None,
                10,
                90,
                False
            )


        self.assertEqual(
            red.evaluadas,
            1
        )


        self.assertEqual(
            red.refuerzos_positivos,
            1
        )


        self.assertEqual(
            red.refuerzos_negativos,
            0
        )


        self.assertEqual(
            red.recompensa_acumulada,
            1
        )


        self.assertEqual(
            red.bitacora[-1]["refuerzo"],
            1
        )


        self.assertEqual(
            red.bitacora[-1]["motivo"],
            "correctamente continuó sin alarma"
        )
    
    def test_aprende_de_sus_errores(self):

        # Siempre que está débil y cerca, el
        # jaguar ataca: el riesgo debe subir

        red = PredictorAtaque()

        x = red.entradas(1, 50, 10)

        riesgo_antes = red.riesgo(x)

        turno = 0

        for _ in range(50):

            turno += 1
            red.observar(turno, True, 1, 50, 10, False)
            turno += 1
            red.observar(turno, True, 1, 50, 10, True)

        self.assertGreater(red.riesgo(x), riesgo_antes)

    def test_guardar_y_cargar(self):

        red = PredictorAtaque()

        red.neurona.pesos = [0.1, 0.2, 0.3, 0.4]

        archivo = "prueba_temporal.json"

        try:

            red.guardar(archivo)

            cargada = PredictorAtaque.cargar(archivo)

            self.assertEqual(cargada.neurona.pesos, [0.1, 0.2, 0.3, 0.4])

        finally:

            ruta = os.path.join(CARPETA_PESOS, archivo)

            if os.path.exists(ruta):

                os.remove(ruta)

    def test_guarda_estadisticas_del_refuerzo(self):

        red = PredictorAtaque()

        red.refuerzos_positivos = 7
        red.recompensa_acumulada = 5

        archivo = "prueba_estadisticas.json"

        try:

            red.guardar(archivo)

            cargada = PredictorAtaque.cargar(archivo)

            self.assertEqual(cargada.refuerzos_positivos, 7)
            self.assertEqual(cargada.recompensa_acumulada, 5)

        finally:

            ruta = os.path.join(CARPETA_PESOS, archivo)

            if os.path.exists(ruta):

                os.remove(ruta)

    def test_dios_no_guarda_si_no_se_pide(self):

        # En las pruebas DIOS no debe tocar los
        # archivos de pesos del juego

        from Logica_Difusa.dios import Dios

        self.assertFalse(Dios().guardar_aprendizaje)

    def test_pesos_entrenados(self):

        # Con el entrenamiento offline, un cazador
        # débil y cerca corre más riesgo que uno
        # fuerte y lejos

        red = PredictorAtaque.cargar()

        if red.neurona.entrenamientos == 0:

            self.skipTest("Falta correr Redes_Neuronales.entrenar_red")

        debil_cerca = red.riesgo(red.entradas(2, 70, 15))
        fuerte_lejos = red.riesgo(red.entradas(9, 20, 95))

        self.assertGreater(debil_cerca, fuerte_lejos)


# ==========================================
# 5. MODO OBSERVADOR
# ==========================================

class PruebasModoObservador(unittest.TestCase):

    def jugar(self, con_red, semilla):

        import random

        from Logica_Difusa.dios import Dios

        random.seed(semilla)

        dios = Dios()

        dios.con_red_neuronal = con_red

        recorrido = []

        with contextlib.redirect_stdout(io.StringIO()):

            dios.nueva_partida()

            for _ in range(1500):

                if not dios.paso(0.05):
                    break

                recorrido.append((
                    dios.cazador.posicion,
                    dios.mundo.posicion_jaguar,
                    dios.cazador.energia,
                ))

        return recorrido, dios

    def test_el_juego_no_cambia_con_la_red(self):

        for semilla in (1000, 1001):

            with self.subTest(semilla=semilla):

                sin_red, _ = self.jugar(False, semilla)
                con_red, dios = self.jugar(True, semilla)

                self.assertEqual(sin_red, con_red)
                self.assertIsNotNone(dios.cazador.red_ataque)


if __name__ == "__main__":

    unittest.main()
