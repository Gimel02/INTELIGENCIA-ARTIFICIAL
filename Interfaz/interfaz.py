import pygame


from Mundo.mundo import MundoSelva
import Mundo.mundo as modulo_mundo
print(
    "ARCHIVO MUNDO QUE PYTHON ESTÁ USANDO:"
)

print(
     modulo_mundo.__file__
)

from Agente_Cazador.agente import AgenteCazador
from Agente_Cazador.sentidos import PLURAL_COLORES
from Agente_Jaguar.agente import AgenteJaguar

from Fisica.cinematica import CuerpoFisico


from Recursos.arbol import Arbol
from Recursos.bayas import Baya
from Recursos.arena import ArenaMovediza
from Recursos.campamento import Campamento
from Recursos.cazador import Cazador
from Recursos.jaguar import Jaguar

class Interfaz:

    def __init__(self):

        pygame.init()


        # =========================================
        # MUNDO
        # =========================================

        self.mundo = MundoSelva()


        # =========================================
        # AGENTE INTELIGENTE
        # =========================================

        self.agente = AgenteCazador(
            self.mundo
        )


        # =========================================
        # JAGUAR (huye cuando detecta al cazador)
        # =========================================

        self.agente_jaguar = AgenteJaguar(
            self.mundo
        )


        # =========================================
        # CUERPOS FÍSICOS
        #
        # masa (kg), fuerza motriz (N),
        # coeficiente de arrastre (N·s/m)
        #
        # El jaguar es más ligero: acelera más
        # rápido, pero su fuerza es menor y su
        # velocidad máxima también. Así el
        # cazador lo puede alcanzar.
        # =========================================

        self.cuerpo_cazador = CuerpoFisico(

            masa=75,

            fuerza_motriz=400,

            coeficiente_arrastre=120,

            posicion=self.agente.posicion

        )


        self.cuerpo_jaguar = CuerpoFisico(

            masa=55,

            fuerza_motriz=330,

            coeficiente_arrastre=120,

            posicion=self.mundo.posicion_jaguar

        )


        # Segundos que espera quieto cuando
        # decide no moverse

        self.pausa_cazador = 0.3

        self.pausa_jaguar = 0.4


        # =========================================
        # PANEL SUPERIOR
        # =========================================

        self.alto_panel = 180

        self.ancho = (
            self.mundo.ancho
        )

        self.alto = (

            self.mundo.alto
            +
            self.alto_panel

        )


        # =========================================
        # PANTALLA
        # =========================================

        self.pantalla = pygame.display.set_mode(

            (
                self.ancho,
                self.alto
            )

        )

        pygame.display.set_caption(
            "Agente Cazador - Jungla"
        )


        # =========================================
        # RECURSOS GRÁFICOS
        # =========================================

        self.arbol = Arbol(
            self.mundo.tamano_celda
        )

        self.baya = Baya(
            self.mundo.tamano_celda
        )

        self.arena = ArenaMovediza(
            self.mundo.tamano_celda
        )

        self.campamento = Campamento(
            self.mundo.tamano_celda
        )

        self.cazador = Cazador(
            self.mundo.tamano_celda
        )

        self.jaguar = Jaguar(
        self.mundo.tamano_celda
        )


        # =========================================
        # FUENTES
        # =========================================

        self.fuente = pygame.font.SysFont(
            "Arial",
            18,
            bold=True
        )

        self.fuente_pequena = pygame.font.SysFont(
            "Arial",
            15
        )

        self.fuente_titulo = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )


        # =========================================
        # SIMULACIÓN para que se empiece a mover 
        # =========================================

        self.ejecutando = True

        self.en_curso = True


        # =========================================
        # RELOJ
        # =========================================

        self.reloj = pygame.time.Clock()


    # =========================================
    # BUCLE PRINCIPAL
    # =========================================

    def ejecutar(self):

        while self.ejecutando:

            # Eventos
            self.manejar_eventos()


            # =====================================
            # TIEMPO DESDE EL CUADRO ANTERIOR
            #
            # La interfaz corre a 60 FPS.
            # dt se limita para que una pausa
            # larga no haga "saltar" a nadie.
            # =====================================

            dt = min(

                self.reloj.tick(60) / 1000,

                0.05

            )


            if self.en_curso:

                self.actualizar(
                    dt
                )


            # =====================================
            # DIBUJAR
            # =====================================

            self.dibujar()

            pygame.display.flip()


        pygame.quit()


    # =========================================
    # ACTUALIZAR SIMULACIÓN
    #
    # 1. La física mueve a cada cuerpo.
    # 2. Cuando un cuerpo llega a su casilla,
    #    su agente decide el siguiente paso.
    #    Así cada quien decide a su propio
    #    ritmo, según su masa y el suelo.
    # =========================================

    def actualizar(
        self,
        dt
    ):

        grid = self.mundo.grid


        # =====================================
        # CAZADOR
        # =====================================

        cuerpo = self.cuerpo_cazador

        cuerpo.actualizar(
            dt,
            grid[cuerpo.destino]
        )


        if cuerpo.en_reposo():

            antes = self.agente.posicion


            self.agente.tomar_decision(
                self.mundo.posicion_jaguar
            )


            if self.agente.posicion != antes:

                cuerpo.mover_a(
                    self.agente.posicion
                )

            else:

                cuerpo.detener(
                    self.pausa_cazador
                )


        # =====================================
        # JAGUAR
        # =====================================

        if self.mundo.jaguar_vivo:

            cuerpo = self.cuerpo_jaguar

            cuerpo.actualizar(
                dt,
                grid[cuerpo.destino]
            )


            if cuerpo.en_reposo():

                destino = (
                    self.agente_jaguar.tomar_decision(
                        self.agente.posicion
                    )
                )


                if destino is not None:

                    cuerpo.mover_a(
                        destino
                    )

                else:

                    cuerpo.detener(
                        self.pausa_jaguar
                    )


        # =====================================
        # ¿LO ATRAPÓ?
        # =====================================

        if (
            self.mundo.jaguar_vivo
            and
            self.agente.posicion
            ==
            self.mundo.posicion_jaguar
        ):

            self.agente.atrapar_jaguar()


    # =========================================
    # EVENTOS
    # =========================================

    def manejar_eventos(self):

        for evento in pygame.event.get():

            # =====================================
            # CERRAR
            # =====================================

            if evento.type == pygame.QUIT:

                self.ejecutando = False


            # =====================================
            # TECLADO
            # =====================================

            elif evento.type == pygame.KEYDOWN:


                # ESPACIO
                # Iniciar / Pausar

                if evento.key == pygame.K_SPACE:

                    self.en_curso = (
                        not self.en_curso
                    )


                # ESC
                # Cerrar programa

                elif evento.key == pygame.K_ESCAPE:

                    self.ejecutando = False


    # =========================================
    # DIBUJARTODO
    # =========================================

    def dibujar(self):

        # Fondo general

        self.pantalla.fill(
            (25, 25, 25)
        )


        # Panel

        self.dibujar_panel()


        # Mundo

        self.dibujar_tablero()


    # =========================================
    # PANEL
    # =========================================

    def dibujar_panel(self):

        pygame.draw.rect(

            self.pantalla,

            (35, 70, 40),

            (
                0,
                0,
                self.ancho,
                self.alto_panel
            )

        )


        # =====================================
        # TÍTULO
        # =====================================

        titulo = self.fuente_titulo.render(

            "AGENTE CAZADOR",

            True,

            (240, 240, 240)

        )

        self.pantalla.blit(
            titulo,
            (20, 8)
        )


        # =====================================
        # ENERGÍA
        # =====================================

        energia = self.fuente.render(

            f"Energía: "
            f"{self.agente.energia}",

            True,

            (255, 230, 90)

        )

        self.pantalla.blit(
            energia,
            (20, 45)
        )


        # =====================================
        # ESTADO
        # =====================================

        estado = self.fuente_pequena.render(

            f"Estado: "
            f"{self.agente.estado}",

            True,

            (240, 240, 240)

        )

        self.pantalla.blit(
            estado,
            (150, 48)
        )


        # =====================================
        # VISTA
        # =====================================

        if self.agente.sentidos.ve_jaguar:

            texto_vista = (
                "Jaguar detectado"
            )

        else:

            texto_vista = (
                "Sin detección"
            )


        vista = self.fuente_pequena.render(

            f"Vista: {texto_vista}",

            True,

            (245, 220, 90)

        )

        self.pantalla.blit(
            vista,
            (20, 78)
        )


        # =====================================
        # OÍDO
        # =====================================

        if (
            self.agente
            .sentidos
            .escucha_jaguar
        ):

            texto_oido = (

                f"{self.agente.sentidos.direccion_sonido} "
                f"({self.agente.sentidos.intensidad_sonido})"

            )

        else:

            texto_oido = (
                "Sin detección"
            )


        oido = self.fuente_pequena.render(

            f"Oído: {texto_oido}",

            True,

            (190, 195, 200)

        )

        self.pantalla.blit(
            oido,
            (200, 78)
        )


        # =====================================
        # MEMORIA
        # =====================================

        revisadas = len(

            self.agente
            .memoria
            .celdas_revisadas

        )


        memoria = self.fuente_pequena.render(

            f"Memoria: "
            f"{revisadas} celdas",

            True,

            (220, 220, 220)

        )

        self.pantalla.blit(
            memoria,
            (400, 78)
        )


        # =====================================
        # TACTO
        # =====================================

        tacto = self.fuente_pequena.render(

            f"Tacto: "
            f"{self.agente.sentidos.sensacion_tacto}",

            True,

            (230, 190, 140)

        )

        self.pantalla.blit(
            tacto,
            (20, 102)
        )


        # =====================================
        # GUSTO
        # =====================================

        gusto = self.fuente_pequena.render(

            f"Gusto: "
            f"{self.agente.sentidos.sensacion_gusto}",

            True,

            (240, 160, 190)

        )

        self.pantalla.blit(
            gusto,
            (200, 102)
        )


        # =====================================
        # OLFATO
        # =====================================

        if (
            self.agente
            .sentidos
            .huele_jaguar
        ):

            texto_olfato = (

                "Jaguar, "
                f"{self.agente.sentidos.intensidad_olor.lower()}"

            )

        elif (
            self.agente
            .sentidos
            .huele_bayas
        ):

            texto_olfato = (
                "Bayas "
                f"{PLURAL_COLORES[self.agente.sentidos.color_olor_bayas]}"
            )

        else:

            texto_olfato = (
                "Sin detección"
            )


        olfato = self.fuente_pequena.render(

            f"Olfato: {texto_olfato}",

            True,

            (110, 200, 245)

        )

        self.pantalla.blit(
            olfato,
            (400, 102)
        )


        # =====================================
        # CONTROLES
        # =====================================

        if self.en_curso:

            texto_control = (
                "ESPACIO: Pausar"
            )

        else:

            texto_control = (
                "ESPACIO: Iniciar"
            )


        control = self.fuente_pequena.render(

            texto_control,

            True,

            (180, 240, 180)

        )

        self.pantalla.blit(
            control,
            (20, 128)
        )


        # =====================================
        # FILA 5: FÍSICA, JAGUAR Y EFICIENCIA
        # =====================================

        fisica = self.fuente_pequena.render(

            f"Cazador: "
            f"{self.cuerpo_cazador.masa} kg, "
            f"{self.cuerpo_cazador.velocidad:.1f} m/s",

            True,

            (200, 200, 255)

        )

        self.pantalla.blit(
            fisica,
            (20, 153)
        )


        if self.mundo.jaguar_vivo:

            texto_jaguar = (
                f"Jaguar: {self.agente_jaguar.estado}, "
                f"{self.cuerpo_jaguar.velocidad:.1f} m/s"
            )

        else:

            texto_jaguar = "Jaguar: cazado"


        jaguar = self.fuente_pequena.render(

            texto_jaguar,

            True,

            (240, 180, 120)

        )

        self.pantalla.blit(
            jaguar,
            (200, 153)
        )


        memoria = self.agente.memoria

        eficiencia = self.fuente_pequena.render(

            f"Pasos: {memoria.pasos} "
            f"(repetidos: {memoria.pasos_repetidos})",

            True,

            (220, 220, 220)

        )

        self.pantalla.blit(
            eficiencia,
            (400, 153)
        )


        # =====================================
        # TACTO: ARENA ALREDEDOR
        # =====================================

        arena_cercana = (
            self.agente
            .sentidos
            .arena_cercana
        )


        if arena_cercana:

            # Solo la inicial: N, S, E, O

            texto_arena = ", ".join(
                direccion[0]
                for direccion in arena_cercana
            )

        else:

            texto_arena = "Ninguna"


        arena = self.fuente_pequena.render(

            f"Arena cerca: {texto_arena}",

            True,

            (230, 190, 140)

        )

        self.pantalla.blit(
            arena,
            (200, 128)
        )


        # =====================================
        # LO QUE HA APRENDIDO DE LAS BAYAS
        # "?" = todavía no la prueba
        # =====================================

        conocimiento = (
            self.agente
            .memoria
            .conocimiento_bayas
        )

        texto_azules = (
            conocimiento["azul"] or "?"
        )

        texto_rojas = (
            conocimiento["roja"] or "?"
        )


        bayas = self.fuente_pequena.render(

            f"Rojas: {texto_rojas}  "
            f"Azules: {texto_azules}",

            True,

            (220, 220, 220)

        )

        self.pantalla.blit(
            bayas,
            (400, 128)
        )


    # =========================================
    # ALCANCE DE UN SENTIDO
    #
    # Dibuja el borde de cada celda.
    # margen: cuántos píxeles hacia adentro
    # de la celda va el cuadro.
    # =========================================

    def dibujar_alcance(
        self,
        celdas,
        color,
        margen
    ):

        tamano = self.mundo.tamano_celda


        for fila, columna in celdas:

            rect = pygame.Rect(

                columna * tamano + margen,

                self.alto_panel
                +
                fila * tamano
                +
                margen,

                tamano - 2 * margen,

                tamano - 2 * margen

            )


            pygame.draw.rect(

                self.pantalla,

                color,

                rect,

                # Grosor
                2

            )


    # =========================================
    # TABLERO
    # =========================================

    def dibujar_tablero(self):

        # =====================================
        # ZONA EXACTA DEL MUNDO
        # =====================================

        zona_mundo = pygame.Rect(

            0,

            self.alto_panel,

            self.mundo.ancho,

            self.mundo.alto

        )


        # =====================================
        # CLIPPING
        #
        # Nada puede dibujarse fuera del
        # área del mundo.
        # =====================================

        self.pantalla.set_clip(
            zona_mundo
        )


        # =====================================
        # FONDO
        # =====================================

        pygame.draw.rect(

            self.pantalla,

            (67, 160, 71),

            zona_mundo

        )


        # =====================================
        # CUADRÍCULA VERTICAL
        # =====================================

        for columna in range(
            self.mundo.columnas + 1
        ):

            x = (

                columna
                *
                self.mundo.tamano_celda

            )


            pygame.draw.line(

                self.pantalla,

                (45, 120, 55),

                (
                    x,
                    self.alto_panel
                ),

                (
                    x,
                    self.alto
                ),

                1

            )


        # =====================================
        # CUADRÍCULA HORIZONTAL
        # =====================================

        for fila in range(
            self.mundo.filas + 1
        ):

            y = (

                self.alto_panel

                +

                fila
                *
                self.mundo.tamano_celda

            )


            pygame.draw.line(

                self.pantalla,

                (45, 120, 55),

                (
                    0,
                    y
                ),

                (
                    self.ancho,
                    y
                ),

                1

            )


        # =====================================
        # ALCANCE DE LOS SENTIDOS
        #
        # Cada sentido tiene su color (el mismo
        # que su texto en el panel) y su cuadro
        # va un poco más adentro de la casilla,
        # para que se vean aunque compartan
        # casillas.
        #
        # Vista:  amarillo, borde exterior
        # Oído:   gris, en medio
        # Olfato: azul cielo, más adentro
        # =====================================

        sentidos = self.agente.sentidos

        posicion = self.agente.posicion


        self.dibujar_alcance(

            sentidos.obtener_celdas_visibles(
                posicion
            ),

            (240, 220, 80),

            0

        )


        self.dibujar_alcance(

            sentidos.obtener_celdas_oido(
                posicion
            ),

            (190, 195, 200),

            5

        )


        self.dibujar_alcance(

            sentidos.obtener_celdas_olfato(
                posicion
            ),

            (110, 200, 245),

            10

        )


        # =====================================
        # RECURSOS DEL MAPA
        # =====================================

        for (
            fila,
            columna
        ), tipo in self.mundo.grid.items():


            # Árbol

            if tipo == 1:

                self.arbol.dibujar(

                    self.pantalla,

                    fila,

                    columna,

                    self.alto_panel

                )


            # Arena

            elif tipo == 4:

                self.arena.dibujar(

                    self.pantalla,

                    fila,

                    columna,

                    self.alto_panel

                )


            # Baya buena

            elif tipo == 5:

                self.baya.dibujar(

                    self.pantalla,

                    fila,

                    columna,

                    True,

                    self.alto_panel

                )


            # Baya mala

            elif tipo == 6:

                self.baya.dibujar(

                    self.pantalla,

                    fila,

                    columna,

                    False,

                    self.alto_panel

                )


        # =====================================
        # CAMPAMENTO
        #
        # Se dibuja ANTES del cazador.
        # =====================================

        fila, columna = (
            self.mundo.campamento
        )


        self.campamento.dibujar(

            self.pantalla,

            fila,

            columna,

            self.alto_panel

        )


        # =====================================
        # JAGUAR
        #
        # Se dibuja en su posición física
        # (entre dos casillas si va caminando).
        # =====================================

        if self.mundo.jaguar_vivo:

            fila_jaguar, columna_jaguar = (
                self.cuerpo_jaguar.posicion_visual()
            )

            self.jaguar.dibujar(
                self.pantalla,
                fila_jaguar,
                columna_jaguar,
                self.alto_panel
            )


        # =====================================
        # CAZADOR
        #
        # Se dibuja en su posición física
        # (entre dos casillas si va caminando).
        # =====================================

        fila, columna = (
            self.cuerpo_cazador.posicion_visual()
        )


        self.cazador.dibujar(

            self.pantalla,

            fila,

            columna,

            self.alto_panel

        )


        # =====================================
        # QUITAR CLIPPING
        # =====================================

        self.pantalla.set_clip(
            None
        )