class Memoria:

    def __init__(self):

        # Celdas que el cazador ya observó
        self.celdas_revisadas = set()

        # Última posición donde vio realmente al puma
        self.ultima_posicion_puma = None

        # Lugar que actualmente está investigando
        self.objetivo_busqueda = None

        # Terreno que el cazador ya conoce
        # (lo vio o lo sintió con el tacto)
        self.arena_conocida = set()

        # Bayas que ha visto: posición -> color
        # La vista solo distingue el color,
        # no sabe si son buenas o malas.
        self.bayas_vistas = {}

        # Lo que ha aprendido al probarlas
        # con el gusto: "buena", "mala" o
        # None si todavía no la prueba.
        self.conocimiento_bayas = {
            "morada": None,
            "roja": None
        }


    # ==========================================
    # REGISTRAR CELDAS OBSERVADAS
    # ==========================================

    def registrar_celdas(self, celdas):

        for celda in celdas:

            self.celdas_revisadas.add(celda)


    # ==========================================
    # RECORDAR AL PUMA
    # ==========================================

    def recordar_puma(self, posicion):

        self.ultima_posicion_puma = posicion


    # ==========================================
    # OLVIDAR POSICIÓN ANTIGUA DEL PUMA
    # ==========================================

    def olvidar_puma(self):

        self.ultima_posicion_puma = None


    # ==========================================
    # COMPROBAR SI UNA CELDA YA FUE VISTA
    # ==========================================

    def fue_revisada(self, posicion):

        return posicion in self.celdas_revisadas


    # ==========================================
    # REINICIAR EXPLORACIÓN
    # ==========================================

    def reiniciar_exploracion(self, celdas_actuales=None):

        self.celdas_revisadas.clear()

        if celdas_actuales:

            self.registrar_celdas(
                celdas_actuales
            )

        self.objetivo_busqueda = None


    # ==========================================
    # REGISTRAR TERRENO
    #
    # observacion: "arena", "morada", "roja",
    # "arbol" o "libre"
    # ==========================================

    def registrar_terreno(self, posicion, observacion):

        # Si ya no hay baya, se olvida

        self.bayas_vistas.pop(posicion, None)


        if observacion in self.conocimiento_bayas:

            self.bayas_vistas[posicion] = observacion

        elif observacion == "arena":

            self.arena_conocida.add(posicion)


    # ==========================================
    # OLVIDAR BAYA
    # (cuando se la come)
    # ==========================================

    def olvidar_baya(self, posicion):

        self.bayas_vistas.pop(posicion, None)


    # ==========================================
    # APRENDER DE UNA BAYA
    #
    # Después de probarla, recuerda si ese
    # color es bueno o malo.
    # Devuelve True si es algo nuevo.
    # ==========================================

    def aprender_baya(self, color, resultado):

        if color not in self.conocimiento_bayas:

            return False


        es_nuevo = (
            self.conocimiento_bayas[color]
            != resultado
        )

        self.conocimiento_bayas[color] = resultado

        return es_nuevo


    # ==========================================
    # COLORES QUE YA SABE QUE SON BUENOS
    # ==========================================

    def colores_buenos(self):

        return {
            color
            for color, resultado in self.conocimiento_bayas.items()
            if resultado == "buena"
        }


    # ==========================================
    # BAYAS BUENAS QUE RECUERDA
    # (solo de colores que ya probó)
    # ==========================================

    @property
    def bayas_buenas(self):

        return {
            posicion
            for posicion, color in self.bayas_vistas.items()
            if self.conocimiento_bayas[color] == "buena"
        }


    # ==========================================
    # BAYAS MALAS QUE RECUERDA
    # (solo de colores que ya probó)
    # ==========================================

    @property
    def bayas_malas(self):

        return {
            posicion
            for posicion, color in self.bayas_vistas.items()
            if self.conocimiento_bayas[color] == "mala"
        }
