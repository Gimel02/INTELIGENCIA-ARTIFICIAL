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
)


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