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


def evaluar_poblacion(
    mundo,
    poblacion,
    posicion_inicial,
    posicion_objetivo,
    peso_colision=0.2
):

    resultados = []

    for numero, cromosoma in enumerate(
        poblacion,
        start=1
    ):

        resultado = simular_cromosoma(
            mundo=mundo,
            posicion_inicial=posicion_inicial,
            posicion_objetivo=posicion_objetivo,
            cromosoma=cromosoma,
            peso_colision=peso_colision
        )

        resultados.append(
            {
                "numero": numero,
                "cromosoma": cromosoma,
                "posicion_final": resultado["posicion_final"],
                "distancia": resultado["distancia"],
                "colisiones": resultado["colisiones"],
                "aptitud": resultado["aptitud"]
            }
        )


    # Ordenar de mejor a peor
    resultados.sort(
        key=lambda individuo: individuo["aptitud"],
        reverse=True
    )

    return resultados


def seleccionar_mejores(
    resultados,
    cantidad_padres=2
):

    padres = resultados[
        :cantidad_padres
    ]

    return padres

# ==========================================
# CRUZA DE DOS CROMOSOMAS
# ==========================================

def cruzar(
    padre1,
    padre2
):

    cromosoma1 = padre1["cromosoma"]
    cromosoma2 = padre2["cromosoma"]

    punto_cruza = (
        len(cromosoma1)
        //
        2
    )

    hijo1 = (
        cromosoma1[:punto_cruza]
        +
        cromosoma2[punto_cruza:]
    )

    hijo2 = (
        cromosoma2[:punto_cruza]
        +
        cromosoma1[punto_cruza:]
    )

    return hijo1, hijo2



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

    print()
    print("EVALUACIÓN DE LA POBLACIÓN")
    print("===========================")


    resultados = evaluar_poblacion(
        mundo=mundo,
        poblacion=poblacion,
        posicion_inicial=mundo.posicion_cazador,
        posicion_objetivo=mundo.posicion_jaguar
    )


    for posicion_ranking, individuo in enumerate(
        resultados,
        start=1
    ):

        print(
            f"{posicion_ranking}. "
            f"Individuo {individuo['numero']}: "
            f"{cromosoma_a_simbolos(individuo['cromosoma'])}"
        )

        print(
            f"   Distancia: {individuo['distancia']} | "
            f"Colisiones: {individuo['colisiones']} | "
            f"Aptitud: {individuo['aptitud']:.4f}"
        )

    print()
    print("PADRES SELECCIONADOS")
    print("====================")


    padres = seleccionar_mejores(
        resultados,
        cantidad_padres=2
    )


    for numero_padre, padre in enumerate(
        padres,
        start=1
    ):

        print(
            f"Padre {numero_padre}: "
            f"Individuo {padre['numero']}"
        )

        print(
            "   Cromosoma:",
            cromosoma_a_simbolos(
                padre["cromosoma"]
            )
        )

        print(
            f"   Aptitud: "
            f"{padre['aptitud']:.4f}"
        )

    print()
    print("CRUZA")
    print("======")


    hijo1, hijo2 = cruzar(
        padres[0],
        padres[1]
    )


    print(
        "Padre 1:",
        cromosoma_a_simbolos(
            padres[0]["cromosoma"]
        )
    )

    print(
        "Padre 2:",
        cromosoma_a_simbolos(
            padres[1]["cromosoma"]
        )
    )

    print(
        "Hijo 1:",
        cromosoma_a_simbolos(
            hijo1
        )
    )

    print(
        "Hijo 2:",
        cromosoma_a_simbolos(
            hijo2
        )
    )