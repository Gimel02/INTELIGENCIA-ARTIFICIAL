# ==========================================
# ART1 - ADAPTIVE RESONANCE THEORY
#
# Red neuronal para reconocimiento y
# aprendizaje ONLINE de patrones binarios.
#
# Cada categoría almacena un prototipo.
#
# La red:
#
# 1. recibe un patrón binario
# 2. busca la categoría más parecida
# 3. calcula la semejanza
# 4. compara con vigilancia rho
# 5. si supera rho -> RESONANCIA
# 6. si no -> crea una categoría nueva
#
# El aprendizaje es:
#
# - online
# - no supervisado
# - competitivo
#
# ==========================================


class ART1:

    def __init__(
        self,
        numero_entradas=4,
        vigilancia=0.5,
        max_categorias=16,
        gamma=0.5
    ):

        if numero_entradas <= 0:
            raise ValueError(
                "numero_entradas debe ser mayor que 0"
            )

        if not 0 <= vigilancia <= 1:
            raise ValueError(
                "La vigilancia debe estar entre 0 y 1"
            )

        if max_categorias <= 0:
            raise ValueError(
                "max_categorias debe ser mayor que 0"
            )

        self.numero_entradas = numero_entradas

        # Parámetro rho
        self.vigilancia = vigilancia

        self.max_categorias = max_categorias

        # ======================================
        # GAMMA
        #
        # Parámetro estabilizador utilizado para
        # calcular los pesos feedforward W.
        #
        # En el ejemplo de clase:
        #
        # gamma = 0.5
        # ======================================

        if gamma <= 0:

            raise ValueError(
                "gamma debe ser mayor que 0"
            )


        self.gamma = gamma

        # Cada elemento es el prototipo binario
        # de una categoría.
        #
        # Ejemplo:
        #
        # [
        #     [1, 1, 0, 0],   # C1
        #     [0, 0, 1, 1],   # C2
        # ]
        #
        self.prototipos = []

        # Para mostrar posteriormente en
        # interfaz qué hizo ART.
        self.ultimo_resultado = None


    # ======================================
    # VALIDAR PATRÓN
    # ======================================

    def validar_patron(self, patron):

        if len(patron) != self.numero_entradas:

            raise ValueError(
                f"ART1 espera "
                f"{self.numero_entradas} entradas"
            )

        if any(valor not in (0, 1) for valor in patron):

            raise ValueError(
                "ART1 solamente acepta "
                "patrones binarios 0/1"
            )


    # ======================================
    # SEMEJANZA
    #
    #        E · V
    # Rs = --------
    #         |E|
    #
    # Para patrones binarios equivale a
    # comparar cuántos unos de la entrada
    # coinciden con el prototipo.
    # ======================================

    def semejanza(
        self,
        patron,
        prototipo
    ):

        self.validar_patron(
            patron
        )

        if len(prototipo) != self.numero_entradas:

            raise ValueError(
                "Prototipo incompatible"
            )


        total_activos = sum(
            patron
        )


        # Evitar división entre cero.

        if total_activos == 0:

            return (
                1.0
                if sum(prototipo) == 0
                else 0.0
            )


        coincidencias = sum(

            entrada * memoria

            for entrada, memoria
            in zip(
                patron,
                prototipo
            )
        )


        return (
            coincidencias
            /
            total_activos
        )


    # ======================================
    # PESOS FEEDFORWARD W
    #
    # A partir del prototipo V de una
    # categoría se calculan sus conexiones
    # hacia la capa de salida:
    #
    #             vi
    # wi = ----------------
    #       gamma + sum(V)
    #
    # Ejemplo de clase:
    #
    # V = [1, 1, 0, 0]
    # gamma = 0.5
    #
    # W = [0.4, 0.4, 0, 0]
    # ======================================

    def pesos_feedforward(
        self,
        prototipo
    ):

        denominador = (
            self.gamma
            +
            sum(prototipo)
        )


        if denominador == 0:

            return [
                0.0
                for _ in prototipo
            ]


        return [

            valor
            /
            denominador

            for valor
            in prototipo

        ]

    # ======================================
    # ACTIVACIÓN DE UNA CATEGORÍA
    #
    # La entrada se propaga mediante los
    # pesos feedforward W.
    #
    # La categoría con mayor activación
    # gana la competencia.
    #
    #       N
    # yj = Σ ei * wji
    #      i=1
    # ======================================

    def activacion_categoria(
        self,
        patron,
        prototipo
    ):

        self.validar_patron(
            patron
        )


        pesos_w = (
            self.pesos_feedforward(
                prototipo
            )
        )


        return sum(

            entrada
            *
            peso

            for entrada, peso
            in zip(
                patron,
                pesos_w
            )

        )


    # ======================================
    # COMPETENCIA
    #
    # Las neuronas de salida compiten.
    #
    # Regresa las categorías ordenadas desde
    # la de mayor activación hasta la menor.
    #
    # Esto permite:
    #
    # GANADORA
    #    ↓
    # ¿supera rho?
    #
    # sí  -> RESONANCIA
    # no  -> RESET
    #        ↓
    #      probar siguiente
    # ======================================

    def categorias_por_competencia(
        self,
        patron
    ):

        categorias = []


        for indice, prototipo in enumerate(
            self.prototipos
        ):

            activacion = (
                self.activacion_categoria(
                    patron,
                    prototipo
                )
            )


            similitud = (
                self.semejanza(
                    patron,
                    prototipo
                )
            )


            categorias.append({
                "indice": indice,
                "activacion": activacion,
                "similitud": similitud,
            })


        categorias.sort(
            key=lambda categoria:
            categoria["activacion"],
            reverse=True
        )


        return categorias

    # ======================================
    # CREAR CATEGORÍA
    # ======================================

    def crear_categoria(
        self,
        patron
    ):

        if (
            len(self.prototipos)
            >=
            self.max_categorias
        ):

            return None


        self.prototipos.append(
            list(patron)
        )


        return (
            len(self.prototipos) - 1
        )


    def aprender(
        self,
        patron
    ):

        self.validar_patron(
            patron
        )


        # ==================================
        # NO EXISTE NINGUNA CATEGORÍA
        # ==================================

        if not self.prototipos:

            indice = self.crear_categoria(
                patron
            )


            resultado = {
                "estado": "NUEVA_CATEGORIA",
                "categoria": indice + 1,
                "similitud": 1.0,
                "activacion": 1.0,
                "vigilancia": self.vigilancia,
                "patron": list(patron),
                "prototipo": list(
                    self.prototipos[indice]
                ),
                "categorias": len(
                    self.prototipos
                ),
                "categorias_reseteadas": [],
                "saturada": False,
            }


            self.ultimo_resultado = (
                resultado
            )


            return resultado


        # ==================================
        # COMPETENCIA
        # ==================================

        candidatas = (
            self.categorias_por_competencia(
                patron
            )
        )


        categorias_reseteadas = []


        # ==================================
        # PROBAR CATEGORÍAS
        #
        # Si una no cumple rho:
        #
        # RESET
        #
        # y se prueba la siguiente.
        # ==================================

        for candidata in candidatas:

            indice = candidata[
                "indice"
            ]

            similitud = candidata[
                "similitud"
            ]

            activacion = candidata[
                "activacion"
            ]


            prototipo_anterior = list(
                self.prototipos[
                    indice
                ]
            )


            # ==============================
            # ¿SUPERA VIGILANCIA?
            # ==============================

            if (
                similitud
                >=
                self.vigilancia
            ):

                # ==========================
                # RESONANCIA
                #
                # El patrón pertenece a
                # esta categoría.
                # ==========================

                nuevo_prototipo = [

                    entrada & memoria

                    for entrada, memoria
                    in zip(
                        patron,
                        prototipo_anterior
                    )

                ]


                self.prototipos[
                    indice
                ] = nuevo_prototipo


                resultado = {

                    "estado":
                        "RESONANCIA",

                    "categoria":
                        indice + 1,

                    "similitud":
                        similitud,

                    "activacion":
                        activacion,

                    "vigilancia":
                        self.vigilancia,

                    "patron":
                        list(patron),

                    "prototipo_anterior":
                        prototipo_anterior,

                    "prototipo":
                        list(
                            nuevo_prototipo
                        ),

                    "categorias":
                        len(
                            self.prototipos
                        ),

                    "categorias_reseteadas":
                        categorias_reseteadas,

                    "saturada":
                        False,
                }


                self.ultimo_resultado = (
                    resultado
                )


                return resultado


            # ==============================
            # RESET
            #
            # Esta categoría ganó la
            # competencia, pero no se parece
            # lo suficiente.
            #
            # Se inhibe y se prueba otra.
            # ==============================

            categorias_reseteadas.append(
                indice + 1
            )


        # ==================================
        # NINGUNA CATEGORÍA RESONÓ
        #
        # El patrón representa un concepto
        # suficientemente diferente.
        # ==================================

        nueva = self.crear_categoria(
            patron
        )


        mejor = candidatas[0]


        # ==================================
        # SATURACIÓN
        # ==================================

        if nueva is None:

            resultado = {

                "estado":
                    "SATURADA",

                "categoria":
                    None,

                "similitud":
                    mejor[
                        "similitud"
                    ],

                "activacion":
                    mejor[
                        "activacion"
                    ],

                "vigilancia":
                    self.vigilancia,

                "patron":
                    list(patron),

                "prototipo":
                    None,

                "categorias":
                    len(
                        self.prototipos
                    ),

                "categorias_reseteadas":
                    categorias_reseteadas,

                "saturada":
                    True,
            }


            self.ultimo_resultado = (
                resultado
            )


            return resultado


        # ==================================
        # CREAR NUEVA CATEGORÍA
        # ==================================

        resultado = {

            "estado":
                "NUEVA_CATEGORIA",

            "categoria":
                nueva + 1,

            # Mostramos qué tan similar era
            # respecto a la mejor categoría
            # anterior.

            "similitud":
                mejor[
                    "similitud"
                ],

            "activacion":
                mejor[
                    "activacion"
                ],

            "vigilancia":
                self.vigilancia,

            "patron":
                list(patron),

            "prototipo":
                list(
                    self.prototipos[
                        nueva
                    ]
                ),

            "categorias":
                len(
                    self.prototipos
                ),

            "categorias_reseteadas":
                categorias_reseteadas,

            "saturada":
                False,
        }


        self.ultimo_resultado = (
            resultado
        )


        return resultado