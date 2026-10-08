import random


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