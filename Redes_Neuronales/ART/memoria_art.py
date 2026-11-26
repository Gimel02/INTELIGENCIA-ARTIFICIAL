# ==========================================
# MEMORIA ART DE UN AGENTE
#
# Cada agente inteligente posee su propia
# memoria ART independiente.
#
# La memoria tiene:
#
# STM - Short Term Memory
#   patrón que observa actualmente.
#
# LTM - Long Term Memory
#   categorías/prototipos aprendidos por ART1.
#
# Por ahora trabaja en MODO OBSERVADOR:
#
# - reconoce patrones
# - crea categorías
# - aprende prototipos
# - NO modifica las decisiones del agente
#
# ==========================================

from Redes_Neuronales.ART.art1 import ART1

from Redes_Neuronales.ART.patron_entorno import (
    analizar_entorno,
    patron_en,
)


# ==========================================
# EXPERIENCIA POR CATEGORÍA
#
# Cada categoría que aprende ART tiene un
# valor de experiencia entre -1 y 1:
#
#   positivo = en ese tipo de lugar le ha
#              ido bien
#   negativo = ese tipo de lugar estuvo
#              ligado a problemas
#
# Se ajusta con:
#
#   valor_nuevo = valor_anterior + α · refuerzo
#
# y se limita entre -1 y 1.
# ==========================================

ALFA_EXPERIENCIA = 0.2

EXPERIENCIA_MINIMA = -1.0
EXPERIENCIA_MAXIMA = 1.0


class MemoriaART:

    def __init__(
        self,
        nombre,
        vigilancia=0.7,
        max_categorias=16
    ):

        self.nombre = nombre

        # ======================================
        # RED ART1
        # ======================================

        self.art = ART1(
            numero_entradas=4,
            vigilancia=vigilancia,
            max_categorias=max_categorias
        )


        # ======================================
        # MEMORIA DE CORTO PLAZO (STM)
        # ======================================

        self.ultimo_patron = None

        self.ultimo_detalle = None

        self.ultimo_resultado = None


        # ======================================
        # ESTADÍSTICAS
        # ======================================

        self.observaciones = 0

        self.resonancias = 0

        self.nuevas_categorias = 0

        self.resets = 0

        self.saturaciones = 0


        # ======================================
        # EXPERIENCIA DE CADA CATEGORÍA
        #
        # número de categoría -> valor (-1 a 1)
        #
        # Si una categoría no aparece, no hay
        # información sobre ella. Es memoria de
        # largo plazo: no se borra entre
        # partidas.
        # ======================================

        self.experiencia = {}


    # ======================================
    # PARÁMETRO DE VIGILANCIA
    # ======================================

    @property
    def vigilancia(self):

        return self.art.vigilancia


    @vigilancia.setter
    def vigilancia(
        self,
        valor
    ):

        if not 0 <= valor <= 1:

            raise ValueError(
                "La vigilancia debe estar "
                "entre 0 y 1"
            )

        self.art.vigilancia = valor


    # ======================================
    # PROTOTIPOS APRENDIDOS
    # ======================================

    @property
    def prototipos(self):

        return self.art.prototipos


    @property
    def numero_categorias(self):

        return len(
            self.art.prototipos
        )


    # ======================================
    # OBSERVAR EL ENTORNO
    #
    # 1. obtiene el patrón local
    # 2. lo guarda en STM
    # 3. ART intenta reconocerlo
    # 4. actualiza LTM si corresponde
    # ======================================

    def observar(
        self,
        agente
    ):

        entorno = analizar_entorno(
            agente
        )


        patron = entorno[
            "patron"
        ]


        # ==================================
        # STM
        # ==================================

        self.ultimo_patron = list(
            patron
        )

        self.ultimo_detalle = entorno[
            "detalle"
        ]


        # ==================================
        # ART1
        # ==================================

        resultado = self.art.aprender(
            patron
        )


        self.ultimo_resultado = resultado

        self.observaciones += 1


        # ==================================
        # ESTADÍSTICAS DE ART
        # ==================================

        estado = resultado[
            "estado"
        ]


        if estado == "RESONANCIA":

            self.resonancias += 1


        elif estado == "NUEVA_CATEGORIA":

            self.nuevas_categorias += 1


        elif estado == "SATURADA":

            self.saturaciones += 1


        self.resets += len(
            resultado.get(
                "categorias_reseteadas",
                []
            )
        )


        return resultado


    # ======================================
    # REINICIAR SOLO LA MEMORIA CORTA
    #
    # IMPORTANTE:
    #
    # Los prototipos NO se borran.
    #
    # Así ART conserva lo aprendido entre
    # partidas mientras el programa siga
    # abierto.
    # ======================================

    # ======================================
    # CONSULTAR SIN APRENDER
    #
    # Compara un patrón con lo que ART ya
    # sabe y regresa:
    #
    #   categoria  (None si no la reconoce)
    #   similitud
    #   activacion
    #   experiencia (None si no hay info)
    #
    # NO modifica prototipos, NO crea
    # categorías, NO cambia pesos ni la
    # memoria de corto plazo.
    # ======================================

    def clasificar_patron(
        self,
        patron
    ):

        resultado = self.art.clasificar(
            patron
        )

        categoria = resultado["categoria"]

        return {
            "patron": list(patron),
            "categoria": categoria,
            "reconocido": categoria is not None,
            "similitud": resultado["similitud"],
            "activacion": resultado["activacion"],
            "experiencia": self.experiencia_de(
                categoria
            ),
        }


    # Lo mismo, pero para una casilla del
    # mapa (por ejemplo, una casilla a la que
    # el cazador piensa huir).

    def clasificar_casilla(
        self,
        mundo,
        posicion
    ):

        return self.clasificar_patron(
            patron_en(
                mundo,
                posicion
            )
        )


    # ======================================
    # REFORZAR UNA CATEGORÍA
    #
    #   refuerzo > 0: le fue bien
    #   refuerzo < 0: le fue mal
    #
    # Regresa el nuevo valor. Si la categoría
    # es None (ART saturada), no hace nada.
    # ======================================

    def reforzar_categoria(
        self,
        categoria,
        refuerzo,
        alfa=ALFA_EXPERIENCIA
    ):

        if categoria is None:

            return None

        if categoria < 1 or categoria > self.numero_categorias:

            raise ValueError(
                f"La categoría C{categoria} no existe"
            )

        anterior = self.experiencia.get(
            categoria,
            0.0
        )

        nuevo = anterior + alfa * refuerzo

        nuevo = max(
            EXPERIENCIA_MINIMA,
            min(EXPERIENCIA_MAXIMA, nuevo)
        )

        self.experiencia[categoria] = nuevo

        return nuevo


    # ======================================
    # CONSULTAR LA EXPERIENCIA
    #
    # None = sin información (todavía no se
    # ha reforzado). Es distinto de 0.0.
    # ======================================

    def experiencia_de(
        self,
        categoria
    ):

        return self.experiencia.get(
            categoria
        )


    def reiniciar_partida(
        self
    ):

        self.ultimo_patron = None

        self.ultimo_detalle = None

        self.ultimo_resultado = None


    # ======================================
    # RESUMEN
    #
    # Después servirá para el panel visual.
    # ======================================

    def resumen(
        self
    ):

        if self.ultimo_resultado is None:

            return {
                "agente": self.nombre,
                "patron": None,
                "categoria": None,
                "similitud": None,
                "vigilancia": self.vigilancia,
                "estado": "SIN_OBSERVACION",
                "categorias": self.numero_categorias,
            }


        resultado = (
            self.ultimo_resultado
        )


        return {
            "agente":
                self.nombre,

            "patron":
                self.ultimo_patron,

            "categoria":
                resultado.get(
                    "categoria"
                ),

            "similitud":
                resultado.get(
                    "similitud"
                ),

            "vigilancia":
                self.vigilancia,

            "estado":
                resultado[
                    "estado"
                ],

            "categorias":
                self.numero_categorias,

            "resets":
                self.resets,
 
            "resonancias":
                self.resonancias,

            "nuevas_categorias":
                self.nuevas_categorias,

            "saturaciones":
                self.saturaciones,
        }