import random
from Mundo.mundo import MundoSelva

# ==========================================
# ALGORITMO GENÉTICO
# ==========================================


# Acciones posibles del agente
ACCIONES = [
    "ARRIBA",
    "ABAJO",
    "IZQUIERDA",
    "DERECHA"
]


# Representación visual de cada acción
SIMBOLOS = {
    "ARRIBA": "^",
    "ABAJO": "v",
    "IZQUIERDA": "<",
    "DERECHA": ">"
}

DESPLAZAMIENTOS = {
    "ARRIBA": (-1, 0),
    "ABAJO": (1, 0),
    "IZQUIERDA": (0, -1),
    "DERECHA": (0, 1)
}


# ==========================================
# GENERAR UN CROMOSOMA
# ==========================================

def generar_cromosoma(longitud=8):

    cromosoma = []

    for _ in range(longitud):

        accion = random.choice(
            ACCIONES
        )

        cromosoma.append(
            accion
        )

    return cromosoma


# ==========================================
# GENERAR UNA POBLACIÓN
# ==========================================

def generar_poblacion(
    cantidad=10,
    longitud_cromosoma=8
):

    poblacion = []

    for _ in range(cantidad):

        cromosoma = generar_cromosoma(
            longitud_cromosoma
        )

        poblacion.append(
            cromosoma
        )

    return poblacion

def calcular_aptitud(
    distancia_objetivo,
    numero_colisiones,
    peso_colision=0.2
):

    aptitud = (
        1 / (distancia_objetivo + 1)
        -
        (numero_colisiones * peso_colision)
    )

    return aptitud

# ==========================================
# SIMULAR UN CROMOSOMA
# ==========================================

def simular_cromosoma(
    mundo,
    posicion_inicial,
    posicion_objetivo,
    cromosoma,
    peso_colision=0.2
):

    posicion_actual = posicion_inicial

    colisiones = 0


    for accion in cromosoma:

        fila, columna = posicion_actual

        cambio_fila, cambio_columna = (
            DESPLAZAMIENTOS[accion]
        )

        nueva_posicion = (
            fila + cambio_fila,
            columna + cambio_columna
        )


        # Si la casilla es transitable,
        # el agente puede avanzar.

        if mundo.es_transitable(
            nueva_posicion
        ):

            posicion_actual = (
                nueva_posicion
            )


        # Si intenta atravesar un árbol
        # o salir del mapa, cuenta colisión.

        else:

            colisiones += 1


    # ======================================
    # DISTANCIA MANHATTAN AL OBJETIVO
    # ======================================

    fila_actual, columna_actual = (
        posicion_actual
    )

    fila_objetivo, columna_objetivo = (
        posicion_objetivo
    )

    distancia = (
        abs(
            fila_actual
            -
            fila_objetivo
        )
        +
        abs(
            columna_actual
            -
            columna_objetivo
        )
    )


    aptitud = calcular_aptitud(
        distancia_objetivo=distancia,
        numero_colisiones=colisiones,
        peso_colision=peso_colision
    )


    return {
        "posicion_final": posicion_actual,
        "distancia": distancia,
        "colisiones": colisiones,
        "aptitud": aptitud
    }


def cromosoma_a_simbolos(cromosoma):

    simbolos = []

    for accion in cromosoma:

        simbolos.append(
            SIMBOLOS[accion]
        )

    return " ".join(
        simbolos
    )


# ==========================================
# PRUEBA
# ==========================================

if __name__ == "__main__":

    poblacion = generar_poblacion(
        cantidad=10,
        longitud_cromosoma=8
    )

    print(
        "POBLACIÓN INICIAL"
    )

    print(
        "================="
    )

    for numero, cromosoma in enumerate(
        poblacion,
        start=1
    ):

        print(
            f"Individuo {numero}:",
            cromosoma_a_simbolos(
                cromosoma
            )
        )

    print()
    print("PRUEBA DE APTITUD")
    print("==================")

    aptitud_prueba = calcular_aptitud(
        distancia_objetivo=3,
        numero_colisiones=1,
        peso_colision=0.2
    )

    print(
        "Aptitud:",
        aptitud_prueba
    )


    print()
    print("SIMULACIÓN DE CROMOSOMA")
    print("=======================")


    mundo = MundoSelva()


    cromosoma_prueba = poblacion[0]


    resultado = simular_cromosoma(
        mundo=mundo,
        posicion_inicial=mundo.posicion_cazador,
        posicion_objetivo=mundo.posicion_jaguar,
        cromosoma=cromosoma_prueba
    )


    print(
        "Cromosoma:",
        cromosoma_a_simbolos(
            cromosoma_prueba
        )
    )

    print(
        "Inicio:",
        mundo.posicion_cazador
    )

    print(
        "Jaguar:",
        mundo.posicion_jaguar
    )

    print(
        "Final:",
        resultado["posicion_final"]
    )

    print(
        "Distancia:",
        resultado["distancia"]
    )

    print(
        "Colisiones:",
        resultado["colisiones"]
    )

    print(
        "Aptitud:",
        round(
            resultado["aptitud"],
            4
        )
    )