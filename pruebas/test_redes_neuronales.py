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

        self.assertEqual(escalon(0.3), 1)
        self.assertEqual(escalon(0), 1)
        self.assertEqual(escalon(-0.3), 0)
        self.assertEqual(escalon(-0.3, bipolar=True), -1)

    def test_lineal_y_mixta(self):

        self.assertEqual(lineal(2.5), 2.5)
        self.assertEqual(lineal_mixta(5, -1, 1), 1)
        self.assertEqual(lineal_mixta(-5, -1, 1), -1)
        self.assertEqual(lineal_mixta(0.4, -1, 1), 0.4)

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

    def test_supervisor_etiqueta_ataque(self):

        # Predice en el turno 1 y en el 2 lo ve
        # atacando: la respuesta correcta era 1

        red = PredictorAtaque()

        red.observar(1, True, 3, 70, 30, False)
        red.observar(2, True, 2, 70, 30, True)

        self.assertEqual(red.ejemplos[-1][1], 1)
        self.assertEqual(red.ataques_reales, 1)

    def test_supervisor_etiqueta_no_ataque(self):

        # Pasan 3 turnos sin ataque: era 0

        red = PredictorAtaque()

        red.observar(1, True, 8, 10, 90, False)

        for turno in range(2, 2 + HORIZONTE):

            red.observar(turno, False, None, 10, 90, False)

        self.assertEqual(red.ejemplos[0][1], 0)

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
