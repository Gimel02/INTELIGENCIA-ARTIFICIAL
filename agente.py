import tkinter as tk
import random
import heapq


# ==========================================
# 1. DEFINICIÓN DEL MUNDO Y TERRENOS
# ==========================================
class MundoSelva:
    def __init__(self, filas=10, columnas=10):
        self.filas = filas
        self.columnas = columnas
        self.grid = {}
        self.generar_mundo()

    def generar_mundo(self):
        # 0: Selva normal       
        # 1: Árboles densos     
        # 4: Arena/Brea         
        # 5: Bayas buenas     
        

        for f in range(self.filas):
            for c in range(self.columnas):

                r = random.random()

                if r < 0.15:
                    self.grid[(f, c)] = 1      #Arbol

                elif r < 0.23:                 #Arena
                    self.grid[(f, c)] = 4      

                elif r < 0.27:
                    self.grid[(f, c)] = 5      # Bayas buenas

                elif r < 0.30:
                    self.grid[(f, c)] = 6      # Bayas malas

                else:
                    self.grid[(f, c)] = 0      # Terreno normal

        self.campamento = self._pos_aleatoria_valida()
        self.inicio_cazador = self.campamento

        self.inicio_puma = self._pos_aleatoria_valida(
              exclude=[self.campamento]
        )

    def _pos_aleatoria_valida(self, exclude=[]):

        while True:

            pos = (
                random.randint(0, self.filas - 1),
                random.randint(0, self.columnas - 1)
            )

            if self.grid[pos] != 1 and pos not in exclude:
                return pos


# ==========================================
# 2. ALGORITMO A*
# ==========================================
class AEstrella:

    @staticmethod
    def heuristica(a, b):

        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def buscar(inicio, objetivo, mapa, limites):

        frontera = []

        heapq.heappush(
            frontera,
            (0, inicio)
        )

        costo_acumulado = {
            inicio: 0
        }

        padres = {
            inicio: None
        }

        filas, columnas = limites

        while frontera:

            _, actual = heapq.heappop(frontera)

            if actual == objetivo:
                break

            vecinos = [
                (actual[0] - 1, actual[1]),
                (actual[0] + 1, actual[1]),
                (actual[0], actual[1] - 1),
                (actual[0], actual[1] + 1)
            ]

            for vecino in vecinos:

                if (
                    0 <= vecino[0] < filas
                    and
                    0 <= vecino[1] < columnas
                ):

                    tipo = mapa[vecino]

                    # Los árboles no se pueden atravesar
                    if tipo == 1:
                        continue

                    # Costos de cada terreno
                    if tipo == 0:
                        costo_mov = 2

                    elif tipo == 4:
                        costo_mov = 8

                    else:
                        costo_mov = 2

                    nuevo_costo = (
                        costo_acumulado[actual]
                        + costo_mov
                    )

                    if (
                        vecino not in costo_acumulado
                        or
                        nuevo_costo < costo_acumulado[vecino]
                    ):

                        costo_acumulado[vecino] = nuevo_costo

                        prioridad = (
                            nuevo_costo
                            + AEstrella.heuristica(
                                vecino,
                                objetivo
                            )
                        )

                        heapq.heappush(
                            frontera,
                            (prioridad, vecino)
                        )

                        padres[vecino] = actual

        # No encontró camino
        if objetivo not in padres:
            return []

        # Construir camino
        camino = []

        actual = objetivo

        while actual != inicio:

            camino.append(actual)

            actual = padres[actual]

        camino.reverse()

        return camino


# ==========================================
# 3. RATONES
# ==========================================
class Raton:

    def __init__(self, pos1, mundo):

        self.pos1 = pos1

        vecinos = [
            (pos1[0] - 1, pos1[1]),
            (pos1[0] + 1, pos1[1]),
            (pos1[0], pos1[1] - 1),
            (pos1[0], pos1[1] + 1)
        ]

        validos = [
            v for v in vecinos

            if
            0 <= v[0] < mundo.filas
            and
            0 <= v[1] < mundo.columnas
            and
            mundo.grid[v] != 1
        ]

        self.pos2 = (
            random.choice(validos)
            if validos
            else pos1
        )

        self.posicion = self.pos1

        self.vivo = True

    def mover(self, pos_puma, mundo):

        if not self.vivo:
            return

        distancia_puma = AEstrella.heuristica(
            self.posicion,
            pos_puma
        )

        # Si el puma está cerca, el ratón huye
        if distancia_puma <= 2:

            vecinos = [
                (self.posicion[0] - 1, self.posicion[1]),
                (self.posicion[0] + 1, self.posicion[1]),
                (self.posicion[0], self.posicion[1] - 1),
                (self.posicion[0], self.posicion[1] + 1)
            ]

            validos = [
                v for v in vecinos

                if
                0 <= v[0] < mundo.filas
                and
                0 <= v[1] < mundo.columnas
                and
                mundo.grid[v] != 1
            ]

            if validos:

                self.posicion = max(
                    validos,
                    key=lambda v:
                    AEstrella.heuristica(
                        v,
                        pos_puma
                    )
                )

        # Si el puma está lejos,
        # se mueve entre sus dos posiciones
        else:

            if self.posicion == self.pos1:
                self.posicion = self.pos2

            else:
                self.posicion = self.pos1


# ==========================================
# 4. PUMA
# ==========================================
class Puma:

    def __init__(self, posicion):

        self.posicion = posicion

        self.vidas = 3

    def cazar(self, ratones, mundo):

        ratones_vivos = [
            r for r in ratones
            if r.vivo
        ]

        if not ratones_vivos:
            return

        # Selecciona al ratón más cercano
        raton_objetivo = min(
            ratones_vivos,
            key=lambda r:
            AEstrella.heuristica(
                self.posicion,
                r.posicion
            )
        )

        camino = AEstrella.buscar(

            self.posicion,

            raton_objetivo.posicion,

            mundo.grid,

            (
                mundo.filas,
                mundo.columnas
            )
        )

        if camino:

            self.posicion = camino[0]

            if self.posicion == raton_objetivo.posicion:

                raton_objetivo.vivo = False

    def huir(self, pos_cazador, mundo):

        vecinos = [
            (self.posicion[0] - 1, self.posicion[1]),
            (self.posicion[0] + 1, self.posicion[1]),
            (self.posicion[0], self.posicion[1] - 1),
            (self.posicion[0], self.posicion[1] + 1)
        ]

        validos = [
            v for v in vecinos

            if
            0 <= v[0] < mundo.filas
            and
            0 <= v[1] < mundo.columnas
            and
            mundo.grid[v] != 1
        ]

        if validos:

            # Busca alejarse lo máximo posible
            self.posicion = max(
                validos,
                key=lambda v:
                AEstrella.heuristica(
                    v,
                    pos_cazador
                )
            )




# ==========================================
# 5. AGENTE CAZADOR
#El cazador fiene dos memorias, una de las celdas que ya reviso y otra de la ultima
#posicion donde vio el puma, si el puma esta dentro de su rango de vision, lo 
#persigue y si no lo ve, sigue buscando en zonas no revisadas. Al inicio el cazador no lo ve
#despues busca en zonas no revisadas, mientras avanza y va guardando las celdas que ya vio.
#despues si el puma entra en el rango, dice puma detectado y guarda la ultima posicion vista del puma
#empieza con el algoritmo A* para perseguirlo y si el puma escapa, el cazador ya no sabe
#donde esta pero recuerda la ultima vez que lo vi estaba aca. cuando llega el puma ya no esta y 
#dice donde no he buscado
# ==========================================
class Cazador:

    def __init__(self, mundo):

        self.mundo = mundo
        self.posicion = mundo.inicio_cazador

        # ==========================
        # ENERGÍA
        # ==========================
        self.energia_max = 100
        self.energia = self.energia_max

        # El terreno completo ya es conocido
        self.mapa_local = self.mundo.grid.copy()

        # ==========================
        # SENTIDO DE LA VISTA 
        # ==========================
        self.rango_vista = 3
        self.ve_puma = False

        # ==========================
        # SENTIDO DEL OÍDO 
        # ==========================
        self.rango_oido = 5
        self.escucha_puma = False
        self.direccion_sonido = None
        self.objetivo_sonido = None

        # ==========================
        # SENTIDO DEL TACTO 
        # ==========================
        self.sensacion_tacto = "Suelo firme"

        # ==========================
        # SENTIDO DEL GUSTO 
        # ==========================
        self.sensacion_gusto = "Sin alimento"
       
        # ==========================
        # MEMORIA 
        # ==========================

        # Celdas que ya fueron observadas
        self.celdas_revisadas = set()

        # Último lugar donde realmente vio al puma
        self.ultima_posicion_puma = None

        # Zona hacia donde está buscando
        self.objetivo_busqueda = None

        # ==========================
        # ESTADO
        # ==========================
        self.estado = "Buscando al Puma "

        self.ruta_planeada = []


    # ==========================================
    # OBTENER CELDAS QUE PUEDE VER
    # ==========================================
    def obtener_celdas_visibles(self):

        visibles = []

        for f in range(self.mundo.filas):

            for c in range(self.mundo.columnas):

                posicion = (f, c)

                distancia = AEstrella.heuristica(
                    self.posicion,
                    posicion
                )

                if distancia <= self.rango_vista:

                    visibles.append(posicion)

        return visibles


    # ==========================================
    # UTILIZAR EL SENTIDO DE LA VISTA 
    # ==========================================
    def usar_vista(self, puma):

        celdas_visibles = self.obtener_celdas_visibles()

        # ======================================
        # MEMORIA:
        # todo lo que acaba de ver se considera
        # una zona ya revisada
        # ======================================
        for celda in celdas_visibles:

            self.celdas_revisadas.add(celda)

        # ======================================
        # ¿EL PUMA ESTÁ DENTRO DE LA VISTA?
        # ======================================
        if puma.posicion in celdas_visibles:

            self.ve_puma = True

            # Guardamos dónde fue visto
            self.ultima_posicion_puma = puma.posicion

            return True

        else:

            self.ve_puma = False

            return False


    #aqui usamos el sentido del oido, si el puma esta dentro del rango del oido
    #el cazador va a escuchar al puma y va a crear un objetivo aproximando hacia
    #donde esta el puma, si el puma esta fuera del rango del oido, el cazador no escucha
    #y no tiene objetivo de sonido
    #aqui se define tipo, viene del norte, sur este o sureste
    def usar_oido(self, puma):

        distancia = AEstrella.heuristica(
            self.posicion,
            puma.posicion
        )

        # Si está demasiado lejos, no escucha nada
        if distancia > self.rango_oido:

            self.escucha_puma = False
            self.direccion_sonido = None
            self.objetivo_sonido = None

            return False

        # Si ya lo está viendo,
        # no necesitamos usar el oído para localizarlo
        if distancia <= self.rango_vista:

            self.escucha_puma = False
            self.direccion_sonido = None
            self.objetivo_sonido = None

            return False

        self.escucha_puma = True

        cazador_f, cazador_c = self.posicion
        puma_f, puma_c = puma.posicion

        diferencia_filas = puma_f - cazador_f
        diferencia_columnas = puma_c - cazador_c

        # ======================================
        # DETERMINAR DIRECCIÓN APROXIMADA
        # ======================================

        if abs(diferencia_filas) >= abs(diferencia_columnas):

            if diferencia_filas < 0:
                self.direccion_sonido = "NORTE"

            else:
                self.direccion_sonido = "SUR"

        else:

            if diferencia_columnas < 0:
                self.direccion_sonido = "OESTE"

            else:
                self.direccion_sonido = "ESTE"

        # Crear un lugar aproximado
        # hacia donde investigar
        self.objetivo_sonido = self.crear_objetivo_sonido()

        return True


    def crear_objetivo_sonido(self):

        f, c = self.posicion

        # Avanzará hasta 3 casillas
        # aproximadamente hacia el sonido
        pasos = 3

        if self.direccion_sonido == "NORTE":
            direccion = (-1, 0)

        elif self.direccion_sonido == "SUR":
            direccion = (1, 0)

        elif self.direccion_sonido == "ESTE":
            direccion = (0, 1)

        elif self.direccion_sonido == "OESTE":
            direccion = (0, -1)

        else:
            return None

        df, dc = direccion

        # Probamos primero 3 casillas,
        # luego 2 y finalmente 1.
        for distancia in range(pasos, 0, -1):

            nueva_f = f + df * distancia
            nueva_c = c + dc * distancia

            posicion = (nueva_f, nueva_c)

            if (
                0 <= nueva_f < self.mundo.filas
                and
                0 <= nueva_c < self.mundo.columnas
                and
                self.mundo.grid[posicion] != 1
            ):

                return posicion

        return None

    def usar_tacto(self, posicion):

        tipo = self.mundo.grid[posicion]

        # Arena movediza
        if tipo == 4:

            self.sensacion_tacto = "¡Arena movediza!"

            return "arena"

        # Terreno normal
        else:

            self.sensacion_tacto = "Suelo firme"

            return "normal"

    # ==========================================
    # SENTIDO DEL GUSTO 
    # ==========================================
    def usar_gusto(self, posicion):

        tipo = self.mundo.grid[posicion]

        # ======================================
        # BAYAS BUENAS
        # ======================================
        if tipo == 5:

            self.sensacion_gusto = "Bayas dulces"

            self.energia = min(
                self.energia_max,
                self.energia + 20
            )

            self.estado = (
                "Bayas dulces: +20 de energía 🫐"
            )

            # La baya desaparece después de comerla
            self.mundo.grid[posicion] = 0
            self.mapa_local[posicion] = 0


        # ======================================
        # BAYAS MALAS
        # ======================================
        elif tipo == 6:

            self.sensacion_gusto = "Bayas amargas"

            self.energia -= 10

            self.energia = max(
                0,
                self.energia
            )

            self.estado = (
                " Bayas amargas: -10 de energía "
            )

            # La baya desaparece después de comerla
            self.mundo.grid[posicion] = 0
            self.mapa_local[posicion] = 0


        # ======================================
        # SIN ALIMENTO
        # ======================================
        else:

            self.sensacion_gusto = "Sin alimento"


    # ==========================================
    # BUSCAR UNA ZONA NO REVISADA 
    # ==========================================
    def seleccionar_objetivo_busqueda(self):

        candidatas = []

        for posicion, tipo in self.mundo.grid.items():

            # No queremos árboles
            if tipo == 1:
                continue

            # Tampoco lugares ya revisados
            if posicion in self.celdas_revisadas:
                continue

            candidatas.append(posicion)

        # ======================================
        # SI YA REVISÓ TODO EL MAPA
        # ======================================
        if not candidatas:

            print(" Ya revisé todo el mapa. Reiniciando búsqueda.")

            self.celdas_revisadas.clear()

            # Marcamos nuevamente como revisada
            # la zona que ve actualmente
            for celda in self.obtener_celdas_visibles():

                self.celdas_revisadas.add(celda)

            # Volvemos a obtener candidatas
            for posicion, tipo in self.mundo.grid.items():

                if tipo != 1 and posicion not in self.celdas_revisadas:

                    candidatas.append(posicion)

        if not candidatas:

            return None

        # ======================================
        # PRIORIZAR LA ZONA NO REVISADA
        # MÁS CERCANA
        # ======================================

        candidatas.sort(
            key=lambda posicion:
            AEstrella.heuristica(
                self.posicion,
                posicion
            )
        )

        # Buscamos una que realmente tenga camino
        for candidata in candidatas:

            camino = AEstrella.buscar(
                self.posicion,
                candidata,
                self.mapa_local,
                (
                    self.mundo.filas,
                    self.mundo.columnas
                )
            )

            if camino:

                return candidata

        return None



    # ==========================================
    # GASTAR ENERGÍA
    # ==========================================
    

    #El ejemplo donde gasta mas energia viene siendo en las arenas movedizas. 
    def gastar_energia(self, posicion):

        tipo = self.mundo.grid[posicion]

        # ======================================
        # COSTO DE MOVIMIENTO
        # ======================================

        # Suelo normal o casilla con bayas
        if tipo == 0 or tipo == 5 or tipo == 6:

            self.energia -= 2

        # Arena movediza
        elif tipo == 4:

            self.energia -= 8

        self.energia = max(
            0,
            self.energia
        )

        # ======================================
        # USAR SENTIDO DEL GUSTO
        # ======================================
        self.usar_gusto(posicion)

    # ==========================================
    # TOMAR DECISIÓN
    # ==========================================
    def tomar_decision(self, puma):

        self.ruta_planeada = []


        # ======================================
        # 1. ¿SE QUEDÓ SIN ENERGÍA?
        # ======================================
        if self.energia <= 0:

            self.estado = "¡Murió de Agotamiento! "

            return


        # ======================================
        # 2. USAR LA VISTA
        # ======================================
        puma_visible = self.usar_vista(puma)
        puma_escuchado = self.usar_oido(puma)


        # ======================================
        # 3. ¿DEBE REGRESAR AL CAMPAMENTO?
        # ======================================
        if self.energia < 30:

            self.estado = "Regresando al Campamento "

            meta = self.mundo.campamento


            # Ya llegó
            if self.posicion == meta:

                self.energia = self.energia_max

                self.estado = "Energía recuperada "

                # Comenzará otra búsqueda
                self.objetivo_busqueda = None

                return


        # ======================================
        # 4. VE AL PUMA 
        # ======================================
        elif puma_visible:

            self.estado = " ¡Puma detectado! Persiguiendo "

            # Sabemos exactamente dónde está
            # porque LO ESTAMOS VIENDO
            meta = puma.posicion

            # Ya no necesitamos el objetivo
            # anterior de búsqueda
            self.objetivo_busqueda = None

            #no lo ve pero lo escucha
        elif puma_escuchado:

            self.estado = (
                f"Sonido detectado hacia el "
                f"{self.direccion_sonido}. Investigando..."
            )

            meta = self.objetivo_sonido

            self.objetivo_busqueda = None

            if meta is None:
                return

        # ======================================
        # 5. NO LO VE, PERO RECUERDA
        #    DÓNDE LO VIO POR ÚLTIMA VEZ
        # ======================================
        elif self.ultima_posicion_puma is not None:

            # Todavía no llega al último
            # lugar donde vio al puma
            if self.posicion != self.ultima_posicion_puma:

                self.estado = (
                    " Investigando última posición del Puma"
                )

                meta = self.ultima_posicion_puma

            else:

                # =================================
                # Llegó pero el puma ya no está
                # =================================

                self.estado = (
                    "El Puma ya no está aquí. "
                    "Continuando búsqueda..."
                )

                # Esa información ya quedó vieja
                self.ultima_posicion_puma = None

                self.objetivo_busqueda = None

                meta = self.seleccionar_objetivo_busqueda()

                if meta is None:

                    return


        # ======================================
        # 6. NO SABE NADA DEL PUMA
        #    → BUSCAR ZONAS NO REVISADAS
        # ======================================
        else:

            self.estado = "Buscando zonas no revisadas..."

            # Si no tenemos objetivo,
            # elegimos uno nuevo.
            if (
                self.objetivo_busqueda is None
                or
                self.objetivo_busqueda in self.celdas_revisadas
            ):

                self.objetivo_busqueda = (
                    self.seleccionar_objetivo_busqueda()
                )

            meta = self.objetivo_busqueda

            if meta is None:

                return


        # ======================================
        # 7. SI YA ESTÁ EN LA META
        # ======================================
        if self.posicion == meta:

            self.objetivo_busqueda = None

            return


        # ======================================
        # 8. CALCULAR RUTA CON A*
        # ======================================
        camino = AEstrella.buscar(

            self.posicion,

            meta,

            self.mapa_local,

            (
                self.mundo.filas,
                self.mundo.columnas
            )
        )


        if not camino:

            self.estado = "No existe ruta disponible "

            self.objetivo_busqueda = None

            return


        # Guardamos la ruta para dibujarla
        self.ruta_planeada = camino

        siguiente_pos = camino[0]


        # ======================================
        # 9. GASTAR ENERGÍA
        # ======================================
        self.gastar_energia(
            siguiente_pos
        )


        # ======================================
        # 10. MOVER CAZADOR
        # ======================================
        self.posicion = siguiente_pos


# ==========================================
# 6. INTERFAZ GRÁFICA
# ==========================================
class SimulacionGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Inteligencia Artificial: Cazador vs Puma"
        )

        self.celda_tam = 60

        self.reiniciar()

        self.crear_interfaz()

        self.dibujar_mundo()

    def crear_interfaz(self):

        panel = tk.Frame(
            self.root,
            bg="#1B4F72",
            pady=10
        )

        panel.pack(
            side=tk.TOP,
            fill=tk.X
        )

        tk.Button(
            panel,
            text="▶ Iniciar",
            command=self.iniciar,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            panel,
            text="⏸ Pausar",
            command=self.pausar,
            bg="#F39C12",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        tk.Button(
            panel,
            text="🔄 Reiniciar",
            command=self.reiniciar_gui,
            bg="#2980B9",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        self.lbl_energia = tk.Label(
            panel,
            text="",
            font=("Arial", 11, "bold"),
            bg="#1B4F72",
            fg="#F1C40F"
        )

        self.lbl_energia.pack(
            side=tk.LEFT,
            padx=15
        )

        self.lbl_puma = tk.Label(
            panel,
            text="",
            font=("Arial", 11, "bold"),
            bg="#1B4F72",
            fg="#E74C3C"
        )

        self.lbl_puma.pack(
            side=tk.LEFT,
            padx=15
        )

        self.lbl_estado = tk.Label(
            panel,
            text="",
            font=("Arial", 11, "bold"),
            bg="#1B4F72",
            fg="white"
        )

        self.lbl_estado.pack(
            side=tk.LEFT,
            padx=15
        )

        self.canvas = tk.Canvas(

            self.root,

            width=
            self.mundo.columnas
            * self.celda_tam,

            height=
            self.mundo.filas
            * self.celda_tam,

            bg="#1a1a1a"
        )

        self.canvas.pack(
            padx=10,
            pady=10
        )

        self.actualizar_labels()

    def reiniciar(self):

        self.corriendo = False

        self.modo_huida = 0

        self.mundo = MundoSelva()

        self.puma = Puma(
            self.mundo.inicio_puma
        )

        self.cazador = Cazador(
            self.mundo
        )

        self.ratones = [

            Raton(

                self.mundo._pos_aleatoria_valida(

                    exclude=[
                        self.mundo.inicio_cazador,
                        self.mundo.inicio_puma
                    ]
                ),

                self.mundo
            )

            for _ in range(5)
        ]

    def reiniciar_gui(self):

        self.reiniciar()

        self.dibujar_mundo()

        self.actualizar_labels()

    def iniciar(self):

        if not self.corriendo:

            self.corriendo = True

            self.ciclo_simulacion()

    def pausar(self):

        self.corriendo = False

    def ciclo_simulacion(self):

        if not self.corriendo:
            return

        # =====================================
        # PUMA EN MODO HUIDA
        # =====================================
        if self.modo_huida > 0:

            self.puma.huir(
                self.cazador.posicion,
                self.mundo
            )

            self.modo_huida -= 1

            self.dibujar_mundo()

            self.actualizar_labels()

            self.root.after(
                150,
                self.ciclo_simulacion
            )

            return

        # =====================================
        # CICLO NORMAL
        # =====================================
        if (
            self.cazador.energia > 0
            and
            self.puma.vidas > 0
        ):

            # 1. Mover ratones
            for r in self.ratones:

                r.mover(
                    self.puma.posicion,
                    self.mundo
                )

            # 2. Mover puma
            self.puma.cazar(
                self.ratones,
                self.mundo
            )

            # 3. Cazador toma decisión
            #
            # YA NO EXISTE:
            # self.cazador.percibir_entorno()
            #
            self.cazador.tomar_decision(
                self.puma
            )

            # =====================================
            # COMPROBAR ATAQUE
            # =====================================
            distancia = AEstrella.heuristica(

                self.cazador.posicion,

                self.puma.posicion
            )

            if (
                distancia <= 1
                and
                self.cazador.estado
                != "Regresando al Campamento ⛺"
            ):

                self.puma.vidas -= 1

                if self.puma.vidas > 0:

                    self.modo_huida = 12

                    self.cazador.estado = (
                        "¡Disparo Acertado! "
                        "El Puma huye "
                    )

                    self.cazador.ruta_planeada = []

                    self.dibujar_mundo()

                    self.actualizar_labels()

                    self.root.after(
                        150,
                        self.ciclo_simulacion
                    )

                    return

                else:

                    self.cazador.estado = (
                        "¡VICTORIA! "
                        "Puma Derrotado 🏆"
                    )

            self.dibujar_mundo()

            self.actualizar_labels()

            self.root.after(
                800,
                self.ciclo_simulacion
            )

    def actualizar_labels(self):

        if self.cazador.energia < 100:

            color_energia = "#E74C3C"

        else:

            color_energia = "#F1C40F"

        self.lbl_energia.config(

            text=
            f"Energía Cazador: "
            f"{self.cazador.energia} ⚡",

            fg=color_energia
        )

        self.lbl_puma.config(

            text=
            f"Vidas del Puma: "
            f"{self.puma.vidas} "
        )

        self.lbl_estado.config(

            text=
            f"Estado: "
            f"{self.cazador.estado}"
        )

        if self.cazador.escucha_puma:
            texto_oido = f" Oído: {self.cazador.direccion_sonido}"
        else:
            texto_oido = " Oído: Sin detección"

    # ==========================================
    # DIBUJAR TODO EL MAPA
    # ==========================================
    def dibujar_mundo(self):

        self.canvas.delete("all")

        colores = {
            0: "#229954",
            1: "#145A32",
            4: "#873600",
            5: "#6C3483",
            6: "#A93226"
        }

        emojis = {

            0: "",
            1: "🌲",
            4: "🟫",
            5: "🫐",
            6: "🍒"
        }

        # =====================================
        # MAPA COMPLETO VISIBLE DESDE EL INICIO
        # =====================================

        for f in range(self.mundo.filas):

            for c in range(self.mundo.columnas):

                tipo = self.mundo.grid[(f, c)]

                x1 = c * self.celda_tam

                y1 = f * self.celda_tam

                x2 = x1 + self.celda_tam

                y2 = y1 + self.celda_tam

                cx = x1 + self.celda_tam / 2

                cy = y1 + self.celda_tam / 2

                # =====================================
                # RANGO DE VISIÓN DEL CAZADOR 
                # =====================================

                distancia_sensorial = AEstrella.heuristica(
                    self.cazador.posicion,
                    (f, c)
                )

                # PRIORIDAD:
                # 1. Vista (amarillo)
                # 2. Oído (gris)
                # 3. Normal

                if distancia_sensorial <= self.cazador.rango_vista:
                    color_borde = "#F7DC6F"   # amarillo suave
                    grosor_borde = 2

                elif distancia_sensorial <= self.cazador.rango_oido:
                    color_borde = "#AEB6BF"   # gris suave
                    grosor_borde = 1

                else:
                    color_borde = "#196F3D"   # borde normal verde
                    grosor_borde = 1

                # Dibujar celda
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=colores[tipo],
                    outline=color_borde,
                    width=grosor_borde
                )

                # Dibujar emoji del terreno
                if emojis[tipo]:

                    self.canvas.create_text(
                        cx,
                        cy,
                        text=emojis[tipo],
                        font=("Segoe UI Emoji", 18)
                    )

        # =====================================
        # RUTA A*
        # =====================================

        if (
            self.cazador.ruta_planeada
            and
            self.modo_huida == 0
        ):

            puntos = [

                (
                    self.cazador.posicion[1]
                    * self.celda_tam
                    + self.celda_tam / 2,

                    self.cazador.posicion[0]
                    * self.celda_tam
                    + self.celda_tam / 2
                )
            ]

            for paso in self.cazador.ruta_planeada:

                puntos.append(

                    (
                        paso[1]
                        * self.celda_tam
                        + self.celda_tam / 2,

                        paso[0]
                        * self.celda_tam
                        + self.celda_tam / 2
                    )
                )

            if len(puntos) > 1:

                self.canvas.create_line(

                    puntos,

                    fill="#F1C40F",

                    width=3,

                    dash=(4, 2)
                )

        # =====================================
        # CAMPAMENTO
        # =====================================

        cf, cc = self.mundo.campamento

        self.canvas.create_text(

            cc * self.celda_tam
            + self.celda_tam / 2,

            cf * self.celda_tam
            + self.celda_tam / 2,

            text="⛺",

            font=(
                "Segoe UI Emoji",
                26
            )
        )

        # =====================================
        # RATONES
        # =====================================

        for raton in self.ratones:

            if raton.vivo:

                cx = (
                    raton.posicion[1]
                    * self.celda_tam
                    + self.celda_tam / 2
                )

                cy = (
                    raton.posicion[0]
                    * self.celda_tam
                    + self.celda_tam / 2
                )

                self.canvas.create_text(

                    cx,
                    cy,

                    text="🐁",

                    font=(
                        "Segoe UI Emoji",
                        26
                    )
                )

        # =====================================
        # PUMA
        # =====================================

        if self.puma.vidas > 0:

            cx = (
                self.puma.posicion[1]
                * self.celda_tam
                + self.celda_tam / 2
            )

            cy = (
                self.puma.posicion[0]
                * self.celda_tam
                + self.celda_tam / 2
            )

            self.canvas.create_text(

                cx,
                cy,

                text="🐆",

                font=(
                    "Segoe UI Emoji",
                    26
                )
            )

        # =====================================
        # CAZADOR
        # =====================================

        cx = (
            self.cazador.posicion[1]
            * self.celda_tam
            + self.celda_tam / 2
        )

        cy = (
            self.cazador.posicion[0]
            * self.celda_tam
            + self.celda_tam / 2
        )

        self.canvas.create_text(

            cx,
            cy,

            text="🤠",

            font=(
                "Segoe UI Emoji",
                26
            )
        )


# ==========================================
# 7. EJECUTAR PROGRAMA
# ==========================================
if __name__ == "__main__":

    root = tk.Tk()

    app = SimulacionGUI(root)

    root.mainloop()