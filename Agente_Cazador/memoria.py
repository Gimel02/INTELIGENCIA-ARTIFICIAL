class Memoria:

    def __init__(self):

        # Celdas que el cazador ya observó
        self.celdas_revisadas = set()

        # Última posición donde vio realmente al puma
        self.ultima_posicion_puma = None

        # Lugar que actualmente está investigando
        self.objetivo_busqueda = None


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