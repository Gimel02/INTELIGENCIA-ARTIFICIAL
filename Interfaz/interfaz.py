from Recursos import raton
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
from Logica_Difusa.dios import obtener_dios

from Fisica.cinematica import CuerpoFisico


from Recursos.arbol import Arbol
from Recursos.bayas import Baya
from Recursos.arena import ArenaMovediza
from Recursos.campamento import Campamento
from Recursos.cazador import Cazador
from Recursos.jaguar import Jaguar
from Recursos.raton import Raton
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

        # El cazador conoce su propio cuerpo
        # (masa, fuerza, velocidad)

        self.agente.cuerpo = self.cuerpo_cazador


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

        self.alto_panel = 260


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

        self.raton_sprite = Raton(
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

        self.agente.cuerpo = self.cuerpo_cazador

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

        self.raton_sprite = Raton(
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

        # =====================================
        # FIN DEL JUEGO
        # =====================================

        if self.agente.vidas <= 0:

            self.en_curso = False

            return


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
                        self.agente.posicion,
                        self.agente.energia,
                        self.mundo.ratones
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
        # ACTUALIZAR RATONES
        # =====================================

        posicion_jaguar = (
            self.cuerpo_jaguar.posicion_visual()
            if self.mundo.jaguar_vivo
            else None
        )

        for raton in self.mundo.ratones:

            # No mover ratones que ya fueron cazados
            if not raton.vivo:
                continue

            # Actualizar movimiento y dirección
            raton.actualizar(
                dt,
                posicion_jaguar
            )

            # Comprobar si el jaguar alcanza al ratón
            if posicion_jaguar is not None:

                fila, columna = raton.posicion_visual()

                distancia = (
                    (fila - posicion_jaguar[0]) ** 2
                    + (columna - posicion_jaguar[1]) ** 2
                ) ** 0.5

                if distancia < 0.6:
                    raton.vivo = False
                    self.agente_jaguar.comer_raton()
           
        
        # =====================================
        # ENCUENTRO CAZADOR - JAGUAR
        #
        # Si el jaguar está atacando, el que
        # pierde es el cazador. Si no, el
        # cazador atrapa al jaguar.
        # =====================================

        if (
            self.mundo.jaguar_vivo
            and
            self.agente.posicion
            ==
            self.mundo.posicion_jaguar
        ):

            if self.agente_jaguar.atacando:

                self.agente.recibir_ataque()

                self.agente_jaguar.despues_de_atacar()

            else:

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


                # B = imprimir la bitácora del cazador
                elif evento.key == pygame.K_b:

                    self.agente.imprimir_conciencia()





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

    def recortar_texto(self, texto, ancho_maximo):

        # Acorta el texto con "..." si no cabe

        if self.fuente_pequena.size(texto)[0] <= ancho_maximo:

            return texto

        while (
            texto
            and
            self.fuente_pequena.size(texto + "...")[0]
            > ancho_maximo
        ):

            texto = texto[:-1]

        return texto + "..."


    def dibujar_panel(self):

        # =====================================
        # FONDO GENERAL DEL HUD
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

        # Línea inferior dorada
        pygame.draw.rect(
            self.pantalla,
            self.C_ORO_PURO,
            (
                0,
                self.alto_panel - 5,
                self.ancho,
                5
            )
        )


        # =====================================
        # FUNCIONES AUXILIARES
        # =====================================

        def dibujar_titulo(
            texto,
            x,
            y,
            color
        ):

            render = self.fuente_titulo.render(
                texto,
                True,
                color
            )

            self.pantalla.blit(
                render,
                (x, y)
            )


        def dibujar_linea(
            texto,
            x,
            y,
            ancho,
            color=(220, 220, 220)
        ):

            texto = self.recortar_texto(
                str(texto),
                ancho
            )

            render = self.fuente_pequena.render(
                texto,
                True,
                color
            )

            self.pantalla.blit(
                render,
                (x, y)
            )


        def dibujar_barra(
            x,
            y,
            ancho,
            valor,
            maximo,
            color,
            etiqueta
        ):

            valor = max(
                0,
                min(valor, maximo)
            )

            texto = self.fuente_UI.render(
                f"{etiqueta}: {int(valor)}",
                True,
                (235, 235, 235)
            )

            self.pantalla.blit(
                texto,
                (x, y)
            )

            fondo = pygame.Rect(
                x,
                y + 22,
                ancho,
                15
            )

            pygame.draw.rect(
                self.pantalla,
                (15, 10, 10),
                fondo,
                border_radius=7
            )

            proporcion = (
                valor / maximo
                if maximo > 0
                else 0
            )

            relleno = pygame.Rect(
                x + 2,
                y + 24,
                int(
                    (ancho - 4)
                    *
                    proporcion
                ),
                11
            )

            pygame.draw.rect(
                self.pantalla,
                color,
                relleno,
                border_radius=6
            )


        # =====================================
        # DISTRIBUCIÓN DE LOS 4 PANELES
        # =====================================

        margen = 18
        separacion = 12

        disponible = (
            self.ancho
            -
            margen * 2
            -
            separacion * 3
        )

        ancho_cazador = int(
            disponible * 0.32
        )

        ancho_sentidos = int(
            disponible * 0.20
        )

        ancho_jaguar = int(
            disponible * 0.28
        )

        ancho_dios = (
            disponible
            -
            ancho_cazador
            -
            ancho_sentidos
            -
            ancho_jaguar
        )

        x_cazador = margen

        x_sentidos = (
            x_cazador
            +
            ancho_cazador
            +
            separacion
        )

        x_jaguar = (
            x_sentidos
            +
            ancho_sentidos
            +
            separacion
        )

        x_dios = (
            x_jaguar
            +
            ancho_jaguar
            +
            separacion
        )

        y_panel = 15

        alto_caja = (
            self.alto_panel - 35
        )


        # =====================================
        # 1. AGENTE CAZADOR
        # =====================================

        rect_cazador = pygame.Rect(
            x_cazador,
            y_panel,
            ancho_cazador,
            alto_caja
        )

        self.dibujar_caja_biselada_solida(
            rect_cazador,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )

        dibujar_titulo(
            "AGENTE CAZADOR",
            x_cazador + 15,
            25,
            self.C_ORO_PURO
        )


        # Energía

        energia = self.agente.energia

        color_energia = (
            self.C_NEON_VERDE
            if energia > 30
            else self.C_NEON_ROJO
        )

        dibujar_barra(
            x_cazador + 15,
            58,
            ancho_cazador - 30,
            energia,
            getattr(
                self.agente,
                "energia_max",
                100
            ),
            color_energia,
            "Energía"
        )


        memoria = self.agente.memoria

        conocimiento = (
            memoria.conocimiento_bayas
        )

        roja = (
            conocimiento["roja"]
            if conocimiento["roja"] is not None
            else "?"
        )

        azul = (
            conocimiento["azul"]
            if conocimiento["azul"] is not None
            else "?"
        )


        dibujar_linea(
            f"Baya roja: {roja}   |   Baya azul: {azul}",
            x_cazador + 15,
            103,
            ancho_cazador - 30
        )


        dibujar_linea(
            (
                f"Memoria: {len(memoria.celdas_revisadas)} "
                f"| Pasos: {memoria.pasos} "
                f"| Rep: {memoria.pasos_repetidos}"
            ),
            x_cazador + 15,
            125,
            ancho_cazador - 30
        )


        vidas_max = getattr(
            self.agente,
            "vidas_max",
            self.agente.vidas
        )

        dibujar_linea(
            (
                f"Vidas: {self.agente.vidas}/{vidas_max} "
                f"| Puntos: {self.agente.puntos}"
            ),
            x_cazador + 15,
            147,
            ancho_cazador - 30,
            self.C_ORO_VIEJO
        )


        dibujar_linea(
            f"Estado: {self.agente.estado}",
            x_cazador + 15,
            169,
            ancho_cazador - 30,
            (240, 190, 120)
        )


        decision = (
            self.agente.decision_difusa
        )

        if decision:

            accion_difusa = (
                decision["accion"]
            )

        else:

            accion_difusa = "-"


        dibujar_linea(
            f"Difuso: {accion_difusa.upper()}",
            x_cazador + 15,
            191,
            ancho_cazador - 30,
            self.C_NEON_VERDE
        )


        dibujar_linea(
            (
                f"Movimiento: "
                f"{self.agente.ultima_accion} "
                f"← {self.agente.fuente_decision}"
            ),
            x_cazador + 15,
            211,
            ancho_cazador - 30,
            self.C_NEON_AZUL
        )


        # =====================================
        # 2. SENTIDOS
        # =====================================

        rect_sentidos = pygame.Rect(
            x_sentidos,
            y_panel,
            ancho_sentidos,
            alto_caja
        )

        self.dibujar_caja_biselada_solida(
            rect_sentidos,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )

        titulo_sentidos = (
            self.fuente_subtitulo.render(
                "SENTIDOS",
                True,
                self.C_ORO_PURO
            )
        )

        self.pantalla.blit(
            titulo_sentidos,
            (
                x_sentidos + 15,
                30
            )
        )


        sentidos = self.agente.sentidos


        vista = (
            "Jaguar"
            if sentidos.ve_jaguar
            else "Nada"
        )

        oido = (
            str(
                sentidos.direccion_sonido
            )
            if sentidos.escucha_jaguar
            else "Silencio"
        )

        if sentidos.huele_jaguar:

            olfato = "Jaguar"

        elif sentidos.huele_bayas:

            olfato = (
                "Bayas "
                +
                PLURAL_COLORES.get(
                    sentidos.color_olor_bayas,
                    ""
                )
            )

        else:

            olfato = "Nada"


        tacto = str(
            sentidos.sensacion_tacto
        )

        gusto = str(
            sentidos.sensacion_gusto
        )


        ancho_slot = (
            ancho_sentidos - 20
        )


        self.dibujar_slot_sentido_animado(
            x_sentidos + 10,
            55,
            ancho_slot,
            "Vista",
            vista,
            sentidos.ve_jaguar,
            self.C_NEON_ROJO
        )


        self.dibujar_slot_sentido_animado(
            x_sentidos + 10,
            91,
            ancho_slot,
            "Oído",
            oido,
            sentidos.escucha_jaguar,
            self.C_NEON_AMARILLO
        )


        olfato_activo = (
            sentidos.huele_jaguar
            or
            sentidos.huele_bayas
        )

        self.dibujar_slot_sentido_animado(
            x_sentidos + 10,
            127,
            ancho_slot,
            "Olfato",
            olfato,
            olfato_activo,
            self.C_NEON_MORADO
        )


        tacto_activo = bool(
            sentidos.arena_cercana
        )

        self.dibujar_slot_sentido_animado(
            x_sentidos + 10,
            163,
            ancho_slot,
            "Tacto",
            tacto,
            tacto_activo,
            self.C_NEON_AZUL
        )


        gusto_activo = (
            gusto != "Sin alimento"
        )

        self.dibujar_slot_sentido_animado(
            x_sentidos + 10,
            199,
            ancho_slot,
            "Gusto",
            gusto,
            gusto_activo,
            self.C_NEON_VERDE
        )


        # =====================================
        # 3. AGENTE JAGUAR
        # =====================================

        rect_jaguar = pygame.Rect(
            x_jaguar,
            y_panel,
            ancho_jaguar,
            alto_caja
        )

        self.dibujar_caja_biselada_solida(
            rect_jaguar,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )


        dibujar_titulo(
            "AGENTE JAGUAR",
            x_jaguar + 15,
            25,
            (255, 150, 80)
        )


        hambre = (
            self.agente_jaguar.hambre
        )


        dibujar_barra(
            x_jaguar + 15,
            58,
            ancho_jaguar - 30,
            hambre,
            getattr(
                self.agente_jaguar,
                "hambre_max",
                100
            ),
            self.C_NEON_ROJO,
            "Hambre"
        )


        if self.mundo.jaguar_vivo:

            estado_jaguar = (
                self.agente_jaguar.estado
            )

        else:

            estado_jaguar = (
                "Jaguar cazado"
            )


        dibujar_linea(
            f"Estado: {estado_jaguar}",
            x_jaguar + 15,
            103,
            ancho_jaguar - 30,
            (255, 190, 130)
        )


        decision_jaguar = (
            self.agente_jaguar.decision_difusa
        )

        if decision_jaguar:

            accion_jaguar = (
                decision_jaguar["accion"]
            )

            entradas_jaguar = (
                decision_jaguar["entradas"]
            )

        else:

            accion_jaguar = "-"

            entradas_jaguar = {}


        dibujar_linea(
            f"Difuso: {accion_jaguar.upper()}",
            x_jaguar + 15,
            127,
            ancho_jaguar - 30,
            self.C_NEON_AMARILLO
        )


        dibujar_linea(
            (
                f"Distancia cazador: "
                f"{entradas_jaguar.get('distancia_cazador', '-')}"
            ),
            x_jaguar + 15,
            149,
            ancho_jaguar - 30
        )


        dibujar_linea(
            (
                f"Energía cazador percibida: "
                f"{entradas_jaguar.get('energia_cazador', '-')}"
            ),
            x_jaguar + 15,
            171,
            ancho_jaguar - 30
        )


        dibujar_linea(
            (
                f"Velocidad: "
                f"{self.cuerpo_jaguar.velocidad:.2f} m/s"
            ),
            x_jaguar + 15,
            193,
            ancho_jaguar - 30,
            (200, 220, 255)
        )


        dibujar_linea(
            (
                "Atacando: "
                +
                (
                    "SÍ"
                    if self.agente_jaguar.atacando
                    else "NO"
                )
            ),
            x_jaguar + 15,
            213,
            ancho_jaguar - 30,
            (
                self.C_NEON_ROJO
                if self.agente_jaguar.atacando
                else (170, 190, 170)
            )
        )


                # =====================================
        # 4. DIOS / CONTROL
        # =====================================

        rect_dios = pygame.Rect(
            x_dios,
            y_panel,
            ancho_dios,
            alto_caja
        )

        self.dibujar_caja_biselada_solida(
            rect_dios,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )


        dibujar_titulo(
            "DIOS",
            x_dios + 15,
            25,
            (255, 255, 255)
        )


        # =====================================
        # REPRESENTACIÓN VISUAL DE DIOS
        # =====================================

        # =====================================
        # SÍMBOLO TEMPORAL DE DIOS
        # =====================================

        simbolo_dios = self.fuente_titulo.render(
            "♛",
            True,
            self.C_ORO_PURO
        )

        simbolo_x = (
            x_dios
            +
            (
                ancho_dios
                -
                simbolo_dios.get_width()
            )
            // 2
        )

        self.pantalla.blit(
            simbolo_dios,
            (
                simbolo_x,
                70
            )
        )


        # =====================================
        # ESTADO DE LA SIMULACIÓN
        # =====================================

        dibujar_linea(
            f"Turno: {self.agente.turno}",
            x_dios + 15,
            132,
            ancho_dios - 30,
            self.C_ORO_PURO
        )


        if self.agente.vidas <= 0:

            estado_simulacion = (
                "FIN DEL JUEGO"
            )

            color_estado = (
                self.C_NEON_ROJO
            )

        elif not self.mundo.jaguar_vivo:

            estado_simulacion = (
                "JAGUAR CAZADO"
            )

            color_estado = (
                self.C_NEON_AMARILLO
            )

        elif self.en_curso:

            estado_simulacion = (
                "EN CURSO"
            )

            color_estado = (
                self.C_NEON_VERDE
            )

        else:

            estado_simulacion = (
                "PAUSADO"
            )

            color_estado = (
                (180, 180, 180)
            )


        dibujar_linea(
            (
                f"Estado: "
                f"{estado_simulacion}"
            ),
            x_dios + 15,
            154,
            ancho_dios - 30,
            color_estado
        )


        # =====================================
        # BOTONES
        # =====================================

        ancho_boton = (
            ancho_dios - 45
        ) // 2


        self.rect_btn_pausa = pygame.Rect(
            x_dios + 15,
            195,
            ancho_boton,
            28
        )


        self.rect_btn_reiniciar = pygame.Rect(
            x_dios
            +
            30
            +
            ancho_boton,
            195,
            ancho_boton,
            28
        )


        if self.en_curso:

            texto_pausa = "PAUSAR"

            color_pausa = (
                150,
                45,
                45
            )

            color_hover = (
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

            color_hover = (
                60,
                200,
                90
            )


        self.dibujar_boton(
            self.rect_btn_pausa,
            texto_pausa,
            color_pausa,
            color_hover
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
        # RATONES
        # Dibujar todos los ratones vivos
        # =====================================

        for raton in self.mundo.ratones:

            # Ignorar los ratones que ya fueron cazados
            if not raton.vivo:
                continue

            # Obtener la posición continua del ratón
            fila_raton, columna_raton = (
                raton.posicion_visual()
            )

            # Dibujar la imagen correspondiente a su dirección
            self.raton_sprite.dibujar(
                sup_entidades,
                fila_raton,
                columna_raton,
                0,
                raton.direccion
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

