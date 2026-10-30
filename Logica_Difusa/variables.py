# ==========================================
# VARIABLES LINGÜÍSTICAS
#
# AGENTE 1: CAZADOR
#
#   Entradas
#   1. reserva (0 a 100 de energía)
#      Energía que le SOBRA después de guardar
#      la necesaria para volver al campamento:
#        reserva = energía - energía para regresar
#   2. distancia (0 a 30 casillas)
#      Distancia Manhattan al jaguar (o a donde
#      lo vio por última vez). Si no sabe nada
#      del jaguar, vale 30 (muy lejos).
#   3. peligro (0 a 100)
#      100 si el jaguar lo ataca, el hambre del
#      jaguar si lo percibe, 0 si no lo percibe.
#
#   Salida: accion (0 a 100)
#      huir · recargar · explorar · perseguir · atacar
#
# AGENTE 2: JAGUAR
#
#   Entradas
#   1. hambre (0 a 100)
#   2. distancia_cazador (0 a 30 casillas)
#   3. energia_cazador (0 a 100): si el cazador
#      está débil, el jaguar se anima a atacar.
#
#   Salida: accion_jaguar (0 a 100)
#      huir · merodear · cazar_raton · atacar
# ==========================================

from Logica_Difusa.funciones_membresia import (
    Termino,
    VariableLinguistica
)


# ==========================================
# CAZADOR
# ==========================================

RESERVA = VariableLinguistica(
    "reserva", 0, 100,
    [
        Termino("muy_baja", "grado_inversa", (8, 18)),
        Termino("baja", "trapezoidal", (8, 18, 25, 35)),
        Termino("media", "trapezoidal", (25, 35, 50, 65)),
        Termino("alta", "grado", (50, 65)),
    ],
    unidad="energía"
)


DISTANCIA = VariableLinguistica(
    "distancia", 0, 30,
    [
        Termino("muy_cerca", "grado_inversa", (1, 3)),
        Termino("cerca", "triangular", (1, 3, 6)),
        Termino("media", "triangular", (3, 6, 10)),
        Termino("lejos", "trapezoidal", (6, 10, 15, 20)),
        Termino("muy_lejos", "grado", (15, 20)),
    ],
    unidad="casillas"
)


PELIGRO = VariableLinguistica(
    "peligro", 0, 100,
    [
        Termino("tranquilo", "grado_inversa", (30, 70)),
        Termino("agresivo", "grado", (30, 70)),
    ],
    unidad="puntos"
)


ACCION = VariableLinguistica(
    "accion", 0, 100,
    [
        Termino("huir", "grado_inversa", (10, 30)),
        Termino("recargar", "triangular", (10, 30, 50)),
        Termino("explorar", "triangular", (30, 50, 70)),
        Termino("perseguir", "triangular", (50, 70, 90)),
        Termino("atacar", "grado", (70, 90)),
    ],
    unidad="puntos"
)


ENTRADAS_CAZADOR = {
    "reserva": RESERVA,
    "distancia": DISTANCIA,
    "peligro": PELIGRO,
}


# ==========================================
# JAGUAR
# ==========================================

HAMBRE = VariableLinguistica(
    "hambre", 0, 100,
    [
        Termino("saciado", "grado_inversa", (30, 50)),
        Termino("hambriento", "trapezoidal", (30, 50, 65, 85)),
        Termino("voraz", "grado", (65, 85)),
    ],
    unidad="puntos"
)


DISTANCIA_CAZADOR = VariableLinguistica(
    "distancia_cazador", 0, 30,
    [
        Termino("cerca", "grado_inversa", (3, 5)),
        Termino("media", "trapezoidal", (3, 5, 8, 12)),
        Termino("lejos", "grado", (8, 12)),
    ],
    unidad="casillas"
)


ENERGIA_CAZADOR = VariableLinguistica(
    "energia_cazador", 0, 100,
    [
        Termino("debil", "grado_inversa", (25, 40)),
        Termino("fuerte", "grado", (25, 40)),
    ],
    unidad="energía"
)


ACCION_JAGUAR = VariableLinguistica(
    "accion_jaguar", 0, 100,
    [
        Termino("huir", "grado_inversa", (15, 40)),
        Termino("merodear", "triangular", (15, 40, 65)),
        Termino("cazar_raton", "triangular", (40, 65, 90)),
        Termino("atacar", "grado", (65, 90)),
    ],
    unidad="puntos"
)


ENTRADAS_JAGUAR = {
    "hambre": HAMBRE,
    "distancia_cazador": DISTANCIA_CAZADOR,
    "energia_cazador": ENERGIA_CAZADOR,
}
