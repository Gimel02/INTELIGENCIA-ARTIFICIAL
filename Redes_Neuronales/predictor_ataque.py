# ==========================================
# RED NEURONAL: ¿EL JAGUAR VA A ATACAR?
#
# Cada cazador tiene su propia red. Con lo
# que percibe del jaguar, calcula el RIESGO
# de que el jaguar lo ataque en los próximos
# turnos.
#
# ESTRUCTURA (microestructura, pág. 56)
#   - Niveles: 2 (entrada y salida)
#   - Neuronas por nivel: 4 de entrada (+ la
#     neurona ficticia del umbral) y 1 de
#     salida
#   - Conexiones: hacia adelante (feed-forward):
#     cada entrada conectada a la salida
#   - Flujo de la información: entrada ->
#     salida
#
# NEURONA: las 3 secciones
#   1. ENTRADA (todas entre 0 y 1)
#        x1 cercanía  = 1 − distancia / 10
#        x2 hambre    = hambre del jaguar / 100
#        x3 se acerca = 1 si está más cerca que
#                       la vez anterior
#        x4 debilidad = 1 − energía del
#                       cazador / 100
#   2. PROCESAMIENTO: net = Σ wi · xi − θ
#   3. SALIDA: función SIGMOIDAL -> riesgo
#      entre 0 y 1. Después un ESCALÓN decide
#      sí o no: riesgo >= 0.6 -> "ATACA".
#
# APRENDIZAJE: supervisado, por corrección de
# error, con la REGLA DELTA (Widrow-Hoff):
#   Δwi = α · xi · (d − y)
#   - OFFLINE: antes de jugar, con miles de
#     ejemplos de partidas sin ventana
#     (Redes_Neuronales/entrenar_red.py).
#   - ONLINE: durante el juego sigue
#     aprendiendo, con un α más pequeño.
#   El supervisor es lo que pasa después: si
#   en los siguientes 3 turnos el cazador
#   percibe al jaguar atacándolo, la respuesta
#   correcta era 1; si no, era 0.
#
# MODO OBSERVADOR: la red predice y aprende,
# pero NO cambia las decisiones del cazador.
# ==========================================

import json
import os
from collections import deque

from Redes_Neuronales.neurona import Neurona
from Redes_Neuronales.funciones_transferencia import escalon


NOMBRES_ENTRADAS = ["cercania", "hambre", "se_acerca", "debilidad"]

# Turnos que espera para saber si su
# predicción fue correcta
HORIZONTE = 3

# Distancia (casillas) con la que la
# cercanía vale 0
DISTANCIA_MAXIMA = 10

# Riesgo desde el cual dice "ATACA"
CORTE = 0.6

# Factor de aprendizaje α
ALFA_OFFLINE = 0.05
ALFA_ONLINE = 0.01

CARPETA_PESOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "pesos"
)

ARCHIVO_PESOS = "predictor_ataque.json"


class PredictorAtaque:

    def __init__(self, neurona=None):

        # Sin entrenar: pesos en 0, riesgo 0.5
        # (menor que el corte: "no ataca")
        self.neurona = neurona or Neurona(
            len(NOMBRES_ENTRADAS),
            transferencia="sigmoidal",
            alfa=ALFA_ONLINE
        )

        # Estadísticas de todo lo que ha
        # aprendido (siguen entre partidas)
        self.aciertos = 0
        self.evaluadas = 0
        self.ataques_reales = 0
        self.ataques_anticipados = 0
        self.falsas_alarmas = 0

        # Error de cada entrenamiento online
        self.historial_errores = []

        # Ejemplos ya etiquetados por el
        # supervisor: (entradas, salida deseada).
        # Sirven para el entrenamiento offline.
        self.ejemplos = []

        # Si es False, solo junta ejemplos y
        # predice, sin cambiar sus pesos
        self.aprende = True

        self.reiniciar_partida()


    def reiniciar_partida(self):

        # Lo que solo vale dentro de una partida

        self.distancia_anterior = None

        # Predicciones esperando saber si fueron
        # correctas: (turno, entradas, predicción)
        self.pendientes = deque()

        self.ultima_entrada = None
        self.ultimo_riesgo = None
        self.ultima_prediccion = None

        self.bitacora = deque(maxlen=200)


    # ======================================
    # 1. ENTRADAS (lo que percibe el cazador)
    # ======================================

    def entradas(self, distancia, hambre, energia):

        se_acerca = (
            1
            if self.distancia_anterior is not None
            and distancia < self.distancia_anterior
            else 0
        )

        return [
            max(0.0, 1 - distancia / DISTANCIA_MAXIMA),
            max(0.0, min(1.0, hambre / 100)),
            se_acerca,
            max(0.0, min(1.0, 1 - energia / 100)),
        ]


    # ======================================
    # 2 y 3. PROCESAMIENTO Y SALIDA
    # ======================================

    def riesgo(self, entradas):

        # Sigmoidal: entre 0 y 1

        return self.neurona.salida(entradas)


    @staticmethod
    def decidir(riesgo):

        # Escalón: 1 = ATACA, 0 = no ataca

        return escalon(riesgo - CORTE)


    def predecir(self, entradas):

        return self.decidir(self.riesgo(entradas))


    # ======================================
    # LO LLAMA EL CAZADOR EN CADA DECISIÓN
    #
    #   percibe:   ¿percibe al jaguar ahora?
    #   distancia: casillas hasta el jaguar
    #   atacando:  ¿lo percibe atacando ahora?
    # ======================================

    def observar(self, turno, percibe, distancia, hambre, energia, atacando):

        # ---- Supervisor: revisa predicciones
        # pasadas y aprende ----

        while self.pendientes:

            turno_pred, x, y = self.pendientes[0]

            if atacando:

                deseada = 1

            elif turno - turno_pred >= HORIZONTE:

                deseada = 0

            else:

                break

            self.pendientes.popleft()

            self.evaluar_y_aprender(turno_pred, x, y, deseada)

        # ---- Nueva predicción ----

        if not percibe or atacando:

            # Sin percibir al jaguar no hay datos;
            # y si ya ataca, ya no es predecir

            self.ultima_prediccion = None
            self.ultimo_riesgo = None

            if not percibe:

                self.distancia_anterior = None

            return None

        x = self.entradas(distancia, hambre, energia)

        riesgo = self.riesgo(x)

        y = self.decidir(riesgo)

        self.distancia_anterior = distancia

        self.ultima_entrada = x
        self.ultimo_riesgo = riesgo
        self.ultima_prediccion = y

        self.pendientes.append((turno, x, y))

        return y


    def evaluar_y_aprender(self, turno, x, y, deseada):

        self.evaluadas += 1

        if y == deseada:

            self.aciertos += 1

        if deseada == 1:

            self.ataques_reales += 1

            if y == 1:

                self.ataques_anticipados += 1

        elif y == 1:

            self.falsas_alarmas += 1

        self.ejemplos.append((x, deseada))

        # Regla delta: Δwi = α · xi · (d − y)
        if self.aprende:

            error = self.neurona.entrenar(x, deseada)

            self.historial_errores.append(abs(error))

        else:

            error = deseada - self.riesgo(x)

        self.bitacora.append({
            "turno": turno,
            "entradas": dict(zip(NOMBRES_ENTRADAS, (round(v, 2) for v in x))),
            "prediccion": y,
            "real": deseada,
            "error": error,
        })


    # ======================================
    # RESUMEN (panel y bitácora)
    # ======================================

    @property
    def porcentaje_aciertos(self):

        if self.evaluadas == 0:

            return None

        return 100 * self.aciertos / self.evaluadas


    def texto_panel(self):

        if self.ultimo_riesgo is None:

            return "Red: sin ver al jaguar"

        texto = "ATACA" if self.ultima_prediccion == 1 else "no ataca"

        return f"Red: {texto} (riesgo {self.ultimo_riesgo:.0%})"


    def imprimir(self, nombre="cazador", ultimas=8):

        n = self.neurona

        print(f"\n=== RED NEURONAL DE {nombre.upper()}: ¿EL JAGUAR VA A ATACAR? ===")
        print(
            "Pesos (sinapsis): "
            + ", ".join(
                f"{nombre_x}={w:.3f}"
                for nombre_x, w in zip(NOMBRES_ENTRADAS, n.pesos)
            )
            + f" | umbral θ={n.umbral:.3f}"
        )
        print(
            f"Entrenamientos: {n.entrenamientos} | α={n.alfa} "
            f"| corte para decir ATACA: {CORTE}"
        )
        print(
            f"En el juego: aciertos {self.aciertos}/{self.evaluadas} "
            f"| ataques anticipados {self.ataques_anticipados}/{self.ataques_reales} "
            f"| falsas alarmas {self.falsas_alarmas}"
        )

        for registro in list(self.bitacora)[-ultimas:]:

            print(
                f"T{registro['turno']:>4} | {registro['entradas']} | "
                f"predijo {registro['prediccion']} | real {registro['real']} | "
                f"error {registro['error']:+.2f}"
            )


    # ======================================
    # GUARDAR Y CARGAR LO APRENDIDO (pesos)
    # ======================================

    def guardar(self, archivo=ARCHIVO_PESOS, extra=None):

        os.makedirs(CARPETA_PESOS, exist_ok=True)

        ruta = os.path.join(CARPETA_PESOS, archivo)

        datos = {
            "entradas": NOMBRES_ENTRADAS,
            "corte": CORTE,
            "neurona": self.neurona.a_diccionario(),
        }

        if extra:

            datos.update(extra)

        with open(ruta, "w", encoding="utf-8") as f:

            json.dump(datos, f, ensure_ascii=False, indent=2)

        return ruta


    @classmethod
    def cargar(cls, archivo=ARCHIVO_PESOS):

        # Si existe el entrenamiento offline, la
        # red empieza con esos pesos; si no,
        # empieza sin saber nada

        ruta = os.path.join(CARPETA_PESOS, archivo)

        if not os.path.exists(ruta):

            return cls()

        with open(ruta, encoding="utf-8") as f:

            datos = json.load(f)

        neurona = Neurona.desde_diccionario(datos["neurona"])

        # En el juego aprende más despacio
        neurona.alfa = ALFA_ONLINE

        return cls(neurona)
