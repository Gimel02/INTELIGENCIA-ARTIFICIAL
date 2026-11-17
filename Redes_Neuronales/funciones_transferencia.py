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
#   - Lineal-mixta   lineal en medio y
#                    acotada en los extremos
#                    (versión 0/1 o -1/1)
#   - Sigmoidal      continua, entre 0 y 1
#   - Gaussiana      campana: centro y anchura
#                    adaptables
#
# En todas, "net" ya trae restado el umbral
# (net = Net - θ), así que "net > 0" es lo
# mismo que "Net > θ".
#
# Programadas a mano, sin librerías.
# ==========================================

import math


def escalon(net, bipolar=False, anterior=None):

    # Como en el PDF (pág. 45):
    #
    #   E = {0, 1}:          E = {-1, 1}:
    #     1    si Net > θ      +1   si Net > θ
    #     y(t) si Net = θ      y(t) si Net = θ
    #     0    si Net < θ      -1   si Net < θ
    #
    # y(t) es la salida anterior de la neurona:
    # si el Net queda exactamente en el umbral,
    # la neurona no cambia. Si todavía no tiene
    # salida anterior, se toma 1.

    if net > 0:

        return 1

    if net < 0:

        return -1 if bipolar else 0

    return 1 if anterior is None else anterior


def lineal(net):

    # Identidad: y = Net - θ (pág. 46). El
    # estado puede ser cualquier número real.

    return net


def lineal_mixta(
    net,
    c=1.0,
    bipolar=False,
    a=None,
    inferior=None,
    superior=None
):

    # La salida es lineal en medio y se queda
    # en un límite en los extremos. El PDF la
    # muestra de 3 formas (x = Net - θ):
    #
    # 1) Pág. 47, con límites b y B
    #    (inferior=b, superior=B):
    #      b        si x <= b
    #      x        si b < x < B
    #      B        si x >= B
    #    El estado queda dentro del intervalo
    #    [b, B].
    #
    # 2) Pág. 39, E = {0, 1}:
    #      0              si x < -c
    #      1              si x > c
    #      x/(2c) + 1/2   en otro caso
    #
    # 3) Pág. 39, E = {-1, 1} (bipolar=True):
    #      -1             si x < -c
    #      1              si x > c
    #      a·x            en otro caso
    #    (a = 1/c para que la línea una -1 y 1)

    if inferior is not None and superior is not None:

        if net <= inferior:

            return inferior

        if net >= superior:

            return superior

        return net

    if bipolar:

        if net < -c:

            return -1

        if net > c:

            return 1

        pendiente = (1.0 / c) if a is None else a

        return pendiente * net

    if net < -c:

        return 0

    if net > c:

        return 1

    return net / (2 * c) + 0.5


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
