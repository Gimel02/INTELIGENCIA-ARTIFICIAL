# ==========================================
# BASE DE CONOCIMIENTO (CONTROL RULE BASE)
#
# Es la memoria del agente: la lista de
# reglas IF-THEN que usa para decidir.
#
# Cada regla tiene:
#   - antecedente (la condición, parte SI)
#   - consecuente (la acción, parte ENTONCES)
#
# Las reglas SOLO tienen la parte verdadera:
# no llevan ELSE. Si la condición no se
# cumple, la regla simplemente pesa 0.
#
# El antecedente se guarda como un árbol:
#   {"var": "reserva", "es": "baja"}
#   {"y":  [cond1, cond2, ...]}   -> AND (min)
#   {"o":  [cond1, cond2, ...]}   -> OR  (max)
#   {"no": cond}                  -> NOT (1 - x)
#
# Las reglas se guardan en archivos JSON
# dentro de Logica_Difusa/bases/.
# ==========================================

import json
import os

from Logica_Difusa.variables import (
    ENTRADAS_CAZADOR,
    ENTRADAS_JAGUAR,
    ACCION,
    ACCION_JAGUAR
)


CARPETA_BASES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "bases"
)


def _condicion(variable, termino):

    return {"var": variable, "es": termino}


# ==========================================
# PERFIL DIFUSO
#
# Lo que tiene cada agente: sus entradas, su
# salida y la forma de sus reglas.
#
# Las reglas siguen siempre la misma forma:
#
#  1. Una MATRIZ fila × columna. Cada celda es
#     una regla:
#       SI fila ES a Y columna ES b
#          Y NO (excepcion ES c)
#       ENTONCES salida ES <celda>
#
#  2. Unas reglas EXTRA para cuando sí se
#     cumple la excepción.
#
# Los antecedentes de las reglas son fijos.
# Los consecuentes se definen mediante la
# base de conocimiento diseñada por el equipo.
# ==========================================

class Perfil:

    def __init__(self, nombre, entradas, salida, fila, columna, excepcion, extras):

        self.nombre = nombre

        self.entradas = entradas

        self.salida = salida

        # (variable, [términos])

        self.fila = fila

        self.columna = columna

        # (variable, término)

        self.excepcion = excepcion

        # Antecedentes de las reglas extra

        self.extras = extras

        self.terminos_salida = list(salida.terminos)


    def plantillas(self):

        variable_fila, terminos_fila = self.fila

        variable_columna, terminos_columna = self.columna

        variable_excepcion, termino_excepcion = self.excepcion

        antecedentes = []

        for a in terminos_fila:

            for b in terminos_columna:

                antecedentes.append({
                    "y": [
                        _condicion(variable_fila, a),
                        _condicion(variable_columna, b),
                        {"no": _condicion(variable_excepcion, termino_excepcion)},
                    ]
                })

        return antecedentes + [dict(extra) for extra in self.extras]


    @property
    def numero_reglas(self):

        return len(self.fila[1]) * len(self.columna[1]) + len(self.extras)


    @property
    def reglas_matriz(self):

        return len(self.fila[1]) * len(self.columna[1])


def _excepcion_y(variable, termino, *condiciones):

    return {"y": [_condicion(variable, termino), *condiciones]}


def _o(variable, *terminos):

    return {"o": [_condicion(variable, t) for t in terminos]}


# ------------------------------------------
# AGENTE 1: CAZADOR (23 reglas)
#   R01-R20: reserva × distancia, jaguar NO agresivo
#   R21-R23: el jaguar está agresivo
# ------------------------------------------

PERFIL_CAZADOR = Perfil(
    "cazador",
    ENTRADAS_CAZADOR,
    ACCION,
    fila=("reserva", ["muy_baja", "baja", "media", "alta"]),
    columna=("distancia", ["muy_cerca", "cerca", "media", "lejos", "muy_lejos"]),
    excepcion=("peligro", "agresivo"),
    extras=[
        _excepcion_y("peligro", "agresivo", _o("distancia", "muy_cerca", "cerca")),
        _excepcion_y("peligro", "agresivo", _condicion("distancia", "media")),
        _excepcion_y("peligro", "agresivo", _o("distancia", "lejos", "muy_lejos")),
    ]
)


# ------------------------------------------
# AGENTE 2: JAGUAR (11 reglas)
#   R01-R09: hambre × distancia, cazador NO débil
#   R10-R11: el cazador está débil
# ------------------------------------------

PERFIL_JAGUAR = Perfil(
    "jaguar",
    ENTRADAS_JAGUAR,
    ACCION_JAGUAR,
    fila=("hambre", ["saciado", "hambriento", "voraz"]),
    columna=("distancia_cazador", ["cerca", "media", "lejos"]),
    excepcion=("energia_cazador", "debil"),
    extras=[
        _excepcion_y("energia_cazador", "debil", _o("distancia_cazador", "cerca", "media")),
        _excepcion_y("energia_cazador", "debil", _condicion("distancia_cazador", "lejos")),
    ]
)


PERFILES = {
    "cazador": PERFIL_CAZADOR,
    "jaguar": PERFIL_JAGUAR,
}


# ==========================================
# TEXTO DE UNA REGLA (para el reporte y la
# bitácora)
# ==========================================

def texto_antecedente(nodo):

    if "var" in nodo:

        return f"{nodo['var']} ES {nodo['es']}"

    if "no" in nodo:

        return f"NO ({texto_antecedente(nodo['no'])})"

    if "y" in nodo:

        return " Y ".join(
            texto_antecedente(hijo) for hijo in nodo["y"]
        )

    if "o" in nodo:

        return "(" + " O ".join(
            texto_antecedente(hijo) for hijo in nodo["o"]
        ) + ")"

    raise ValueError(f"Nodo de antecedente desconocido: {nodo}")


def texto_regla(regla):

    return (
        f"{regla['id']}: SI {texto_antecedente(regla['si'])} "
        f"ENTONCES {regla['entonces'][0]} ES {regla['entonces'][1]}"
    )


# ==========================================
# BASE DE CONOCIMIENTO
# ==========================================

class BaseConocimiento:

    def __init__(self, perfil, nombre, reglas, origen="", descripcion="", aptitud=None):

        if isinstance(perfil, str):

            perfil = PERFILES[perfil]

        self.perfil = perfil

        self.nombre = nombre

        self.reglas = reglas

        self.origen = origen

        self.descripcion = descripcion

        # Calificación que le dio el AG (si la
        # entrenó el AG)

        self.aptitud = aptitud

        self.validar()


    # --------------------------------------
    # Revisa que cada regla use variables y
    # términos que sí existen
    # --------------------------------------

    def validar(self):

        entradas = self.perfil.entradas

        salida = self.perfil.salida

        def revisar(nodo):

            if "var" in nodo:

                variable = entradas.get(nodo["var"])

                if variable is None or nodo["es"] not in variable.terminos:

                    raise ValueError(f"Condición inválida: {nodo}")

            elif "no" in nodo:

                revisar(nodo["no"])

            else:

                for hijo in nodo.get("y", nodo.get("o", [])):

                    revisar(hijo)


        for regla in self.reglas:

            revisar(regla["si"])

            variable, termino = regla["entonces"]

            if variable != salida.nombre or termino not in salida.terminos:

                raise ValueError(f"Consecuente inválido: {regla}")


    # --------------------------------------
    # CROMOSOMA <-> REGLAS
    #
    # Punto de conexión con el AG: cada gen es
    # el consecuente de una regla, guardado
    # como número (posición del término de
    # salida: 0 = huir, ...).
    # --------------------------------------

    def a_cromosoma(self):

        return [
            self.perfil.terminos_salida.index(regla["entonces"][1])
            for regla in self.reglas
        ]


    @classmethod
    def desde_cromosoma(cls, perfil, cromosoma, nombre="Base de conocimiento", origen="equipo", aptitud=None):

        if isinstance(perfil, str):

            perfil = PERFILES[perfil]

        antecedentes = perfil.plantillas()

        if len(cromosoma) != len(antecedentes):

            raise ValueError(
                f"El cromosoma debe tener {len(antecedentes)} genes"
            )

        reglas = [
            {
                "id": f"R{numero:02d}",
                "si": antecedente,
                "entonces": [perfil.salida.nombre, perfil.terminos_salida[gen]],
            }
            for numero, (antecedente, gen) in enumerate(
                zip(antecedentes, cromosoma), start=1
            )
        ]

        return cls(perfil, nombre, reglas, origen=origen, aptitud=aptitud)


    def reemplazar_consecuente(self, id_regla, termino):

        # El AG (o una persona) puede cambiar la
        # acción de una sola regla

        if termino not in self.perfil.salida.terminos:

            raise ValueError(f"Término de salida inválido: {termino}")

        for regla in self.reglas:

            if regla["id"] == id_regla:

                regla["entonces"] = [self.perfil.salida.nombre, termino]

                return

        raise KeyError(f"No existe la regla {id_regla}")


    # --------------------------------------
    # MATRIZ fila × columna
    # --------------------------------------

    def matriz(self):

        filas = self.perfil.fila[1]

        columnas = self.perfil.columna[1]

        acciones = [
            regla["entonces"][1]
            for regla in self.reglas[:self.perfil.reglas_matriz]
        ]

        return {
            fila: dict(zip(columnas, acciones[i * len(columnas):(i + 1) * len(columnas)]))
            for i, fila in enumerate(filas)
        }


    def imprimir(self):

        print(f"\n=== {self.nombre} ({self.origen}) ===")

        if self.aptitud is not None:

            print(f"Aptitud en el entrenamiento: {self.aptitud:.2f}")

        columnas = self.perfil.columna[1]

        encabezado = f"{self.perfil.fila[0]} \\ {self.perfil.columna[0]}"

        print(encabezado.ljust(30) + "".join(c.ljust(12) for c in columnas))

        for fila, celdas in self.matriz().items():

            print(fila.ljust(30) + "".join(celdas[c].ljust(12) for c in columnas))

        print(f"Si {self.perfil.excepcion[0]} ES {self.perfil.excepcion[1]}:")

        for regla in self.reglas[self.perfil.reglas_matriz:]:

            print("  " + texto_regla(regla))


    # --------------------------------------
    # GUARDAR Y CARGAR (JSON)
    # --------------------------------------

    def a_diccionario(self):

        return {
            "agente": self.perfil.nombre,
            "nombre": self.nombre,
            "origen": self.origen,
            "descripcion": self.descripcion,
            "aptitud": self.aptitud,
            "reglas": self.reglas,
        }


    def guardar(self, archivo):

        ruta = ruta_base(archivo)

        os.makedirs(os.path.dirname(ruta), exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:

            json.dump(self.a_diccionario(), f, ensure_ascii=False, indent=2)

        return ruta


    @classmethod
    def cargar(cls, archivo):

        with open(ruta_base(archivo), encoding="utf-8") as f:

            datos = json.load(f)

        return cls(
            datos["agente"],
            datos["nombre"],
            datos["reglas"],
            origen=datos.get("origen", ""),
            descripcion=datos.get("descripcion", ""),
            aptitud=datos.get("aptitud"),
        )


def ruta_base(archivo):

    if os.path.isabs(archivo):

        return archivo

    return os.path.join(CARPETA_BASES, archivo)


# ==========================================
# BASE DE CONOCIMIENTO
#
# Reglas IF-THEN diseñadas por el equipo
# para controlar el comportamiento difuso
# del cazador y del jaguar.
# ==========================================

# CAZADOR. Filas: reserva. Columnas: distancia
# (muy_cerca, cerca, media, lejos, muy_lejos)

MATRIZ_CAZADOR = [
    # muy_baja: sin energía, siempre recargar
    ["recargar", "recargar", "recargar", "recargar", "recargar"],
    # baja: solo ataca si lo tiene encima
    ["atacar", "perseguir", "recargar", "recargar", "recargar"],
    # media
    ["atacar", "perseguir", "perseguir", "explorar", "explorar"],
    # alta
    ["atacar", "atacar", "perseguir", "perseguir", "explorar"],
]

# Jaguar agresivo: cerca, media, lejos

EXTRAS_CAZADOR = ["huir", "recargar", "explorar"]


# JAGUAR. Filas: hambre. Columnas: distancia
# al cazador (cerca, media, lejos). Imitan las
# reglas que ya tenía el jaguar.

MATRIZ_JAGUAR = [
    # saciado: huye si lo ven, si no merodea
    ["huir", "merodear", "merodear"],
    # hambriento: huye, pero busca ratones
    ["huir", "cazar_raton", "cazar_raton"],
    # voraz: ataca si lo tiene a su alcance
    ["atacar", "atacar", "cazar_raton"],
]

# Cazador débil: cerca o media, lejos

EXTRAS_JAGUAR = ["atacar", "merodear"]


def base_equipo(agente):

    perfil = PERFILES[agente]

    if agente == "cazador":

        acciones = [a for fila in MATRIZ_CAZADOR for a in fila] + EXTRAS_CAZADOR

    else:

        acciones = [a for fila in MATRIZ_JAGUAR for a in fila] + EXTRAS_JAGUAR

    cromosoma = [perfil.terminos_salida.index(a) for a in acciones]

    base = BaseConocimiento.desde_cromosoma(
        perfil,
        cromosoma,
        nombre=f"{agente.capitalize()}: reglas del equipo",
        origen="equipo"
    )

    base.descripcion = (
    "Base de conocimiento formada por reglas IF-THEN "
    "diseñadas por el equipo."
)

    return base
