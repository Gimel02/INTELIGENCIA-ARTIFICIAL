# ==========================================
# ENTRENAMIENTO OFFLINE DE LA RED
# "¿EL JAGUAR VA A ATACAR?"
#
# 1. Juega partidas sin ventana con DIOS y
#    junta ejemplos ya etiquetados por el
#    supervisor: (entradas, ¿atacó?).
#      - entrenamiento: semillas 0 a 149
#      - prueba:        semillas 1000 a 1059
#        (mapas que la red nunca vio)
# 2. Preprocesa: los ataques son pocos (cerca
#    del 3 %), así que se repiten los ejemplos
#    de ataque hasta igualar a los de "no
#    ataca". Si no, la red aprende a decir
#    siempre "no ataca".
# 3. Entrena con la regla delta por épocas
#    (pasadas completas por los ejemplos),
#    hasta que el error deja de bajar.
# 4. Mide qué tan bien predice en los mapas de
#    prueba y guarda los pesos en
#    Redes_Neuronales/pesos/predictor_ataque.json
#
# Cómo correrlo (desde la carpeta del
# proyecto):
#
#   python3 -m Redes_Neuronales.entrenar_red
# ==========================================

import contextlib
import io
import random

from Redes_Neuronales.neurona import Neurona
from Redes_Neuronales.predictor_ataque import (
    PredictorAtaque,
    NOMBRES_ENTRADAS,
    ALFA_OFFLINE,
    CORTE,
)


SEMILLAS_ENTRENAMIENTO = range(0, 150)
SEMILLAS_PRUEBA = range(1000, 1060)

EPOCAS = 30

PASOS_POR_PARTIDA = 8000


# ==========================================
# 1. JUNTAR EJEMPLOS
# ==========================================

def juntar_ejemplos(semillas):

    from Logica_Difusa.dios import Dios

    dios = Dios()

    # Redes nuevas que solo observan (no
    # aprenden) mientras juntan ejemplos
    for nombre in ("cazador", "interceptor"):

        red = PredictorAtaque()

        red.aprende = False

        dios.redes[nombre] = red

    for semilla in semillas:

        random.seed(semilla)

        with contextlib.redirect_stdout(io.StringIO()):

            dios.nueva_partida()

            for _ in range(PASOS_POR_PARTIDA):

                if not dios.paso(0.05):

                    break

    ejemplos = []

    for red in dios.redes.values():

        ejemplos.extend(red.ejemplos)

    return ejemplos


# ==========================================
# 2. PREPROCESAR: BALANCEAR
# ==========================================

def balancear(ejemplos):

    ataques = [e for e in ejemplos if e[1] == 1]
    no_ataques = [e for e in ejemplos if e[1] == 0]

    if not ataques:

        return list(ejemplos)

    repeticiones = max(1, len(no_ataques) // len(ataques))

    return no_ataques + ataques * repeticiones


# ==========================================
# 3. ENTRENAR POR ÉPOCAS
# ==========================================

def entrenar(ejemplos, epocas=EPOCAS, alfa=ALFA_OFFLINE, semilla=1):

    neurona = Neurona(
        len(NOMBRES_ENTRADAS),
        transferencia="sigmoidal",
        alfa=alfa
    )

    azar = random.Random(semilla)

    curva = []

    for _ in range(epocas):

        orden = list(ejemplos)

        azar.shuffle(orden)

        error_total = 0.0

        for x, d in orden:

            error = neurona.entrenar(x, d)

            error_total += error ** 2

        # Error cuadrático medio de la época
        curva.append(error_total / len(orden))

    return neurona, curva


# ==========================================
# 4. MEDIR
# ==========================================

def medir(neurona, ejemplos):

    red = PredictorAtaque(neurona)

    anticipados = reales = falsas = negativos = aciertos = 0

    for x, d in ejemplos:

        y = red.predecir(x)

        aciertos += y == d

        if d == 1:

            reales += 1
            anticipados += y == 1

        else:

            negativos += 1
            falsas += y == 1

    return {
        "ejemplos": len(ejemplos),
        "aciertos": aciertos,
        "ataques_reales": reales,
        "ataques_anticipados": anticipados,
        "no_ataques": negativos,
        "falsas_alarmas": falsas,
    }


def main():

    print("Juntando ejemplos de entrenamiento...")
    entrenamiento = juntar_ejemplos(SEMILLAS_ENTRENAMIENTO)

    print("Juntando ejemplos de prueba...")
    prueba = juntar_ejemplos(SEMILLAS_PRUEBA)

    balanceados = balancear(entrenamiento)

    neurona, curva = entrenar(balanceados)

    resultado = medir(neurona, prueba)

    # Para comparar: una red sin entrenar
    sin_entrenar = medir(PredictorAtaque().neurona, prueba)

    red = PredictorAtaque(neurona)

    ruta = red.guardar(extra={
        "entrenamiento": {
            "partidas": len(SEMILLAS_ENTRENAMIENTO),
            "ejemplos": len(entrenamiento),
            "ataques": sum(d for _, d in entrenamiento),
            "ejemplos_balanceados": len(balanceados),
            "epocas": EPOCAS,
            "alfa": ALFA_OFFLINE,
            "error_por_epoca": [round(e, 5) for e in curva],
        },
        "prueba": resultado,
        "prueba_sin_entrenar": sin_entrenar,
    })

    r = resultado

    print()
    print(f"Ejemplos de entrenamiento: {len(entrenamiento)} "
          f"({sum(d for _, d in entrenamiento)} ataques)")
    print(f"Error por época: {curva[0]:.4f} -> {curva[-1]:.4f}")
    print(
        "Pesos: "
        + ", ".join(f"{n}={w:.3f}" for n, w in zip(NOMBRES_ENTRADAS, neurona.pesos))
        + f" | umbral θ={neurona.umbral:.3f}"
    )
    print(f"Prueba ({r['ejemplos']} ejemplos de mapas nuevos, corte {CORTE}):")
    print(f"  ataques anticipados: {r['ataques_anticipados']}/{r['ataques_reales']}")
    print(f"  falsas alarmas: {r['falsas_alarmas']}/{r['no_ataques']}")
    print(f"  aciertos: {r['aciertos'] / r['ejemplos']:.0%}")
    print(f"Sin entrenar anticipaba {sin_entrenar['ataques_anticipados']}/{sin_entrenar['ataques_reales']}")
    print(f"Pesos guardados en {ruta}")


if __name__ == "__main__":

    main()
