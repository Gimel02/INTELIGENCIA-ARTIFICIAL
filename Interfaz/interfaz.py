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


from Recursos.arbol import Arbol
from Recursos.bayas import Baya
from Recursos.arena import ArenaMovediza
from Recursos.campamento import Campamento
from Recursos.cazador import Cazador
from Recursos.puma import Puma

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
        # PANEL SUPERIOR
        # =========================================

        self.alto_panel = 130

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

        self.puma = Puma(
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
        # VELOCIDAD DEL AGENTE
        # =========================================

        # Cada cuánto toma una decisión
        # 500 ms = dos veces por segundo

        self.intervalo_agente = 500

        self.ultimo_movimiento = (
            pygame.time.get_ticks()
        )


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
            # ACTUALIZAR AGENTE
            # =====================================

            tiempo_actual = (
                pygame.time.get_ticks()
            )


            if self.en_curso:

                if (

                    tiempo_actual
                    -
                    self.ultimo_movimiento

                    >=

                    self.intervalo_agente

                ):

                    self.agente.tomar_decision(

                        self.mundo.posicion_puma

                    )


                    self.ultimo_movimiento = (
                        tiempo_actual
                    )


            # =====================================
            # DIBUJAR
            # =====================================

            self.dibujar()

            pygame.display.flip()


            # La interfaz puede correr a 60 FPS,
            # aunque el cazador solo tome una
            # decisión cada 500 ms.

            self.reloj.tick(60)


        pygame.quit()


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

        if self.agente.sentidos.ve_puma:

            texto_vista = (
                "Puma detectado"
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
            .escucha_puma
        ):

            texto_oido = (

                self.agente
                .sentidos
                .direccion_sonido

            )

        else:

            texto_oido = (
                "Sin detección"
            )


        oido = self.fuente_pequena.render(

            f"Oído: {texto_oido}",

            True,

            (210, 220, 230)

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
            (20, 105)
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
            # RANGO DEL OÍDO
            # =====================================

            celdas_oido = (

                self.agente
                .sentidos
                .obtener_celdas_oido(

                    self.agente.posicion

                )

            )


            for fila, columna in celdas_oido:

                rect = pygame.Rect(

                    columna
                    *
                    self.mundo.tamano_celda,

                    self.alto_panel
                    +
                    fila
                    *
                    self.mundo.tamano_celda,

                    self.mundo.tamano_celda,

                    self.mundo.tamano_celda

                )


                pygame.draw.rect(

                    self.pantalla,

                    # Gris
                    (174, 182, 191),

                    rect,

                    # Grosor
                    1

                )




        # =====================================
        # RANGO DE VISIÓN
        # =====================================

        celdas_visibles = (

            self.agente
            .sentidos
            .obtener_celdas_visibles(

                self.agente.posicion

            )

        )


        for fila, columna in celdas_visibles:

            rect = pygame.Rect(

                columna*self.mundo.tamano_celda,

                self.alto_panel
                +
                fila*self.mundo.tamano_celda,

                self.mundo.tamano_celda,

                self.mundo.tamano_celda

            )


            pygame.draw.rect(

                self.pantalla,

                (240, 220, 80),

                rect,

                2

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
        # PUMA
        #
        # Por ahora lo dibujamos directamente.
        # Después conectamos Recursos/puma.py.
        # =====================================
        if self.mundo.puma_vivo:

            fila_puma, columna_puma = (
                self.mundo.posicion_puma
            )

            self.puma.dibujar(
                self.pantalla,
                fila_puma,
                columna_puma,
                self.alto_panel
            )


        # =====================================
        # CAZADOR
        #
        # IMPORTANTE:
        # YA NO SE USA inicio_cazador.
        # =====================================

        fila, columna = (
            self.agente.posicion
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