# ==========================================
# FUNCIONES DE TRANSFERENCIA (O DE SALIDA)
#
# Transforman el estado de activación de la
# neurona en su señal de salida:
#
#   y = f(net)
#
# Son las funciones típicas del PDF (pág. 37
# a 48):
#
#   - Escalón        (salida 0/1 o -1/1)
#   - Lineal         f(x) = x
#   - Lineal-mixta   lineal, pero acotada
#                    entre un límite inferior
#                    y uno superior
#   - Sigmoidal      continua, entre 0 y 1
#   - Gaussiana      campana: centro y anchura
#                    adaptables
#
# Programadas a mano, sin librerías.
# ==========================================

import math


def escalon(net, bipolar=False):

    # E = {0, 1}:  1 si net >= 0, si no 0
    # E = {-1, 1}: 1 si net >= 0, si no -1

    if net >= 0:

        return 1

    return -1 if bipolar else 0


def lineal(net):

    # Identidad: la salida es la entrada total

    return net


def lineal_mixta(net, limite_inferior=-1.0, limite_superior=1.0):

    # Abajo del límite inferior vale el límite
    # inferior; arriba del superior vale el
    # superior; en medio es lineal

    if net <= limite_inferior:

        return limite_inferior

    if net >= limite_superior:

        return limite_superior

    return net


def sigmoidal(net, pendiente=1.0):

    # f(x) = 1 / (1 + e^(-g·x))

    # Se evita el desbordamiento con valores
    # muy negativos
    if net * pendiente < -60:

        return 0.0

    return 1.0 / (1.0 + math.exp(-pendiente * net))


def gaussiana(net, centro=0.0, anchura=1.0):

    # f(x) = e^(-((x - c)^2) / (2·a^2))

    return math.exp(-((net - centro) ** 2) / (2 * anchura ** 2))


# Por nombre (para elegirla desde la neurona)

FUNCIONES = {
    "escalon": escalon,
    "lineal": lineal,
    "lineal_mixta": lineal_mixta,
    "sigmoidal": sigmoidal,
    "gaussiana": gaussiana,
}
