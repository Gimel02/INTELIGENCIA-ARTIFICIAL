# ==========================================
# OPERADORES DIFUSOS (MÉTODO DE MAMDANI)
#
#   AND difuso   = mínimo  (min)
#   OR difuso    = máximo  (max)
#   NOT difuso   = 1 - valor
#   Implicación  = min: recorta el conjunto de
#                  salida a la altura de la
#                  fuerza de la regla
#   Agregación   = max de las conclusiones de
#   (AGG)          todas las reglas
# ==========================================


def AND(*valores):

    return min(valores)


def OR(*valores):

    return max(valores)


def NOT(valor):

    return 1.0 - valor


def implicacion(fuerza_regla, grado_salida):

    # Mamdani: min(fuerza, μ_salida(x))

    return min(fuerza_regla, grado_salida)


def AGG(*valores):

    # Une las conclusiones con max. Si no hay
    # ninguna regla activa, el resultado es 0.

    return max(valores) if valores else 0.0
