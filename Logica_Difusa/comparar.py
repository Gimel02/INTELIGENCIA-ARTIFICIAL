# ==========================================
# COMPARAR BASES DE CONOCIMIENTO
#
#   python3 -m Logica_Difusa.comparar
#   python3 -m Logica_Difusa.comparar 60
#
# Juega cada combinación de reglas del
# cazador contra cada combinación de reglas
# del jaguar en mapas que el AG NUNCA vio
# (semillas 1000 en adelante).
#
#   entrenadas -> reglas del AG
#   equipo     -> reglas escritas por nosotros
#   aleatorio  -> reglas al azar (control)
# ==========================================

import sys
import time

from Logica_Difusa.base_conocimiento import base_aleatoria
from Logica_Difusa.dios import cargar_base
from Logica_Difusa.simulador import evaluar


TIPOS = ["entrenadas", "equipo", "aleatorio"]

SEMILLA_INICIAL = 1000


def obtener(agente, tipo):

    if tipo == "aleatorio":

        return base_aleatoria(agente)

    return cargar_base(agente, tipo)


def comparar(cantidad=60):

    semillas = range(SEMILLA_INICIAL, SEMILLA_INICIAL + cantidad)

    filas = []

    for tipo_cazador in TIPOS:

        for tipo_jaguar in TIPOS:

            r = evaluar(
                obtener("cazador", tipo_cazador),
                obtener("jaguar", tipo_jaguar),
                semillas
            )

            filas.append((tipo_cazador, tipo_jaguar, r))

    return filas


if __name__ == "__main__":

    cantidad = int(sys.argv[1]) if len(sys.argv) > 1 else 60

    inicio = time.time()

    filas = comparar(cantidad)

    print(f"\nComparación en {cantidad} mapas nuevos (semillas {SEMILLA_INICIAL} en adelante)\n")

    print(
        "Cazador".ljust(12) + "Jaguar".ljust(12)
        + "Jaguar cazado".rjust(14) + "Cazador muerto".rjust(16)
        + "Tiempo".rjust(8) + "Turnos".rjust(8) + "Ratones".rjust(9)
        + "Apt. cazador".rjust(14) + "Apt. jaguar".rjust(13)
    )

    for tipo_cazador, tipo_jaguar, r in filas:

        muertos = r["cazador_atacado_pct"] + r["cazador_agotado_pct"]

        print(
            tipo_cazador.ljust(12) + tipo_jaguar.ljust(12)
            + f"{r['jaguar_cazado_pct']:13.0f}%"
            + f"{muertos:15.0f}%"
            + f"{r['tiempo_pct']:7.0f}%"
            + f"{r['turnos_promedio']:8.1f}"
            + f"{r['ratones_promedio']:9.1f}"
            + f"{r['aptitud_cazador']:14.1f}"
            + f"{r['aptitud_jaguar']:13.1f}"
        )

    print(f"\n({time.time() - inicio:.0f} s)")
