# ==========================================
# DIOS: ORQUESTADOR DE AGENTES
#
# Coordina:
#   Agente 1 -> CAZADOR (control difuso)
#   Agente 2 -> JAGUAR  (control difuso)
#   Ratones  -> reglas fijas
#
# Las reglas difusas del cazador y del jaguar
# son las reglas diseñadas por el equipo.
#
# El algoritmo genético se utiliza únicamente
# para optimizar el MOVIMIENTO del cazador.
# ==========================================

from Logica_Difusa.base_conocimiento import base_equipo
from Logica_Difusa.motor_mamdani import ControladorDifuso


AGENTES_DIFUSOS = {
    "Agente 1": "cazador",
    "Agente 2": "jaguar",
}

AGENTE_TONTO = "ratones"


REGLAS_TONTO = [
    "Si el jaguar está a 3 casillas o menos: huir en línea recta por el eje que más los separa.",
    "Si no ve al jaguar: caminar en una dirección al azar y cambiarla cada 0.8 a 2 segundos.",
    "Si choca con un árbol o un borde: elegir otra dirección libre, sin regresarse si puede.",
]


class Dios:

    def __init__(self):

        # Se conserva para mostrarlo en la interfaz.
        self.modo = "equipo"

        self.agentes = {
            nombre: ControladorDifuso(
                base_equipo(agente)
            )
            for nombre, agente
            in AGENTES_DIFUSOS.items()
        }


    def consultar(
        self,
        nombre,
        entradas
    ):

        return self.agentes[
            nombre
        ].decidir(
            entradas
        )


    def controlador(
        self,
        agente
    ):

        for nombre, tipo in (
            AGENTES_DIFUSOS.items()
        ):

            if tipo == agente:

                return self.agentes[
                    nombre
                ]

        raise KeyError(
            agente
        )


    def decision_tonto(
        self,
        raton
    ):

        return raton.estado


    def descripcion(self):

        return " | ".join(
            controlador.base.nombre
            for controlador
            in self.agentes.values()
        )


# ==========================================
# UNA SOLA INSTANCIA DE DIOS
# ==========================================

_dios = None


def obtener_dios():

    global _dios

    if _dios is None:

        _dios = Dios()

    return _dios


def controlador_por_defecto(
    agente
):

    return obtener_dios().controlador(
        agente
    )