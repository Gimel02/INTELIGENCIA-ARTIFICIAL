# ==========================================
# DIOS: ORQUESTADOR DE AGENTES
#
# Coordina a los agentes de la selva:
#
#   Agente 1     -> CAZADOR (control difuso)
#   Agente 2     -> JAGUAR  (control difuso)
#   Agente Tonto -> RATONES (reglas fijas, sin
#                   memoria y sin aprender)
#
# El cazador y el jaguar tienen cada uno su
# controlador difuso y su BASE DE CONOCIMIENTO
# (su memoria), que entrena el AG.
#
# DIOS:
#   - le pregunta a cada agente qué haría
#     (consultar),
#   - deja que el AG cambie sus reglas
#     (actualizar_base / ajustar_regla),
#   - elige qué reglas se usan en la ventana:
#     las entrenadas o las del equipo (tecla D),
#   - compara reglas sin ventana (comparar).
# ==========================================

import os

from Logica_Difusa.base_conocimiento import (
    BaseConocimiento,
    base_equipo,
    ruta_base
)

from Logica_Difusa.motor_mamdani import ControladorDifuso


# Agente -> tipo de agente

AGENTES_DIFUSOS = {
    "Agente 1": "cazador",
    "Agente 2": "jaguar",
}

AGENTE_TONTO = "ratones"


# Juegos de reglas que se pueden usar

MODOS = ["entrenadas", "equipo"]

MODO_INICIAL = "equipo"


def archivo_base(agente, modo):

    return f"{agente}_{modo}.json"


def cargar_base(agente, modo):

    archivo = archivo_base(agente, modo)

    if os.path.exists(ruta_base(archivo)):

        return BaseConocimiento.cargar(archivo)


    base = base_equipo(agente)

    if modo == "equipo":

        base.guardar(archivo)

    else:

        # Todavía no se entrena: usa las
        # reglas del equipo

        base.nombre = f"{agente.capitalize()}: sin entrenar (reglas del equipo)"

        print(
            f"[DIOS] El {agente} aún no está entrenado. Ejecuta: "
            f"python3 -m Logica_Difusa.entrenamiento_genetico {agente}"
        )

    return base


# ==========================================
# AGENTE TONTO: los ratones
#
# No tienen lógica difusa ni base de
# conocimiento. Siguen siempre las mismas
# reglas fijas (Agente_Raton/agente.py).
# ==========================================

REGLAS_TONTO = [
    "Si el jaguar está a 3 casillas o menos: huir en línea recta por el eje que más los separa.",
    "Si no ve al jaguar: caminar en una dirección al azar y cambiarla cada 0.8 a 2 segundos.",
    "Si choca con un árbol o un borde: elegir otra dirección libre, sin regresarse si puede.",
]


class Dios:

    def __init__(self, modo=MODO_INICIAL):

        self.modo = modo

        self.agentes = {
            nombre: ControladorDifuso(cargar_base(agente, modo))
            for nombre, agente in AGENTES_DIFUSOS.items()
        }


    # --------------------------------------
    # CONSULTAR LA DECISIÓN DE UN AGENTE
    # --------------------------------------

    def consultar(self, nombre, entradas):

        return self.agentes[nombre].decidir(entradas)


    def controlador(self, agente):

        # agente: "cazador" o "jaguar"

        for nombre, tipo in AGENTES_DIFUSOS.items():

            if tipo == agente:

                return self.agentes[nombre]

        raise KeyError(agente)


    def decision_tonto(self, raton):

        # El Agente Tonto no razona: su estado
        # sale de sus reglas fijas

        return raton.estado


    # --------------------------------------
    # PUNTO DE CONEXIÓN CON EL AG
    # --------------------------------------

    def actualizar_base(self, nombre, base, guardar=True):

        # El AG entrega una base nueva (o
        # mejorada) y DIOS se la da al agente

        self.agentes[nombre].cambiar_base(base)

        if guardar:

            base.guardar(archivo_base(AGENTES_DIFUSOS[nombre], "entrenadas"))


    def ajustar_regla(self, nombre, id_regla, termino):

        # Cambiar solo una regla

        self.agentes[nombre].base.reemplazar_consecuente(
            id_regla,
            termino
        )


    # --------------------------------------
    # REGLAS QUE SE USAN EN LA VENTANA
    # --------------------------------------

    def cambiar_modo(self):

        self.modo = MODOS[(MODOS.index(self.modo) + 1) % len(MODOS)]

        for nombre, agente in AGENTES_DIFUSOS.items():

            self.agentes[nombre].cambiar_base(cargar_base(agente, self.modo))

        return self.modo


    def descripcion(self):

        return " | ".join(
            controlador.base.nombre for controlador in self.agentes.values()
        )


    # --------------------------------------
    # COMPARAR REGLAS (sin ventana)
    # --------------------------------------

    def comparar(self, semillas, max_turnos=400):

        from Logica_Difusa.simulador import evaluar

        resultados = {}

        for modo in MODOS:

            resultados[modo] = evaluar(
                cargar_base("cazador", modo),
                cargar_base("jaguar", modo),
                semillas,
                max_turnos=max_turnos
            )

        return resultados


# Un solo DIOS para todo el programa

_dios = None


def obtener_dios():

    global _dios

    if _dios is None:

        _dios = Dios()

    return _dios


def controlador_por_defecto(agente):

    return obtener_dios().controlador(agente)
