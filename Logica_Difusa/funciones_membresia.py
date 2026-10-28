# ==========================================
# FUNCIONES DE MEMBRESÍA
#
# Cada función recibe un valor x y regresa
# su grado de membresía, que SIEMPRE va de
# 0 a 1.
#
# Tipos que usamos (los mismos de clase):
#
#   GRADO (sube):            ___/‾‾‾
#     x <= x0 -> 0
#     x >= x1 -> 1
#
#   GRADO INVERSA (baja):    ‾‾‾\___
#     x <= x0 -> 1
#     x >= x1 -> 0
#
#   TRIANGULAR:              __/\__
#     x0 = inicio, x1 = pico, x2 = fin
#
#   TRAPEZOIDAL:             __/‾‾\__
#     x0 = inicio, x1 y x2 = meseta, x3 = fin
# ==========================================


def grado(x, x0, x1):

    if x <= x0:

        return 0.0

    if x >= x1:

        return 1.0

    return (x - x0) / (x1 - x0)


def grado_inversa(x, x0, x1):

    if x <= x0:

        return 1.0

    if x >= x1:

        return 0.0

    return (x1 - x) / (x1 - x0)


def triangular(x, x0, x1, x2):

    if x <= x0 or x >= x2:

        return 0.0

    if x <= x1:

        return (x - x0) / (x1 - x0)

    return (x2 - x) / (x2 - x1)


def trapezoidal(x, x0, x1, x2, x3):

    if x <= x0 or x >= x3:

        return 0.0

    if x < x1:

        return (x - x0) / (x1 - x0)

    if x <= x2:

        return 1.0

    return (x3 - x) / (x3 - x2)


# Nombre del tipo -> función

TIPOS = {
    "grado": grado,
    "grado_inversa": grado_inversa,
    "triangular": triangular,
    "trapezoidal": trapezoidal,
}


# ==========================================
# TÉRMINO LINGÜÍSTICO
#
# Un término es una palabra (por ejemplo
# "cerca") con su función de membresía y
# sus puntos X0, X1, X2, X3.
# ==========================================

class Termino:

    def __init__(self, nombre, tipo, puntos):

        if tipo not in TIPOS:

            raise ValueError(
                f"Tipo de membresía desconocido: {tipo}"
            )

        self.nombre = nombre

        self.tipo = tipo

        self.puntos = tuple(puntos)

        self._funcion = TIPOS[tipo]


    def grado(self, x):

        valor = self._funcion(x, *self.puntos)

        # Por seguridad, siempre entre 0 y 1

        return max(0.0, min(1.0, valor))


# ==========================================
# VARIABLE LINGÜÍSTICA
#
# Tiene un nombre, un universo de discurso
# [minimo, maximo] y sus términos.
# ==========================================

class VariableLinguistica:

    def __init__(self, nombre, minimo, maximo, terminos, unidad=""):

        self.nombre = nombre

        self.minimo = minimo

        self.maximo = maximo

        self.unidad = unidad

        self.terminos = {
            termino.nombre: termino
            for termino in terminos
        }


    def recortar(self, x):

        # Un valor fuera del universo se lleva
        # al borde más cercano

        return max(self.minimo, min(self.maximo, x))


    def fuzzificar(self, x):

        # Regresa {término: grado} para un
        # valor concreto

        x = self.recortar(x)

        return {
            nombre: termino.grado(x)
            for nombre, termino in self.terminos.items()
        }
