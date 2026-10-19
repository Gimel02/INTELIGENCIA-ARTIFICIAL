import random

ACCIONES = [
    "ARRIBA",
    "ABAJO",
    "IZQUIERDA",
    "DERECHA"
]

DESPLAZAMIENTOS = {
    "ARRIBA": (-1, 0),
    "ABAJO": (1, 0),
    "IZQUIERDA": (0, -1),
    "DERECHA": (0, 1)
}

def generar_cromosoma(longitud=8):
    return [random.choice(ACCIONES) for _ in range(longitud)]

def generar_poblacion(cantidad=10, longitud_cromosoma=8):
    return [generar_cromosoma(longitud_cromosoma) for _ in range(cantidad)]

def calcular_aptitud_jaguar(distancia_objetivo, numero_colisiones, numero_arenas=0, peso_arena=0.15):
    # Penalizamos la arena moderadamente para que la evite, pero pueda cruzarla si es necesario
    aptitud = (
        1 / (distancia_objetivo + 1)
        - (numero_colisiones * 0.5)
        - (numero_arenas * peso_arena)
    )
    return aptitud

def simular_cromosoma_jaguar(mundo, posicion_inicial, posicion_objetivo, cromosoma, arena_conocida=None):
    if arena_conocida is None:
        arena_conocida = set()

    posicion_actual = posicion_inicial
    colisiones = 0
    arenas = 0
    primer_paso_invalido = False

    distancia_inicial = abs(posicion_inicial[0] - posicion_objetivo[0]) + abs(posicion_inicial[1] - posicion_objetivo[1])
    progreso_inmediato = 0

    for indice, accion in enumerate(cromosoma):
        fila, columna = posicion_actual
        df, dc = DESPLAZAMIENTOS[accion]
        nueva_posicion = (fila + df, columna + dc)

        if mundo.es_transitable(nueva_posicion):
            posicion_actual = nueva_posicion

            if indice == 0:
                dist_paso = abs(posicion_actual[0] - posicion_objetivo[0]) + abs(posicion_actual[1] - posicion_objetivo[1])
                progreso_inmediato = distancia_inicial - dist_paso

            # Detectar arena en la simulación
            if mundo.grid.get(nueva_posicion) == 4 or nueva_posicion in arena_conocida:
                arenas += 1

            if posicion_actual == posicion_objetivo:
                break
        else:
            colisiones += 1
            if indice == 0:
                primer_paso_invalido = True

    distancia_final = abs(posicion_actual[0] - posicion_objetivo[0]) + abs(posicion_actual[1] - posicion_objetivo[1])
    
    aptitud = calcular_aptitud_jaguar(distancia_final, colisiones, arenas)
    aptitud += progreso_inmediato * 0.20

    if primer_paso_invalido:
        aptitud -= 1.0

    return {
        "posicion_final": posicion_actual,
        "distancia": distancia_final,
        "aptitud": aptitud
    }

def elegir_accion_genetica_jaguar(mundo, posicion_inicial, posicion_objetivo, arena_conocida=None):
    poblacion = generar_poblacion(cantidad=15, longitud_cromosoma=10)
    mejor_global = None

    for _ in range(10):  # Generaciones
        resultados = []
        for crom in poblacion:
            res = simular_cromosoma_jaguar(mundo, posicion_inicial, posicion_objetivo, crom, arena_conocida)
            resultados.append({"cromosoma": crom, "aptitud": res["aptitud"]})

        resultados.sort(key=lambda x: x["aptitud"], reverse=True)
        mejor = resultados[0]

        if mejor_global is None or mejor["aptitud"] > mejor_global["aptitud"]:
            mejor_global = mejor

        # Reproducción por élite y mutación
        nueva_poblacion = [mejor["cromosoma"]]
        while len(nueva_poblacion) < 15:
            padre = random.choice(resultados[:5])["cromosoma"]
            hijo = padre.copy()
            if random.random() < 0.2:
                idx = random.randint(0, len(hijo) - 1)
                hijo[idx] = random.choice(ACCIONES)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion

    if mejor_global and mejor_global["cromosoma"]:
        return mejor_global["cromosoma"][0]
    return None