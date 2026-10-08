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


            # ==================================
            # OBJETIVO ALCANZADO
            # ==================================

            if posicion_actual == posicion_objetivo:

                break


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


# ==========================================
# MUTACIÓN
# ==========================================

def mutar(
    cromosoma,
    probabilidad_mutacion=0.10
):

    cromosoma_mutado = (
        cromosoma.copy()
    )

    for indice in range(
        len(cromosoma_mutado)
    ):

        if random.random() < probabilidad_mutacion:

            accion_anterior = (
                cromosoma_mutado[indice]
            )

            acciones_posibles = [
                accion
                for accion in ACCIONES
                if accion != accion_anterior
            ]

            nueva_accion = random.choice(
                acciones_posibles
            )

            cromosoma_mutado[indice] = (
                nueva_accion
            )

    return cromosoma_mutado


def crear_nueva_generacion(
    resultados,
    tamano_poblacion=10,
    cantidad_elite=2,
    cantidad_padres=4,
    probabilidad_mutacion=0.10
):

    nueva_poblacion = []


    # ======================================
    # ELITISMO
    # ======================================
    # Los mejores individuos pasan
    # directamente a la siguiente generación.

    elite = resultados[
        :cantidad_elite
    ]

    for individuo in elite:

        nueva_poblacion.append(
            individuo["cromosoma"].copy()
        )


    # ======================================
    # SELECCIÓN DE PADRES
    # ======================================

    padres = resultados[
        :cantidad_padres
    ]


    # ======================================
    # GENERAR HIJOS
    # ======================================

    while len(nueva_poblacion) < tamano_poblacion:

        padre1, padre2 = random.sample(
            padres,
            2
        )

        hijo1, hijo2 = cruzar(
            padre1,
            padre2
        )


        hijo1 = mutar(
            hijo1,
            probabilidad_mutacion
        )

        hijo2 = mutar(
            hijo2,
            probabilidad_mutacion
        )


        nueva_poblacion.append(
            hijo1
        )


        if len(nueva_poblacion) < tamano_poblacion:

            nueva_poblacion.append(
                hijo2
            )


    return nueva_poblacion


# ==========================================
# EVOLUCIÓN GENÉTICA
# ==========================================

def evolucionar(
    mundo,
    posicion_inicial,
    posicion_objetivo,
    tamano_poblacion=10,
    longitud_cromosoma=20,
    max_generaciones=20,
    cantidad_elite=2,
    cantidad_padres=4,
    probabilidad_mutacion=0.10,
    peso_colision=0.2,
    mostrar_progreso=True
):

    # ======================================
    # POBLACIÓN INICIAL ALEATORIA
    # ======================================

    poblacion = generar_poblacion(
        cantidad=tamano_poblacion,
        longitud_cromosoma=longitud_cromosoma
    )


    mejor_global = None


    # ======================================
    # CICLO DE GENERACIONES
    # ======================================

    for generacion in range(
        1,
        max_generaciones + 1
    ):

        resultados = evaluar_poblacion(
            mundo=mundo,
            poblacion=poblacion,
            posicion_inicial=posicion_inicial,
            posicion_objetivo=posicion_objetivo,
            peso_colision=peso_colision
        )


        mejor = resultados[0]


        # Guardamos el mejor individuo
        if (
            mejor_global is None
            or
            mejor["aptitud"]
            >
            mejor_global["aptitud"]
        ):

            mejor_global = mejor


        if mostrar_progreso:
             print(
                        f"Generación {generacion:02d} | "
                        f"Aptitud: {mejor['aptitud']:.4f} | "
                        f"Distancia: {mejor['distancia']} | "
                        f"Colisiones: {mejor['colisiones']}"
                    )


        # ==================================
        # SOLUCIÓN PERFECTA
        # ==================================

        if (
            mejor["distancia"] == 0
            and
            mejor["colisiones"] == 0
        ):

            print()

            if mostrar_progreso:
                print()
                print(
                    "OBJETIVO ALCANZADO"
                )

            return (
                mejor,
                generacion
            )


        # ==================================
        # CREAR SIGUIENTE GENERACIÓN
        # ==================================

        poblacion = crear_nueva_generacion(
            resultados=resultados,
            tamano_poblacion=tamano_poblacion,
            cantidad_elite=cantidad_elite,
            cantidad_padres=cantidad_padres,
            probabilidad_mutacion=probabilidad_mutacion
        )


    # ======================================
    # SI NO ENCONTRÓ SOLUCIÓN PERFECTA
    # ======================================

    return (
        mejor_global,
        max_generaciones
    )


# ==========================================
# ELEGIR SIGUIENTE ACCIÓN CON AG
# ==========================================

def elegir_accion_genetica(
    mundo,
    posicion_inicial,
    posicion_objetivo
):

    mejor_individuo, generaciones = evolucionar(
        mundo=mundo,
        posicion_inicial=posicion_inicial,
        posicion_objetivo=posicion_objetivo,
        tamano_poblacion=10,
        longitud_cromosoma=20,
        max_generaciones=20,
        cantidad_elite=2,
        cantidad_padres=4,
        probabilidad_mutacion=0.10,
        mostrar_progreso=False
    )


    if mejor_individuo is None:

        return None


    cromosoma = (
        mejor_individuo["cromosoma"]
    )


    if not cromosoma:

        return None


    # Solo ejecutamos el primer movimiento.
    # Después el entorno puede cambiar y
    # volveremos a calcular una estrategia.

    accion = cromosoma[0]

    return accion


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

    print()
    print("MUTACIÓN")
    print("========")


    hijo1_mutado = mutar(
        hijo1,
        probabilidad_mutacion=0.10
    )

    hijo2_mutado = mutar(
        hijo2,
        probabilidad_mutacion=0.10
    )


    print(
        "Hijo 1 original:",
        cromosoma_a_simbolos(
            hijo1
        )
    )

    print(
        "Hijo 1 mutado:  ",
        cromosoma_a_simbolos(
            hijo1_mutado
        )
    )

    print()

    print(
        "Hijo 2 original:",
        cromosoma_a_simbolos(
            hijo2
        )
    )

    print(
        "Hijo 2 mutado:  ",
        cromosoma_a_simbolos(
            hijo2_mutado
        )
    )

    print()
    print("GENERACIÓN 2")
    print("============")


    poblacion_2 = crear_nueva_generacion(
        resultados=resultados,
        tamano_poblacion=10,
        cantidad_elite=2,
        cantidad_padres=4,
        probabilidad_mutacion=0.10
    )


    resultados_2 = evaluar_poblacion(
        mundo=mundo,
        poblacion=poblacion_2,
        posicion_inicial=mundo.posicion_cazador,
        posicion_objetivo=mundo.posicion_jaguar
    )


    for posicion_ranking, individuo in enumerate(
        resultados_2,
        start=1
    ):

        print(
            f"{posicion_ranking}. "
            f"{cromosoma_a_simbolos(individuo['cromosoma'])}"
        )

        print(
            f"   Distancia: {individuo['distancia']} | "
            f"Colisiones: {individuo['colisiones']} | "
            f"Aptitud: {individuo['aptitud']:.4f}"
        )

    print()
    print("EVOLUCIÓN AUTOMÁTICA")
    print("====================")


    mundo_evolucion = MundoSelva()


    mejor_individuo, generaciones_usadas = evolucionar(
        mundo=mundo_evolucion,
        posicion_inicial=mundo_evolucion.posicion_cazador,
        posicion_objetivo=mundo_evolucion.posicion_jaguar,
        tamano_poblacion=10,
        longitud_cromosoma=20,
        max_generaciones=20,
        cantidad_elite=2,
        cantidad_padres=4,
        probabilidad_mutacion=0.10
    )


    print()
    print(
        "MEJOR RESULTADO"
    )

    print(
        "==============="
    )


    print(
        "Cromosoma:",
        cromosoma_a_simbolos(
            mejor_individuo["cromosoma"]
        )
    )

    print(
        "Distancia:",
        mejor_individuo["distancia"]
    )

    print(
        "Colisiones:",
        mejor_individuo["colisiones"]
    )

    print(
        "Aptitud:",
        round(
            mejor_individuo["aptitud"],
            4
        )
    )

    print(
        "Generaciones usadas:",
        generaciones_usadas
    )

    print()
    print("DECISIÓN DINÁMICA")
    print("==================")


    accion = elegir_accion_genetica(
        mundo=mundo_evolucion,
        posicion_inicial=mundo_evolucion.posicion_cazador,
        posicion_objetivo=mundo_evolucion.posicion_jaguar
    )


    print(
        "Posición cazador:",
        mundo_evolucion.posicion_cazador
    )

    print(
        "Posición Jaguar:",
        mundo_evolucion.posicion_jaguar
    )

    print(
        "Acción elegida:",
        accion
    )

    if accion is not None:

        print(
            "Símbolo:",
            SIMBOLOS[accion]
        )