# ==========================================
# ESCENARIOS DE DEMOSTRACIÓN
#
# Sirven para la exposición: en lugar de
# depender de la suerte del mapa, cada
# escenario usa siempre el mismo mapa (por su
# semilla) y coloca al jaguar a cierta
# distancia del campamento, con cierta
# hambre.
#
#   Tecla 1 -> Demo caza
#   Tecla 2 -> Demo peligro
#   Tecla R -> mapa al azar
#
# Los mapas se escogieron probando muchas
# semillas en el simulador sin ventana y
# quedándonos con las que muestran mejor
# cada comportamiento (con el método de
# defuzzificación por altura máxima, que es
# el que está por defecto):
#
#   Demo caza: en 29 de 30 partidas el
#   cazador explora, detecta, persigue,
#   ataca, caza al jaguar y regresa. Si
#   falla (casi siempre porque el jaguar
#   acorralado contraataca), se presiona 1
#   otra vez.
#
#   Demo peligro: en todas las pruebas el
#   cazador empieza recargando y huyendo.
#
# En la ventana el azar no se fija, así que
# cada vez que se presiona la tecla la
# partida es un poco distinta.
# ==========================================

import random

from Algoritmos.a_Estrella import AEstrella


class Escenario:

    def __init__(
        self,
        nombre,
        descripcion,
        semilla,
        distancia_jaguar,
        hambre_jaguar,
        energia_cazador=100,
        aumento_hambre=None
    ):

        self.nombre = nombre
        self.descripcion = descripcion
        self.semilla = semilla
        self.distancia_jaguar = distancia_jaguar
        self.hambre_jaguar = hambre_jaguar
        self.energia_cazador = energia_cazador

        # Cuánto sube el hambre del jaguar por
        # turno (None = lo normal del jaguar)
        self.aumento_hambre = aumento_hambre


ESCENARIOS = {

    1: Escenario(
        "Demo caza",
        "explorar -> detectar -> perseguir -> atacar -> cazar -> regresar",
        semilla=114,
        distancia_jaguar=6,
        hambre_jaguar=0,
        aumento_hambre=1,
    ),

    2: Escenario(
        "Demo peligro",
        "jaguar hambriento y cerca -> el cazador huye o recarga",
        semilla=31,
        distancia_jaguar=3,
        hambre_jaguar=85,
        energia_cazador=60,
    ),
}


def crear_mundo(escenario):

    # El mismo mapa cada vez

    from Mundo.mundo import MundoSelva

    random.seed(escenario.semilla)

    return MundoSelva()


def casilla_para_jaguar(escenario, mundo):

    # Una casilla libre (sin árbol ni arena) a la
    # distancia pedida del campamento y con
    # camino desde él. Siempre la misma para la
    # misma semilla.

    campamento = mundo.campamento

    candidatas = []

    for fila in range(mundo.filas):

        for columna in range(mundo.columnas):

            casilla = (fila, columna)

            if casilla == campamento:
                continue

            if not mundo.es_transitable(casilla):
                continue

            if mundo.grid.get(casilla, 0) == 4:
                continue

            distancia = AEstrella.heuristica(campamento, casilla)

            if distancia != escenario.distancia_jaguar:
                continue

            if not AEstrella.buscar(campamento, casilla, mundo):
                continue

            candidatas.append(casilla)

    if not candidatas:

        return None

    return random.Random(escenario.semilla).choice(sorted(candidatas))


def aplicar(escenario, mundo, cazador, jaguar, fijar_azar=True):

    casilla = casilla_para_jaguar(escenario, mundo)

    if casilla is not None:

        mundo.mover_jaguar(casilla)

        mundo.inicio_jaguar = casilla

    jaguar.hambre = escenario.hambre_jaguar

    jaguar.actualizar_nivel_hambre()

    if escenario.aumento_hambre is not None:

        jaguar.aumento_hambre = escenario.aumento_hambre

    cazador.energia = escenario.energia_cazador

    # En el simulador, desde aquí el azar
    # también es siempre el mismo

    if fijar_azar:

        random.seed(escenario.semilla + 1000)

    return casilla
