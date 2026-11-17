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
# Aprendizaje que utiliza realmente
# el juego actual.

ALFA_REFUERZO = 0.03

CARPETA_PESOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "pesos"
)

ARCHIVO_PESOS = "predictor_refuerzo.json"

# Estadísticas que también se guardan, para que
# el panel siga contando desde donde se quedó
ESTADISTICAS = (
    "aciertos",
    "evaluadas",
    "ataques_reales",
    "ataques_anticipados",
    "falsas_alarmas",
    "refuerzos_positivos",
    "refuerzos_negativos",
    "recompensa_acumulada",
)


def archivo_de(nombre):

    # Cada cazador guarda lo que aprendió en su
    # propio archivo (cada uno aprende solo)

    return f"predictor_refuerzo_{nombre}.json"


class PredictorAtaque:

    def __init__(self, neurona=None):

        # Sin entrenar: pesos en 0, riesgo 0.5
        # (menor que el corte: "no ataca")
        self.neurona = neurona or Neurona(
            len(NOMBRES_ENTRADAS),
            transferencia="sigmoidal",
            alfa=ALFA_REFUERZO
        )

        # Estadísticas de todo lo que ha
        # aprendido (siguen entre partidas)
        self.aciertos = 0
        self.evaluadas = 0
        self.ataques_reales = 0
        self.ataques_anticipados = 0
        self.falsas_alarmas = 0
        # ======================================
        # ESTADÍSTICAS DE REFUERZO
        # ======================================

        self.refuerzos_positivos = 0

        self.refuerzos_negativos = 0

        self.recompensa_acumulada = 0

        self.historial_refuerzos = []

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


    def decidir(self, riesgo):

        # Escalón: 1 = ATACA, 0 = no ataca. Si el
        # riesgo queda justo en el corte, conserva
        # su predicción anterior (como en el PDF).

        return escalon(
            riesgo - CORTE,
            anterior=self.ultima_prediccion
        )


    def predecir(self, entradas):

        return self.decidir(self.riesgo(entradas))


    # ======================================
    # LO LLAMA EL CAZADOR EN CADA DECISIÓN
    #
    #   percibe:   ¿percibe al jaguar ahora?
    #   distancia: casillas hasta el jaguar
    #   atacando:  ¿lo percibe atacando ahora?
    # ======================================

    def observar(
        self,
        turno,
        percibe,
        distancia,
        hambre,
        energia,
        atacando
    ):

        # ======================================
        # CRÍTICO DEL APRENDIZAJE
        #
        # No entrega una respuesta correcta.
        #
        # Únicamente decide:
        #
        #   +1 éxito
        #   -1 fracaso
        # ======================================

        while self.pendientes:

            (
                turno_pred,
                x,
                accion,
                riesgo
            ) = self.pendientes[0]


            # ----------------------------------
            # EL JAGUAR SÍ ATACÓ
            # ----------------------------------

            if atacando:

                if accion == 1:

                    refuerzo = +1

                    motivo = (
                        "anticipó correctamente "
                        "el ataque"
                    )

                else:

                    refuerzo = -1

                    motivo = (
                        "no anticipó el ataque"
                    )


            # ----------------------------------
            # PASÓ EL HORIZONTE Y NO ATACÓ
            # ----------------------------------

            elif (
                turno - turno_pred
                >=
                HORIZONTE
            ):

                if accion == 0:

                    refuerzo = +1

                    motivo = (
                        "correctamente continuó "
                        "sin alarma"
                    )

                else:

                    refuerzo = -1

                    motivo = (
                        "falsa alarma de ataque"
                    )


            else:

                break


            self.pendientes.popleft()


            self.aplicar_refuerzo(
                turno_pred,
                x,
                accion,
                riesgo,
                refuerzo,
                motivo
            )


        # ======================================
        # NUEVA PREDICCIÓN
        # ======================================

        if not percibe or atacando:

            self.ultima_prediccion = None

            self.ultimo_riesgo = None


            if not percibe:

                self.distancia_anterior = None


            return None


        x = self.entradas(
            distancia,
            hambre,
            energia
        )


        riesgo = self.riesgo(x)

        accion = self.decidir(
            riesgo
        )


        self.distancia_anterior = (
            distancia
        )

        self.ultima_entrada = x

        self.ultimo_riesgo = riesgo

        self.ultima_prediccion = accion


        # La experiencia queda esperando
        # la opinión del crítico.

        self.pendientes.append(
            (
                turno,
                x,
                accion,
                riesgo
            )
        )


        return accion

    # ======================================
    # RECIBIR REFUERZO DEL CRÍTICO
    # ======================================

    def aplicar_refuerzo(
        self,
        turno,
        entradas,
        accion,
        riesgo,
        refuerzo,
        motivo
    ):

        self.evaluadas += 1


        # ==================================
        # ÉXITO / FRACASO
        # ==================================

        if refuerzo > 0:

            self.refuerzos_positivos += 1

            # Conservamos esta variable porque
            # ya la usa código anterior.
            self.aciertos += 1

        else:

            self.refuerzos_negativos += 1


        self.recompensa_acumulada += (
            refuerzo
        )


        self.historial_refuerzos.append(
            refuerzo
        )


        # ==================================
        # APRENDIZAJE ONLINE
        #
        # Aquí ya NO existe:
        #
        # deseada = 0 / 1
        #
        # Solo:
        #
        # +1 / -1
        # ==================================

        if self.aprende:

            ajuste = (
                self.neurona.reforzar(
                    entradas,
                    accion,
                    refuerzo
                )
            )

        else:

            ajuste = 0.0


        self.bitacora.append({

            "turno": turno,

            "entradas": dict(
                zip(
                    NOMBRES_ENTRADAS,
                    (
                        round(v, 2)
                        for v in entradas
                    )
                )
            ),

            "accion": accion,

            "riesgo": round(
                riesgo,
                4
            ),

            "refuerzo": refuerzo,

            "motivo": motivo,

            "ajuste": ajuste,
        })


        print(
            f"[RED - REFUERZO] "
            f"acción={'ATACA' if accion else 'NO ATACA'} | "
            f"{refuerzo:+d} | "
            f"{motivo}"
        )

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
            f"Aprendizaje por REFUERZO ONLINE | "
            f"+1: {self.refuerzos_positivos} | "
            f"-1: {self.refuerzos_negativos} | "
            f"recompensa acumulada: "
            f"{self.recompensa_acumulada:+d}"
        )

        for registro in list(
            self.bitacora
        )[-ultimas:]:

            print(
                f"T{registro['turno']:>4} | "
                f"{registro['entradas']} | "
                f"acción "
                f"{'ATACA' if registro['accion'] else 'NO ATACA'} | "
                f"refuerzo "
                f"{registro['refuerzo']:+d} | "
                f"{registro['motivo']}"
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
            "estadisticas": {
                campo: getattr(self, campo)
                for campo in ESTADISTICAS
            },
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
        neurona.alfa = ALFA_REFUERZO

        red = cls(neurona)

        # Sigue contando desde donde se quedó
        for campo, valor in datos.get("estadisticas", {}).items():

            if campo in ESTADISTICAS:

                setattr(red, campo, valor)

        return red
