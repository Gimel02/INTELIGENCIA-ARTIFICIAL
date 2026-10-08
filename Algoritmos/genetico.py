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
# MOSTRAR CROMOSOMA CON SÍMBOLOS
# ==========================================

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

    cromosoma = generar_cromosoma(
        longitud=8
    )

    print(
        "Cromosoma:"
    )

    print(
        cromosoma
    )

    print(
        "Movimientos:"
    )

    print(
        cromosoma_a_simbolos(
            cromosoma
        )
    )