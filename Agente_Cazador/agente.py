from collections import deque

from Agente_Cazador.memoria import Memoria
from Agente_Cazador.sentidos import Sentidos, PLURAL_COLORES

from Algoritmos.a_Estrella import AEstrella
from Algoritmos.persecucion import Persecucion
from Algoritmos.huida import Huida

from Algoritmos.genetico import (
    elegir_accion_genetica,
    DESPLAZAMIENTOS
)

from Logica_Difusa.variables import DISTANCIA

#GIMEL COMMIT PRUEBA
class AgenteCazador:

    # Cuánto vale cada casilla nueva que vería
    # al explorar, comparado con el costo de
    # caminar (2 por casilla de pasto)

    PESO_TERRENO_NUEVO = 1

    def __init__(self, mundo, controlador=None):

        # ==========================================
        # MUNDO
        # ==========================================

        self.mundo = mundo


        # ==========================================
        # CONTROL DIFUSO (MAMDANI)
        #
        # Es el que decide QUÉ hacer en cada turno:
        # huir, recargar, explorar, perseguir o
        # atacar. Si no le pasan uno, usa el del
        # agente activo del orquestador (DIOS).
        # ==========================================

        if controlador is None:

            from Logica_Difusa.dios import controlador_por_defecto

            controlador = controlador_por_defecto("cazador")

        self.controlador = controlador

        # Última decisión difusa: acción, x* y
        # las reglas que más pesaron

        self.decision_difusa = None

        self.posicion = (
            mundo.inicio_cazador
        )

        # Recordar las últimas posiciones para evitar
        # que el cazador vaya y vuelva entre dos casillas.
        self.ultimas_posiciones = deque(
            [self.posicion],
            maxlen=6
        )


        # ==========================================
        # ENERGÍA
        # ==========================================

        self.energia_max = 100

        self.energia = (
            self.energia_max
        )


        # ==========================================
        # VIDA
        #
        # El jaguar puede atacarlo cuando invierte
        # los papeles. Si lo alcanza, lo caza y el
        # juego termina (una sola vida).
        # ==========================================

        self.vidas_max = 1

        self.vidas = self.vidas_max

        self.dano_ataque = 30


        # ==========================================
        # AUTOCONCIENCIA
        #
        # El agente sabe:
        # - qué percibe con cada sentido y cuál
        #   usó para decidir
        # - cuánto pesa y qué tan rápido puede ir
        #   (su cuerpo físico)
        # - qué acciones ha tomado (bitácora)
        # - si tiene un problema al decidir, y
        #   reacciona
        # ==========================================

        # Cuerpo físico (lo asigna la interfaz)

        self.cuerpo = None

        # Número de decisión

        self.turno = 0

        # Lo que percibe ahora con cada sentido

        self.percepcion = {}

        # Sentido (o motivo) que causó la
        # última decisión

        self.sentido_usado = "ninguno"

        # Meta y motivo de la última decisión

        self.meta_actual = None

        self.fallo_decision = None

        self.motivo = ""

        # Última acción: ARRIBA, ABAJO, ...,
        # o QUIETO

        self.ultima_accion = "QUIETO"

        # Quién decidió el paso: "AG", "A*",
        # "ataque directo" o "-"

        self.fuente_decision = "-"

        # Últimas 40 decisiones

        self.bitacora = deque(
            maxlen=40
        )

        # Problema detectado (None si no hay)

        self.problema_actual = None

        # Contadores para detectar problemas

        self.turnos_sin_moverse = 0

        self.fallos_seguidos = 0

        # Reacción a problemas: metas que
        # descarta por unos turnos

        self.metas_descartadas = {}


        # ==========================================
        # PREMIOS Y CASTIGOS
        #
        # Buena decisión del AG: +1 de batería
        # El AG propone chocar: -2 de batería
        # Cazar al jaguar: +30 de batería
        # Ser atacado: -10 puntos
        # ==========================================

        self.puntos = 0

        self.premio_buena_decision = 1

        self.castigo_choque = 2

        self.premio_cazar = 30

        # El AG propuso chocar en esta decisión

        self.choque_ag = False

        # Texto del último premio o castigo

        self.ultimo_premio = ""


        # ==========================================
        # SENTIDOS
        # ==========================================

        # Los valores de rango de vista, oído y olfato
        # se encuentran únicamente en sentidos.py

        self.sentidos = Sentidos(
            mundo
        )

        
        # ==========================================
        # MEMORIA
        # ==========================================

        self.memoria = Memoria()

        # La casilla inicial cuenta como pisada

        self.memoria.visitas[
            self.posicion
        ] = 1

        self.turno_ultima_percepcion_jaguar = None
        self.ultimo_peligro_percibido = 0.0     

        
        # ==========================================
        # ESTADO
        # ==========================================

        self.estado = (
            "Buscando al Jaguar"
        )


        # ==========================================
        # RUTA PLANEADA
        # ==========================================

        self.ruta_planeada = []


    # ==========================================
    # FILA
    # ==========================================

    @property
    def fila(self):

        return self.posicion[0]


    # ==========================================
    # COLUMNA
    # ==========================================

    @property
    def columna(self):

        return self.posicion[1]


    # ==========================================
    # LIMPIAR INFORMACIÓN DEL JAGUAR
    # ==========================================

    def limpiar_informacion_jaguar(self):

        # Olvidar última posición conocida

        self.memoria.olvidar_jaguar()


        # Cancelar objetivo anterior

        self.memoria.objetivo_busqueda = None


        # Cancelar ruta

        self.ruta_planeada = []


        # Limpiar sentidos

        self.sentidos.ve_jaguar = False

        self.sentidos.escucha_jaguar = False

        self.sentidos.direccion_sonido = None

        self.sentidos.intensidad_sonido = None

        self.sentidos.objetivo_sonido = None

        self.sentidos.huele_jaguar = False

        self.sentidos.intensidad_olor = None

        self.sentidos.objetivo_olor = None


    # ==========================================
    # CAZAR JAGUAR
    # ==========================================

    def comprobar_caza_jaguar(
        self,
        posicion_jaguar
    ):

        # Si ya fue cazado, no hacemos nada

        if not self.mundo.jaguar_vivo:

            return False


        # Para cazarlo ambos deben estar
        # exactamente en la misma celda

        if self.posicion == posicion_jaguar:

            return self.atrapar_jaguar()


        return False


    # ==========================================
    # ATRAPAR JAGUAR
    #
    # También se usa cuando el cazador y el
    # jaguar se cruzan en el camino.
    # ==========================================

    def atrapar_jaguar(self):

        if not self.mundo.jaguar_vivo:

            return False


        # Mientras el jaguar lo ataca o se
        # retira después del ataque, no lo
        # puede atrapar

        if getattr(
            self.mundo,
            "jaguar_peligroso",
            False
        ):

            return False


        self.mundo.cazar_jaguar()

        # Premio: cazar al jaguar

        self.energia = min(
            self.energia_max,
            self.energia + self.premio_cazar
        )

        self.puntos += 50

        self.limpiar_informacion_jaguar()

        self.estado = (
            "¡Jaguar cazado! "
            "Regresando a la cabaña"
        )

        return True


    # ==========================================
    # RECIBIR ATAQUE DEL JAGUAR
    # ==========================================

    def recibir_ataque(self):

        self.energia = max(
            0,
            self.energia - self.dano_ataque
        )

        self.vidas = max(
            0,
            self.vidas - 1
        )

        # Castigo: lo atacó el enemigo

        self.puntos -= 10


        if self.vidas == 0:

            self.estado = (
                "¡El jaguar lo cazó! "
                "Fin del juego"
            )

        else:

            self.estado = (
                "¡Atacado por el jaguar! "
                f"Vidas: {self.vidas}"
            )


        # Olvida la ruta que llevaba

        self.ruta_planeada = []


    # ==========================================
    # BUSCAR ZONA NO REVISADA
    # ==========================================

    def seleccionar_objetivo_busqueda(
        self
    ):

        candidatas = []


        # ==========================================
        # BUSCAR CELDAS NO REVISADAS
        # ==========================================

        for posicion, tipo in (
            self.mundo.grid.items()
        ):

            # Los árboles no son transitables

            if tipo == 1:

                continue


            # No elegir bayas malas que recuerda

            if posicion in (
                self.memoria.bayas_malas
            ):

                continue


            # Metas descartadas por un problema
            # (por ejemplo, no tenían ruta)

            if posicion in self.metas_descartadas:

                continue


            # Si ya fue revisada,
            # no necesitamos volver todavía

            if self.memoria.fue_revisada(
                posicion
            ):

                continue


            candidatas.append(
                posicion
            )


        # ==========================================
        # YA REVISÓ TODO EL MAPA
        # ==========================================

        if not candidatas:

            visibles_actuales = (
                self.sentidos
                .obtener_celdas_visibles(
                    self.posicion
                )
            )


            # Reiniciar exploración

            self.memoria.reiniciar_exploracion(
                visibles_actuales
            )


            # Volver a buscar candidatas

            for posicion, tipo in (
                self.mundo.grid.items()
            ):

                if tipo == 1:

                    continue


                if posicion in (
                    self.memoria.bayas_malas
                ):

                    continue


                if posicion in self.metas_descartadas:

                    continue


                if self.memoria.fue_revisada(
                    posicion
                ):

                    continue


                candidatas.append(
                    posicion
                )


        # ==========================================
        # NO HAY CANDIDATAS
        # ==========================================

        if not candidatas:

            return None


        # ==========================================
        # EXPLORACIÓN POR FRONTERAS
        #
        # 1. Con una sola búsqueda calcula cuánto
        #    le cuesta llegar a cada casilla
        #    (suelo, bayas malas y casillas que
        #    ya pisó cuestan más).
        # 2. A cada candidata le resta cuántas
        #    casillas nuevas vería desde ahí.
        # 3. Elige la de menor puntaje: cerca,
        #    sin repetir camino y que descubra
        #    mucho terreno.
        # ==========================================

        costos = AEstrella.costos_desde(

            self.posicion,

            self.mundo,

            self.memoria.bayas_malas,

            self.memoria.visitas

        )


        mejor = None

        mejor_puntaje = None


        for candidata in candidatas:

            # No puede llegar

            if candidata not in costos:

                continue


            puntaje = (

                costos[candidata]

                -

                self.PESO_TERRENO_NUEVO
                *
                self.terreno_nuevo_desde(
                    candidata
                )

            )


            if (
                mejor_puntaje is None
                or
                puntaje < mejor_puntaje
            ):

                mejor = candidata

                mejor_puntaje = puntaje


        return mejor


    # ==========================================
    # TERRENO NUEVO DESDE UNA CASILLA
    #
    # Cuántas casillas que todavía no ha
    # revisado vería si estuviera ahí.
    # ==========================================

    def terreno_nuevo_desde(
        self,
        posicion
    ):

        rango = self.sentidos.rango_vista

        fila, columna = posicion

        nuevas = 0


        for df in range(-rango, rango + 1):

            for dc in range(-rango, rango + 1):

                celda = (
                    fila + df,
                    columna + dc
                )


                if (

                    self.mundo.dentro_limites(
                        celda
                    )

                    and

                    not self.memoria.fue_revisada(
                        celda
                    )

                    and

                    self.sentidos.puede_ver(
                        posicion,
                        celda
                    )

                ):

                    nuevas += 1


        return nuevas


    # ==========================================
    # PROCESAR TERRENO
    # ==========================================

    def procesar_terreno(
        self,
        posicion
    ):

        tipo = self.mundo.grid[
            posicion
        ]


        # ==========================================
        # TACTO
        # ==========================================

        _, arena_vecina = (
            self.sentidos.usar_tacto(
                posicion
            )
        )


        # Recordar la arena que sintió
        # alrededor, antes de pisarla

        for celda in arena_vecina:

            self.memoria.registrar_terreno(
                celda,
                "arena"
            )


        # ==========================================
        # GASTAR ENERGÍA
        # ==========================================

        # Arena movediza

        if tipo == 4:

            self.energia -= 8


        # Terreno normal / bayas

        else:

            self.energia -= 2


        self.energia = max(
            0,
            self.energia
        )


        # ==========================================
        # GUSTO
        # ==========================================

        # Antes de comerla, ve de qué color es

        color = (
            self.sentidos.observar(
                posicion
            )
        )


        # ==========================================
        # YA SABE QUE ESE COLOR ES MALO:
        # NO SE LA COME
        #
        # Puede pasar por encima, pero la deja
        # donde está.
        # ==========================================

        if (
            self.memoria.conocimiento_bayas.get(
                color
            )
            == "mala"
        ):

            self.sentidos.sensacion_gusto = (
                f"No come bayas "
                f"{PLURAL_COLORES[color]}"
            )

            return


        alimento = (
            self.sentidos.usar_gusto(
                posicion
            )
        )


        # ==========================================
        # BAYA BUENA
        # ==========================================

        if alimento == "baya_buena":

            self.energia += 20


            self.energia = min(

                self.energia,

                self.energia_max

            )


            self.estado = (
                "Bayas buenas: +20 energía"
            )


            # ======================================
            # APRENDE QUE ESE COLOR ES BUENO
            # ======================================

            if self.memoria.aprender_baya(
                color,
                "buena"
            ):

                self.estado = (
                    f"¡Aprendió: bayas {PLURAL_COLORES[color]} "
                    "son buenas! (+20)"
                )


            # La baya desaparece

            self.mundo.grid[
                posicion
            ] = 0

            self.memoria.olvidar_baya(
                posicion
            )


        # ==========================================
        # BAYA MALA
        # ==========================================

        elif alimento == "baya_mala":

            self.energia -= 10


            self.energia = max(

                0,

                self.energia

            )


            self.estado = (
                "Bayas malas: -10 energía"
            )


            # ======================================
            # APRENDE QUE ESE COLOR ES MALO
            # ======================================

            if self.memoria.aprender_baya(
                color,
                "mala"
            ):

                self.estado = (
                    f"¡Aprendió: bayas {PLURAL_COLORES[color]} "
                    "son malas! (-10)"
                )


            # La baya desaparece

            self.mundo.grid[
                posicion
            ] = 0

            self.memoria.olvidar_baya(
                posicion
            )


    # ==========================================
    # BUSCAR BAYA BUENA RECORDADA
    #
    # Solo la elige si está más cerca
    # que el campamento.
    # ==========================================

    def buscar_baya_recordada(self):

        if not self.memoria.bayas_buenas:

            return None


        camino_campamento = AEstrella.buscar(

            self.posicion,

            self.mundo.campamento,

            self.mundo,

            self.memoria.bayas_malas

        )


        mejor = None

        mejor_largo = None


        for baya in (
            self.memoria.bayas_buenas
        ):

            if baya == self.posicion:

                continue


            camino = AEstrella.buscar(

                self.posicion,

                baya,

                self.mundo,

                self.memoria.bayas_malas

            )


            if not camino:

                continue


            if (
                mejor_largo is None
                or
                len(camino) < mejor_largo
            ):

                mejor = baya

                mejor_largo = len(camino)


        if mejor is None:

            return None


        # Si el campamento está más cerca,
        # mejor ir al campamento

        if (
            camino_campamento
            and
            len(camino_campamento)
            <=
            mejor_largo
        ):

            return None


        return mejor


        # ==========================================
    # BUSCAR BAYA DESCONOCIDA
    #
    # El cazador puede investigar una baya
    # cuyo color todavía no haya probado.
    # ==========================================

    def buscar_baya_desconocida(self):

        candidatas = []


        # ======================================
        # BAYAS QUE HA VISTO
        # ======================================

        for posicion, color in (
            self.memoria.bayas_vistas.items()
        ):

            conocimiento = (
                self.memoria
                .conocimiento_bayas
                .get(color)
            )


            # Solo queremos colores desconocidos

            if conocimiento is None:

                candidatas.append(
                    posicion
                )


        if not candidatas:

            return None


        # ======================================
        # BUSCAR LA MÁS CERCANA
        # ======================================

        mejor = None
        mejor_largo = None


        for baya in candidatas:

            camino = AEstrella.buscar(
                self.posicion,
                baya,
                self.mundo,
                self.memoria.bayas_malas,
                self.memoria.visitas
            )


            if not camino:

                continue


            if (
                mejor_largo is None
                or
                len(camino) < mejor_largo
            ):

                mejor = baya
                mejor_largo = len(camino)


        return mejor

        # ==========================================
    # ENERGÍA NECESARIA PARA REGRESAR
    # AL CAMPAMENTO
    # ==========================================

    def energia_para_regresar(self):

        if self.posicion == self.mundo.campamento:

            return 0


        camino = AEstrella.buscar(
            self.posicion,
            self.mundo.campamento,
            self.mundo,
            self.memoria.bayas_malas,
            {}
        )


        # Si por alguna razón no encuentra ruta,
        # usamos una reserva conservadora.

        if not camino:

            return 30


        energia_necesaria = 0


        for posicion in camino:

            tipo = self.mundo.grid[
                posicion
            ]


            if tipo == 4:

                # Arena movediza
                energia_necesaria += 8

            else:

                # Suelo normal / bayas
                energia_necesaria += 2


        return energia_necesaria
    
    # ==========================================
    # PERCIBIR JAGUAR
    # ==========================================


    def percibir_jaguar(
        self,
        posicion_jaguar
    ):

        # ==========================================
        # JAGUAR TODAVÍA VIVO
        # ==========================================

        if self.mundo.jaguar_vivo:

            # ======================================
            # VISTA
            # ======================================

            percepcion_visual = (
                self.sentidos.usar_vista(

                    self.posicion,

                    posicion_jaguar

                )
            )


            # ======================================
            # MEMORIA DE CELDAS OBSERVADAS
            # ======================================

            self.memoria.registrar_celdas(

                percepcion_visual[
                    "celdas_visibles"
                ]

            )


            # ======================================
            # MEMORIA DEL TERRENO QUE VE
            # (bayas buenas, bayas malas, arena)
            # ======================================

            for celda, observacion in (
                percepcion_visual[
                    "terreno"
                ].items()
            ):

                self.memoria.registrar_terreno(
                    celda,
                    observacion
                )


            # ======================================
            # ¿VIO AL JAGUAR?
            # ======================================

            jaguar_visible = (
                percepcion_visual[
                    "detectado"
                ]
            )


            # ======================================
            # RECORDAR POSICIÓN
            # ======================================

            if jaguar_visible:

                self.memoria.recordar_jaguar(
                    posicion_jaguar
                )


            # ======================================
            # OÍDO
            # ======================================

            jaguar_escuchado = (
                self.sentidos.usar_oido(

                    self.posicion,

                    posicion_jaguar

                )
            )


            # ======================================
            # OLFATO
            # ======================================

            jaguar_olido = (
                self.sentidos.usar_olfato(

                    self.posicion,

                    posicion_jaguar

                )
            )


            return (
                jaguar_visible,
                jaguar_escuchado,
                jaguar_olido
            )


        # ==========================================
        # JAGUAR YA CAZADO
        # ==========================================

        # Aunque no exista el jaguar,
        # el cazador sigue viendo el entorno.

        celdas_visibles = (
            self.sentidos
            .obtener_celdas_visibles(
                self.posicion
            )
        )


        self.memoria.registrar_celdas(
            celdas_visibles
        )


        for celda in celdas_visibles:

            self.memoria.registrar_terreno(
                celda,
                self.sentidos.observar(
                    celda
                )
            )


        # No puede detectar un jaguar muerto

        self.sentidos.ve_jaguar = False

        self.sentidos.escucha_jaguar = False

        self.sentidos.direccion_sonido = None

        self.sentidos.intensidad_sonido = None

        self.sentidos.objetivo_sonido = None

        self.sentidos.huele_jaguar = False

        self.sentidos.intensidad_olor = None

        self.sentidos.objetivo_olor = None


        return (
            False,
            False,
            False
        )


        # ==========================================
    # ACTUALIZAR HAMBRE
    # ==========================================

    def actualizar_hambre(self):

        self.hambre += self.aumento_hambre

        self.hambre = min(
            self.hambre,
            self.hambre_max
        )

    # ==========================================
    # TOMAR DECISIÓN (CON AUTOCONCIENCIA)
    #
    # 1. Revisa lo que percibe y su cuerpo.
    # 2. Decide y actúa (decidir_y_actuar).
    # 3. Registra lo que hizo en la bitácora.
    # 4. Revisa si tuvo un problema y, si lo
    #    hay, reacciona.
    # ==========================================

    def tomar_decision(
        self,
        posicion_jaguar
    ):

        self.turno += 1

        posicion_antes = self.posicion

        energia_antes = self.energia

        self.meta_actual = None

        self.motivo = ""

        # Lo marca decidir_y_actuar si la ruta
        # falla ("sin ruta" o "bloqueado")

        self.fallo_decision = None

        self.choque_ag = False

        self.ultimo_premio = ""


        # Las metas descartadas vuelven a
        # considerarse después de unos turnos

        for meta in list(self.metas_descartadas):

            self.metas_descartadas[meta] -= 1

            if self.metas_descartadas[meta] <= 0:

                del self.metas_descartadas[meta]


        # ==========================================
        # DECIDIR Y ACTUAR
        # ==========================================

        self.decidir_y_actuar(
            posicion_jaguar
        )


        # ==========================================
        # CONCIENCIA DE SUS SENTIDOS
        # ==========================================

        self.percepcion = self.resumen_sentidos()

        self.sentido_usado = self.sentido_de_la_decision()


        # ==========================================
        # CONCIENCIA DE SUS ACCIONES
        # ==========================================

        self.ultima_accion = self.nombre_accion(
            posicion_antes,
            self.posicion
        )

        if self.posicion != posicion_antes:

            resultado = "avanzó"

        elif self.fallo_decision is not None:

            resultado = self.fallo_decision

        else:

            resultado = "quieto"


        # ==========================================
        # ¿TUVO UN PROBLEMA?
        # ==========================================

        self.problema_actual = self.detectar_problema(
            resultado
        )


        if self.problema_actual is not None:

            self.reaccionar_a_problema()


        # ==========================================
        # PREMIOS Y CASTIGOS
        # ==========================================

        self.aplicar_premios(
            resultado
        )


        # ==========================================
        # BITÁCORA
        # ==========================================

        self.bitacora.append({

            "turno": self.turno,
            "desde": posicion_antes,
            "hasta": self.posicion,
            "accion": self.ultima_accion,
            "meta": self.meta_actual,
            "motivo": (
                self.motivo
                or self.estado
            ).split("|")[0].strip(),
            "sentido": self.sentido_usado,
            "fuente": self.fuente_decision,
            "resultado": resultado,
            "energia": (
                energia_antes,
                self.energia
            ),
            "problema": self.problema_actual,
            "premio": self.ultimo_premio,
            "difuso": (
                self.decision_difusa["explicacion"]
                if self.decision_difusa
                else ""
            )

        })


    # ==========================================
    # PREMIOS Y CASTIGOS
    #
    # Como en otros proyectos, el premio es más
    # batería (energía) y el castigo es perderla.
    # ==========================================

    def aplicar_premios(self, resultado):

        premios = []


        # Castigo: el AG propuso chocar

        if self.choque_ag:

            self.energia = max(
                0,
                self.energia - self.castigo_choque
            )

            self.puntos -= self.castigo_choque

            premios.append(
                f"-{self.castigo_choque} batería (chocó)"
            )


        # Premio: buena decisión del AG (el paso
        # es válido y lo acerca a su meta)

        if (
            resultado == "avanzó"
            and
            self.fuente_decision == "AG"
        ):

            self.energia = min(
                self.energia_max,
                self.energia + self.premio_buena_decision
            )

            self.puntos += self.premio_buena_decision

            premios.append(
                f"+{self.premio_buena_decision} batería "
                "(buena decisión)"
            )


        self.ultimo_premio = ", ".join(premios)


    # ==========================================
    # RESUMEN DE LO QUE PERCIBE
    # ==========================================

    def resumen_sentidos(self):

        sentidos = self.sentidos


        if sentidos.ve_jaguar:

            vista = "jaguar a la vista"

        else:

            vista = "nada"


        if sentidos.escucha_jaguar:

            oido = (
                f"jaguar al {sentidos.direccion_sonido}"
            )

        else:

            oido = "nada"


        if sentidos.huele_jaguar:

            olfato = "olor a jaguar"

        elif sentidos.huele_bayas:

            olfato = "olor a bayas"

        else:

            olfato = "nada"


        return {

            "vista": vista,
            "oido": oido,
            "olfato": olfato,
            "tacto": sentidos.sensacion_tacto,
            "gusto": sentidos.sensacion_gusto

        }


    # ==========================================
    # ¿QUÉ SENTIDO CAUSÓ LA DECISIÓN?
    # ==========================================

    def sentido_de_la_decision(self):

        motivo = self.motivo or self.estado


        if (
            "ataca" in motivo
            or
            "Acorralado" in motivo
            or
            "Acechando" in motivo
        ):

            return "percepción del enemigo"

        if (
            "detectado" in motivo
            or
            "alcance" in motivo
        ):

            return "vista"

        if "Escuchó" in motivo:

            return "oído"

        if "rastro" in motivo:

            return "olfato"

        if (
            "huyó" in motivo
            or
            "Investigando" in motivo
            or
            "Buscando zonas" in motivo
        ):

            return "memoria"

        if (
            "energía" in motivo.lower()
            or
            "campamento" in motivo
            or
            "cabaña" in motivo
        ):

            return "energía"

        if "baya" in motivo.lower():

            return "memoria / gusto"

        return "ninguno"


    # ==========================================
    # NOMBRE DE LA ACCIÓN
    # ==========================================

    @staticmethod
    def nombre_accion(desde, hasta):

        cambio = (
            hasta[0] - desde[0],
            hasta[1] - desde[1]
        )

        nombres = {

            (-1, 0): "ARRIBA",
            (1, 0): "ABAJO",
            (0, -1): "IZQUIERDA",
            (0, 1): "DERECHA"

        }

        return nombres.get(
            cambio,
            "QUIETO"
        )


    # ==========================================
    # CONCIENCIA DE SU CUERPO (PESO)
    #
    # Con su masa y su fuerza calcula qué tan
    # rápido puede ir en cada suelo y cuánto
    # tardaría en recorrer un camino.
    # ==========================================

    def conciencia_fisica(self):

        if self.cuerpo is None:

            return None


        return {

            "masa": self.cuerpo.masa,
            "fuerza": self.cuerpo.fuerza_motriz,
            "velocidad": self.cuerpo.velocidad,
            "v_max_pasto": self.cuerpo.velocidad_maxima(0),
            "v_max_arena": self.cuerpo.velocidad_maxima(4)

        }


    def tiempo_estimado(self, camino):

        # Segundos para recorrer un camino,
        # según su velocidad máxima en cada
        # suelo (depende de su masa)

        if self.cuerpo is None or not camino:

            return None


        from Fisica.cinematica import (
            METROS_POR_CASILLA
        )


        segundos = 0.0

        for casilla in camino:

            segundos += (
                METROS_POR_CASILLA
                /
                self.cuerpo.velocidad_maxima(
                    self.mundo.grid[casilla]
                )
            )

        return segundos


    def tiempo_a_la_cabana(self):

        camino = AEstrella.buscar(
            self.posicion,
            self.mundo.campamento,
            self.mundo,
            self.memoria.bayas_malas,
            {}
        )

        if self.posicion == self.mundo.campamento:

            return 0.0

        return self.tiempo_estimado(
            camino
        )


    # ==========================================
    # IMPRIMIR SU AUTOCONCIENCIA (tecla B)
    # ==========================================

    def imprimir_conciencia(self, ultimas=10):

        print()
        print("========== AUTOCONCIENCIA DEL CAZADOR ==========")


        print("Sentidos:")

        for sentido, valor in self.percepcion.items():

            print(f"   {sentido:7s}: {valor}")


        fisica = self.conciencia_fisica()

        if fisica is not None:

            print(
                f"Cuerpo: {fisica['masa']} kg, "
                f"fuerza {fisica['fuerza']} N, "
                f"velocidad {fisica['velocidad']:.2f} m/s "
                f"(máx. {fisica['v_max_pasto']:.2f} en pasto, "
                f"{fisica['v_max_arena']:.2f} en arena)"
            )

            tiempo = self.tiempo_a_la_cabana()

            if tiempo is not None:

                print(
                    f"Tardaría {tiempo:.1f} s en llegar "
                    "a la cabaña"
                )


        print(
            f"Energía: {self.energia}  "
            f"Vidas: {self.vidas}/{self.vidas_max}  "
            f"Puntos: {self.puntos}"
        )

        print(
            f"Problema actual: "
            f"{self.problema_actual or 'ninguno'}"
        )

        if self.metas_descartadas:

            print(
                "Metas descartadas: "
                f"{sorted(self.metas_descartadas)}"
            )


        print(
            f"Control difuso: "
            f"{self.controlador.base.nombre}"
        )

        print(f"Últimas {ultimas} decisiones:")

        for registro in list(self.bitacora)[-ultimas:]:

            print(
                f"   #{registro['turno']:4d} "
                f"{registro['accion']:9s} "
                f"{registro['desde']}->{registro['hasta']} "
                f"meta {registro['meta']} | "
                f"{registro['motivo'][:38]} | "
                f"sentido: {registro['sentido']} | "
                f"{registro['fuente']} | "
                f"{registro['resultado']}"
                + (
                    f" | PROBLEMA: {registro['problema']}"
                    if registro["problema"]
                    else ""
                )
                + (
                    f" | {registro['premio']}"
                    if registro.get("premio")
                    else ""
                )
                + (
                    f"\n          difuso: {registro['difuso']}"
                    if registro.get("difuso")
                    else ""
                )
            )

        print("================================================")


    # ==========================================
    # CASILLAS QUE NO DEBE USAR COMO META
    # ==========================================

    def casillas_prohibidas(self):

        return (
            set(self.memoria.bayas_malas)
            |
            set(self.metas_descartadas)
        )


    # ==========================================
    # CASILLA VECINA ALCANZABLE
    # ==========================================

    def vecina_alcanzable(self, meta):

        prohibidas = self.casillas_prohibidas()

        opciones = [

            vecina

            for vecina in self.mundo.vecinos_validos(
                meta
            )

            if vecina not in prohibidas

        ]


        # La más cercana a la que sí haya camino

        opciones.sort(
            key=lambda vecina:
            AEstrella.heuristica(
                self.posicion,
                vecina
            )
        )


        for vecina in opciones:

            if vecina == self.posicion:

                return vecina

            if AEstrella.buscar(
                self.posicion,
                vecina,
                self.mundo,
                self.memoria.bayas_malas,
                {}
            ):

                return vecina


        return None


    # ==========================================
    # DETECTAR PROBLEMAS AL DECIDIR
    # ==========================================

    def detectar_problema(self, resultado):

        # Situaciones normales en las que no
        # moverse no es un problema

        terminado = (
            self.vidas <= 0
            or
            "Murió" in self.estado
            or
            "misión cumplida" in self.estado
            or
            "Energía recuperada" in self.estado
        )


        if resultado == "avanzó":

            self.turnos_sin_moverse = 0

        elif not terminado:

            self.turnos_sin_moverse += 1


        if resultado in ("sin ruta", "bloqueado"):

            self.fallos_seguidos += 1

        else:

            self.fallos_seguidos = 0


        if terminado:

            return None


        # Sin ruta hacia su meta

        if resultado == "sin ruta":

            return "sin ruta"


        # No pudo dar el paso

        if resultado == "bloqueado":

            return "bloqueado"


        # Lleva varios turnos sin moverse

        if self.turnos_sin_moverse >= 6:

            return "atascado"


        # Va y viene entre dos casillas:
        # A -> B -> A -> B

        recientes = [
            registro["hasta"]
            for registro in list(self.bitacora)[-3:]
        ] + [self.posicion]


        # Solo es un problema si va y viene con
        # la MISMA meta. Si la meta se mueve (por
        # ejemplo, el jaguar huye en zigzag),
        # seguirla no es un error.

        metas = [
            registro["meta"]
            for registro in list(self.bitacora)[-3:]
        ] + [self.meta_actual]


        if (
            len(recientes) == 4
            and
            recientes[0] == recientes[2]
            and
            recientes[1] == recientes[3]
            and
            recientes[0] != recientes[1]
            and
            len(set(metas)) == 1
        ):

            return "dando vueltas"


        return None


    # ==========================================
    # REACCIONAR A UN PROBLEMA
    # ==========================================

    def reaccionar_a_problema(self):

        problema = self.problema_actual


        # Sin ruta o bloqueado: descarta esa meta
        # por 15 turnos y busca otra

        if problema in ("sin ruta", "bloqueado"):

            if self.meta_actual is not None:

                self.metas_descartadas[
                    self.meta_actual
                ] = 15

            self.memoria.objetivo_busqueda = None


        # Atascado: cambia de zona de búsqueda

        elif problema == "atascado":

            if self.memoria.objetivo_busqueda is not None:

                self.metas_descartadas[
                    self.memoria.objetivo_busqueda
                ] = 15

            self.memoria.objetivo_busqueda = None

            self.turnos_sin_moverse = 0


        # Dando vueltas con la misma meta:
        # descarta esa meta y busca otra

        elif problema == "dando vueltas":

            if self.meta_actual is not None:

                self.metas_descartadas[
                    self.meta_actual
                ] = 15

            self.memoria.objetivo_busqueda = None


    # ==========================================
    # CALCULAR NIVEL DE PELIGRO
    # ==========================================

    def calcular_peligro(
        self,
        jaguar_percibido,
        posicion_amenaza
    ):

        # Si el Jaguar ya no está vivo,
        # no existe peligro.

        if not self.mundo.jaguar_vivo:

            self.turno_ultima_percepcion_jaguar = None
            self.ultimo_peligro_percibido = 0.0

            return 0.0


        # Si no conoce ninguna posición del Jaguar,
        # no tiene información suficiente para
        # calcular peligro.

        if posicion_amenaza is None:

            return 0.0


        # ======================================
        # 1. HAMBRE DEL JAGUAR
        # ======================================

        hambre = getattr(
            self.mundo,
            "hambre_jaguar",
            0
        )

        hambre = max(
            0,
            min(100, hambre)
        )

        peligro_hambre = (
            hambre * 0.40
        )


        # ======================================
        # 2. CERCANÍA DEL JAGUAR
        # ======================================

        distancia = AEstrella.heuristica(
            self.posicion,
            posicion_amenaza
        )

        peligro_cercania = max(
            0,
            40 - distancia * 4
        )


        # ======================================
        # 3. JAGUAR ATACANDO
        # ======================================

        peligro_ataque = (
            30
            if getattr(
                self.mundo,
                "jaguar_atacando",
                False
            )
            else 0
        )


        peligro = (
            peligro_hambre
            +
            peligro_cercania
            +
            peligro_ataque
        )


        # ======================================
        # 4. MEMORIA DEL PELIGRO
        # ======================================

        if jaguar_percibido:

            # Guarda el momento y el nivel
            # de peligro mientras sí percibe
            # al Jaguar.

            self.turno_ultima_percepcion_jaguar = (
                self.turno
            )

            self.ultimo_peligro_percibido = (
                peligro
            )

        else:

            # Nunca ha percibido al Jaguar.

            if self.turno_ultima_percepcion_jaguar is None:

                return 0.0


            turnos_sin_percibir = (
                self.turno
                -
                self.turno_ultima_percepcion_jaguar
            )


            # El recuerdo del peligro dura
            # 6 turnos y disminuye poco a poco.

            factor_memoria = max(
                0.0,
                1.0 - turnos_sin_percibir / 6.0
            )


            peligro = (
                self.ultimo_peligro_percibido
                *
                factor_memoria
            )


        # Mantener siempre el peligro
        # dentro del rango 0 a 100.

        peligro = max(
            0,
            min(100, peligro)
        )


        return round(
            peligro,
            2
        )

    # ==========================================
    # DECISIÓN DIFUSA
    #
    # Prepara las 3 entradas del controlador
    # difuso y le pregunta qué hacer:
    #
    #   reserva   = energía - energía para volver
    #   distancia = casillas hasta el jaguar (o
    #               hasta donde lo vio); 30 si no
    #               sabe nada
    #   peligro   = 100 si el jaguar lo ataca, su
    #               hambre si lo percibe, 0 si no
    #               lo percibe
    #
    # Regresa la acción y la posición del
    # jaguar que conoce (o None).
    # ==========================================

    def entradas_difusas(
        self,
        posicion_jaguar,
        jaguar_percibido,
        energia_regreso
    ):

        if not self.mundo.jaguar_vivo:

            posicion_amenaza = None

        elif jaguar_percibido:

            posicion_amenaza = posicion_jaguar

        else:

            posicion_amenaza = (
                self.memoria.ultima_posicion_jaguar
            )


        if posicion_amenaza is None:

            distancia = DISTANCIA.maximo

        else:

            distancia = AEstrella.heuristica(
                self.posicion,
                posicion_amenaza
            )


        peligro = self.calcular_peligro(
            jaguar_percibido,
            posicion_amenaza
        )

        entradas = {
            "reserva": max(0, self.energia - energia_regreso),
            "distancia": distancia,
            "peligro": peligro,
        }

        return entradas, posicion_amenaza


    def decidir_difuso(
        self,
        posicion_jaguar,
        jaguar_percibido,
        energia_regreso
    ):

        entradas, posicion_amenaza = self.entradas_difusas(
            posicion_jaguar,
            jaguar_percibido,
            energia_regreso
        )

        accion, x_estrella = self.controlador.decidir(
            entradas
        )

        explicacion = self.controlador.explicar()


        # Si las reglas dicen "huir" pero no sabe
        # dónde está el jaguar, no tiene de qué
        # huir: sigue explorando

        if accion == "huir" and posicion_amenaza is None:

            accion = "explorar"

            explicacion += " (huir sin saber dónde está el jaguar -> explorar)"


        self.decision_difusa = {
            "accion": accion,
            "x": x_estrella,
            "entradas": entradas,
            "explicacion": explicacion,
        }

        return accion, posicion_amenaza


    # ==========================================
    # DECIDIR Y ACTUAR
    # ==========================================

    def decidir_y_actuar(
        self,
        posicion_jaguar
    ):

        # Limpiar ruta anterior

        self.ruta_planeada = []
        self.fuente_decision = "-"

        # ==========================================
        # 0. SIN VIDAS: YA NO SE MUEVE
        # ==========================================

        if self.vidas <= 0:

            self.estado = (
                "¡El jaguar lo cazó! "
                "Fin del juego"
            )

            return


        # ==========================================
        # 1. COMPROBAR ENERGÍA
        # ==========================================

        if self.energia <= 0:

            # Si alcanzó el campamento justo
            # con la última energía, sobrevive.

            if (
                self.posicion
                ==
                self.mundo.campamento
            ):

                self.energia = (
                    self.energia_max
                )

                self.estado = (
                    "Energía recuperada"
                )

            else:

                self.estado = (
                    "Murió de agotamiento"
                )

                return


        # ==========================================
        # 2. COMPROBAR SI YA ESTÁ
        # SOBRE EL JAGUAR
        # ==========================================

        if (
            self.mundo.jaguar_vivo
            and
            self.posicion == posicion_jaguar
            and
            self.modo_difuso_actual == "atacar"
        ):

            self.comprobar_caza_jaguar(
                posicion_jaguar
            )


        # ==========================================
        # 3. UTILIZAR SENTIDOS
        # ==========================================

        (
            jaguar_visible,
            jaguar_escuchado,
            jaguar_olido
        ) = self.percibir_jaguar(
            posicion_jaguar
        )


        # Olfato de bayas dulces

        self.sentidos.usar_olfato_bayas(
            self.posicion,
            self.memoria.colores_buenos()
        )

        energia_regreso = (
            self.energia_para_regresar()
        )


        jaguar_percibido = (
            jaguar_visible
            or
            jaguar_escuchado
            or
            jaguar_olido
        )


        # ==========================================
        # 4. DECISIÓN DIFUSA (MAMDANI)
        #
        # El controlador difuso decide QUÉ hacer:
        #   huir, recargar, explorar, perseguir
        #   o atacar.
        # Después, el AG de movimiento (o A*)
        # decide CÓMO llegar.
        # ==========================================

        modo, posicion_amenaza = self.decidir_difuso(
            posicion_jaguar,
            jaguar_percibido,
            energia_regreso
        )

        self.modo_difuso_actual = modo


        # Huir solo tiene sentido si sabe dónde
        # está el jaguar

        en_peligro = (
            modo == "huir"
            and
            self.mundo.jaguar_vivo
            and
            posicion_amenaza is not None
        )

        modo_supervivencia = (
            modo == "recargar"
        )

        quiere_cazar = (
            modo in ("perseguir", "atacar")
        )


        if en_peligro:

            escape = Huida.elegir_escape(
                self.posicion,
                posicion_amenaza,
                self.mundo
            )


            # Nunca huye hacia una baya mala

            if escape in self.memoria.bayas_malas:

                escape = None


            if escape is not None:

                meta = escape

                self.estado = (
                    "¡El jaguar lo ataca! Huyendo"
                )

            else:

                meta = self.posicion

                self.estado = (
                    "¡Acorralado por el jaguar!"
                )


        elif modo_supervivencia:

            meta = (
                self.mundo.campamento
            )

            self.estado = (
                "Poca energía: "
                "regresando al campamento"
            )


            # ======================================
            # YA ESTÁ EN EL CAMPAMENTO
            # ======================================

            if self.posicion == meta:

                self.energia = (
                    self.energia_max
                )

                self.estado = (
                    "Energía recuperada"
                )

                self.memoria.objetivo_busqueda = (
                    None
                )

                return


            # ======================================
            # ¿CONOCE UNA BAYA BUENA?
            # ======================================

            baya = (
                self.buscar_baya_recordada()
            )


            if baya is not None:

                meta = baya

                self.estado = (
                    "Poca energía: "
                    "va por una baya buena"
                )


            # ======================================
            # SI NO HAY BAYA BUENA,
            # CONTINUAR AL CAMPAMENTO
            # ======================================

            else:

                meta = (
                    self.mundo.campamento
                )

                self.estado = (
                    "Poca energía: "
                    "regresando al campamento"
                )


        # ==========================================
        # 5. VE AL JAGUAR
        # ==========================================

        elif (
            quiere_cazar
            and
            self.mundo.jaguar_vivo
            and
            jaguar_visible
        ):

            # ======================================
            # PERSECUCIÓN
            #
            # Apunta a donde va a estar el jaguar,
            # no a donde está ahora.
            # ======================================

            meta = Persecucion.punto_intercepcion(

                self.posicion,

                posicion_jaguar,

                self.memoria
                .penultima_posicion_jaguar,

                self.mundo,

                prohibidas=self.casillas_prohibidas()

            )


            # ATACAR (decisión difusa): va directo a
            # donde está el jaguar, sin calcular
            # dónde cortarle el paso

            if modo == "atacar":

                meta = posicion_jaguar

            elif meta == posicion_jaguar:

                meta_persecucion = self.vecina_alcanzable(
                    posicion_jaguar
                )

                if meta_persecucion is not None:

                    meta = meta_persecucion

            if meta == posicion_jaguar:

                self.estado = (
                    "¡Jaguar detectado! Persiguiendo"
                )

            else:

                self.estado = (
                    "¡Jaguar detectado! "
                    "Cortándole el paso"
                )


            # Cancelar búsqueda anterior

            self.memoria.objetivo_busqueda = (
                None
            )


        # ==========================================
        # 6. NO LO VE,
        # PERO LO ESCUCHA
        # ==========================================

        elif (
            quiere_cazar
            and
            self.mundo.jaguar_vivo
            and
            jaguar_escuchado
        ):

            meta = (
                self.sentidos
                .objetivo_sonido
            )


            self.estado = (

                "Escuchó al Jaguar hacia "

                f"{self.sentidos.direccion_sonido}"

            )


            self.memoria.objetivo_busqueda = (
                None
            )


            if meta is None:

                return


        # ==========================================
        # 6.1 NO LO VE NI LO ESCUCHA,
        # PERO LO HUELE
        #
        # Si los árboles bloquean el rastro,
        # sigue explorando.
        # ==========================================

        elif (
            quiere_cazar
            and
            self.mundo.jaguar_vivo
            and
            jaguar_olido
            and
            self.sentidos.objetivo_olor
            is not None
        ):

            meta = (
                self.sentidos
                .objetivo_olor
            )


            self.estado = (

                "Siguiendo el rastro del Jaguar "

                f"({self.sentidos.intensidad_olor})"

            )


            self.memoria.objetivo_busqueda = (
                None
            )


        # ==========================================
        # 7. RECUERDA AL JAGUAR
        # ==========================================

        elif (
            quiere_cazar
            and
            self.mundo.jaguar_vivo
            and
            self.memoria
            .ultima_posicion_jaguar
            is not None
        ):

            # ======================================
            # ¿HACIA DÓNDE SE FUE?
            #
            # Si sabe en qué dirección huía,
            # busca 2 casillas más adelante de
            # donde lo vio por última vez.
            # ======================================

            ultima = Persecucion.punto_intercepcion(

                self.posicion,

                self.memoria
                .ultima_posicion_jaguar,

                self.memoria
                .penultima_posicion_jaguar,

                self.mundo,

                adelanto=2,

                prohibidas=self.casillas_prohibidas()

            )


            # ======================================
            # TODAVÍA NO LLEGA
            # ======================================

            if self.posicion != ultima:

                meta = ultima


                self.estado = (
                    "Siguiendo hacia donde "
                    "huyó el Jaguar"
                )


            # ======================================
            # LLEGÓ Y EL JAGUAR NO ESTÁ
            # ======================================

            else:

                self.memoria.olvidar_jaguar()


                self.memoria.objetivo_busqueda = (
                    None
                )


                self.estado = (
                    "El Jaguar ya no está aquí. "
                    "Continuando búsqueda"
                )


                meta = (
                    self.seleccionar_objetivo_busqueda()
                )


                if meta is None:

                    return


        # ==========================================
        # 7.1 YA CAZÓ AL JAGUAR:
        # REGRESAR A LA CABAÑA
        # ==========================================

        elif not self.mundo.jaguar_vivo:

            meta = (
                self.mundo.campamento
            )


            # ======================================
            # YA LLEGÓ: MISIÓN CUMPLIDA
            # ======================================

            if self.posicion == meta:

                self.energia = (
                    self.energia_max
                )

                self.estado = (
                    "En la cabaña: "
                    "¡misión cumplida!"
                )

                return


            self.estado = (
                "¡Jaguar cazado! "
                "Regresando a la cabaña"
            )


                # ==========================================
        # 8. EXPLORACIÓN
        # ==========================================

        else:

            # ======================================
            # PRIMERO APRENDER DE BAYAS DESCONOCIDAS
            # ======================================

            baya_desconocida = (
                self.buscar_baya_desconocida()
            )


            if baya_desconocida is not None:

                meta = baya_desconocida

                self.estado = (
                    "Investigando una baya desconocida"
                )

                self.memoria.objetivo_busqueda = (
                    None
                )


            # ======================================
            # SI NO HAY BAYAS POR INVESTIGAR,
            # EXPLORACIÓN NORMAL
            # ======================================

            else:

                self.estado = (
                    "Buscando zonas no revisadas"
                )


                if (

                    self.memoria.objetivo_busqueda
                    is None

                    or

                    self.memoria.fue_revisada(

                        self.memoria
                        .objetivo_busqueda

                    )

                ):

                    self.memoria.objetivo_busqueda = (
                        self.seleccionar_objetivo_busqueda()
                    )


                meta = (
                    self.memoria
                    .objetivo_busqueda
                )


                if meta is None:

                    return


        # ==========================================
        # META PROHIBIDA: ACECHAR AL LADO
        #
        # Si la meta es una casilla que no puede
        # pisar (baya mala) o que ya falló, va a
        # la casilla vecina alcanzable más cercana.
        # Por ejemplo, si el jaguar está parado en
        # una baya mala, lo acecha desde al lado.
        # ==========================================

        if meta in self.casillas_prohibidas():

            alternativa = self.vecina_alcanzable(
                meta
            )

            if alternativa is not None:

                meta = alternativa

                self.estado = (
                    "Acechando: su meta está "
                    "en una casilla prohibida"
                )


        # Para la autoconciencia: qué meta eligió
        # y por qué

        self.meta_actual = meta

        self.motivo = self.estado


        # ==========================================
        # 9. YA ESTÁ EN LA META
        # ==========================================

        if self.posicion == meta:

            self.memoria.objetivo_busqueda = (
                None
            )

            return


   
                # ==========================================
        # JAGUAR AL ALCANCE INMEDIATO
        # ==========================================
                # Distancia Manhattan entre el cazador
        # y la posición actual del Jaguar

        distancia_jaguar = (
            abs(
                self.posicion[0]
                -
                posicion_jaguar[0]
            )
            +
            abs(
                self.posicion[1]
                -
                posicion_jaguar[1]
            )
        )

        if (
            self.mundo.jaguar_vivo
            and
            distancia_jaguar == 1
            and
            modo == "atacar"
        ):

            print(
                "[CAZA]",
                "Posición:",
                self.posicion,
                "| Jaguar:",
                posicion_jaguar,
                "| Modo:",
                modo,
                "| Atacando"
            )

            camino = [
                posicion_jaguar
            ]
            self.fuente_decision = "ataque directo"

            self.estado = (
                "¡Jaguar al alcance! Atacando"
            )


        # ==========================================
        # SUPERVIVENCIA: A* OBLIGATORIO
        # ==========================================

        elif modo_supervivencia:

            camino = AEstrella.buscar(
                self.posicion,
                meta,
                self.mundo,
                self.memoria.bayas_malas,
                {}
            )
            self.fuente_decision = "A*"

            print(
                "[SUPERVIVENCIA]",
                "Posición:", self.posicion,
                "| Meta:", meta,
                "| Energía:", self.energia,
                "| Energía regreso:", energia_regreso,
                "| Ruta:",
                camino[:5] if camino else []
            )


        # ==========================================
        # ALGORITMO GENÉTICO
        # ==========================================

        else:

            accion_genetica = elegir_accion_genetica(
                mundo=self.mundo,
                posicion_inicial=self.posicion,
                posicion_objetivo=meta,
                visitas_previas=self.memoria.visitas,
                prohibidas=self.memoria.bayas_malas,

                # PERCEPCIÓN -> AG: dónde percibe al
                # enemigo y si debe evitarlo

                enemigo=(
                    posicion_jaguar
                    if jaguar_percibido
                    else None
                ),
                evitar_enemigo=(
                    jaguar_percibido
                    and
                    getattr(
                        self.mundo,
                        "jaguar_atacando",
                        False
                    )
                )
            )

            # ... todo lo que ya tienes del AG


            siguiente_posicion_genetica = None


            if accion_genetica is not None:

                cambio_fila, cambio_columna = (
                    DESPLAZAMIENTOS[
                        accion_genetica
                    ]
                )


                siguiente_posicion_genetica = (
                    self.posicion[0] + cambio_fila,
                    self.posicion[1] + cambio_columna
                )


            # ¿El AG propuso chocar con un
            # obstáculo (árbol, borde o baya mala)?

            self.choque_ag = (
                siguiente_posicion_genetica is not None
                and
                (
                    not self.mundo.es_transitable(
                        siguiente_posicion_genetica
                    )
                    or
                    siguiente_posicion_genetica
                    in self.memoria.bayas_malas
                )
            )


            # ======================================
            # MOVIMIENTO GENÉTICO VÁLIDO
            # ======================================

            # Costo real de cada casilla hasta la
            # meta (rodeando árboles y bayas
            # malas). Sirve para comprobar que el
            # paso del AG de verdad lo acerca.

            costos_meta = AEstrella.costos_desde(
                meta,
                self.mundo,
                self.memoria.bayas_malas
            )


            acerca = (
                siguiente_posicion_genetica is not None
                and
                costos_meta.get(
                    siguiente_posicion_genetica,
                    float("inf")
                )
                <
                costos_meta.get(
                    self.posicion,
                    float("inf")
                )
            )


            # El paso del AG se acepta solo si es
            # válido Y lo acerca a la meta. Si no,
            # se usa el A*. Así no puede ir y
            # volver entre dos casillas.

            if (
                siguiente_posicion_genetica is not None
                and
                self.mundo.es_transitable(
                    siguiente_posicion_genetica
                )
                and
                siguiente_posicion_genetica
                not in self.memoria.bayas_malas
                and
                acerca
            ):

                tipo_terreno = (
                    self.mundo.grid[
                        siguiente_posicion_genetica
                    ]
                )


                nombres_terreno = {
                    0: "NORMAL",
                    4: "ARENA",
                    5: "BAYA",
                    6: "BAYA"
                }


                print(
                    "[AG]",
                    "Posición:", self.posicion,
                    "| Meta:", meta,
                    "| Acción:", accion_genetica,
                    "| Siguiente:", siguiente_posicion_genetica,
                    "| Terreno:",
                    nombres_terreno.get(
                        tipo_terreno,
                        tipo_terreno
                    ),
                    "| Energía:",
                    self.energia
                )

                camino = [
                    siguiente_posicion_genetica
                ]
                self.fuente_decision = "AG"

                self.estado += (
                    " | Decisión genética: "
                    f"{accion_genetica}"
                )


            # ======================================
            # RESPALDO CON A*
            # ======================================

            else:

                camino = AEstrella.buscar(
                    self.posicion,
                    meta,
                    self.mundo,
                    self.memoria.bayas_malas,
                    self.memoria.visitas
                )

                self.fuente_decision = "A*"


        # ==========================================
        # 11. NO EXISTE CAMINO
        # ==========================================

        if not camino:

            self.estado = (
                "No existe ruta disponible"
            )

            self.fallo_decision = "sin ruta"

            self.memoria.objetivo_busqueda = (
                None
            )

            return

        

        # ==========================================
        # 12. GUARDAR RUTA
        # ==========================================

        self.ruta_planeada = (
            camino
        )


        # El agente avanza una sola celda
        # por cada ciclo de decisión.

        siguiente_posicion = (
            camino[0]
        )


        # ==========================================
        # 12.1 ROMPER BUCLE DE DOS POSICIONES
        # ==========================================
        # Si el siguiente paso nos devuelve a la casilla
        # anterior, buscar otra vecina transitable.

        if (
            len(self.ultimas_posiciones) >= 2
            and
            siguiente_posicion == self.ultimas_posiciones[-2]
        ):

            posicion_anterior = self.ultimas_posiciones[-2]

            alternativas = [
                vecino
                for vecino in self.mundo.vecinos_validos(
                    self.posicion
                )
                if vecino != posicion_anterior
                and self.mundo.es_transitable(vecino)
                and vecino not in self.memoria.bayas_malas
            ]

            if alternativas:
                alternativas.sort(
                    key=lambda vecino: (
                        AEstrella.heuristica(
                            vecino,
                            meta
                        ),
                        self.memoria.visitas.get(
                            vecino,
                            0
                        )
                    )
                )

                siguiente_posicion = alternativas[0]
                self.fuente_decision = "anti-bucle"
                camino = [siguiente_posicion]
                self.ruta_planeada = camino


        # ==========================================
        # 13. COMPROBAR POSICIÓN
        # ==========================================

        if (
            not self.mundo.es_transitable(
                siguiente_posicion
            )
            or
            siguiente_posicion
            in self.memoria.bayas_malas
        ):

            self.estado = (
                "Movimiento bloqueado"
            )

            self.fallo_decision = "bloqueado"

            return


        # ==========================================
        # 14. MOVER CAZADOR
        # ==========================================

        movimiento_valido = (
            self.mundo.mover_cazador(
                siguiente_posicion
            )
        )


        if movimiento_valido:

            self.posicion = (
                siguiente_posicion
            )

            # Guardar la posición alcanzada para detectar
            # un posible regreso inmediato en el próximo turno.
            self.ultimas_posiciones.append(
                self.posicion
            )


            # Contar el paso (y si repite casilla)

            self.memoria.registrar_paso(
                siguiente_posicion
            )


            # ======================================
            # 15. PROCESAR TERRENO
            # ======================================

            self.procesar_terreno(
                siguiente_posicion
            )


            # ======================================
            # 16. COMPROBAR SI CAZÓ AL JAGUAR
            # ======================================

            if (
                self.mundo.jaguar_vivo
                and
                self.posicion == posicion_jaguar
                and
                modo == "atacar"
            ):

                self.comprobar_caza_jaguar(
                    posicion_jaguar
                )


            # ======================================
            # 17. VOLVER A PERCIBIR
            #
            # Después de moverse, usa otra vez
            # la vista, el oído y el olfato desde
            # la casilla nueva. Así todo lo que
            # muestra el panel corresponde a la
            # misma casilla donde está parado.
            # ======================================

            self.percibir_jaguar(
                posicion_jaguar
            )


            self.sentidos.usar_olfato_bayas(
                self.posicion,
                self.memoria.colores_buenos()
            )
