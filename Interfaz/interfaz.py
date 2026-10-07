import pygame
import os
import math

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

        self.alto_panel = 190


        # =========================================
        # RESOLUCIÓN NATIVA
        # =========================================

        info_pantalla = pygame.display.Info()

        self.ancho = info_pantalla.current_w
        self.alto = info_pantalla.current_h


        # =========================================
        # AJUSTAR TAMAÑO DEL MAPA
        # =========================================

        margen_lateral = 120
        margen_inferior = 80

        espacio_disponible_x = (
            self.ancho
            -
            margen_lateral
        )

        espacio_disponible_y = (
            self.alto
            -
            self.alto_panel
            -
            margen_inferior
        )

        tamano_posible_x = (
            espacio_disponible_x
            //
            self.mundo.columnas
        )

        tamano_posible_y = (
            espacio_disponible_y
            //
            self.mundo.filas
        )

        self.mundo.tamano_celda = min(
            tamano_posible_x,
            tamano_posible_y
        )

        self.mundo.ancho = (
            self.mundo.columnas
            *
            self.mundo.tamano_celda
        )

        self.mundo.alto = (
            self.mundo.filas
            *
            self.mundo.tamano_celda
        )


        # =========================================
        # CENTRAR MAPA
        # =========================================

        self.offset_mapa_x = (
            (self.ancho - self.mundo.ancho)
            //
            2
        )

        self.offset_mapa_y = (
            self.alto_panel
            +
            (
                (
                    self.alto
                    -
                    self.alto_panel
                    -
                    self.mundo.alto
                )
                //
                2
            )
        )


        # =========================================
        # PANTALLA
        # =========================================

        self.pantalla = pygame.display.set_mode(
            (
                self.ancho,
                self.alto
            ),
            pygame.NOFRAME
        )

        pygame.display.set_caption(
            "Agente Cazador vs Jaguar"
        )

        # =========================================
        # FONDO VISUAL DE MAIN
        # =========================================

        ruta_fondo = os.path.join(
            "Recursos",
            "images",
            "fondo.jpg"
        )

        try:

            imagen_raw = pygame.image.load(
                ruta_fondo
            ).convert()

            self.fondo_juego = pygame.transform.smoothscale(
                imagen_raw,
                (
                    self.ancho,
                    self.alto
                )
            )

            self.usa_fondo_img = True

        except Exception:

            print(
                "No se encontró fondo.jpg. Usando color base."
            )

            self.usa_fondo_img = False


        


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
        # FUENTES DEL VISUAL DE MAIN
        # =========================================

        self.fuente_subtitulo = pygame.font.SysFont(
            "trebuchetms,georgia",
            13,
            bold=True
        )

        self.fuente_UI = pygame.font.SysFont(
            "trebuchetms,arial",
            14,
            bold=True
        )

        self.fuente_numeros = pygame.font.SysFont(
            "impact,arialblack",
            18
        )

        # =========================================
        # COLORES DEL VISUAL DE MAIN
        # =========================================

        self.C_MADERA_FONDO = (28, 19, 14)
        self.C_MADERA_BASE = (42, 28, 22)
        self.C_MADERA_LUZ = (65, 45, 33)
        self.C_MADERA_SOMBRA = (15, 10, 8)

        self.C_ORO_PURO = (255, 215, 0)
        self.C_ORO_VIEJO = (184, 134, 11)
        self.C_BRONCE = (140, 95, 30)

        self.C_NEON_ROJO = (255, 60, 60)
        self.C_NEON_VERDE = (50, 255, 100)
        self.C_NEON_AZUL = (60, 180, 255)
        self.C_NEON_AMARILLO = (255, 220, 50)
        self.C_NEON_MORADO = (200, 80, 255)

        # =========================================
        # SIMULACIÓN para que se empiece a mover 
        # =========================================

        self.ejecutando = True

        self.en_curso = True


        # =========================================
        # RELOJ
        # =========================================

        self.reloj = pygame.time.Clock()

    def reiniciar_simulacion(self):

        # =========================================
        # CREAR MUNDO NUEVO
        # =========================================

        self.mundo = MundoSelva()


        # =========================================
        # RECALCULAR TAMAÑO DEL MAPA
        # =========================================

        espacio_disponible_x = (
            self.ancho
            -
            120
        )

        espacio_disponible_y = (
            self.alto
            -
            self.alto_panel
            -
            80
        )

        tamano_posible_x = (
            espacio_disponible_x
            //
            self.mundo.columnas
        )

        tamano_posible_y = (
            espacio_disponible_y
            //
            self.mundo.filas
        )

        self.mundo.tamano_celda = min(
            tamano_posible_x,
            tamano_posible_y
        )

        self.mundo.ancho = (
            self.mundo.columnas
            *
            self.mundo.tamano_celda
        )

        self.mundo.alto = (
            self.mundo.filas
            *
            self.mundo.tamano_celda
        )


        # =========================================
        # CENTRAR NUEVO MAPA
        # =========================================

        self.offset_mapa_x = (
            self.ancho
            -
            self.mundo.ancho
        ) // 2

        self.offset_mapa_y = (
            self.alto_panel
            +
            (
                (
                    self.alto
                    -
                    self.alto_panel
                    -
                    self.mundo.alto
                )
                //
                2
            )
        )


        # =========================================
        # NUEVOS AGENTES
        # =========================================

        self.agente = AgenteCazador(
            self.mundo
        )

        self.agente_jaguar = AgenteJaguar(
            self.mundo
        )


        # =========================================
        # NUEVA FÍSICA
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


        # Al reiniciar queda pausado
        self.en_curso = False

    
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

                # ESPACIO = pausa / continuar
                if evento.key == pygame.K_SPACE:

                    self.en_curso = (
                        not self.en_curso
                    )


                # R = reiniciar
                elif evento.key == pygame.K_r:

                    self.reiniciar_simulacion()


                # ESC = salir
                elif evento.key == pygame.K_ESCAPE:

                    self.ejecutando = False


            # =====================================
            # CLIC DEL MOUSE
            # =====================================

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    posicion_mouse = evento.pos


                    if (
                        hasattr(
                            self,
                            "rect_btn_pausa"
                        )
                        and
                        self.rect_btn_pausa.collidepoint(
                            posicion_mouse
                        )
                    ):

                        self.en_curso = (
                            not self.en_curso
                        )


                    if (
                        hasattr(
                            self,
                            "rect_btn_reiniciar"
                        )
                        and
                        self.rect_btn_reiniciar.collidepoint(
                            posicion_mouse
                        )
                    ):

                        self.reiniciar_simulacion()

    def dibujar(self):

        # =====================================
        # FONDO GENERAL
        # =====================================

        if self.usa_fondo_img:

            self.pantalla.blit(
                self.fondo_juego,
                (0, 0)
            )

        else:

            self.pantalla.fill(
                self.C_MADERA_SOMBRA
            )


        # =====================================
        # MUNDO
        # =====================================

        self.dibujar_tablero()


        # =====================================
        # PANEL
        # =====================================

        self.dibujar_panel()

    def dibujar_caja_biselada_solida(
        self,
        rect,
        color_base,
        color_luz,
        color_sombra,
        grosor_borde=2
    ):

        pygame.draw.rect(
            self.pantalla,
            color_base,
            rect,
            border_radius=8
        )

        pygame.draw.line(
            self.pantalla,
            color_luz,
            (rect.left + 5, rect.top),
            (rect.right - 5, rect.top),
            grosor_borde
        )

        pygame.draw.line(
            self.pantalla,
            color_luz,
            (rect.left, rect.top + 5),
            (rect.left, rect.bottom - 5),
            grosor_borde
        )

        pygame.draw.line(
            self.pantalla,
            color_sombra,
            (rect.left + 5, rect.bottom),
            (rect.right - 5, rect.bottom),
            grosor_borde
        )

        pygame.draw.line(
            self.pantalla,
            color_sombra,
            (rect.right, rect.top + 5),
            (rect.right, rect.bottom - 5),
            grosor_borde
        )

    def dibujar_slot_sentido_animado(
        self,
        x,
        y,
        ancho,
        nombre_sentido,
        valor_texto,
        esta_activo,
        color_activo
    ):

        alto_slot = 32

        rect_slot = pygame.Rect(
            x,
            y,
            ancho,
            alto_slot
        )

        pygame.draw.rect(
            self.pantalla,
            (20, 14, 10),
            rect_slot,
            border_radius=5
        )

        pygame.draw.rect(
            self.pantalla,
            (45, 30, 20),
            rect_slot,
            1,
            border_radius=5
        )

        label = self.fuente_UI.render(
            nombre_sentido,
            True,
            self.C_ORO_VIEJO
        )

        self.pantalla.blit(
            label,
            (
                x + 10,
                y + 8
            )
        )

        if esta_activo:

            color_capsula = color_activo
            color_texto = (255, 255, 255)

        else:

            color_capsula = (50, 60, 55)
            color_texto = (150, 160, 155)

        ancho_capsula = ancho - 90

        rect_capsula = pygame.Rect(
            x + 82,
            y + 4,
            ancho_capsula,
            alto_slot - 8
        )

        # Glow cuando el sentido está activo
        if esta_activo:

            tiempo = pygame.time.get_ticks()

            glow_alpha = int(
                40
                +
                30 * math.sin(
                    tiempo / 150.0
                )
            )

            superficie_glow = pygame.Surface(
                (
                    ancho_capsula + 6,
                    alto_slot - 2
                ),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                superficie_glow,
                (
                    *color_activo,
                    glow_alpha
                ),
                superficie_glow.get_rect(),
                border_radius=4
            )

            self.pantalla.blit(
                superficie_glow,
                (
                    rect_capsula.x - 3,
                    rect_capsula.y - 3
                )
            )

        pygame.draw.rect(
            self.pantalla,
            color_capsula,
            rect_capsula,
            border_radius=4
        )

        # Evitar textos demasiado largos
        if len(valor_texto) > 18:
            valor_texto = (
                valor_texto[:15]
                +
                "..."
            )

        valor = self.fuente_UI.render(
            valor_texto,
            True,
            color_texto
        )

        vx = (
            rect_capsula.x
            +
            (
                rect_capsula.width
                -
                valor.get_width()
            )
            // 2
        )

        vy = (
            rect_capsula.y
            +
            (
                rect_capsula.height
                -
                valor.get_height()
            )
            // 2
        )

        self.pantalla.blit(
            valor,
            (
                vx,
                vy
            )
        )

    def dibujar_boton(
        self,
        rect,
        texto,
        color_base,
        color_hover
    ):

        mouse = pygame.mouse.get_pos()

        esta_sobre = rect.collidepoint(
            mouse
        )

        if esta_sobre:

            color = color_hover

        else:

            color = color_base


        pygame.draw.rect(
            self.pantalla,
            color,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            self.pantalla,
            self.C_ORO_VIEJO,
            rect,
            2,
            border_radius=6
        )


        texto_render = self.fuente_UI.render(
            texto,
            True,
            (255, 255, 255)
        )

        x_texto = (
            rect.x
            +
            (
                rect.width
                -
                texto_render.get_width()
            )
            // 2
        )

        y_texto = (
            rect.y
            +
            (
                rect.height
                -
                texto_render.get_height()
            )
            // 2
        )

        self.pantalla.blit(
            texto_render,
            (
                x_texto,
                y_texto
            )
        )

    def dibujar_panel(self):

        # =====================================
        # FONDO GENERAL
        # =====================================

        pygame.draw.rect(
            self.pantalla,
            self.C_MADERA_FONDO,
            (
                0,
                0,
                self.ancho,
                self.alto_panel
            )
        )

        for x in range(
            0,
            self.ancho,
            150
        ):

            pygame.draw.line(
                self.pantalla,
                (20, 12, 8),
                (x, 0),
                (x, self.alto_panel),
                3
            )


        pygame.draw.rect(
            self.pantalla,
            self.C_ORO_PURO,
            (
                0,
                self.alto_panel - 6,
                self.ancho,
                6
            )
        )


        # =====================================
        # TAMAÑOS DE BLOQUES
        # =====================================

        margen = 25
        separacion = 25

        ancho_izq = 330
        ancho_der = 400

        ancho_centro = (
            self.ancho
            -
            ancho_izq
            -
            ancho_der
            -
            margen * 2
            -
            separacion * 2
        )

        x_izq = margen

        x_centro = (
            x_izq
            +
            ancho_izq
            +
            separacion
        )

        x_der = (
            x_centro
            +
            ancho_centro
            +
            separacion
        )


        # =====================================
        # BLOQUE IZQUIERDO
        # =====================================

        rect_izq = pygame.Rect(
            x_izq,
            20,
            ancho_izq,
            145
        )

        self.dibujar_caja_biselada_solida(
            rect_izq,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )


        titulo1 = self.fuente_titulo.render(
            "AGENTE",
            True,
            (255, 255, 255)
        )

        titulo2 = self.fuente_titulo.render(
            " CAZADOR",
            True,
            self.C_ORO_PURO
        )

        self.pantalla.blit(
            titulo1,
            (
                x_izq + 20,
                35
            )
        )

        self.pantalla.blit(
            titulo2,
            (
                x_izq + 20 + titulo1.get_width(),
                35
            )
        )


        estado = str(
            self.agente.estado
        )

        if len(estado) > 32:
            estado = estado[:29] + "..."


        texto_estado = self.fuente_UI.render(
            f"Estado: {estado}",
            True,
            self.C_ORO_VIEJO
        )

        self.pantalla.blit(
            texto_estado,
            (
                x_izq + 20,
                75
            )
        )


        if self.mundo.jaguar_vivo:

            texto_jaguar = (
                f"Jaguar: "
                f"{self.agente_jaguar.estado}"
            )

        else:

            texto_jaguar = (
                "Jaguar: cazado"
            )


        jaguar = self.fuente_UI.render(
            texto_jaguar,
            True,
            (240, 180, 120)
        )

        self.pantalla.blit(
            jaguar,
            (
                x_izq + 20,
                105
            )
        )


        fisica = self.fuente_pequena.render(
            (
                f"Cazador {self.cuerpo_cazador.velocidad:.1f} m/s"
                f"   Jaguar {self.cuerpo_jaguar.velocidad:.1f} m/s"
            ),
            True,
            (210, 210, 220)
        )

        self.pantalla.blit(
            fisica,
            (
                x_izq + 20,
                135
            )
        )


        # =====================================
        # BLOQUE CENTRAL - SENTIDOS
        # =====================================

        rect_centro = pygame.Rect(
            x_centro,
            20,
            ancho_centro,
            145
        )

        self.dibujar_caja_biselada_solida(
            rect_centro,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )


        titulo_sentidos = (
            self.fuente_subtitulo.render(
                "MATRIZ SENSORIAL",
                True,
                self.C_ORO_PURO
            )
        )

        self.pantalla.blit(
            titulo_sentidos,
            (
                x_centro + 20,
                30
            )
        )


        sentidos = self.agente.sentidos


        vista = (
            "Jaguar detectado"
            if sentidos.ve_jaguar
            else "Sin detección"
        )


        oido = (
            str(sentidos.direccion_sonido)
            if sentidos.escucha_jaguar
            else "Silencio"
        )


        if sentidos.huele_jaguar:

            olfato = "Jaguar"

        elif sentidos.huele_bayas:

            olfato = (
                "Bayas "
                +
                PLURAL_COLORES[
                    sentidos.color_olor_bayas
                ]
            )

        else:

            olfato = "Sin detección"


        tacto = str(
            sentidos.sensacion_tacto
        )

        gusto = str(
            sentidos.sensacion_gusto
        )

                # =====================================
        # SLOTS VISUALES DE LOS 5 SENTIDOS
        # =====================================

        padding = 15

        ancho_slot = (
            ancho_centro
            -
            padding * 3
        ) // 2

        x_col1 = (
            x_centro
            +
            padding
        )

        x_col2 = (
            x_col1
            +
            ancho_slot
            +
            padding
        )


        # =====================================
        # VISIÓN
        # =====================================

        self.dibujar_slot_sentido_animado(
            x_col1,
            55,
            ancho_slot,
            "Visión",
            vista,
            sentidos.ve_jaguar,
            self.C_NEON_ROJO
        )


        # =====================================
        # OÍDO
        # =====================================

        self.dibujar_slot_sentido_animado(
            x_col1,
            95,
            ancho_slot,
            "Oído",
            oido,
            sentidos.escucha_jaguar,
            self.C_NEON_AMARILLO
        )


        # =====================================
        # OLFATO
        # =====================================

        olfato_activo = (
            sentidos.huele_jaguar
            or
            sentidos.huele_bayas
        )

        self.dibujar_slot_sentido_animado(
            x_col2,
            55,
            ancho_slot,
            "Olfato",
            olfato,
            olfato_activo,
            self.C_NEON_MORADO
        )


        # =====================================
        # TACTO
        # =====================================

        tacto_activo = bool(
            sentidos.arena_cercana
        )

        self.dibujar_slot_sentido_animado(
            x_col2,
            95,
            ancho_slot,
            "Tacto",
            tacto,
            tacto_activo,
            self.C_NEON_AZUL
        )


        # =====================================
        # GUSTO
        # =====================================

        gusto_activo = (
            gusto != "Sin alimento"
        )

        x_gusto = (
            x_centro
            +
            (
                ancho_centro
                -
                ancho_slot
            )
            // 2
        )

        self.dibujar_slot_sentido_animado(
            x_gusto,
            132,
            ancho_slot,
            "Gusto",
            gusto,
            gusto_activo,
            self.C_NEON_VERDE
        )

            

        # =====================================
        # BLOQUE DERECHO
        # =====================================

        rect_der = pygame.Rect(
            x_der,
            20,
            ancho_der,
            145
        )

        self.dibujar_caja_biselada_solida(
            rect_der,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )


        energia = self.agente.energia


        titulo_energia = (
            self.fuente_UI.render(
                f"ENERGÍA: {int(energia)}%",
                True,
                self.C_ORO_PURO
            )
        )

        self.pantalla.blit(
            titulo_energia,
            (
                x_der + 20,
                35
            )
        )


        # Fondo barra energía

        barra_fondo = pygame.Rect(
            x_der + 20,
            65,
            ancho_der - 40,
            20
        )

        pygame.draw.rect(
            self.pantalla,
            (15, 10, 10),
            barra_fondo,
            border_radius=10
        )


        ancho_energia = int(
            (
                ancho_der - 46
            )
            *
            max(
                0,
                min(
                    energia / 100,
                    1
                )
            )
        )


        if energia > 30:

            color_energia = (
                self.C_NEON_VERDE
            )

        else:

            color_energia = (
                self.C_NEON_ROJO
            )


        barra_energia = pygame.Rect(
            x_der + 23,
            68,
            ancho_energia,
            14
        )

        pygame.draw.rect(
            self.pantalla,
            color_energia,
            barra_energia,
            border_radius=7
        )


        memoria = self.agente.memoria


        info1 = self.fuente_pequena.render(
            (
                f"Memoria: "
                f"{len(memoria.celdas_revisadas)} celdas"
            ),
            True,
            (220, 220, 220)
        )

        self.pantalla.blit(
            info1,
            (
                x_der + 20,
                100
            )
        )


        info2 = self.fuente_pequena.render(
            (
                f"Pasos: {memoria.pasos} "
                f"| Repetidos: {memoria.pasos_repetidos}"
            ),
            True,
            (220, 220, 220)
        )

        self.pantalla.blit(
            info2,
            (
                x_der + 20,
                120
            )
        )

            # =====================================
        # BOTONES
        # =====================================

        ancho_boton = (
            ancho_der - 55
        ) // 2


        self.rect_btn_pausa = pygame.Rect(
            x_der + 20,
            137,
            ancho_boton,
            25
        )

        self.rect_btn_reiniciar = pygame.Rect(
            x_der
            +
            35
            +
            ancho_boton,
            137,
            ancho_boton,
            25
        )


        if self.en_curso:

            texto_pausa = "PAUSAR"

            color_pausa = (
                150,
                45,
                45
            )

            color_pausa_hover = (
                220,
                70,
                70
            )

        else:

            texto_pausa = "INICIAR"

            color_pausa = (
                40,
                130,
                65
            )

            color_pausa_hover = (
                60,
                200,
                90
            )


        self.dibujar_boton(
            self.rect_btn_pausa,
            texto_pausa,
            color_pausa,
            color_pausa_hover
        )


        self.dibujar_boton(
            self.rect_btn_reiniciar,
            "REINICIAR",
            (
                40,
                90,
                160
            ),
            (
                70,
                140,
                230
            )
        )
        

    def dibujar_alcance(
        self,
        celdas,
        color,
        margen
    ):

        tamano = self.mundo.tamano_celda

        for fila, columna in celdas:

            rect = pygame.Rect(

                self.offset_mapa_x
                +
                columna * tamano
                +
                margen,

                self.offset_mapa_y
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
                2
            )

    def dibujar_tablero(self):


        # =====================================
        # ZONA DEL MUNDO CENTRADA
        # =====================================

        zona_mundo = pygame.Rect(

            self.offset_mapa_x,
            self.offset_mapa_y,
            self.mundo.ancho,
            self.mundo.alto

        )


        # =====================================
        # FONDO DEL MAPA
        # =====================================

        pygame.draw.rect(

            self.pantalla,

            (67, 160, 71),

            zona_mundo

        )


        # =====================================
        # CLIPPING
        # =====================================

        self.pantalla.set_clip(
            zona_mundo
        )


        # =====================================
        # CUADRÍCULA VERTICAL
        # =====================================

        for columna in range(
            self.mundo.columnas + 1
        ):

            x = (
                self.offset_mapa_x
                +
                columna * self.mundo.tamano_celda
            )

            pygame.draw.line(

                self.pantalla,

                (45, 120, 55),

                (
                    x,
                    self.offset_mapa_y
                ),

                (
                    x,
                    self.offset_mapa_y
                    +
                    self.mundo.alto
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
                self.offset_mapa_y
                +
                fila * self.mundo.tamano_celda
            )

            pygame.draw.line(

                self.pantalla,

                (45, 120, 55),

                (
                    self.offset_mapa_x,
                    y
                ),

                (
                    self.offset_mapa_x
                    +
                    self.mundo.ancho,
                    y
                ),

                1
            )


        # =====================================
        # SENTIDOS
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
        # SUPERFICIE DE ENTIDADES
        # =====================================

        sup_entidades = pygame.Surface(

            (
                self.mundo.ancho,
                self.mundo.alto
            ),

            pygame.SRCALPHA

        )


        # =====================================
        # RECURSOS
        # =====================================

        for (
            fila,
            columna
        ), tipo in self.mundo.grid.items():

            if tipo == 1:

                self.arbol.dibujar(
                    sup_entidades,
                    fila,
                    columna,
                    0
                )

            elif tipo == 4:

                self.arena.dibujar(
                    sup_entidades,
                    fila,
                    columna,
                    0
                )

            elif tipo == 5:

                self.baya.dibujar(
                    sup_entidades,
                    fila,
                    columna,
                    True,
                    0
                )

            elif tipo == 6:

                self.baya.dibujar(
                    sup_entidades,
                    fila,
                    columna,
                    False,
                    0
                )


        # =====================================
        # CAMPAMENTO
        # =====================================

        fila, columna = self.mundo.campamento

        self.campamento.dibujar(

            sup_entidades,

            fila,
            columna,
            0

        )


        # =====================================
        # JAGUAR
        # =====================================

        if self.mundo.jaguar_vivo:

            fila_jaguar, columna_jaguar = (
                self.cuerpo_jaguar.posicion_visual()
            )

            self.jaguar.dibujar(

                sup_entidades,

                fila_jaguar,
                columna_jaguar,
                0

            )


        # =====================================
        # CAZADOR
        # =====================================

        fila, columna = (
            self.cuerpo_cazador.posicion_visual()
        )

        self.cazador.dibujar(

            sup_entidades,

            fila,
            columna,
            0

        )


        # =====================================
        # PEGAR ENTIDADES EN EL MAPA CENTRADO
        # =====================================

        self.pantalla.blit(

            sup_entidades,

            (
                self.offset_mapa_x,
                self.offset_mapa_y
            )

        )


        # =====================================
        # QUITAR CLIPPING
        # =====================================

        self.pantalla.set_clip(
            None
        )
        # =====================================
        # MARCO ALREDEDOR DEL MAPA
        # =====================================

        marco_rect = pygame.Rect(

            self.offset_mapa_x - 10,

            self.offset_mapa_y - 10,

            self.mundo.ancho + 20,

            self.mundo.alto + 20
        )

        self.dibujar_marco_hueco_mapa(

            marco_rect,

            self.C_MADERA_BASE,

            self.C_MADERA_LUZ,

            self.C_MADERA_SOMBRA,

            grosor_madera=6
        )

        # =========================================

    def dibujar_marco_hueco_mapa(
        self,
        rect,
        color_base,
        color_luz,
        color_sombra,
        grosor_madera=6
    ):

        # Sombra exterior
        pygame.draw.rect(

            self.pantalla,

            (10, 5, 5),

            rect.inflate(8, 8).move(2, 4),

            grosor_madera + 4,

            border_radius=12
        )


        # Base de madera
        pygame.draw.rect(

            self.pantalla,

            color_base,

            rect.inflate(4, 4),

            grosor_madera,

            border_radius=8
        )


        # Ribete dorado interior
        pygame.draw.rect(

            self.pantalla,

            self.C_ORO_PURO,

            rect.inflate(-2, -2),

            2,

            border_radius=4
        )

