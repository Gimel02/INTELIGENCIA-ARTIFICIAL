# ==========================================
# ENTRENAMIENTO GENÉTICO DE LAS REGLAS
#
# El AG crea y mejora la base de conocimiento
# del cazador (Agente 1) o del jaguar
# (Agente 2).
#
# - Cromosoma: un gen por regla (23 para el
#   cazador, 11 para el jaguar). Cada gen es
#   el CONSECUENTE de su regla, como número:
#     cazador: 0 huir, 1 recargar, 2 explorar,
#              3 perseguir, 4 atacar
#     jaguar:  0 huir, 1 merodear,
#              2 cazar_raton, 3 atacar
#   Los antecedentes son fijos (ver
#   Perfil.plantillas en base_conocimiento.py).
#
# - Aptitud: promedio de puntos al jugar en
#   varios mapas contra las reglas actuales
#   del otro agente (ver simulador.py).
#
# - Operadores (los mismos del AG del
#   movimiento): elitismo (2), torneo de 3,
#   cruce de un punto (70 %) y mutación por gen.
#
# Uso:
#   python3 -m Logica_Difusa.entrenamiento_genetico cazador
#   python3 -m Logica_Difusa.entrenamiento_genetico jaguar
#   python3 -m Logica_Difusa.entrenamiento_genetico jaguar 16 12 30
#                        (agente, población, generaciones, mapas)
#
# Lo recomendable es entrenar primero al
# jaguar y después al cazador (contra el
# jaguar ya entrenado).
# ==========================================

import json
import random
import sys
import time

from Logica_Difusa.base_conocimiento import (
    BaseConocimiento,
    PERFILES,
    base_equipo,
    ruta_base
)

from Logica_Difusa.dios import cargar_base, archivo_base
from Logica_Difusa.simulador import evaluar, MAX_TURNOS


TAMANO_POBLACION = 16
GENERACIONES = 12
MAPAS_ENTRENAMIENTO = 30          # semillas 0, 1, ..., 29
CANTIDAD_ELITE = 2
TAMANO_TORNEO = 3
PROPORCION_CRUCE = 0.7
PROBABILIDAD_MUTACION = 0.08
SEMILLA_AG = 2026


# ==========================================
# OPERADORES
# ==========================================

def cromosoma_aleatorio(perfil, generador):

    valores = len(perfil.terminos_salida)

    return [generador.randrange(valores) for _ in range(perfil.numero_reglas)]


def mutar(cromosoma, perfil, generador, probabilidad=PROBABILIDAD_MUTACION):

    valores = len(perfil.terminos_salida)

    hijo = list(cromosoma)

    for i in range(len(hijo)):

        if generador.random() < probabilidad:

            # Siempre cambia a OTRA acción

            opciones = [v for v in range(valores) if v != hijo[i]]

            hijo[i] = generador.choice(opciones)

    return hijo


def cruzar(padre, madre, generador):

    if generador.random() >= PROPORCION_CRUCE:

        return list(padre), list(madre)

    corte = generador.randrange(1, len(padre))

    return (
        padre[:corte] + madre[corte:],
        madre[:corte] + padre[corte:],
    )


def torneo(poblacion_evaluada, generador):

    competidores = generador.sample(poblacion_evaluada, TAMANO_TORNEO)

    return max(competidores, key=lambda par: par[1])[0]


# ==========================================
# APTITUD (con memoria para no repetir)
# ==========================================

class Evaluador:

    def __init__(self, agente, rival, semillas):

        self.agente = agente

        self.perfil = PERFILES[agente]

        # Base del otro agente (fija mientras
        # se entrena este)

        self.rival = rival

        self.semillas = list(semillas)

        self.cache = {}


    def __call__(self, cromosoma):

        clave = tuple(cromosoma)

        if clave not in self.cache:

            base = BaseConocimiento.desde_cromosoma(self.perfil, cromosoma)

            if self.agente == "cazador":

                resultado = evaluar(base, self.rival, self.semillas)

            else:

                resultado = evaluar(self.rival, base, self.semillas)

            self.cache[clave] = resultado[f"aptitud_{self.agente}"]

        return self.cache[clave]


# ==========================================
# CICLO DEL AG
# ==========================================

def entrenar(
    agente,
    tamano_poblacion=TAMANO_POBLACION,
    generaciones=GENERACIONES,
    mapas=MAPAS_ENTRENAMIENTO,
    semilla=SEMILLA_AG,
    mostrar=True
):

    perfil = PERFILES[agente]

    rival_tipo = "jaguar" if agente == "cazador" else "cazador"

    rival = cargar_base(rival_tipo, "entrenadas")

    if mostrar:

        print(f"Entrenando al {agente} contra: {rival.nombre}")

    generador = random.Random(semilla)

    evaluar_cromosoma = Evaluador(agente, rival, range(mapas))


    # Población inicial: las reglas del equipo
    # (semilla), algunas variaciones de ellas y
    # el resto al azar

    semilla_equipo = base_equipo(agente).a_cromosoma()

    poblacion = [semilla_equipo]

    while len(poblacion) < tamano_poblacion // 2:

        poblacion.append(mutar(semilla_equipo, perfil, generador, 0.2))

    while len(poblacion) < tamano_poblacion:

        poblacion.append(cromosoma_aleatorio(perfil, generador))


    historial = []

    inicio = time.time()

    for generacion in range(1, generaciones + 1):

        evaluada = sorted(
            ((c, evaluar_cromosoma(c)) for c in poblacion),
            key=lambda par: par[1],
            reverse=True
        )

        mejor, mejor_aptitud = evaluada[0]

        promedio = sum(a for _, a in evaluada) / len(evaluada)

        historial.append({
            "generacion": generacion,
            "mejor": round(mejor_aptitud, 2),
            "promedio": round(promedio, 2),
            "peor": round(evaluada[-1][1], 2),
        })

        if mostrar:

            print(
                f"Generación {generacion:2d} | mejor {mejor_aptitud:7.2f} "
                f"| promedio {promedio:7.2f} | {time.time() - inicio:5.0f} s",
                flush=True
            )


        if generacion == generaciones:

            break


        # Nueva generación: élite + hijos

        nueva = [c for c, _ in evaluada[:CANTIDAD_ELITE]]

        while len(nueva) < tamano_poblacion:

            padre = torneo(evaluada, generador)

            madre = torneo(evaluada, generador)

            hijo1, hijo2 = cruzar(padre, madre, generador)

            nueva.append(mutar(hijo1, perfil, generador))

            if len(nueva) < tamano_poblacion:

                nueva.append(mutar(hijo2, perfil, generador))

        poblacion = nueva


    base = BaseConocimiento.desde_cromosoma(
        perfil,
        mejor,
        nombre=f"{agente.capitalize()}: reglas entrenadas con AG",
        origen="AG",
        aptitud=round(mejor_aptitud, 2)
    )

    base.descripcion = (
        f"Entrenada con un AG: población {tamano_poblacion}, "
        f"{generaciones} generaciones, {mapas} mapas "
        f"(semillas 0-{mapas - 1}), semilla del AG {semilla}, "
        f"contra '{rival.nombre}'. "
        f"Aptitud de las reglas del equipo en la generación 1: "
        f"{evaluar_cromosoma(semilla_equipo):.2f}."
    )

    return base, historial


if __name__ == "__main__":

    agente = sys.argv[1] if len(sys.argv) > 1 else "cazador"

    if agente not in PERFILES:

        sys.exit("El agente debe ser 'cazador' o 'jaguar'")

    numeros = [int(a) for a in sys.argv[2:]]

    poblacion = numeros[0] if len(numeros) > 0 else TAMANO_POBLACION

    generaciones = numeros[1] if len(numeros) > 1 else GENERACIONES

    mapas = numeros[2] if len(numeros) > 2 else MAPAS_ENTRENAMIENTO

    base, historial = entrenar(agente, poblacion, generaciones, mapas)

    ruta = base.guardar(archivo_base(agente, "entrenadas"))

    with open(ruta_base(f"historial_{agente}.json"), "w", encoding="utf-8") as f:

        json.dump(historial, f, indent=2)

    base.imprimir()

    print(f"\nBase guardada en {ruta}")
