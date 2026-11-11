from Recursos import raton
import pygame
import os
import math

import Mundo.mundo as modulo_mundo
print(
    "ARCHIVO MUNDO QUE PYTHON ESTÁ USANDO:"
)

print(
     modulo_mundo.__file__
)

from Agente_Cazador.sentidos import PLURAL_COLORES
from Logica_Difusa.dios import (
    obtener_dios,
    JAGUAR_EN_CUEVA,
    CAZADOR_DERROTADO,
    GANA_CAZADOR,
    GANA_INTERCEPTOR,
)
from Mundo import escenarios


from Recursos.arbol import Arbol
from Recursos.bayas import Baya
from Recursos.arena import ArenaMovediza
from Recursos.campamento import Campamento
from Recursos.cazador import Cazador
from Recursos.jaguar import Jaguar
from Recursos.raton import Raton

from Recursos.cueva import Cueva
from Recursos.interceptor import Interceptor, CampamentoInterceptor

class Interfaz:

    # =========================================
    # LO QUE SE DIBUJA VIENE DE DIOS
    # =========================================

    @property
    def mundo(self):
        return self.dios.mundo

    @property
    def agente(self):
        return self.dios.cazador

    @property
    def agente_jaguar(self):
        return self.dios.jaguar

    @property
    def cuerpo_cazador(self):
        return self.dios.cuerpo_cazador

    @property
    def cuerpo_jaguar(self):
        return self.dios.cuerpo_jaguar

    @property
    def escenario_actual(self):
        return self.dios.escenario

    @property
    def agente_interceptor(self):
        return self.dios.interceptor

    @property
    def cuerpo_interceptor(self):
        return self.dios.cuerpo_interceptor

    def __init__(self):

        pygame.init()
        # =========================================
        # DIOS (ORQUESTADOR)
        #
        # DIOS crea el mundo, los agentes y sus
        # cuerpos, controla los turnos y decide
        # cuándo termina la partida. La interfaz
        # solo dibuja y recibe las teclas.
        # =========================================

        self.dios = obtener_dios()

        self.dios.nueva_partida()


       # =========================================
        # PANEL SUPERIOR
        # =========================================

        self.alto_panel = 260

        # =========================================
        # PANEL LATERAL DE DIOS
        #
        # Solo para demostración visual del
        # funcionamiento del orquestador.
        # =========================================

        self.ancho_panel_dios_lateral = 340

        self.margen_mapa = 30

        self.separacion_panel_dios = 20

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
            self.ancho_panel_dios_lateral
            -
            self.separacion_panel_dios
            -
            (self.margen_mapa * 2)
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

        # =========================================
        # CENTRAR MAPA SOLO DENTRO DEL ÁREA
        # IZQUIERDA
        # =========================================

        ancho_area_mapa = (
            self.ancho
            -
            self.ancho_panel_dios_lateral
            -
            self.separacion_panel_dios
            -
            (self.margen_mapa * 2)
        )


        self.offset_mapa_x = (
            self.margen_mapa
            +
            max(
                0,
                (
                    ancho_area_mapa
                    -
                    self.mundo.ancho
                )
                // 2
            )
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
        # IMAGEN DEL DIOS ORQUESTADOR
        # =========================================

        ruta_dios = os.path.join(
            "Recursos",
            "images",
            "dios.png"
        )

        try:

            imagen_dios_raw = pygame.image.load(
                ruta_dios
            ).convert_alpha()

            self.imagen_dios = pygame.transform.smoothscale(
                imagen_dios_raw,
                (110, 110)
            )

            print("Imagen de DIOS cargada correctamente.")

        except Exception as error:

            print(f"Error al cargar imagen de DIOS: {error}")

            self.imagen_dios = None


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

        self.campamento_interceptor = CampamentoInterceptor(
            self.mundo.tamano_celda
        )

        self.cueva = Cueva(
                    self.mundo.tamano_celda
        )

        self.cazador = Cazador(
            self.mundo.tamano_celda
        )

        self.interceptor = Interceptor(
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

    def reiniciar_simulacion(self, escenario=None):

        # =========================================
        # DIOS CREA LA PARTIDA NUEVA
        #
        # Con escenario: siempre el mismo mapa
        # (teclas 1 y 2). Sin escenario: al azar.
        # =========================================

        self.dios.nueva_partida(escenario)


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

        ancho_area_mapa = (
            self.ancho
            -
            self.ancho_panel_dios_lateral
            -
            self.separacion_panel_dios
            -
            (self.margen_mapa * 2)
        )


        self.offset_mapa_x = (
            self.margen_mapa
            +
            max(
                0,
                (
                    ancho_area_mapa
                    -
                    self.mundo.ancho
                )
                // 2
            )
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

        self.campamento_interceptor = CampamentoInterceptor(
            self.mundo.tamano_celda
        )

        self.cueva = Cueva(
            self.mundo.tamano_celda
        )

        self.cazador = Cazador(
            self.mundo.tamano_celda
        )

        self.interceptor = Interceptor(
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
        # DIOS AVANZA LA SIMULACIÓN
        #
        # Turnos, encuentros y fin del juego los
        # controla DIOS. Si la partida terminó,
        # la interfaz se detiene.
        # =====================================

        if not self.dios.paso(dt):

            self.en_curso = False


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


                # B = imprimir la bitácora del cazador,
                # la del jaguar y la de DIOS
                elif evento.key == pygame.K_b:

                    self.agente.imprimir_conciencia()

                    self.agente_jaguar.imprimir_conciencia()

                    if self.agente_interceptor is not None:

                        self.agente_interceptor.imprimir_conciencia()

                    for nombre_red, agente_red in (
                        ("Rodrigo", self.agente),
                        ("Gonzalo", self.agente_interceptor),
                    ):

                        red = getattr(agente_red, "red_ataque", None)

                        if red is not None:

                            red.imprimir(nombre_red)

                    print("\n=== BITÁCORA DE DIOS ===")

                    for registro in self.dios.bitacora:

                        print(registro)


                # I = encender / apagar al interceptor
                # (cazador rival)
                # (empieza otra partida en el mismo
                # escenario)
                elif evento.key == pygame.K_i:

                    self.dios.con_interceptor = (
                        not self.dios.con_interceptor
                    )

                    self.reiniciar_simulacion(
                        self.escenario_actual
                    )


                # N = encender / apagar la red neuronal
                # de los cazadores (empieza otra
                # partida; lo aprendido se conserva)
                elif evento.key == pygame.K_n:

                    self.dios.con_red_neuronal = (
                        not self.dios.con_red_neuronal
                    )

                    self.reiniciar_simulacion(
                        self.escenario_actual
                    )


                # 1 y 2 = escenarios de demostración
                elif evento.key in (pygame.K_1, pygame.K_KP1):

                    self.reiniciar_simulacion(
                        escenarios.ESCENARIOS[1]
                    )


                elif evento.key in (pygame.K_2, pygame.K_KP2):

                    self.reiniciar_simulacion(
                        escenarios.ESCENARIOS[2]
                    )





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
        # MAPA
        # =====================================

        self.dibujar_tablero()


        # =====================================
        # HUD SUPERIOR ORIGINAL
        #
        # Rodrigo + sentidos + Jaguar +
        # Gonzalo + sentidos + DIOS.
        #
        # ESTO NO SE QUITA.
        # =====================================

        self.dibujar_panel()


        # =====================================
        # PANEL LATERAL EXTRA DE DIOS
        #
        # Solo para demostrar visualmente
        # el funcionamiento del orquestador.
        # =====================================

        self.dibujar_panel_dios_lateral()


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

    # =========================================
    # DIVIDIR TEXTO EN VARIAS LÍNEAS
    # PARA EL PANEL DE DIOS
    # =========================================

    def envolver_texto(
        self,
        texto,
        fuente,
        ancho_maximo
    ):

        palabras = str(texto).split()

        lineas = []

        linea_actual = ""


        for palabra in palabras:

            prueba = (
                f"{linea_actual} {palabra}"
                .strip()
            )


            if (
                fuente.size(prueba)[0]
                <=
                ancho_maximo
            ):

                linea_actual = prueba

            else:

                if linea_actual:

                    lineas.append(
                        linea_actual
                    )

                linea_actual = palabra


        if linea_actual:

            lineas.append(
                linea_actual
            )


        return lineas
    
    # =========================================
    # PANEL LATERAL DEL ORQUESTADOR DIOS
    # =========================================

    def dibujar_panel_dios_lateral(self):

        margen_derecho = 25

        x = (
            self.ancho
            -
            self.ancho_panel_dios_lateral
            -
            margen_derecho
        )

        y = (
            self.alto_panel
            +
            25
        )

        ancho = (
            self.ancho_panel_dios_lateral
        )

        alto = (
            self.alto
            -
            y
            -
            25
        )


        rect_panel = pygame.Rect(
            x,
            y,
            ancho,
            alto
        )


        # =====================================
        # CAJA PRINCIPAL
        # =====================================

        self.dibujar_caja_biselada_solida(
            rect_panel,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA,
            grosor_borde=3
        )


        # =====================================
        # TÍTULO
        # =====================================

        titulo = self.fuente_titulo.render(
            "ORQUESTADOR DIOS",
            True,
            self.C_ORO_PURO
        )


        self.pantalla.blit(
            titulo,
            (
                x + 18,
                y + 18
            )
        )


        subtitulo = (
            self.fuente_pequena.render(
                "Decisiones y eventos en tiempo real",
                True,
                (190, 170, 120)
            )
        )


        self.pantalla.blit(
            subtitulo,
            (
                x + 18,
                y + 50
            )
        )


        # Línea divisoria

        pygame.draw.line(
            self.pantalla,
            self.C_ORO_VIEJO,
            (
                x + 15,
                y + 78
            ),
            (
                x + ancho - 15,
                y + 78
            ),
            2
        )


        # =====================================
        # ESTADO ACTUAL
        # =====================================

        cursor_y = (
            y + 95
        )


        turno = (
            self.dios.turno_actual()
        )


        estado_partida = (
            "FINALIZADA"
            if self.dios.terminada
            else "EN CURSO"
        )


        jaguar_estado = (
            "VIVO"
            if self.mundo.jaguar_vivo
            else "CAPTURADO"
        )


        cazadores_vivos = 0


        for _, agente, _ in self.dios.cazadores():

            if (
                agente is not None
                and
                agente.vidas > 0
            ):

                cazadores_vivos += 1


        estado_red = (
            "ACTIVA"
            if self.dios.con_red_neuronal
            else "APAGADA"
        )


        datos_estado = [

            (
                "Turno",
                str(turno)
            ),

            (
                "Partida",
                estado_partida
            ),

            (
                "Jaguar",
                jaguar_estado
            ),

            (
                "Cazadores activos",
                str(cazadores_vivos)
            ),

            (
                "Red neuronal",
                estado_red
            ),
        ]


        for etiqueta, valor in datos_estado:

            texto_etiqueta = (
                self.fuente_UI.render(
                    f"{etiqueta}:",
                    True,
                    (190, 170, 120)
                )
            )


            self.pantalla.blit(
                texto_etiqueta,
                (
                    x + 18,
                    cursor_y
                )
            )


            texto_valor = (
                self.fuente_UI.render(
                    valor,
                    True,
                    (
                        self.C_NEON_VERDE
                        if valor
                        in (
                            "EN CURSO",
                            "VIVO",
                            "ACTIVA"
                        )
                        else
                        (235, 235, 235)
                    )
                )
            )


            self.pantalla.blit(
                texto_valor,
                (
                    x + 155,
                    cursor_y
                )
            )


            cursor_y += 25


        # =====================================
        # ÚLTIMA DECISIÓN DE DIOS
        # =====================================

        cursor_y += 8


        pygame.draw.line(
            self.pantalla,
            self.C_ORO_VIEJO,
            (
                x + 15,
                cursor_y
            ),
            (
                x + ancho - 15,
                cursor_y
            ),
            1
        )


        cursor_y += 15


        titulo_ultima = (
            self.fuente_UI.render(
                "ÚLTIMA DECISIÓN",
                True,
                self.C_NEON_AMARILLO
            )
        )


        self.pantalla.blit(
            titulo_ultima,
            (
                x + 18,
                cursor_y
            )
        )


        cursor_y += 27


        bitacora = list(
            self.dios.bitacora
        )


        if bitacora:

            ultima = bitacora[-1]

            ultima = ultima.replace(
                "[DIOS] ",
                "",
                1
            )


            lineas = self.envolver_texto(
                ultima,
                self.fuente_UI,
                ancho - 36
            )


            for linea in lineas:

                render = (
                    self.fuente_UI.render(
                        linea,
                        True,
                        self.C_NEON_VERDE
                    )
                )


                self.pantalla.blit(
                    render,
                    (
                        x + 18,
                        cursor_y
                    )
                )


                cursor_y += 20

        else:

            render = (
                self.fuente_UI.render(
                    "Sin decisiones todavía",
                    True,
                    (160, 160, 160)
                )
            )


            self.pantalla.blit(
                render,
                (
                    x + 18,
                    cursor_y
                )
            )


            cursor_y += 20


        # =====================================
        # HISTORIAL DE DECISIONES
        # =====================================

        cursor_y += 12


        pygame.draw.line(
            self.pantalla,
            self.C_ORO_VIEJO,
            (
                x + 15,
                cursor_y
            ),
            (
                x + ancho - 15,
                cursor_y
            ),
            1
        )


        cursor_y += 15


        titulo_historial = (
            self.fuente_UI.render(
                "DECISIONES RECIENTES",
                True,
                self.C_ORO_PURO
            )
        )


        self.pantalla.blit(
            titulo_historial,
            (
                x + 18,
                cursor_y
            )
        )


        cursor_y += 30


        # Últimos 8 eventos

        eventos = (
            bitacora[-8:]
            if bitacora
            else []
        )


        for evento in eventos:

            evento = evento.replace(
                "[DIOS] ",
                "",
                1
            )


            lineas = self.envolver_texto(
                "• " + evento,
                self.fuente_pequena,
                ancho - 38
            )


            for linea in lineas:

                # Evitar salir del panel

                if (
                    cursor_y
                    >
                    rect_panel.bottom - 25
                ):

                    return


                render = (
                    self.fuente_pequena.render(
                        linea,
                        True,
                        (220, 220, 220)
                    )
                )


                self.pantalla.blit(
                    render,
                    (
                        x + 18,
                        cursor_y
                    )
                )


                cursor_y += 18


            cursor_y += 7
    
    # =========================================
    # TEXTO DE LA REGLA MÁS FUERTE Y DEL
    # CENTROIDE (para el panel)
    # =========================================

    # =========================================
    # LÍNEA DE LA RED NEURONAL DE UN CAZADOR
    # =========================================

    def texto_red(self, agente):

        red = getattr(agente, "red_ataque", None)

        if red is None:

            return "Red neuronal: apagada (N)", (160, 160, 160)

        if red.ultima_prediccion == 1:

            return red.texto_panel(), self.C_NEON_ROJO

        return red.texto_panel(), (200, 170, 255)


    def texto_regla_y_centroide(self, agente):

        decision = getattr(agente, "decision_difusa", None)

        if not decision:

            return ""

        regla = agente.controlador.regla_dominante()

        x = decision.get("x")

        partes = []

        if regla is not None:

            partes.append(f"{regla[0]} {regla[2]:.2f}")

        if x is not None:

            partes.append(f"x*={x:.0f}")

        return f"  ({', '.join(partes)})" if partes else ""



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


        def dibujar_nombre_cazador(
            nombre,
            subtitulo,
            x,
            color_nombre,
            color_subtitulo,
            ancho_caja,
            subtitulo_corto
        ):

            # Título grande y, a su derecha en la
            # misma línea, el subtítulo pequeño
            # (así no se encima con la energía)

            y_titulo = 24

            render = self.fuente_titulo.render(
                nombre,
                True,
                color_nombre
            )

            self.pantalla.blit(
                render,
                (x, y_titulo)
            )

            x_sub = x + render.get_width() + 10

            # Si no cabe en la caja, la versión
            # corta ("C1")
            if (
                x_sub
                + self.fuente_pequena.size(subtitulo)[0]
                > x - 12 + ancho_caja - 10
            ):

                subtitulo = subtitulo_corto

            sub = self.fuente_pequena.render(
                subtitulo,
                True,
                color_subtitulo
            )

            self.pantalla.blit(
                sub,
                (
                    x_sub,
                    y_titulo
                    + render.get_height()
                    - sub.get_height()
                    - 4
                )
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

        def dibujar_sentidos_agente(
            agente,
            x,
            ancho,
            titulo
        ):

            rect = pygame.Rect(
                x,
                y_panel,
                ancho,
                alto_caja
            )

            self.dibujar_caja_biselada_solida(
                rect,
                self.C_MADERA_BASE,
                self.C_MADERA_LUZ,
                self.C_MADERA_SOMBRA
            )


            titulo_render = (
                self.fuente_subtitulo.render(
                    titulo,
                    True,
                    self.C_ORO_PURO
                )
            )

            self.pantalla.blit(
                titulo_render,
                (
                    x + 6,
                    30
                )
            )


            sentidos = agente.sentidos


            # ==============================
            # VISTA
            # ==============================

            vista = (
                "Jaguar"
                if sentidos.ve_jaguar
                else "Nada"
            )


            # ==============================
            # OÍDO
            # ==============================

            oido = (
                str(sentidos.direccion_sonido)
                if sentidos.escucha_jaguar
                else "Silencio"
            )


            # ==============================
            # OLFATO
            # ==============================

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


            # ==============================
            # TACTO
            # ==============================

            tacto = str(
                sentidos.sensacion_tacto
            )


            # ==============================
            # GUSTO
            # ==============================

            gusto = str(
                sentidos.sensacion_gusto
            )


            ancho_slot = ancho - 10


            self.dibujar_slot_sentido_animado(
                x + 5,
                55,
                ancho_slot,
                "Vista",
                vista,
                sentidos.ve_jaguar,
                self.C_NEON_ROJO
            )


            self.dibujar_slot_sentido_animado(
                x + 5,
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
                x + 5,
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
                x + 5,
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
                x + 5,
                199,
                ancho_slot,
                "Gusto",
                gusto,
                gusto_activo,
                self.C_NEON_VERDE
            )

        # =====================================
        # DISTRIBUCIÓN DE LOS 6 PANELES
        #
        # Rodrigo | Sentidos R | Jaguar |
        # Gonzalo | Sentidos G | DIOS
        # =====================================

        margen = 10
        separacion = 6

        disponible = (
            self.ancho
            -
            margen * 2
            -
            separacion * 5
        )

        # Rodrigo
        ancho_rodrigo = int(disponible * 0.22)

        # Sentidos de Rodrigo
        ancho_sentidos_rodrigo = int(disponible * 0.11)

        # Jaguar
        ancho_jaguar = int(disponible * 0.18)

        # Gonzalo
        ancho_gonzalo = int(disponible * 0.22)

        # Sentidos de Gonzalo
        ancho_sentidos_gonzalo = int(disponible * 0.11)

        # DIOS usa lo restante
        ancho_dios = (
            disponible
            -
            ancho_rodrigo
            -
            ancho_sentidos_rodrigo
            -
            ancho_jaguar
            -
            ancho_gonzalo
            -
            ancho_sentidos_gonzalo
        )


        x_rodrigo = margen

        x_sentidos_rodrigo = (
            x_rodrigo
            +
            ancho_rodrigo
            +
            separacion
        )

        x_jaguar = (
            x_sentidos_rodrigo
            +
            ancho_sentidos_rodrigo
            +
            separacion
        )

        x_gonzalo = (
            x_jaguar
            +
            ancho_jaguar
            +
            separacion
        )

        x_sentidos_gonzalo = (
            x_gonzalo
            +
            ancho_gonzalo
            +
            separacion
        )

        x_dios = (
            x_sentidos_gonzalo
            +
            ancho_sentidos_gonzalo
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
            x_rodrigo,
            y_panel,
            ancho_rodrigo,
            alto_caja
        )

        self.dibujar_caja_biselada_solida(
            rect_cazador,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )

        # Nombre y, en la misma línea, a qué
        # cazador corresponde
        dibujar_nombre_cazador(
            "RODRIGO",
            "CAZADOR 1",
            x_rodrigo + 12,
            self.C_ORO_PURO,
            (190, 170, 120),
            ancho_rodrigo,
            "C1"
        )


        # Energía

        energia = self.agente.energia

        color_energia = (
            self.C_NEON_VERDE
            if energia > 30
            else self.C_NEON_ROJO
        )

        dibujar_barra(
            x_rodrigo + 15,
            58,
            ancho_rodrigo - 30,
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
            x_rodrigo + 15,
            103,
            ancho_rodrigo - 30
        )


        # Red neuronal: ¿el jaguar va a atacar?
        texto_red, color_red = self.texto_red(self.agente)

        dibujar_linea(
            texto_red,
            x_rodrigo + 15,
            125,
            ancho_rodrigo - 30,
            color_red
        )


        vidas_max = getattr(
            self.agente,
            "vidas_max",
            self.agente.vidas
        )

        dibujar_linea(
            (
                f"Vidas: {self.agente.vidas}/{vidas_max} "
                f"| Puntos: {self.agente.puntos} "
                f"| Mem: {len(memoria.celdas_revisadas)}"
            ),
            x_rodrigo + 15,
            147,
            ancho_rodrigo - 30,
            self.C_ORO_VIEJO
        )


        dibujar_linea(
            f"Estado: {self.agente.estado}",
            x_rodrigo + 15,
            169,
            ancho_rodrigo - 30,
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
            (
                f"Difuso: {accion_difusa.upper()}"
                f"{self.texto_regla_y_centroide(self.agente)}"
            ),
            x_rodrigo + 15,
            191,
            ancho_rodrigo - 30,
            self.C_NEON_VERDE
        )


        dibujar_linea(
            (
                f"Movimiento: "
                f"{self.agente.ultima_accion}  "
                f"| Motor: {self.agente.fuente_decision}"
            ),
            x_rodrigo + 15,
            211,
            ancho_rodrigo - 30,
            self.C_NEON_AZUL
        )

        # =====================================
        # SENTIDOS DE RODRIGO
        # Solo se muestran si sigue vivo
        # =====================================

        if self.agente.vidas > 0:

            dibujar_sentidos_agente(
                self.agente,
                x_sentidos_rodrigo,
                ancho_sentidos_rodrigo,
                "SENTIDOS R."
            )

        else:

            rect_sentidos_rodrigo = pygame.Rect(
                x_sentidos_rodrigo,
                y_panel,
                ancho_sentidos_rodrigo,
                alto_caja
            )

            self.dibujar_caja_biselada_solida(
                rect_sentidos_rodrigo,
                self.C_MADERA_BASE,
                self.C_MADERA_LUZ,
                self.C_MADERA_SOMBRA
            )

            dibujar_linea(
                "SENTIDOS R.",
                x_sentidos_rodrigo + 6,
                30,
                ancho_sentidos_rodrigo - 12,
                self.C_ORO_PURO
            )

            dibujar_linea(
                "DERROTADO",
                x_sentidos_rodrigo + 6,
                100,
                ancho_sentidos_rodrigo - 12,
                self.C_NEON_ROJO
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
            "JAGUAR",
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
            (
                f"Difuso: {accion_jaguar.upper()}"
                f"{self.texto_regla_y_centroide(self.agente_jaguar)}"
            ),
            x_jaguar + 15,
            127,
            ancho_jaguar - 30,
            self.C_NEON_AMARILLO
        )


        dibujar_linea(
            (
                f"Hambre {entradas_jaguar.get('hambre', '-')} | "
                f"Dist {entradas_jaguar.get('distancia_cazador', '-')} | "
                f"Energía caz. {entradas_jaguar.get('energia_cazador', '-')}"
            ),
            x_jaguar + 15,
            149,
            ancho_jaguar - 30
        )


        dibujar_linea(
            (
                f"Movimiento: "
                f"{self.agente_jaguar.ultima_accion}  "
                f"| Motor: {self.agente_jaguar.fuente_movimiento}"
            ),
            x_jaguar + 15,
            171,
            ancho_jaguar - 30,
            self.C_NEON_AZUL
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
        # 4. GONZALO - CAZADOR 2
        # =====================================

        gonzalo = self.agente_interceptor

        rect_gonzalo = pygame.Rect(
            x_gonzalo,
            y_panel,
            ancho_gonzalo,
            alto_caja
        )

        self.dibujar_caja_biselada_solida(
            rect_gonzalo,
            self.C_MADERA_BASE,
            self.C_MADERA_LUZ,
            self.C_MADERA_SOMBRA
        )

        dibujar_nombre_cazador(
            "GONZALO",
            "CAZADOR 2",
            x_gonzalo + 12,
            self.C_NEON_AZUL,
            (120, 170, 255),
            ancho_gonzalo,
            "C2"
        )


        if gonzalo is None:

            dibujar_linea(
                "DESACTIVADO",
                x_gonzalo + 12,
                90,
                ancho_gonzalo - 24,
                (160, 160, 160)
            )

            dibujar_linea(
                "Tecla I para activar",
                x_gonzalo + 12,
                115,
                ancho_gonzalo - 24,
                self.C_NEON_AZUL
            )

        else:

            energia_gonzalo = gonzalo.energia

            color_energia_gonzalo = (
                self.C_NEON_VERDE
                if energia_gonzalo > 30
                else self.C_NEON_ROJO
            )

            dibujar_barra(
                x_gonzalo + 15,
                58,
                ancho_gonzalo - 30,
                energia_gonzalo,
                getattr(
                    gonzalo,
                    "energia_max",
                    100
                ),
                color_energia_gonzalo,
                "Energía"
            )

            memoria_gonzalo = gonzalo.memoria
            conocimiento_gonzalo = memoria_gonzalo.conocimiento_bayas

            roja_gonzalo = (
                conocimiento_gonzalo["roja"]
                if conocimiento_gonzalo["roja"] is not None
                else "?"
            )

            azul_gonzalo = (
                conocimiento_gonzalo["azul"]
                if conocimiento_gonzalo["azul"] is not None
                else "?"
            )

            dibujar_linea(
                f"Baya roja: {roja_gonzalo} | Baya azul: {azul_gonzalo}",
                x_gonzalo + 15,
                103,
                ancho_gonzalo - 30
            )

            # Red neuronal: ¿el jaguar va a atacar?
            texto_red_g, color_red_g = self.texto_red(gonzalo)

            dibujar_linea(
                texto_red_g,
                x_gonzalo + 15,
                125,
                ancho_gonzalo - 30,
                color_red_g
            )

            vidas_max_gonzalo = getattr(
                gonzalo,
                "vidas_max",
                gonzalo.vidas
            )

            dibujar_linea(
                (
                    f"Vidas: {gonzalo.vidas}/{vidas_max_gonzalo} "
                    f"| Puntos: {gonzalo.puntos} "
                    f"| Mem: {len(memoria_gonzalo.celdas_revisadas)}"
                ),
                x_gonzalo + 15,
                147,
                ancho_gonzalo - 30,
                self.C_ORO_VIEJO
            )

            dibujar_linea(
                f"Estado: {gonzalo.estado}",
                x_gonzalo + 15,
                169,
                ancho_gonzalo - 30,
                (120, 190, 255)
            )

            if gonzalo.decision_difusa:
                accion_gonzalo = gonzalo.decision_difusa["accion"]
            else:
                accion_gonzalo = "-"

            dibujar_linea(
                (
                    f"Difuso: {accion_gonzalo.upper()}"
                    f"{self.texto_regla_y_centroide(gonzalo)}"
                ),
                x_gonzalo + 15,
                191,
                ancho_gonzalo - 30,
                self.C_NEON_VERDE
            )

            dibujar_linea(
                (
                    f"Movimiento: {gonzalo.ultima_accion} "
                    f"| Motor: {gonzalo.fuente_decision}"
                ),
                x_gonzalo + 15,
                211,
                ancho_gonzalo - 30,
                self.C_NEON_AZUL
            )


        # =====================================
        # 5. SENTIDOS DE GONZALO
        # Solo se muestran si sigue vivo
        # =====================================

        if (
            gonzalo is not None
            and gonzalo.vidas > 0
        ):

            dibujar_sentidos_agente(
                gonzalo,
                x_sentidos_gonzalo,
                ancho_sentidos_gonzalo,
                "SENTIDOS G."
            )

        else:

            rect_sentidos_gonzalo = pygame.Rect(
                x_sentidos_gonzalo,
                y_panel,
                ancho_sentidos_gonzalo,
                alto_caja
            )

            self.dibujar_caja_biselada_solida(
                rect_sentidos_gonzalo,
                self.C_MADERA_BASE,
                self.C_MADERA_LUZ,
                self.C_MADERA_SOMBRA
            )

            dibujar_linea(
                "SENTIDOS G.",
                x_sentidos_gonzalo + 6,
                30,
                ancho_sentidos_gonzalo - 12,
                self.C_ORO_PURO
            )

            if gonzalo is None:

                texto_estado_gonzalo = "INACTIVO"

            else:

                texto_estado_gonzalo = "DERROTADO"

            dibujar_linea(
                texto_estado_gonzalo,
                x_sentidos_gonzalo + 6,
                100,
                ancho_sentidos_gonzalo - 12,
                (
                    (150, 150, 150)
                    if gonzalo is None
                    else self.C_NEON_ROJO
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
            "ORQUESTADOR",
            x_dios + 15,
            25,
            (255, 255, 255)
        )




        # =====================================
        # REPRESENTACIÓN VISUAL DE DIOS
        # =====================================
        

        if self.imagen_dios is not None:

            # Centrar imagen dentro del panel
            imagen_x = (
                x_dios
                +
                (ancho_dios - self.imagen_dios.get_width()) // 2
            )

            # Dibujar imagen del Dios orquestador
            self.pantalla.blit(
                self.imagen_dios,
                (
                    imagen_x,
                    45
                )
            )

        else:
            #mostrar simbolo si no se pudo carga imagen
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
                    simbolo_dios.get_width())// 2
            )

            self.pantalla.blit(
                simbolo_dios,
                (
                    simbolo_x,70)
            )

           
        # =====================================
        # ESTADO DE LA SIMULACIÓN
        # =====================================

        escenario_texto = (
            self.escenario_actual.nombre
            if self.escenario_actual is not None
            else "Mapa al azar"
        )

        dibujar_linea(
            f"Turno: {self.agente.turno} | {escenario_texto}",
            x_dios + 15,
            132,
            ancho_dios - 30,
            self.C_ORO_PURO
        )


        # El resultado lo decide DIOS

        if self.dios.terminada:

            estado_simulacion = (
                self.dios.resultado
            )

            color_estado = self.C_NEON_ROJO

        # Con rival: quién atrapó primero al
        # jaguar (la partida sigue mientras
        # regresan a la cabaña)

        elif (
            self.agente_interceptor is not None
            and self.dios.ganador is not None
        ):

            if self.dios.ganador == "interceptor":

                estado_simulacion = GANA_INTERCEPTOR
                color_estado = (120, 170, 255)

            else:

                estado_simulacion = GANA_CAZADOR
                color_estado = self.C_NEON_AMARILLO

        elif self.agente_jaguar.regresando_cueva:

            estado_simulacion = (
                "JAGUAR A CUEVA"
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


        # Los resultados largos se muestran sin
        # "Estado:" para que quepan

        dibujar_linea(
            (
                estado_simulacion
                if len(estado_simulacion) > 10
                else f"Estado: {estado_simulacion}"
            ),
            x_dios + 15,
            154,
            ancho_dios - 30,
            color_estado
        )


        # Agente 3: interceptor, cazador rival
        # (tecla I)

        interceptor = self.agente_interceptor

        if interceptor is None:

            texto_interceptor = "Interceptor: apagado"

        elif interceptor.vidas <= 0:

            texto_interceptor = "Interceptor: derrotado"

        elif interceptor.decision_difusa is None:

            texto_interceptor = "Interceptor: esperando"

        else:

            texto_interceptor = (
                "Int.: "
                f"{interceptor.decision_difusa['accion'].upper()}"
            )

        dibujar_linea(
            texto_interceptor,
            x_dios + 15,
            174,
            ancho_dios - 30,
            (120, 170, 255)
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

    # =========================================
    # AVISO DE PELEA: estallido y "¡PELEA!"
    # donde se cruzaron los cazadores
    # =========================================

    

    def dibujar_pelea(self):

        pelea = self.dios.ultima_pelea

        if pelea is None:

            return

        tamano = self.mundo.tamano_celda

        fila, columna = pelea["lugar"]

        x = int(self.offset_mapa_x + columna * tamano + tamano / 2)
        y = int(self.offset_mapa_y + fila * tamano + tamano / 2)

        # Crece y se desvanece con el tiempo
        avance = 1 - max(0.0, pelea["tiempo"]) / 1.5

        radio = int(tamano * (0.6 + 0.6 * avance))

        estallido = pygame.Surface(
            (radio * 2 + 4, radio * 2 + 4),
            pygame.SRCALPHA
        )

        alfa = int(220 * (1 - avance)) + 35

        pygame.draw.circle(
            estallido,
            (255, 90, 40, alfa // 2),
            (radio + 2, radio + 2),
            radio
        )

        pygame.draw.circle(
            estallido,
            (255, 220, 60, alfa),
            (radio + 2, radio + 2),
            radio,
            4
        )

        self.pantalla.blit(
            estallido,
            (x - radio - 2, y - radio - 2)
        )

        texto = self.fuente_UI.render(
            pelea["texto"],
            True,
            (255, 255, 255)
        )

        fondo = pygame.Rect(
            0, 0,
            texto.get_width() + 12,
            texto.get_height() + 6
        )

        fondo.center = (x, y - tamano)

        pygame.draw.rect(
            self.pantalla,
            (170, 30, 30),
            fondo,
            border_radius=6
        )

        self.pantalla.blit(
            texto,
            (fondo.x + 6, fondo.y + 3)
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

        # Cabaña del interceptor (azul)

        cabana = getattr(
            self.mundo,
            "campamento_interceptor",
            None
        )

        if cabana is not None:

            self.campamento_interceptor.dibujar(
                sup_entidades,
                cabana[0],
                cabana[1],
                0
            )

        # =====================================
        # CUEVA DEL JAGUAR
        # =====================================

        fila, columna = self.mundo.cueva

        self.cueva.dibujar(
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
        # INTERCEPTOR (cazador rival, azul)
        # =====================================

        if (
            self.agente_interceptor is not None
            and self.agente_interceptor.vidas > 0
        ):

            fila_i, columna_i = (
                self.cuerpo_interceptor.posicion_visual()
            )

            self.interceptor.dibujar(

                sup_entidades,

                fila_i,
                columna_i,
                0

            )


        # =====================================
        # CAZADOR
        # =====================================

        # Con rival, si el cazador muere ya no se
        # dibuja (salió del juego)

        if (
            self.agente.vidas > 0
            or self.agente_interceptor is None
        ):

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
        # PELEA ENTRE CAZADORES (la decide DIOS)
        # =====================================

        self.dibujar_pelea()


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

