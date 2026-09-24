from Agente_Cazador.memoria import Memoria
from Agente_Cazador.sentidos import Sentidos

from Algoritmos.a_Estrella import AEstrella


class AgenteCazador:

    def __init__(self, mundo):

        # ==========================================
        # MUNDO
        # ==========================================

        self.mundo = mundo

        self.posicion = (
            mundo.inicio_cazador
        )


        # ==========================================
        # ENERGÍA
        # ==========================================

        self.energia_max = 100

        self.energia = (
            self.energia_max
        )


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


        # ==========================================
        # ESTADO
        # ==========================================

        self.estado = (
            "Buscando al Puma"
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
    # LIMPIAR INFORMACIÓN DEL PUMA
    # ==========================================

    def limpiar_informacion_puma(self):

        # Olvidar última posición conocida

        self.memoria.olvidar_puma()


        # Cancelar objetivo anterior

        self.memoria.objetivo_busqueda = None


        # Cancelar ruta

        self.ruta_planeada = []


        # Limpiar sentidos

        self.sentidos.ve_puma = False

        self.sentidos.escucha_puma = False

        self.sentidos.direccion_sonido = None

        self.sentidos.objetivo_sonido = None

        self.sentidos.huele_puma = False

        self.sentidos.intensidad_olor = None

        self.sentidos.objetivo_olor = None


    # ==========================================
    # CAZAR PUMA
    # ==========================================

    def comprobar_caza_puma(
        self,
        posicion_puma
    ):

        # Si ya fue cazado, no hacemos nada

        if not self.mundo.puma_vivo:

            return False


        # Para cazarlo ambos deben estar
        # exactamente en la misma celda

        if self.posicion == posicion_puma:

            self.mundo.cazar_puma()

            self.limpiar_informacion_puma()

            self.estado = (
                "¡Puma cazado! "
                "Continuando exploración"
            )

            return True


        return False


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
        # ORDENAR POR DISTANCIA
        # ==========================================

        candidatas.sort(

            key=lambda posicion:

            AEstrella.heuristica(
                self.posicion,
                posicion
            )

        )


        # ==========================================
        # BUSCAR UNA CELDA
        # A LA QUE REALMENTE PUEDA LLEGAR
        # ==========================================

        for candidata in candidatas:

            camino = AEstrella.buscar(

                self.posicion,

                candidata,

                self.mundo

            )


            if camino:

                return candidata


        return None


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

        self.sentidos.usar_tacto(
            posicion
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


            # La baya desaparece

            self.mundo.grid[
                posicion
            ] = 0


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


            # La baya desaparece

            self.mundo.grid[
                posicion
            ] = 0


    # ==========================================
    # PERCIBIR PUMA
    # ==========================================

    def percibir_puma(
        self,
        posicion_puma
    ):

        # ==========================================
        # PUMA TODAVÍA VIVO
        # ==========================================

        if self.mundo.puma_vivo:

            # ======================================
            # VISTA
            # ======================================

            percepcion_visual = (
                self.sentidos.usar_vista(

                    self.posicion,

                    posicion_puma

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
            # ¿VIO AL PUMA?
            # ======================================

            puma_visible = (
                percepcion_visual[
                    "detectado"
                ]
            )


            # ======================================
            # RECORDAR POSICIÓN
            # ======================================

            if puma_visible:

                self.memoria.recordar_puma(
                    posicion_puma
                )


            # ======================================
            # OÍDO
            # ======================================

            puma_escuchado = (
                self.sentidos.usar_oido(

                    self.posicion,

                    posicion_puma

                )
            )


            # ======================================
            # OLFATO
            # ======================================

            puma_olido = (
                self.sentidos.usar_olfato(

                    self.posicion,

                    posicion_puma

                )
            )


            return (
                puma_visible,
                puma_escuchado,
                puma_olido
            )


        # ==========================================
        # PUMA YA CAZADO
        # ==========================================

        # Aunque no exista el puma,
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


        # No puede detectar un puma muerto

        self.sentidos.ve_puma = False

        self.sentidos.escucha_puma = False

        self.sentidos.direccion_sonido = None

        self.sentidos.objetivo_sonido = None

        self.sentidos.huele_puma = False

        self.sentidos.intensidad_olor = None

        self.sentidos.objetivo_olor = None


        return (
            False,
            False,
            False
        )


    # ==========================================
    # TOMAR DECISIÓN
    # ==========================================

    def tomar_decision(
        self,
        posicion_puma
    ):

        # Limpiar ruta anterior

        self.ruta_planeada = []


        # ==========================================
        # 1. COMPROBAR ENERGÍA
        # ==========================================

        if self.energia <= 0:

            self.estado = (
                "Murió de agotamiento"
            )

            return


        # ==========================================
        # 2. COMPROBAR SI YA ESTÁ
        # SOBRE EL PUMA
        # ==========================================

        if (
            self.mundo.puma_vivo
            and
            self.posicion == posicion_puma
        ):

            self.comprobar_caza_puma(
                posicion_puma
            )


        # ==========================================
        # 3. UTILIZAR SENTIDOS
        # ==========================================

        (
            puma_visible,
            puma_escuchado,
            puma_olido
        ) = self.percibir_puma(
            posicion_puma
        )


        # ==========================================
        # 4. POCA ENERGÍA
        # ==========================================

        if self.energia < 30:

            meta = (
                self.mundo.campamento
            )


            self.estado = (
                "Regresando al campamento"
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


        # ==========================================
        # 5. VE AL PUMA
        # ==========================================

        elif (
            self.mundo.puma_vivo
            and
            puma_visible
        ):

            meta = (
                posicion_puma
            )


            self.estado = (
                "¡Puma detectado! Persiguiendo"
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
            self.mundo.puma_vivo
            and
            puma_escuchado
        ):

            meta = (
                self.sentidos
                .objetivo_sonido
            )


            self.estado = (

                "Escuchó al Puma hacia "

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
            self.mundo.puma_vivo
            and
            puma_olido
            and
            self.sentidos.objetivo_olor
            is not None
        ):

            meta = (
                self.sentidos
                .objetivo_olor
            )


            self.estado = (

                "Siguiendo el rastro del Puma "

                f"({self.sentidos.intensidad_olor})"

            )


            self.memoria.objetivo_busqueda = (
                None
            )


        # ==========================================
        # 7. RECUERDA AL PUMA
        # ==========================================

        elif (
            self.mundo.puma_vivo
            and
            self.memoria
            .ultima_posicion_puma
            is not None
        ):

            ultima = (
                self.memoria
                .ultima_posicion_puma
            )


            # ======================================
            # TODAVÍA NO LLEGA
            # ======================================

            if self.posicion != ultima:

                meta = ultima


                self.estado = (
                    "Investigando última "
                    "posición del Puma"
                )


            # ======================================
            # LLEGÓ Y EL PUMA NO ESTÁ
            # ======================================

            else:

                self.memoria.olvidar_puma()


                self.memoria.objetivo_busqueda = (
                    None
                )


                self.estado = (
                    "El Puma ya no está aquí. "
                    "Continuando búsqueda"
                )


                meta = (
                    self.seleccionar_objetivo_busqueda()
                )


                if meta is None:

                    return


        # ==========================================
        # 8. EXPLORACIÓN
        #
        # También entra aquí cuando
        # el puma ya fue cazado.
        # ==========================================

        else:

            if self.mundo.puma_vivo:

                self.estado = (
                    "Buscando zonas no revisadas"
                )

            else:

                self.estado = (
                    "Puma cazado. "
                    "Explorando la selva"
                )


            # ======================================
            # CREAR OBJETIVO
            # ======================================

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
        # 9. YA ESTÁ EN LA META
        # ==========================================

        if self.posicion == meta:

            self.memoria.objetivo_busqueda = (
                None
            )

            return


        # ==========================================
        # 10. CALCULAR CAMINO CON A*
        # ==========================================

        camino = AEstrella.buscar(

            self.posicion,

            meta,

            self.mundo

        )


        # ==========================================
        # 11. NO EXISTE CAMINO
        # ==========================================

        if not camino:

            self.estado = (
                "No existe ruta disponible"
            )


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
        # 13. COMPROBAR POSICIÓN
        # ==========================================

        if not self.mundo.es_transitable(
            siguiente_posicion
        ):

            self.estado = (
                "Movimiento bloqueado"
            )

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


            # ======================================
            # 15. PROCESAR TERRENO
            # ======================================

            self.procesar_terreno(
                siguiente_posicion
            )


            # ======================================
            # 16. COMPROBAR SI CAZÓ AL PUMA
            # ======================================

            if (
                self.mundo.puma_vivo
                and
                self.posicion == posicion_puma
            ):

                self.comprobar_caza_puma(
                    posicion_puma
                )