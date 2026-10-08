from Agente_Cazador.memoria import Memoria
from Agente_Cazador.sentidos import Sentidos, PLURAL_COLORES

from Algoritmos.a_Estrella import AEstrella
from Algoritmos.persecucion import Persecucion

from Algoritmos.genetico import (
    elegir_accion_genetica,
    DESPLAZAMIENTOS
)


class AgenteCazador:

    # Cuánto vale cada casilla nueva que vería
    # al explorar, comparado con el costo de
    # caminar (2 por casilla de pasto)

    PESO_TERRENO_NUEVO = 1

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

        # La casilla inicial cuenta como pisada

        self.memoria.visitas[
            self.posicion
        ] = 1


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


        self.mundo.cazar_jaguar()

        self.limpiar_informacion_jaguar()

        self.estado = (
            "¡Jaguar cazado! "
            "Regresando a la cabaña"
        )

        return True


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
    # TOMAR DECISIÓN
    # ==========================================

    def tomar_decision(
        self,
        posicion_jaguar
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
        # SOBRE EL JAGUAR
        # ==========================================

        if (
            self.mundo.jaguar_vivo
            and
            self.posicion == posicion_jaguar
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


            # ======================================
            # ¿HAY COMIDA MÁS CERCA
            # QUE EL CAMPAMENTO?
            # ======================================

            baya = (
                self.buscar_baya_recordada()
            )


            if baya is not None:

                meta = baya

                self.estado = (
                    "Poca energía: "
                    "va por bayas que recuerda"
                )


            elif (

                self.sentidos.huele_bayas

                and

                self.sentidos.objetivo_olor_bayas
                is not None

                and

                AEstrella.heuristica(
                    self.posicion,
                    self.mundo.campamento
                )
                >
                self.sentidos.rango_olfato_bayas

            ):

                meta = (
                    self.sentidos
                    .objetivo_olor_bayas
                )

                self.estado = (
                    "Poca energía: "
                    "siguiendo olor dulce"
                )


        # ==========================================
        # 5. VE AL JAGUAR
        # ==========================================

        elif (
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

                self.mundo

            )


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

                adelanto=2

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

            self.estado = (
                "Buscando zonas no revisadas"
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
        # 10. DECISIÓN MEDIANTE ALGORITMO GENÉTICO
        # ==========================================

        accion_genetica = elegir_accion_genetica(
            mundo=self.mundo,
            posicion_inicial=self.posicion,
            posicion_objetivo=meta
        )


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


        # ==========================================
        # SI EL AG ENCONTRÓ UN MOVIMIENTO VÁLIDO
        # ==========================================

        if (
            siguiente_posicion_genetica is not None
            and
            self.mundo.es_transitable(
                siguiente_posicion_genetica
            )
        ):

            print(
                "[AG]",
                "Posición:",
                self.posicion,
                "| Meta:",
                meta,
                "| Acción:",
                accion_genetica,
                "| Siguiente:",
                siguiente_posicion_genetica
            )

            camino = [
                siguiente_posicion_genetica
            ]

            self.estado += (
                " | Decisión genética: "
                f"{accion_genetica}"
            )


        # ==========================================
        # RESPALDO CON A*
        #
        # Si el AG no produce una acción válida,
        # utilizamos el sistema anterior.
        # ==========================================

        else:

            camino = AEstrella.buscar(
                self.posicion,
                meta,
                self.mundo,
                self.memoria.bayas_malas,
                self.memoria.visitas
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
