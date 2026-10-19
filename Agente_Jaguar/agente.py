
import random

from Algoritmos.a_Estrella import AEstrella
#from Algoritmos.huida import Huida
from Algoritmos.persecucion import Persecucion
from Agente_Jaguar.memoria import MemoriaJaguar
from Algoritmos.genetica_jaguar import elegir_accion_genetica_jaguar,DESPLAZAMIENTOS


class AgenteJaguar:

    def __init__(self, mundo):

        self.mundo = mundo

        # Detección del cazador
        self.rango_deteccion = 4

        # Movimiento cuando está tranquilo
        self.probabilidad_merodear = 0.35

        # Memoria para evitar ciclos de movimiento
        self.posiciones_recientes = []
        self.max_posiciones_recientes = 4
        self.celdas_visitadas = set()
        self.cazador_anterior = None

        # Memoria independiente del Jaguar
        self.memoria = MemoriaJaguar()
        self.cazador_anterior = None

        # Hambre
        self.hambre = 0
        self.hambre_max = 100
        self.aumento_hambre = 2
        self.estado_hambre = "NORMAL"

        # Caza de ratones
        self.rango_olfato_ratones = 6
        self.saciedad_raton = 50

        # Ataque al cazador
        self.energia_debil_cazador = 30
        self.rango_ataque = 8
        self.atacando = False
        self.retirada = 0
        self.decisiones_retirada = 6

        # Estado del mundo
        mundo.jaguar_peligroso = False
        mundo.jaguar_atacando = False

        self.estado = "Descansando"



    # ==========================================
    # POSICIÓN
    # ==========================================

    @property
    def posicion(self):
        return self.mundo.posicion_jaguar

    # ==========================================
    # DISTANCIA ORTOGONAL
    # No considera movimientos diagonales
    # ==========================================

    @staticmethod
    def distancia_ortogonal(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # ==========================================
    # VECINOS ORTOGONALES
    # ==========================================

    def vecinos_ortogonales(self, posicion=None):

        if posicion is None:
            posicion = self.posicion

        fila, columna = posicion

        candidatos = [
            (fila - 1, columna),
            (fila + 1, columna),
            (fila, columna - 1),
            (fila, columna + 1)
        ]

        # El mundo valida los obstáculos y límites.
        # Además comprobamos que solo avance una casilla.
        vecinos_validos = self.mundo.vecinos_validos(
            posicion
        )

        permitidos = []

        for vecino in vecinos_validos:

            if vecino not in candidatos:
                continue

            if self.distancia_ortogonal(
                posicion, vecino
            ) != 1:
                continue

            permitidos.append(vecino)

        return permitidos

        

    # ==========================================
    # MEMORIA DE POSICIONES
    # ==========================================

    def recordar_posicion(self, posicion=None):

        if posicion is None:
            posicion = self.posicion

        if (
            not self.posiciones_recientes
            or self.posiciones_recientes[-1] != posicion
        ):
            self.posiciones_recientes.append(posicion)

        self.posiciones_recientes = (
            self.posiciones_recientes[
                -self.max_posiciones_recientes:
            ]
        )

    # ==========================================
    # ELEGIR ESCAPE SIN REPETIR MOVIMIENTOS
    # ==========================================

    def elegir_escape_sin_bucle(
        self,
        posicion_cazador
    ):

        opciones = self.vecinos_ortogonales()

        if not opciones:
            return None

        # Primero intenta no regresar a las
        # últimas casillas visitadas.
        alternativas = [
            vecino
            for vecino in opciones
            if vecino not in self.posiciones_recientes
        ]

        if alternativas:
            opciones = alternativas

        # Escoge la casilla que más lo aleje
        # del cazador usando distancia ortogonal.
        distancias = {
            vecino: self.distancia_ortogonal(
                vecino,
                posicion_cazador
            )
            for vecino in opciones
        }

        distancia_maxima = max(distancias.values())

        mejores = [
            vecino
            for vecino in opciones
            if distancias[vecino] == distancia_maxima
        ]

        return random.choice(mejores)

    # ==========================================
    # ACTUALIZAR HAMBRE
    # ==========================================

    def actualizar_hambre(self):

        self.hambre = min(
            self.hambre + self.aumento_hambre,
            self.hambre_max
        )

        self.actualizar_nivel_hambre()

    def actualizar_nivel_hambre(self):

        if self.hambre >= 80:
            self.estado_hambre = "HAMBRE INDOMABLE"

        elif self.hambre >= 40:
            self.estado_hambre = "HAMBRIENTO"

        else:
            self.estado_hambre = "NORMAL"

    # ==========================================
    # TOMAR DECISIÓN
    # ==========================================

    def tomar_decision(
        self,
        posicion_cazador,
        energia_cazador=100,
        ratones=None
    ):

        if not self.mundo.jaguar_vivo:
            return None

        self.actualizar_hambre()

        if ratones is None:
            ratones = []

        ratones_vivos = [
            raton
            for raton in ratones
            if getattr(raton, "vivo", False)
        ]

        distancia = self.distancia_ortogonal(
            self.posicion,
            posicion_cazador
        )

        posicion_anterior = self.posicion

        destino = self.decidir(
            posicion_cazador,
            energia_cazador,
            ratones_vivos,
            distancia
        )

        # Solo permitir un paso ortogonal.
        # Evita saltos y diagonales.
        if destino is not None:

            self.recordar_posicion(posicion_anterior)

            self.mundo.mover_jaguar(destino)

            # Si al llegar pisa una baya (tipo 5 o 6), se la come y limpia la celda para liberar espacio
            tipo_suelo = self.mundo.grid.get(destino, 0)
            if tipo_suelo in (5, 6):
                self.hambre = max(0, self.hambre - 35)
                self.actualizar_nivel_hambre()
                self.mundo.grid[destino] = 0  # La baya desaparece y la casilla queda libre
                self.estado = "¡Comió una baya al pasar!"

            return destino

        # ==========================================
        # MOVIMIENTO Y LIMPIZA DE TERRENO (BAYAS)
        # ==========================================
        if destino is not None:

            self.recordar_posicion(posicion_anterior)
            
            # Guardar en celdas visitadas para evitar dar vueltas
            self.celdas_visitadas.add(destino)

            # Mover físicamente al jaguar en el mundo
            self.mundo.mover_jaguar(destino)

            # Si al llegar pisa una baya (tipo 5 o 6), se la come y limpia la celda
            tipo_suelo = self.mundo.grid.get(destino, 0)
            if tipo_suelo in (5, 6):
                self.hambre = max(0, self.hambre - 35)
                self.actualizar_nivel_hambre()

                self.mundo.grid[destino] = 0
                self.memoria.olvidar_baya(destino)

                self.estado = "¡Comió una baya al pasar!"

        return destino

    # ==========================================
    # TOMAR DECISIÓN SEGÚN SU ESTADO
    # ==========================================

    # ==========================================
    # TOMAR DECISIÓN (VERSIÓN CORREGIDA Y UNIFICADA)
    # ==========================================

    def tomar_decision(
        self,
        posicion_cazador,
        energia_cazador=100,
        ratones=None
    ):
        if not self.mundo.jaguar_vivo:
            return None

        self.actualizar_hambre()

        if ratones is None:
            ratones = []

        ratones_vivos = [
            raton
            for raton in ratones
            if getattr(raton, "vivo", False)
        ]

        distancia = self.distancia_ortogonal(
            self.posicion,
            posicion_cazador
        )

        posicion_anterior = self.posicion

        destino = self.decidir(
            posicion_cazador,
            energia_cazador,
            ratones_vivos,
            distancia
        )

        # Actualizar estados del mundo antes de mover
        self.cazador_anterior = posicion_cazador
        self.mundo.jaguar_atacando = self.atacando
        self.mundo.jaguar_peligroso = (
            self.atacando
            or self.retirada == self.decisiones_retirada
        )

        # Mover al agente si existe un destino válido
        if destino is not None:
            self.recordar_posicion(posicion_anterior)
            self.celdas_visitadas.add(destino)
            self.mundo.mover_jaguar(destino)

            # Procesar consumo de bayas en la casilla alcanzada
            self.procesar_terreno_jaguar(destino)

        return destino

    # ==========================================
    # TOMAR DECISIÓN SEGÚN SU ESTADO
    # ==========================================

    def decidir(
        self,
        posicion_cazador,
        energia_cazador,
        ratones_vivos,
        distancia
    ):
            # 0. Retirarse después de atacar
            if self.retirada > 0:
                self.retirada -= 1
                self.atacando = False
                self.estado = "Retirándose tras el ataque"
                return self.elegir_escape_inteligente(posicion_cazador)

            # 1. Decidir si puede atacar al cazador
            cazador_debil = energia_cazador < self.energia_debil_cazador
            hambre_indomable = self.hambre >= 80
            alcance = self.rango_ataque if self.atacando else self.rango_deteccion

            if (cazador_debil or hambre_indomable) and distancia <= alcance:
                self.atacando = True
                if cazador_debil:
                    self.estado = "¡Atacando al cazador débil!"
                else:
                    self.estado = "¡Hambre indomable! Atacando"

                meta = Persecucion.punto_intercepcion(
                    self.posicion,
                    posicion_cazador,
                    self.cazador_anterior,
                    self.mundo
                )
                return self.paso_hacia(meta)

            self.atacando = False

            # 2. Si detecta al cazador, huye utilizando escape inteligente
            if distancia <= self.rango_deteccion:
                destino = self.elegir_escape_inteligente(posicion_cazador)

                if destino is None:
                    if distancia <= 2:
                        self.atacando = True
                        self.estado = "¡Acorralado! Contraataca"
                        return self.paso_hacia(posicion_cazador)

                    self.estado = "Acorralado"
                    return None

                self.estado = "Huyendo (Escape Inteligente)"
                return destino

            # 3. Si tiene hambre, busca ratones
            if self.hambre >= 40 and ratones_vivos:
                cercano = min(
                    ratones_vivos,
                    key=lambda raton: self.distancia_ortogonal(
                        self.posicion,
                        raton.posicion
                    )
                )

                distancia_raton = self.distancia_ortogonal(
                    self.posicion,
                    cercano.posicion
                )

                if distancia_raton <= self.rango_olfato_ratones:
                    self.estado = "Cazando ratón"
                    return self.paso_hacia(cercano.posicion)

                self.estado = "Buscando ratones"
                return self.merodear(cruzar_arena=True)

            # 4. Si está tranquilo, puede descansar o merodear
            if random.random() > self.probabilidad_merodear:
                self.estado = "Descansando"
                return None

            self.estado = "Merodeando"
            return self.merodear()


    

    # ==========================================
    # DAR UN PASO HACIA UNA META USANDO A*
    # ==========================================

    def paso_hacia(self, meta):

        if meta is None or meta == self.posicion:
            return None

        camino = AEstrella.buscar(
            self.posicion,
            meta,
            self.mundo
        )

        if not camino:
            return None

        # Elegir únicamente el primer paso del camino.
        siguiente = camino[0]

        # Evitar que un camino devuelva una diagonal.
        if siguiente not in self.vecinos_ortogonales():
                return None

        return siguiente

    # ==========================================
    # MERODEAR SIN DIAGONALES NI CICLOS
    # ==========================================

    def merodear(self, cruzar_arena=False):
        opciones = self.vecinos_ortogonales()

        if not cruzar_arena:
            opciones = [
                vecino
                for vecino in opciones
                if self.mundo.grid.get(vecino, 0) != 4
            ]

        # Evitar el campamento
        opciones = [
            vecino
            for vecino in opciones
            if vecino != self.mundo.campamento
        ]

        if not opciones:
            return None

        # Priorizar casillas que NO haya visitado en su historial general o reciente
        no_visitadas = [
            vecino
            for vecino in opciones
            if vecino not in self.celdas_visitadas and vecino not in self.posiciones_recientes
        ]

        if no_visitadas:
            opciones = no_visitadas
        else:
            # Si ya visitó todas, al menos evitar las estrictamente recientes
            alternativas = [
                vecino
                for vecino in opciones
                if vecino not in self.posiciones_recientes
            ]
            if alternativas:
                opciones = alternativas

        return random.choice(opciones)

    # ==========================================
    # COMER UN RATÓN
    # ==========================================

    def comer_raton(self):

        self.hambre = max(
            0,
            self.hambre - self.saciedad_raton
        )

        self.actualizar_nivel_hambre()

        self.estado = "¡Comió un ratón!"

    # ==========================================
    # DESPUÉS DE ATACAR AL CAZADOR
    # ==========================================

    def despues_de_atacar(self):

        self.atacando = False
        self.retirada = self.decisiones_retirada

        self.hambre = max(
            0,
            self.hambre - 40
        )

        self.actualizar_nivel_hambre()

        self.mundo.jaguar_peligroso = True
        self.mundo.jaguar_atacando = False

        self.estado = "¡Atacó al cazador!"


# ==========================================
    # REGISTRAR POSICIÓN Y MEMORIA DEL ENTORNO
    # ==========================================

    def recordar_posicion(self, posicion=None):
        if posicion is None:
            posicion = self.posicion
        self.memoria.recordar_posicion(posicion)

    def actualizar_memoria_entorno(self):
        # Escanea los vecinos inmediatos para registrar bayas o arena
        for vecino in self.vecinos_ortogonales():
            tipo = self.mundo.grid.get(vecino, 0)
            self.memoria.registrar_terreno(vecino, tipo)

    # ==========================================
    # COMER BAYAS (Alimento del Jaguar)
    # ==========================================

    def procesar_terreno_jaguar(self, posicion):
        tipo = self.mundo.grid.get(posicion, 0)
        
        # Si la casilla tiene cualquier tipo de baya (5 o 6), el jaguar se la come
        if tipo in (5, 6):
            self.hambre = max(0, self.hambre - 35)
            self.actualizar_nivel_hambre()
            
            # La baya desaparece del mundo y se convierte en terreno libre (0) para hacer espacio
            self.mundo.grid[posicion] = 0
            self.memoria.olvidar_baya(posicion)
            
            self.estado = "¡Comió una baya para abrir paso!"

    # ==========================================
    # ESCAPE INTELIGENTE (Prioriza la vida ante todo)
    # ==========================================

    
    def elegir_escape_inteligente(self, posicion_cazador):
        self.actualizar_memoria_entorno()
        opciones = self.vecinos_ortogonales()

        if not opciones:
            return None

        distancia_actual = self.distancia_ortogonal(
            self.posicion, posicion_cazador
        )

        # Se considera acorralado cuando el cazador está muy cerca.
        acorralado = distancia_actual <= 2

        # Primero se buscan casillas que no sean arena movediza.
        opciones_seguras = [
            vecino for vecino in opciones
            if self.mundo.grid.get(vecino, 0) != 4
            and vecino not in self.memoria.memoria_arena
            and vecino != posicion_cazador
        ]

        # Si hay una salida segura, evita la arena.
        # Si está acorralado, puede considerar todas las opciones.
        if opciones_seguras and not acorralado:
            opciones = opciones_seguras
        else:
            opciones = [
                vecino for vecino in opciones
                if vecino != posicion_cazador
            ]

        if not opciones:
            return None

        mejor_opcion = None
        mejor_puntaje = -float("inf")

        for vecino in opciones:
            distancia_cazador = self.distancia_ortogonal(
                vecino, posicion_cazador
            )

            # La prioridad principal es alejarse del cazador.
            puntaje = distancia_cazador * 30

            tipo_suelo = self.mundo.grid.get(vecino, 0)
            es_arena = (
                tipo_suelo == 4
                or vecino in self.memoria.memoria_arena
            )

            # La arena es un último recurso.
            if es_arena:
                if acorralado:
                    puntaje -= 5
                else:
                    puntaje -= 100

            # Las bayas ayudan a recuperar hambre.
            if tipo_suelo in (5, 6):
                puntaje += 25

            # Evita regresar a posiciones recientes si es posible.
            if vecino in self.memoria.posiciones_recientes:
                puntaje -= 10

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_opcion = vecino

        return mejor_opcion
