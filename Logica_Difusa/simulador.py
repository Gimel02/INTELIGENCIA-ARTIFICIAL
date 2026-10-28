# ==========================================
# SIMULADOR SIN VENTANA
#
# Juega partidas completas sin pygame para
# poder probar (y entrenar) las bases de
# conocimiento muchas veces y rápido.
#
# En cada partida juegan:
#   - el cazador (Agente 1) con su base,
#   - el jaguar (Agente 2) con su base,
#   - los ratones (Agente Tonto), siempre
#     con sus reglas fijas.
#
# Se juega por turnos: primero decide el
# cazador, luego el jaguar y luego se mueven
# los ratones. En la ventana se mueven con
# física y a velocidades un poco distintas,
# así que esto es una aproximación del juego.
#
# Cada partida usa una SEMILLA: con la misma
# semilla el mapa y el azar son iguales, así
# que la comparación entre bases es justa.
# ==========================================

import contextlib
import io
import random

from Mundo.mundo import MundoSelva
from Agente_Cazador.agente import AgenteCazador
from Agente_Jaguar.agente import AgenteJaguar
from Logica_Difusa.motor_mamdani import ControladorDifuso


MAX_TURNOS = 400

# Castigo por cada turno que el cazador se
# queda en la cabaña con la energía llena
# antes de cazar al jaguar (no tiene nada que
# recargar, solo se está escondiendo)

CASTIGO_ESCONDERSE = 0.5
ENERGIA_LLENA = 95

# Pasos de los ratones por turno (ellos se
# mueven de forma continua)

PASOS_RATON = 6
DT_RATON = 0.05


# ==========================================
# APTITUD DE UNA PARTIDA
# ==========================================

def aptitud_cazador(partida, max_turnos=MAX_TURNOS):

    # Cazar: +100, +50 si es rápido, +20 si
    # vuelve a la cabaña. Morir: -100.
    # Se acaba el tiempo: -10.
    # Esconderse en la cabaña con energía
    # llena: -0.5 por turno.

    castigo = CASTIGO_ESCONDERSE * partida["turnos_escondido"]

    if partida["turno_caza"] is not None:

        return (
            100
            + 50 * (1 - partida["turno_caza"] / max_turnos)
            + (20 if partida["final"] == "regresó" else 0)
            - castigo
        )

    if partida["final"] in ("atacado", "agotado"):

        return -100 - castigo

    return -10 - castigo


def aptitud_jaguar(partida, max_turnos=MAX_TURNOS):

    # Cazar al cazador: +100. Sobrevivir: +50.
    # Ser cazado: -100, pero entre más aguante,
    # menos castigo. Cada ratón comido: +5.

    ratones = 5 * partida["ratones_comidos"]

    if partida["final"] == "atacado":

        return 100 + ratones

    if partida["turno_caza"] is not None:

        return -100 + 50 * partida["turno_caza"] / max_turnos + ratones

    return 50 + ratones


# ==========================================
# UNA PARTIDA
# ==========================================

def _encuentro(mundo, cazador, jaguar):

    # Igual que en la interfaz: si coinciden y
    # el jaguar ataca, pierde el cazador; si no,
    # el cazador lo atrapa

    if mundo.jaguar_vivo and cazador.posicion == mundo.posicion_jaguar:

        if jaguar.atacando:

            cazador.recibir_ataque()

            jaguar.despues_de_atacar()

        else:

            cazador.atrapar_jaguar()


def _mover_ratones(mundo, jaguar):

    comidos = 0

    for raton in mundo.ratones:

        if not raton.vivo:

            continue

        for _ in range(PASOS_RATON):

            posicion_jaguar = mundo.posicion_jaguar if mundo.jaguar_vivo else None

            raton.actualizar(DT_RATON, posicion_jaguar)

            if posicion_jaguar is None:

                continue

            fila, columna = raton.posicion_visual()

            distancia = (
                (fila - posicion_jaguar[0]) ** 2
                + (columna - posicion_jaguar[1]) ** 2
            ) ** 0.5

            if distancia < 0.6:

                raton.vivo = False

                jaguar.comer_raton()

                comidos += 1

                break

    return comidos


def jugar_partida(base_cazador, base_jaguar, semilla, max_turnos=MAX_TURNOS):

    random.seed(semilla)

    with contextlib.redirect_stdout(io.StringIO()):

        mundo = MundoSelva()

        cazador = AgenteCazador(mundo, controlador=ControladorDifuso(base_cazador))

        jaguar = AgenteJaguar(mundo, controlador=ControladorDifuso(base_jaguar))

        turno_caza = None

        final = "tiempo"

        ratones_comidos = 0

        acciones = {}

        turnos_escondido = 0

        for turno in range(1, max_turnos + 1):

            cazador.tomar_decision(mundo.posicion_jaguar)

            if (
                turno_caza is None
                and cazador.posicion == mundo.campamento
                and cazador.energia >= ENERGIA_LLENA
            ):

                turnos_escondido += 1

            if cazador.decision_difusa:

                accion = cazador.decision_difusa["accion"]

                acciones[accion] = acciones.get(accion, 0) + 1

            _encuentro(mundo, cazador, jaguar)


            if mundo.jaguar_vivo:

                jaguar.tomar_decision(
                    cazador.posicion,
                    cazador.energia,
                    mundo.ratones
                )

                _encuentro(mundo, cazador, jaguar)

            ratones_comidos += _mover_ratones(mundo, jaguar)


            if not mundo.jaguar_vivo and turno_caza is None:

                turno_caza = turno


            if cazador.vidas <= 0:

                final = "atacado"

                break

            if cazador.energia <= 0 and cazador.posicion != mundo.campamento:

                final = "agotado"

                break

            if turno_caza is not None and cazador.posicion == mundo.campamento:

                final = "regresó"

                break

        else:

            if turno_caza is not None:

                final = "cazado"


    partida = {
        "semilla": semilla,
        "final": final,
        "turno_caza": turno_caza,
        "turnos": turno,
        "ratones_comidos": ratones_comidos,
        "turnos_escondido": turnos_escondido,
        "acciones": acciones,
    }

    partida["aptitud_cazador"] = aptitud_cazador(partida, max_turnos)

    partida["aptitud_jaguar"] = aptitud_jaguar(partida, max_turnos)

    return partida


# ==========================================
# VARIAS PARTIDAS
# ==========================================

def evaluar(base_cazador, base_jaguar, semillas, max_turnos=MAX_TURNOS):

    partidas = [
        jugar_partida(base_cazador, base_jaguar, semilla, max_turnos)
        for semilla in semillas
    ]

    total = len(partidas)

    def porcentaje(condicion):

        return 100 * sum(1 for p in partidas if condicion(p)) / total

    return {
        "partidas": partidas,
        "aptitud_cazador": sum(p["aptitud_cazador"] for p in partidas) / total,
        "aptitud_jaguar": sum(p["aptitud_jaguar"] for p in partidas) / total,
        "jaguar_cazado_pct": porcentaje(lambda p: p["turno_caza"] is not None),
        "cazador_atacado_pct": porcentaje(lambda p: p["final"] == "atacado"),
        "cazador_agotado_pct": porcentaje(lambda p: p["final"] == "agotado"),
        "tiempo_pct": porcentaje(lambda p: p["final"] == "tiempo"),
        "turnos_promedio": sum(p["turnos"] for p in partidas) / total,
        "ratones_promedio": sum(p["ratones_comidos"] for p in partidas) / total,
        "escondido_promedio": sum(p["turnos_escondido"] for p in partidas) / total,
    }
