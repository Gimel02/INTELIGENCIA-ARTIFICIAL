# ==========================================
# NEURONA ARTIFICIAL (PERCEPTRÓN)
#
# Una neurona tiene 3 secciones:
#
#   1. ENTRADA:  recibe las señales x1 ... xN
#   2. PROCESAMIENTO:
#        - regla de propagación (entrada
#          global):
#            net = Σ wi · xi − θ
#        - función de activación F: identidad
#          (el estado de activación es el net)
#   3. SALIDA: función de transferencia f
#            y = f(net)
#
# Los PESOS wi son la SINAPSIS: ahí se guarda
# lo que la red sabe.
#
# El umbral θ se maneja como una "neurona
# ficticia" (pág. 49): una entrada x0 = 1 con
# peso w0 = −θ. Así:
#
#   net = w0·1 + Σ wi · xi
#
# APRENDIZAJE (supervisado, por corrección de
# error, pág. 65):
#
#   Δwi = α · xi · (d − y)
#
#   d = salida deseada (la dice el supervisor)
#   y = salida obtenida
#   α = factor de aprendizaje (0 < α <= 1)
#
# La misma fórmula da dos reglas del PDF,
# según la función de transferencia:
#   - con ESCALÓN, y vale 0 o 1: es la regla
#     del PERCEPTRÓN (Rosenblatt). Solo cambia
#     los pesos cuando se equivoca.
#   - con una función CONTINUA (lineal o
#     sigmoidal): es la REGLA DELTA de
#     Widrow-Hoff (ADALINE, pág. 66). Corrige
#     según qué tan lejos quedó, y se
#     estabiliza aunque los datos no se puedan
#     separar con una línea.
#
# Si la neurona acierta (d = y), los pesos no
# cambian. La red terminó de aprender cuando
# los pesos ya no cambian (dw/dt = 0).
# ==========================================

from Redes_Neuronales.funciones_transferencia import FUNCIONES


class Neurona:

    def __init__(
        self,
        numero_entradas,
        transferencia="escalon",
        alfa=0.1,
        pesos=None,
        umbral=0.0
    ):

        self.numero_entradas = numero_entradas

        self.transferencia = transferencia

        self.funcion = FUNCIONES[transferencia]

        self.alfa = alfa

        # Pesos de las conexiones (sinapsis).
        # Empiezan en 0: la neurona no sabe nada.
        self.pesos = (
            list(pesos)
            if pesos is not None
            else [0.0] * numero_entradas
        )

        # Neurona ficticia: w0 = −θ
        self.w0 = -umbral

        # Estadísticas del aprendizaje
        self.entrenamientos = 0
        self.correcciones = 0
        self.entrenamientos_sin_cambio = 0


    @property
    def umbral(self):

        return -self.w0


    # ======================================
    # 2. PROCESAMIENTO
    # ======================================

    def net(self, entradas):

        # Regla de propagación:
        # net = Σ wi · xi − θ

        if len(entradas) != self.numero_entradas:

            raise ValueError(
                f"Se esperaban {self.numero_entradas} entradas"
            )

        return self.w0 + sum(
            w * x
            for w, x in zip(self.pesos, entradas)
        )


    def activacion(self, entradas):

        # Función de activación F = identidad:
        # a(t+1) = net(t)

        return self.net(entradas)


    # ======================================
    # 3. SALIDA
    # ======================================

    def salida(self, entradas):

        # y = f(net)

        return self.funcion(self.activacion(entradas))


    # ======================================
    # APRENDIZAJE POR CORRECCIÓN DE ERROR
    # ======================================

    def entrenar(self, entradas, deseada):

        # Regresa el error (d − y)

        obtenida = self.salida(entradas)

        error = deseada - obtenida

        self.entrenamientos += 1

        if abs(error) < 1e-9:

            self.entrenamientos_sin_cambio += 1

            return 0

        # Δwi = α · xi · (d − y)
        self.pesos = [
            w + self.alfa * x * error
            for w, x in zip(self.pesos, entradas)
        ]

        # La neurona ficticia tiene entrada 1
        self.w0 += self.alfa * 1 * error

        self.correcciones += 1

        self.entrenamientos_sin_cambio = 0

        return error


    # ======================================
    # GUARDAR Y CARGAR LOS PESOS
    # (el conocimiento de la red)
    # ======================================

    def a_diccionario(self):

        return {
            "transferencia": self.transferencia,
            "alfa": self.alfa,
            "pesos": self.pesos,
            "w0": self.w0,
            "entrenamientos": self.entrenamientos,
            "correcciones": self.correcciones,
        }


    @classmethod
    def desde_diccionario(cls, datos):

        neurona = cls(
            len(datos["pesos"]),
            transferencia=datos["transferencia"],
            alfa=datos["alfa"],
            pesos=datos["pesos"],
        )

        neurona.w0 = datos["w0"]

        neurona.entrenamientos = datos.get("entrenamientos", 0)

        neurona.correcciones = datos.get("correcciones", 0)

        return neurona
