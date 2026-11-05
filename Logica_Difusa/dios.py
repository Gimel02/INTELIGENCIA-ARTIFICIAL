# ==========================================
# DIOS: ORQUESTADOR DE LA SIMULACIÓN
#
# DIOS controla todo. Es como el árbitro de
# un juego de mesa: los agentes dicen qué
# quieren hacer y DIOS aplica las reglas del
# mundo.
#
#   1. Crea el mundo (al azar o un escenario
#      de demostración).
#   2. Crea a los agentes y le da a cada uno
#      su base de conocimiento:
#        Agente 1 -> CAZADOR     (control difuso)
#        Agente 2 -> JAGUAR      (control difuso)
#        Agente 3 -> INTERCEPTOR (control difuso):
#                    un segundo cazador, RIVAL
#                    del primero. Es igual al
#                    cazador (mismas 23 reglas,
#                    sentidos, memoria y AG),
#                    con su propio controlador
#                    y SU PROPIA CABAÑA.
#        Ratones  -> Agente Tonto (reglas fijas)
#   3. Controla los turnos, en este orden:
#      cazador -> interceptor -> jaguar ->
#      ratones.
#   4. Aplica las reglas del mundo:
#        - el jaguar atrapa ratones
#        - el jaguar reacciona al cazador que
#          tenga más cerca
#        - encuentro de cada cazador con el
#          jaguar
#        - pelea entre los dos cazadores: el
#          que pierde muere
#        - si ya no queda ningún cazador vivo,
#          el jaguar regresa a su cueva
#   5. Decide cuándo termina la partida:
#        - el jaguar llegó a su cueva
#        - el cazador perdió todas sus vidas
#   6. Anota lo que pasa en su bitácora.
#
# La interfaz solo dibuja: cada cuadro le
# pide a DIOS que avance (paso) y luego
# dibuja el mundo como DIOS lo dejó.
#
# Las reglas difusas del cazador y del jaguar
# son las diseñadas por el equipo. El
# algoritmo genético se usa únicamente para
# el MOVIMIENTO de los cazadores.
# ==========================================

import random
from collections import deque

from Logica_Difusa.base_conocimiento import base_equipo
from Logica_Difusa.motor_mamdani import ControladorDifuso


AGENTES_DIFUSOS = {
    "Agente 1": "cazador",
    "Agente 2": "jaguar",
    "Agente 3": "interceptor",
}

# Base de conocimiento que usa cada agente.
# El interceptor es otro cazador: usa las
# mismas reglas, pero con su propio
# controlador (decide por su cuenta).

BASE_DEL_AGENTE = {
    "cazador": "cazador",
    "jaguar": "jaguar",
    "interceptor": "cazador",
}

AGENTE_TONTO = "ratones"


REGLAS_TONTO = [
    "Si el jaguar está a 3 casillas o menos: huir en línea recta por el eje que más los separa.",
    "Si no ve al jaguar: caminar en una dirección al azar y cambiarla cada 0.8 a 2 segundos.",
    "Si choca con un árbol o un borde: elegir otra dirección libre, sin regresarse si puede.",
]


# ==========================================
# CUERPOS FÍSICOS
#
# masa (kg), fuerza motriz (N),
# coeficiente de arrastre (N·s/m)
#
# El jaguar es más ligero: acelera más
# rápido, pero su fuerza es menor y su
# velocidad máxima también. Así el cazador
# lo puede alcanzar. Los dos cazadores tienen
# el mismo cuerpo.
# ==========================================

FISICA_CAZADOR = {
    "masa": 75,
    "fuerza_motriz": 400,
    "coeficiente_arrastre": 120,
}

FISICA_JAGUAR = {
    "masa": 55,
    "fuerza_motriz": 330,
    "coeficiente_arrastre": 120,
}

# Segundos que espera quieto cuando decide
# no moverse

PAUSA_CAZADOR = 0.3
PAUSA_JAGUAR = 0.4

# Distancia (en casillas) a la que el jaguar
# atrapa a un ratón

DISTANCIA_ATRAPAR_RATON = 0.6


# ==========================================
# CABAÑA DEL INTERCEPTOR
#
# DIOS la pone en una casilla de pasto:
#   - lo más lejos posible de la cabaña del
#     cazador,
#   - a por lo menos 4 casillas de la cueva y
#     del jaguar,
#   - con al menos 3 casillas de pasto
#     alrededor (no en una esquina ni en un
#     pasillo),
#   - dentro de una zona limpia grande (por lo
#     menos 25 casillas unidas sin bayas ni
#     arena), para que nunca quede encerrado
#     por una baya mala,
#   - y con camino a la otra cabaña.
# No usa el azar, así que el mapa es el mismo
# con o sin interceptor.
# ==========================================

DISTANCIA_MINIMA_CUEVA = 4
PASTO_MINIMO_ALREDEDOR = 3
ZONA_LIMPIA_MINIMA = 25


# ==========================================
# PELEA ENTRE CAZADORES (RIVALES)
#
# Si los dos cazadores se tocan (están en la
# misma casilla o se cruzan en el camino,
# según donde se ven en pantalla), pelean a
# muerte:
# gana el que tenga MÁS energía y sigue en el
# juego; el que pierde MUERE y sale del juego.
# Si empatan, los dos pierden 10 de energía,
# siguen vivos y no pueden volver a pelear
# durante 3 segundos. En las cabañas y junto a
# ellas no se pelea.
# ==========================================

DANO_EMPATE = 10
ESPERA_PELEA = 3.0

# Distancia (en casillas, como se ven en
# pantalla) a la que se tocan para pelear:
# menos de un cuerpo de distancia
DISTANCIA_PELEA = 0.6

# Segundos que se muestra "¡PELEA!" en el mapa
DURACION_AVISO_PELEA = 1.5


# ==========================================
# RESULTADOS POSIBLES DE UNA PARTIDA
# ==========================================

JAGUAR_EN_CUEVA = "JAGUAR EN CUEVA"
CAZADOR_DERROTADO = "CAZADOR DERROTADO"

# Con rival: quién atrapó primero al jaguar
# (la partida sigue: los dos regresan a la
# cabaña)

GANA_CAZADOR = "GANA CAZADOR"
GANA_INTERCEPTOR = "GANA INTERCEPTOR"


class Dios:

    def __init__(self):

        # Se conserva para mostrarlo en la interfaz.
        self.modo = "equipo"

        # Base de conocimiento + motor difuso de
        # cada agente inteligente
        self.agentes = {
            nombre: ControladorDifuso(
                base_equipo(BASE_DEL_AGENTE[agente])
            )
            for nombre, agente
            in AGENTES_DIFUSOS.items()
        }

        # ¿Juega el interceptor? (tecla I)
        self.con_interceptor = True

        # Partida actual (la crea nueva_partida)
        self.mundo = None
        self.escenario = None
        self.cazador = None
        self.jaguar = None
        self.interceptor = None
        self.cuerpo_cazador = None
        self.cuerpo_jaguar = None
        self.cuerpo_interceptor = None

        self.terminada = False
        self.resultado = None

        # Quién atrapó al jaguar (con rival)
        self.ganador = None

        # Segundos que faltan para que los
        # cazadores puedan volver a pelear
        self.espera_pelea = 0.0

        # Última pelea, para dibujarla:
        # {"lugar": (fila, columna), "texto": ...,
        #  "tiempo": segundos que le quedan}
        self.ultima_pelea = None

        # Lo que va pasando en la partida
        self.bitacora = deque(maxlen=100)


    # ======================================
    # BASES DE CONOCIMIENTO
    # ======================================

    def consultar(
        self,
        nombre,
        entradas
    ):

        return self.agentes[
            nombre
        ].decidir(
            entradas
        )


    def controlador(
        self,
        agente
    ):

        for nombre, tipo in (
            AGENTES_DIFUSOS.items()
        ):

            if tipo == agente:

                return self.agentes[
                    nombre
                ]

        raise KeyError(
            agente
        )


    def decision_tonto(
        self,
        raton
    ):

        return raton.estado


    def descripcion(self):

        return " | ".join(
            controlador.base.nombre
            for controlador
            in self.agentes.values()
        )


    # ======================================
    # 1 y 2. CREAR EL MUNDO Y LOS AGENTES
    # ======================================

    def nueva_partida(self, escenario=None):

        # Se importan aquí porque los agentes, a
        # su vez, le piden su controlador a DIOS

        from Mundo.mundo import MundoSelva
        from Mundo import escenarios
        from Agente_Cazador.agente import AgenteCazador
        from Agente_Jaguar.agente import AgenteJaguar
        from Fisica.cinematica import CuerpoFisico

        self.escenario = escenario

        # Con escenario: siempre el mismo mapa
        # (teclas 1 y 2). Sin escenario: al azar.

        if escenario is None:

            self.mundo = MundoSelva()

        else:

            self.mundo = escenarios.crear_mundo(
                escenario
            )


        # Cada agente recibe SU base de
        # conocimiento desde DIOS

        self.cazador = AgenteCazador(
            self.mundo,
            controlador=self.controlador("cazador")
        )
        # Cazador 1

        self.cazador.nombre = "Rodrigo"

        self.jaguar = AgenteJaguar(
            self.mundo,
            controlador=self.controlador("jaguar")
        )


        # Escenario de demostración: coloca al
        # jaguar, su hambre y la energía del
        # cazador

        if escenario is not None:

            escenarios.aplicar(
                escenario,
                self.mundo,
                self.cazador,
                self.jaguar,
                fijar_azar=False
            )

            # Cada vez que se presiona la tecla,
            # la partida es un poco distinta
            random.seed()


        # Cuerpos físicos

        self.cuerpo_cazador = CuerpoFisico(
            posicion=self.cazador.posicion,
            **FISICA_CAZADOR
        )

        # El cazador conoce su propio cuerpo
        # (masa, fuerza, velocidad)
        self.cazador.cuerpo = self.cuerpo_cazador

        self.cuerpo_jaguar = CuerpoFisico(
            posicion=self.mundo.posicion_jaguar,
            **FISICA_JAGUAR
        )


        # Cabañas de los cazadores
        self.mundo.campamentos = [self.mundo.campamento]
        self.mundo.campamento_interceptor = None


        # Agente 3: el interceptor, otro cazador
        # igual al primero, con su propio
        # controlador y su propia cabaña

        if self.con_interceptor:

            cabana = self.elegir_cabana_interceptor()

            self.mundo.campamento_interceptor = cabana
            self.mundo.campamentos.append(cabana)

            self.interceptor = AgenteCazador(
                self.mundo,
                controlador=self.controlador("interceptor"),
                campamento=cabana
            )
            # Cazador 2

            self.interceptor.nombre = "Gonzalo"


            # ==========================================
            # LOS DOS CAZADORES SE RECONOCEN COMO RIVALES
            #
            # Ninguno es "el interceptor".
            # Cualquiera puede activar la conducta
            # INTERCEPTAR.
            # ==========================================

            self.cazador.rival = self.interceptor
            self.interceptor.rival = self.cazador

            if escenario is not None:

                self.interceptor.energia = escenario.energia_cazador

            self.cuerpo_interceptor = CuerpoFisico(
                posicion=self.interceptor.posicion,
                **FISICA_CAZADOR
            )

            self.interceptor.cuerpo = self.cuerpo_interceptor

        else:

            self.interceptor = None
            self.cuerpo_interceptor = None
            self.cazador.rival = None

       
        self.terminada = False
        self.resultado = None
        self.ganador = None
        self.espera_pelea = 0.0
        self.ultima_pelea = None
        self.bitacora.clear()

        if escenario is None:

            self.anotar("Nueva partida en un mapa al azar")

        else:

            self.anotar(
                f"Escenario: {escenario.nombre} "
                f"({escenario.descripcion})"
            )


    # --------------------------------------
    # Dónde va la cabaña del interceptor
    # --------------------------------------

    def elegir_cabana_interceptor(self):

        from Algoritmos.a_Estrella import AEstrella

        mundo = self.mundo
        campamento = mundo.campamento

        # Casillas a las que se llega desde la
        # cabaña del cazador (por cualquier
        # camino)
        alcanzables = AEstrella.costos_desde(campamento, mundo)

        # Zonas limpias: casillas unidas por
        # pasto, sin bayas (5 y 6) ni arena (4)
        tamano_zona = self.zonas_limpias()

        prohibidas = {
            campamento,
            mundo.cueva,
            mundo.posicion_jaguar,
        }

        def pasto_alrededor(casilla):

            return sum(
                1
                for vecino in mundo.vecinos_validos(casilla)
                if mundo.grid.get(vecino, 0) == 0
            )

        def buena(casilla, pasto_minimo, zona_minima):

            return (
                mundo.grid.get(casilla, 0) == 0
                and casilla not in prohibidas
                and AEstrella.heuristica(casilla, mundo.cueva) >= DISTANCIA_MINIMA_CUEVA
                and AEstrella.heuristica(casilla, mundo.posicion_jaguar) >= DISTANCIA_MINIMA_CUEVA
                and pasto_alrededor(casilla) >= pasto_minimo
                and tamano_zona.get(casilla, 0) >= zona_minima
            )

        # Si ninguna cumple todo, se va aflojando
        for pasto_minimo, zona_minima in (
            (PASTO_MINIMO_ALREDEDOR, ZONA_LIMPIA_MINIMA),
            (2, ZONA_LIMPIA_MINIMA),
            (2, 1),
            (1, 1),
        ):

            candidatas = [
                casilla
                for casilla in alcanzables
                if buena(casilla, pasto_minimo, zona_minima)
            ]

            if candidatas:

                # La más lejana a la otra cabaña (en
                # un empate, la primera en orden)
                return max(
                    sorted(candidatas),
                    key=lambda casilla: AEstrella.heuristica(casilla, campamento)
                )

        return campamento


    def zonas_limpias(self):

        # {casilla de pasto: tamaño de su zona
        # limpia}. Recorrido por anchura.

        mundo = self.mundo

        pasto = {
            casilla
            for casilla, tipo in mundo.grid.items()
            if tipo == 0
        }

        tamano = {}

        for inicio in pasto:

            if inicio in tamano:
                continue

            zona = [inicio]
            vistos = {inicio}
            i = 0

            while i < len(zona):

                for vecino in mundo.vecinos_validos(zona[i]):

                    if vecino in pasto and vecino not in vistos:

                        vistos.add(vecino)
                        zona.append(vecino)

                i += 1

            for casilla in zona:

                tamano[casilla] = len(zona)

        return tamano


    # ======================================
    # LOS CAZADORES DE LA PARTIDA
    # ======================================

    def cazadores(self):

        # (nombre, agente, cuerpo)

        lista = [("cazador", self.cazador, self.cuerpo_cazador)]

        if self.interceptor is not None:

            lista.append(
                ("interceptor", self.interceptor, self.cuerpo_interceptor)
            )

        return lista


    def cazadores_vivos(self):

        return [
            (nombre, agente, cuerpo)
            for nombre, agente, cuerpo in self.cazadores()
            if agente.vidas > 0
        ]


    def interceptor_activo(self):

        return (
            self.interceptor is not None
            and self.interceptor.vidas > 0
        )


    # ======================================
    # 3. AVANZAR LA SIMULACIÓN
    #
    # La interfaz lo llama en cada cuadro con
    # dt (segundos desde el cuadro anterior).
    # Regresa False cuando la partida terminó.
    # ======================================

    def paso(self, dt):

        if self.terminada:

            return False

        if self.revisar_fin():

            return False

        self.espera_pelea = max(0.0, self.espera_pelea - dt)

        if self.ultima_pelea is not None:

            self.ultima_pelea["tiempo"] -= dt

            if self.ultima_pelea["tiempo"] <= 0:

                self.ultima_pelea = None

        if self.cazador.vidas > 0:

            self.turno_cazador(
                dt,
                "cazador",
                self.cazador,
                self.cuerpo_cazador
            )
        if self.interceptor_activo():

            self.turno_cazador(
                dt,
                "interceptor",
                self.interceptor,
                self.cuerpo_interceptor
            )

        self.turno_jaguar(dt)

        if self.revisar_fin():

            return False

        self.turno_ratones(dt)

        self.resolver_encuentro()

        return True


    # --------------------------------------
    # Turno de un cazador (Agente 1 o 3)
    #
    # Su cuerpo avanza; cuando llega a la
    # casilla, el cazador decide otra vez.
    # --------------------------------------

    def turno_cazador(self, dt, nombre, agente, cuerpo):

        cuerpo.actualizar(
            dt,
            self.mundo.grid[cuerpo.destino]
        )

        if not cuerpo.en_reposo():

            return

        antes = agente.posicion

        jaguar_vivo_antes = self.mundo.jaguar_vivo

        agente.tomar_decision(
            self.mundo.posicion_jaguar
        )

        # ¿Lo atrapó en su propio turno?
        if jaguar_vivo_antes and not self.mundo.jaguar_vivo:

            self.registrar_caza(nombre)

        if agente.posicion != antes:

            cuerpo.mover_a(
                agente.posicion
            )

        else:

            cuerpo.detener(
                PAUSA_CAZADOR
            )


    # --------------------------------------
    # A quién ve el jaguar: al cazador vivo
    # que tenga más cerca (posición y energía)
    # --------------------------------------

    def cazador_mas_cercano(self):

        from Algoritmos.a_Estrella import AEstrella

        vivos = self.cazadores_vivos()

        if len(vivos) <= 1:

            agente = vivos[0][1] if vivos else self.cazador

            return agente.posicion, agente.energia

        jaguar = self.mundo.posicion_jaguar

        _, agente, _ = min(
            vivos,
            key=lambda c: AEstrella.heuristica(jaguar, c[1].posicion)
        )

        return agente.posicion, agente.energia


    # --------------------------------------
    # Turno del Agente 2 (jaguar)
    # --------------------------------------

    def turno_jaguar(self, dt):

        if not self.mundo.jaguar_vivo:

            return

        cuerpo = self.cuerpo_jaguar

        cuerpo.actualizar(
            dt,
            self.mundo.grid[cuerpo.destino]
        )

        if not cuerpo.en_reposo():

            return

        posicion_cazador, energia_cazador = (
            self.cazador_mas_cercano()
        )

        destino = self.jaguar.tomar_decision(
            posicion_cazador,
            energia_cazador,
            self.mundo.ratones
        )

        if destino is not None:

            cuerpo.mover_a(
                destino
            )

        else:

            cuerpo.detener(
                PAUSA_JAGUAR
            )


    # --------------------------------------
    # Turno del Agente Tonto (ratones)
    #
    # Se mueven con sus reglas fijas. DIOS
    # revisa si el jaguar atrapó a alguno.
    # --------------------------------------

    def turno_ratones(self, dt):

        posicion_jaguar = (
            self.cuerpo_jaguar.posicion_visual()
            if self.mundo.jaguar_vivo
            else None
        )

        for raton in self.mundo.ratones:

            # Los ratones cazados ya no se mueven
            if not raton.vivo:
                continue

            raton.actualizar(
                dt,
                posicion_jaguar
            )

            if posicion_jaguar is None:
                continue

            fila, columna = raton.posicion_visual()

            distancia = (
                (fila - posicion_jaguar[0]) ** 2
                + (columna - posicion_jaguar[1]) ** 2
            ) ** 0.5

            if distancia < DISTANCIA_ATRAPAR_RATON:

                raton.vivo = False

                self.jaguar.comer_raton()

                self.anotar("El jaguar atrapó un ratón")


    # ======================================
    # 4. REGLAS DEL MUNDO: ENCUENTROS
    # ======================================

    def resolver_encuentro(self):

        self.pelea_entre_cazadores()

        for nombre, agente, _ in self.cazadores():

            self.encuentro_con_jaguar(nombre, agente)


    # --------------------------------------
    # Un cazador y el jaguar en la misma
    # casilla:
    #   - si el jaguar está atacando, el
    #     cazador pierde una vida;
    #   - si no, el cazador atrapa al jaguar.
    # --------------------------------------

    def encuentro_con_jaguar(self, nombre, agente):

        if (
            agente.vidas <= 0
            or not self.mundo.jaguar_vivo
            or agente.posicion != self.mundo.posicion_jaguar
        ):

            return

        if not self.jaguar.atacando:

            if agente.atrapar_jaguar():

                self.registrar_caza(nombre)

            return

        agente.recibir_ataque()

        self.jaguar.despues_de_atacar()

        self.anotar(
            f"El jaguar atacó al {nombre} "
            f"(vidas: {agente.vidas})"
        )

        # Si ya no queda ningún cazador vivo, el
        # jaguar regresa a su cueva

        if not self.cazadores_vivos():

            self.jaguar.regresando_cueva = True
            self.jaguar.en_cueva = False
            self.jaguar.estado = "Regresando a la cueva"

            self.anotar("El jaguar ganó y regresa a su cueva")


    def registrar_caza(self, nombre):

        if self.ganador is not None:

            return

        self.ganador = nombre

        self.anotar(f"El {nombre} atrapó al jaguar")

        if self.interceptor is not None:

            self.anotar(
                GANA_INTERCEPTOR
                if nombre == "interceptor"
                else GANA_CAZADOR
            )


    # --------------------------------------
    # Pelea entre los dos cazadores (rivales)
    # --------------------------------------

    def pelea_entre_cazadores(self):

        from Algoritmos.a_Estrella import AEstrella

        if (
            not self.interceptor_activo()
            or self.cazador.vidas <= 0
            or self.espera_pelea > 0
        ):

            return

        a = self.cazador
        b = self.interceptor

        nombre_a = getattr(
            a,
            "nombre",
            "Rodrigo"
        )

        nombre_b = getattr(
            b,
            "nombre",
            "Gonzalo"
        )

        # Pelean solo si se tocan en pantalla:
        # a menos de 0.6 casillas (también cuando
        # se cruzan caminando). Se usa lo que se
        # ve, porque la casilla de un cazador
        # cambia en cuanto decide moverse, antes
        # de que su cuerpo llegue

        visual_a = self.cuerpo_cazador.posicion_visual()
        visual_b = self.cuerpo_interceptor.posicion_visual()

        distancia_visual = (
            (visual_a[0] - visual_b[0]) ** 2
            + (visual_a[1] - visual_b[1]) ** 2
        ) ** 0.5

        if distancia_visual > DISTANCIA_PELEA:

            return

        # En las cabañas y junto a ellas no se
        # pelea
        for campamento in self.mundo.campamentos:

            if (
                AEstrella.heuristica(a.posicion, campamento) <= 1
                or AEstrella.heuristica(b.posicion, campamento) <= 1
            ):

                return

        print(
            f"[DIOS - ENCUENTRO] {nombre_a} y {nombre_b} se encontraron | "
            f"{nombre_a}: {a.energia} energía | "
            f"{nombre_b}: {b.energia} energía | "
            f"{nombre_a} competitivo: {a.estado_competitivo} | "
            f"{nombre_b} competitivo: {b.estado_competitivo}"
        )
                
        if a.energia == b.energia:

            a.energia = max(0, a.energia - DANO_EMPATE)
            b.energia = max(0, b.energia - DANO_EMPATE)

            texto = f"¡PELEA! Empate (-{DANO_EMPATE} los dos)"

            self.anotar(
                f"Los cazadores pelearon y empataron "
                f"(los dos: -{DANO_EMPATE} de energía)"
            )

            self.espera_pelea = ESPERA_PELEA

        else:

            if a.energia > b.energia:

                ganador, perdedor = ("cazador", a), ("interceptor", b)

            else:

                ganador, perdedor = ("interceptor", b), ("cazador", a)

            # El que pierde muere y sale del juego
            self.eliminar_cazador(
                perdedor[1],
                f"¡Derrotado por el {ganador[0]}! Fuera del juego"
            )

            ganador[1].puntos += 10

            texto = f"¡PELEA! Gana {ganador[0]}"

            self.anotar(
                f"El {ganador[0]} le ganó la pelea al {perdedor[0]} "
                f"(energía {ganador[1].energia} contra "
                f"{perdedor[1].energia}): el {perdedor[0]} muere"
            )
            nombre_ganador = getattr(
                ganador[1],
                "nombre",
                ganador[0]
            )

            nombre_perdedor = getattr(
                perdedor[1],
                "nombre",
                perdedor[0]
            )

            print(
                f"[PELEA] GANA {nombre_ganador} | "
                f"{nombre_perdedor} queda fuera"
            )

        # Para que se vea en el mapa, a la mitad
        # de los dos
        self.ultima_pelea = {
            "lugar": (
                (visual_a[0] + visual_b[0]) / 2,
                (visual_a[1] + visual_b[1]) / 2,
            ),
            "texto": texto,
            "tiempo": DURACION_AVISO_PELEA,
        }


    # --------------------------------------
    # Un cazador muere y sale del juego
    # --------------------------------------

    def eliminar_cazador(self, agente, motivo):

        agente.vidas = 0

        agente.estado = motivo

        agente.ruta_planeada = []


    # ======================================
    # 5. ¿TERMINÓ LA PARTIDA?
    # ======================================

    def revisar_fin(self):

        if self.jaguar.en_cueva:

            resultado = JAGUAR_EN_CUEVA

        elif (
            not self.cazadores_vivos()
            and not self.jaguar.regresando_cueva
        ):

            resultado = CAZADOR_DERROTADO

        else:

            return False

        self.terminada = True
        self.resultado = resultado

        self.anotar(f"FIN DE LA PARTIDA: {resultado}")

        return True


    # ======================================
    # 6. BITÁCORA
    # ======================================

    def turno_actual(self):

        return self.cazador.turno if self.cazador else 0


    def anotar(self, texto):

        registro = f"[DIOS] Turno {self.turno_actual()}: {texto}"

        self.bitacora.append(registro)

        print(registro)


# ==========================================
# UNA SOLA INSTANCIA DE DIOS
# ==========================================

_dios = None


def obtener_dios():

    global _dios

    if _dios is None:

        _dios = Dios()

    return _dios


def controlador_por_defecto(
    agente
):

    return obtener_dios().controlador(
        agente
    )
