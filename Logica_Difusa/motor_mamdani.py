# ==========================================
# MOTOR DE INFERENCIA MAMDANI
#
# Fases del sistema de control difuso:
#
#   Input -> Fuzzificación -> Inferencia
#   (con la Control Rule Base) ->
#   Defuzzificación -> Output
#
# 1. FUZZIFICACIÓN: cada número de entrada se
#    convierte en grados de membresía (0 a 1).
# 2. INFERENCIA:
#    a) se evalúa el antecedente de cada regla
#       con AND = min, OR = max, NOT = 1 - x
#       (eso da la FUERZA de la regla);
#    b) IMPLICACIÓN = min: se recorta el
#       conjunto de salida a esa altura;
#    c) AGREGACIÓN = max de todos los recortes.
# 3. DEFUZZIFICACIÓN por CENTROIDE:
#       x* = Σ x·μ(x) / Σ μ(x)
# 4. OUTPUT: x* y la acción que le corresponde.
# ==========================================

from Logica_Difusa.operadores import (
    AND,
    OR,
    NOT,
    implicacion,
    AGG
)



# Paso para discretizar el universo de salida
# (0, 1, 2, ..., 100 -> 101 puntos)

PASO_CENTROIDE = 1.0


# ==========================================
# 1. FUZZIFICACIÓN
# ==========================================

def fuzzificar(valores, entradas):

    # valores  = {"reserva": 22, "distancia": 4, ...}
    # entradas = variables lingüísticas del agente
    # regresa  = {"reserva": {"baja": 0.7, ...}, ...}

    return {
        nombre: variable.fuzzificar(valores[nombre])
        for nombre, variable in entradas.items()
    }


# ==========================================
# 2a. EVALUAR ANTECEDENTE (fuerza de la regla)
# ==========================================

def evaluar(nodo, grados):

    if "var" in nodo:

        return grados[nodo["var"]][nodo["es"]]

    if "no" in nodo:

        return NOT(evaluar(nodo["no"], grados))

    if "y" in nodo:

        return AND(*(evaluar(hijo, grados) for hijo in nodo["y"]))

    if "o" in nodo:

        return OR(*(evaluar(hijo, grados) for hijo in nodo["o"]))

    raise ValueError(f"Nodo de antecedente desconocido: {nodo}")


# ==========================================
# UNIVERSO DE SALIDA DISCRETIZADO
# ==========================================

def universo_salida(salida, paso=PASO_CENTROIDE):

    puntos = []

    x = salida.minimo

    while x <= salida.maximo + 1e-9:

        puntos.append(round(x, 6))

        x += paso

    return puntos


# ==========================================
# 3. DEFUZZIFICACIÓN: CENTROIDE
# ==========================================

def centroide(xs, mus):

    suma_mu = sum(mus)

    if suma_mu == 0:

        # Ninguna regla se activó: no hay área.
        # Regresamos None para que el agente
        # use su acción por defecto.

        return None

    suma_x_mu = sum(x * mu for x, mu in zip(xs, mus))

    return suma_x_mu / suma_mu


def termino_de_salida(salida, x):

    # La acción es el término de salida con
    # mayor grado en x*

    grados = salida.fuzzificar(x)

    return max(grados, key=grados.get)

def accion_dominante(salida, alturas):

    # La acción final debe ser una acción que
    # realmente haya sido activada por las reglas.
    #
    # No usamos el centroide para elegir entre
    # acciones categóricas porque podría crear
    # una acción intermedia que ninguna regla
    # pidió, por ejemplo:
    #
    # HUIR + ATACAR -> EXPLORAR
    #
    # En caso de empate se respeta el orden de
    # los términos definido en variables.py.

    mayor_altura = max(
        alturas.values(),
        default=0.0
    )

    if mayor_altura <= 0:

        return None

    for nombre in salida.terminos:

        if abs(
            alturas.get(nombre, 0.0)
            -
            mayor_altura
        ) < 1e-9:

            return nombre

    return None

# ==========================================
# CONTROLADOR DIFUSO
#
# Junta todo. Cada agente tiene el suyo, con
# su propia base de conocimiento.
# ==========================================

class ControladorDifuso:

    # Si ninguna regla se activa (Σμ = 0)

    ACCION_POR_DEFECTO = {
        "cazador": "explorar",
        "jaguar": "merodear",
    }

    def __init__(self, base, paso=PASO_CENTROIDE):

        self.paso = paso

        # Última decisión con todos sus pasos
        # (para la bitácora y el reporte)

        self.ultima_traza = None

        self.cambiar_base(base)


    def cambiar_base(self, base):

        # Punto de conexión: el AG o el
        # orquestador cambian las reglas

        self.base = base

        self.entradas = base.perfil.entradas

        self.salida = base.perfil.salida

        self.xs = universo_salida(self.salida, self.paso)

        # Grados de cada término de salida en
        # cada punto del universo (se calculan
        # una sola vez)

        self.grados_salida = {
            nombre: [termino.grado(x) for x in self.xs]
            for nombre, termino in self.salida.terminos.items()
        }


    def decidir(self, valores, guardar_traza=True):

        # ---- 1. Fuzzificación ----

        grados = fuzzificar(valores, self.entradas)


        # ---- 2a. Fuerza de cada regla ----

        fuerzas = []

        for regla in self.base.reglas:

            fuerza = evaluar(regla["si"], grados)

            fuerzas.append(
                (regla["id"], regla["entonces"][1], fuerza)
            )


        # ---- 2b. Implicación (min) ----
        # Si varias reglas llevan al mismo
        # término, basta con la más fuerte
        # (porque después se agrega con max).

        altura_por_termino = {nombre: 0.0 for nombre in self.salida.terminos}

        for _, termino, fuerza in fuerzas:

            altura_por_termino[termino] = AGG(
                altura_por_termino[termino],
                fuerza
            )


        recortes = {
            termino: [
                implicacion(altura, mu)
                for mu in self.grados_salida[termino]
            ]
            for termino, altura in altura_por_termino.items()
            if altura > 0
        }


        # ---- 2c. Agregación (max) ----

        agregado = [
            AGG(*(recorte[i] for recorte in recortes.values()))
            for i in range(len(self.xs))
        ]


        # ---- 3. Centroide ----

        x_estrella = centroide(self.xs, agregado)


        # ---- 4. Acción lingüística dominante ----
        #
        # El centroide se conserva como valor numérico
        # para la traza y el análisis del controlador.
        #
        # La acción real se obtiene del consecuente
        # con mayor activación para evitar acciones
        # "fantasma" creadas por promediar categorías.

        accion = accion_dominante(
            self.salida,
            altura_por_termino
        )

        if accion is None:

            accion = self.ACCION_POR_DEFECTO[
                self.base.perfil.nombre
            ]


        if guardar_traza:

            self.ultima_traza = {
                "entradas": dict(valores),
                "grados": grados,
                "fuerzas": fuerzas,
                "alturas": altura_por_termino,
                "xs": self.xs,
                "agregado": agregado,
                "x_estrella": x_estrella,
                "accion": accion,
            }

        return accion, x_estrella


    # --------------------------------------
    # Resumen corto de la última decisión
    # --------------------------------------

    def explicar(self):

        traza = self.ultima_traza

        if traza is None:

            return "Sin decisiones todavía"

        activas = sorted(
            (f for f in traza["fuerzas"] if f[2] > 0),
            key=lambda f: -f[2]
        )

        reglas = ", ".join(
            f"{id_regla}->{termino} ({fuerza:.2f})"
            for id_regla, termino, fuerza in activas[:3]
        )

        x = traza["x_estrella"]

        x_texto = "-" if x is None else f"{x:.1f}"

        return f"x*={x_texto} {traza['accion']} | {reglas}"
