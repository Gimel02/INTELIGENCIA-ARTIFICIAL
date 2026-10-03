import pygame

import os

import math



# =========================================
# FORZAR PANTALLA COMPLETA SIN BORDES 
# =========================================

# Esto asegura que la ventana se ancle en el 
# pixel 0,0 de tu monitor.

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"



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


        # =========================================
        # INICIALIZACIÓN DE PYGAME
        # =========================================

        pygame.init()
        
        
        pygame.font.init()



        # =========================================
        # DETECCIÓN DE RESOLUCIÓN NATIVA
        # =========================================
        
        info_pantalla = pygame.display.Info()
        
        
        self.ancho = (
            info_pantalla.current_w
        )
        
        
        self.alto = (
            info_pantalla.current_h
        )



        # =========================================
        # CREACIÓN DE LA VENTANA BORDERLESS
        # =========================================

        self.pantalla = pygame.display.set_mode(
            
            (
                self.ancho, 
                self.alto
            ), 
            
            pygame.NOFRAME
            
        )


        pygame.display.set_caption(
            "Expedición Selva - Animada y Amigable"
        )



        # =========================================
        # DIMENSIONES DEL PANEL SUPERIOR
        # =========================================
        
        self.alto_panel = 190



        # =========================================
        # MUNDO Y CÁLCULO MATEMÁTICO DE CELDAS
        # =========================================

        self.mundo = MundoSelva()

        
        # Espacio exacto para el mapa con márgenes
        
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
        
        
        # Celda cuadrada perfecta
        
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
        # CENTRADO ABSOLUTO DEL TABLERO
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
        # INICIALIZACIÓN DEL AGENTE
        # =========================================

        self.agente = AgenteCazador(
            
            self.mundo
            
        )



        # =========================================
        # INICIALIZACIÓN DE RECURSOS ESCALADOS
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
        # CARGA DE FONDOS CON ANTI-CRASH
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
            
            
        except Exception as e:
            
            print(
                "No se encontró el fondo. Usando color base."
            )
            
            self.usa_fondo_img = False



        # =========================================
        # PALETA DE COLORES LUXURY / EXPEDITION
        # =========================================

        # Maderas Finas
        
        self.C_MADERA_FONDO = (
            28, 19, 14
        )
        
        self.C_MADERA_BASE = (
            42, 28, 22
        )
        
        self.C_MADERA_LUZ = (
            65, 45, 33
        )
        
        self.C_MADERA_SOMBRA = (
            15, 10, 8
        )
        
        
        # Metales y Ornamentos
        
        self.C_ORO_PURO = (
            255, 215, 0
        )
        
        self.C_ORO_VIEJO = (
            184, 134, 11
        )
        
        self.C_BRONCE = (
            140, 95, 30
        )
        
        
        # Luces Neón para Indicadores
        
        self.C_NEON_ROJO = (
            255, 60, 60
        )
        
        self.C_NEON_VERDE = (
            50, 255, 100
        )
        
        self.C_NEON_AZUL = (
            60, 180, 255
        )
        
        self.C_NEON_AMARILLO = (
            255, 220, 50
        )
        
        self.C_NEON_MORADO = (
            200, 80, 255
        )



        # =========================================
        # MOTOR TIPOGRÁFICO CON SOPORTE EMOJI
        # =========================================

        self.fuente_titulo = pygame.font.SysFont(
            
            "trebuchetms,georgia", 
            28, 
            bold=True
            
        )


        self.fuente_subtitulo = pygame.font.SysFont(
            
            "trebuchetms,georgia", 
            13, 
            bold=True
            
        )


        self.fuente_UI = pygame.font.SysFont(
            
            "segoe ui emoji, apple color emoji, trebuchetms, arial", 
            14, 
            bold=True
            
        )
        
        
        self.fuente_numeros = pygame.font.SysFont(
            
            "impact,arialblack", 
            18
            
        )
        
        
        self.fuente_pequena = pygame.font.SysFont(
            
            "trebuchetms,arial", 
            11, 
            bold=True
            
        )



        # =========================================
        # CONTROL DE SIMULACIÓN Y ANIMACIONES
        # =========================================

        self.ejecutando = True


        self.en_curso = True


        self.intervalo_agente = 500


        self.ultimo_movimiento = (
            pygame.time.get_ticks()
        )


        self.reloj = pygame.time.Clock()
        
        
        # Posición del ratón para botones interactivos
        
        self.mouse_x = 0
        
        self.mouse_y = 0



    # =========================================
    # FUNCIÓN DE REINICIO TOTAL
    # =========================================
    
    def reiniciar_simulacion(self):
        
        print(
            "Iniciando secuencia de reinicio del mundo..."
        )
        
        
        self.mundo = MundoSelva()
        
        
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
            
            
        self.agente = AgenteCazador(
            
            self.mundo
            
        )
        
        
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
        
        
        self.ultimo_movimiento = (
            pygame.time.get_ticks()
        )
        
        
        self.en_curso = False



    # =========================================
    # BUCLE DE JUEGO (GAME LOOP)
    # =========================================

    def ejecutar(self):

        while self.ejecutando:

            self.manejar_eventos()


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


            self.dibujar()


            pygame.display.flip()


            self.reloj.tick(60)


        pygame.quit()



    # =========================================
    # GESTOR DE EVENTOS (INPUTS)
    # =========================================

    def manejar_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                self.ejecutando = False


            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:

                    self.en_curso = (
                        not self.en_curso
                    )


                elif evento.key == pygame.K_ESCAPE:

                    self.ejecutando = False
                    
                    
                elif evento.key == pygame.K_r:
                    
                    self.reiniciar_simulacion()


            elif evento.type == pygame.MOUSEMOTION:
                
                # Guardamos la posición del mouse para animaciones
                
                self.mouse_x, self.mouse_y = evento.pos


            elif evento.type == pygame.MOUSEBUTTONDOWN:
                
                if evento.button == 1:
                    
                    # Calcular posición de botones interactivos
                    
                    ancho_bloque_der = 400
                    
                    
                    margen_x_derecho = (
                        
                        self.ancho 
                        - 
                        ancho_bloque_der 
                        - 
                        20
                        
                    )
                    
                    
                    ancho_btn = (
                        
                        (ancho_bloque_der - 60) 
                        // 
                        2
                        
                    )
                    
                    
                    rect_btn_pausa = pygame.Rect(
                        
                        margen_x_derecho + 20, 
                        85, 
                        ancho_btn, 
                        50
                        
                    )
                    
                    
                    if rect_btn_pausa.collidepoint(evento.pos):
                        
                        self.en_curso = (
                            not self.en_curso
                        )
                        
                        
                    rect_btn_reinicio = pygame.Rect(
                        
                        margen_x_derecho + 40 + ancho_btn, 
                        85, 
                        ancho_btn, 
                        50
                        
                    )
                    
                    
                    if rect_btn_reinicio.collidepoint(evento.pos):
                        
                        self.reiniciar_simulacion()



    # =========================================
    # MOTOR DE DIBUJO (RENDERIZADO PRINCIPAL)
    # =========================================

    def dibujar(self):

        # Capa 1: Limpieza
        
        self.pantalla.fill(
            
            self.C_MADERA_SOMBRA
            
        )


        # Capa 2: Tablero, Mapa y Marco Hueco
        
        self.dibujar_tablero()


        # Capa 3: Interfaz Superior Amigable
        
        self.dibujar_panel()



    # =========================================
    # ELEMENTOS GRÁFICOS COMPLEJOS Y ANIMADOS
    # =========================================

    def dibujar_caja_biselada_solida(
        
        self, 
        rect, 
        color_base,
        color_luz,
        color_sombra,
        grosor_borde=2
        
    ):
        
        """ 
        Dibuja una caja sólida para los menús superiores.
        No usar esta función para tapar el mapa.
        """

        for i in range(1, 6):
            
            pygame.draw.rect(
                
                self.pantalla, 
                
                (0, 0, 0, 80 - (i*15)), 
                
                rect.inflate(i, i).move(0, i), 
                
                border_radius=10
                
            )
            
        
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
        
        
        lista_esquinas = [
            
            (rect.left + 8, rect.top + 8), 
            
            (rect.right - 8, rect.top + 8),
            
            (rect.left + 8, rect.bottom - 8), 
            
            (rect.right - 8, rect.bottom - 8)
            
        ]
        
        
        for px, py in lista_esquinas:
            
            pygame.draw.circle(
                
                self.pantalla, 
                
                self.C_MADERA_SOMBRA, 
                
                (px, py), 
                
                5
                
            )
            
            pygame.draw.circle(
                
                self.pantalla, 
                
                self.C_BRONCE, 
                
                (px, py), 
                
                4
                
            )
            
            pygame.draw.circle(
                
                self.pantalla, 
                
                self.C_ORO_PURO, 
                
                (px - 1, py - 1), 
                
                1
                
            )



    def dibujar_marco_hueco_mapa(
        
        self, 
        rect, 
        color_base,
        color_luz,
        color_sombra,
        grosor_madera=6
        
    ):
        
        """ 
        DIBUJA UN MARCO COMPLETAMENTE HUECO EN EL CENTRO
        Soluciona el bug de la caja que tapaba todo el mapa.
        """

        # Sombra exterior
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            (10, 5, 5), 
            
            rect.inflate(8, 8).move(2, 4), 
            
            grosor_madera + 4, 
            
            border_radius=12
            
        )
        
        
        # Base de madera (solo los bordes)
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            color_base, 
            
            rect.inflate(4, 4), 
            
            grosor_madera, 
            
            border_radius=8
            
        )
        
        
        # Ribete interno de Oro
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            self.C_ORO_PURO, 
            
            rect.inflate(-2, -2), 
            
            2, 
            
            border_radius=4
            
        )



    def dibujar_barra_animada(
        
        self, 
        x, 
        y, 
        ancho, 
        alto, 
        ratio, 
        color_fluido, 
        texto_interior
        
    ):
        
        radio_medallon = (
            (alto // 2) + 8
        )
        
        
        cx = (
            x + radio_medallon
        )
        
        
        cy = (
            y + alto // 2
        )
        
        
        ancho_tubo = (
            ancho - radio_medallon
        )
        
        
        rect_tubo = pygame.Rect(
            
            cx, 
            y, 
            ancho_tubo, 
            alto
            
        )
        
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            (15, 10, 10), 
            
            rect_tubo, 
            
            border_radius = alto // 2
            
        )
        
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            self.C_ORO_VIEJO, 
            
            rect_tubo, 
            
            2, 
            
            border_radius = alto // 2
            
        )


        progreso = max(
            0, min(1, ratio)
        )
        
        
        ancho_relleno = int(
            progreso * (ancho_tubo - 6)
        )
        
        
        if ancho_relleno > 10:
            
            rect_relleno = pygame.Rect(
                
                cx + 3, 
                y + 3, 
                ancho_relleno, 
                alto - 6
                
            )
            
            pygame.draw.rect(
                
                self.pantalla, 
                
                color_fluido, 
                
                rect_relleno, 
                
                border_radius = (alto - 6) // 2
                
            )
            
            
            # Animación de brillo fluyendo
            
            tiempo = pygame.time.get_ticks()
            
            
            brillo_alpha = int(
                
                90 
                + 
                40 
                * 
                math.sin(tiempo / 200.0)
                
            )
            
            
            rect_brillo = pygame.Rect(
                
                cx + 5, 
                y + 4, 
                ancho_relleno - 4, 
                (alto - 6) // 2
                
            )
            
            
            superficie_brillo = pygame.Surface(
                
                (rect_brillo.width, rect_brillo.height), 
                
                pygame.SRCALPHA
                
            )
            
            
            superficie_brillo.fill(
                
                (255, 255, 255, brillo_alpha)
                
            )
            
            
            self.pantalla.blit(
                
                superficie_brillo, 
                
                rect_brillo
                
            )


        pygame.draw.circle(
            
            self.pantalla, 
            
            self.C_MADERA_SOMBRA, 
            
            (cx, cy + 3), 
            
            radio_medallon
            
        )
        
        
        pygame.draw.circle(
            
            self.pantalla, 
            
            self.C_ORO_PURO, 
            
            (cx, cy), 
            
            radio_medallon
            
        )
        
        
        pygame.draw.circle(
            
            self.pantalla, 
            
            self.C_ORO_VIEJO, 
            
            (cx, cy), 
            
            radio_medallon - 2
            
        )
        
        
        pygame.draw.circle(
            
            self.pantalla, 
            
            self.C_MADERA_FONDO, 
            
            (cx, cy), 
            
            radio_medallon - 5
            
        )
        
        
        pygame.draw.circle(
            
            self.pantalla, 
            
            color_fluido, 
            
            (cx, cy), 
            
            radio_medallon - 8
            
        )
        
        
        pygame.draw.circle(
            
            self.pantalla, 
            
            (255, 255, 255), 
            
            (cx - 2, cy - 2), 
            
            2
            
        )


        texto_rend = self.fuente_numeros.render(
            
            texto_interior, 
            
            True, 
            
            (255, 255, 255)
            
        )
        
        
        texto_sombra = self.fuente_numeros.render(
            
            texto_interior, 
            
            True, 
            
            (0, 0, 0)
            
        )
        
        
        tx = (
            cx 
            + 
            (ancho_tubo - texto_rend.get_width()) 
            // 
            2
        )
        
        
        ty = (
            y 
            + 
            (alto - texto_rend.get_height()) 
            // 
            2
        )
        
        
        self.pantalla.blit(
            
            texto_sombra, 
            
            (tx + 2, ty + 2)
            
        )
        
        
        self.pantalla.blit(
            
            texto_rend, 
            
            (tx, ty)
            
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
            
            (x + 10, y + (alto_slot - 14) // 2)
            
        )
        
        
        if esta_activo:
            
            color_capsula = color_activo
            
            color_texto = (255, 255, 255)
            
        else:
            
            color_capsula = (50, 60, 55)
            
            color_texto = (150, 160, 155)
            
            
        ancho_capsula = (
            ancho - 85
        )
            
            
        rect_capsula = pygame.Rect(
            
            x + 75, 
            y + 4, 
            ancho_capsula, 
            alto_slot - 8
            
        )
        
        
        # Animación de Glow palpitante
        
        if esta_activo:
            
            tiempo = pygame.time.get_ticks()
            
            
            glow_alpha = int(
                
                40 
                + 
                30 
                * 
                math.sin(tiempo / 150.0)
                
            )
            
            
            superficie_glow = pygame.Surface(
                
                (ancho_capsula + 6, alto_slot - 2), 
                
                pygame.SRCALPHA
                
            )
            
            
            pygame.draw.rect(
                
                superficie_glow, 
                
                (*color_activo, glow_alpha), 
                
                superficie_glow.get_rect(), 
                
                border_radius=4
                
            )
            
            
            self.pantalla.blit(
                
                superficie_glow, 
                
                (rect_capsula.x - 3, rect_capsula.y - 3)
                
            )
        
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            color_capsula, 
            
            rect_capsula, 
            
            border_radius=4
            
        )
        
        
        valor_rend = self.fuente_UI.render(
            
            valor_texto, 
            
            True, 
            
            color_texto
            
        )
        
        
        vx = (
            rect_capsula.x 
            + 
            (rect_capsula.width - valor_rend.get_width()) 
            // 
            2
        )
        
        
        vy = (
            rect_capsula.y 
            + 
            (rect_capsula.height - valor_rend.get_height()) 
            // 
            2
        )
        
        
        self.pantalla.blit(
            
            valor_rend, 
            
            (vx, vy)
            
        )



    def dibujar_boton_interactivo(
        
        self,
        rect_boton,
        color_base,
        color_luz,
        color_sombra,
        texto_boton
        
    ):
        
        esta_sobre = rect_boton.collidepoint(
            
            (self.mouse_x, self.mouse_y)
            
        )
        
        
        if esta_sobre:
            
            color_usar = color_luz
            
            
            pygame.draw.rect(
                
                self.pantalla, 
                
                (*color_luz, 100), 
                
                rect_boton.inflate(6, 6), 
                
                border_radius=12
                
            )
            
        else:
            
            color_usar = color_base
            
            
        self.dibujar_caja_biselada_solida(
            
            rect_boton, 
            
            color_usar, 
            
            color_luz, 
            
            color_sombra, 
            
            grosor_borde=3
            
        )
        
        
        t_rend = self.fuente_UI.render(
            
            texto_boton, 
            
            True, 
            
            (255, 255, 255)
            
        )
        
        
        self.pantalla.blit(
            
            t_rend, 
            
            (
                rect_boton.x + (rect_boton.width - t_rend.get_width()) // 2, 
                rect_boton.y + 16
            )
            
        )



    # =========================================
    # RENDERIZADO DEL PANEL SUPERIOR COMPLETO
    # =========================================

    def dibujar_panel(self):

        rect_panel_base = pygame.Rect(
            
            0, 
            0, 
            self.ancho, 
            self.alto_panel
            
        )
        
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            self.C_MADERA_FONDO, 
            
            rect_panel_base
            
        )
        
        
        for i in range(0, self.ancho, 150):
            
            pygame.draw.line(
                
                self.pantalla, 
                
                (20, 12, 8), 
                
                (i, 0), 
                
                (i, self.alto_panel), 
                
                3
                
            )
            
            
        pygame.draw.rect(
            
            self.pantalla, 
            
            self.C_ORO_PURO, 
            
            (0, self.alto_panel - 6, self.ancho, 6)
            
        )
        
        
        pygame.draw.rect(
            
            self.pantalla, 
            
            self.C_MADERA_SOMBRA, 
            
            (0, self.alto_panel - 8, self.ancho, 2)
            
        )


        # =====================================
        # CÁLCULO DE MÁRGENES PERFECTOS
        # =====================================
        
        espacio_entre_bloques = 25
        
        
        ancho_bloque_izq = 330
        
        
        ancho_bloque_der = 400
        
        
        ancho_bloque_cen = (
            
            self.ancho 
            - 
            ancho_bloque_izq 
            - 
            ancho_bloque_der 
            - 
            (espacio_entre_bloques * 4)
            
        )
        
        
        x_izq = espacio_entre_bloques
        
        
        x_cen = (
            
            x_izq 
            + 
            ancho_bloque_izq 
            + 
            espacio_entre_bloques
            
        )
        
        
        x_der = (
            
            self.ancho 
            - 
            ancho_bloque_der 
            - 
            espacio_entre_bloques
            
        )


        # =====================================
        # BLOQUE 1: IDENTIFICACIÓN Y ESTADO
        # =====================================
        
        rect_bloque_izq = pygame.Rect(
            
            x_izq, 
            20, 
            ancho_bloque_izq, 
            145
            
        )
        
        
        self.dibujar_caja_biselada_solida(
            
            rect_bloque_izq, 
            
            self.C_MADERA_BASE, 
            
            self.C_MADERA_LUZ, 
            
            self.C_MADERA_SOMBRA
            
        )
        
        
        txt_ag = self.fuente_titulo.render(
            
            "AGENTE", 
            
            True, 
            
            (255, 255, 255)
            
        )
        
        
        txt_cz = self.fuente_titulo.render(
            
            " CAZADOR", 
            
            True, 
            
            self.C_ORO_PURO
            
        )
        
        
        self.pantalla.blit(
            
            txt_ag, 
            
            (x_izq + 25, 40)
            
        )
        
        
        self.pantalla.blit(
            
            txt_cz, 
            
            (x_izq + 25 + txt_ag.get_width(), 40)
            
        )
        
        
        tiempo = pygame.time.get_ticks()
        
        
        color_online = (
            
            50, 
            
            int(150 + 100 * math.sin(tiempo / 300.0)), 
            
            100
            
        )
        
        
        sys_lbl = self.fuente_pequena.render(
            
            "SISTEMA AUTÓNOMO ONLINE", 
            
            True, 
            
            color_online
            
        )
        
        
        self.pantalla.blit(
            
            sys_lbl, 
            
            (x_izq + 28, 75)
            
        )
        
        
        estado_str = str(
            
            getattr(self.agente, 'estado', 'Iniciando')
            
        )
        
        
        if len(estado_str) > 28:
            
            estado_str = estado_str[:25] + "..."
            
            
        estado_rend = self.fuente_UI.render(
            
            f"ESTADO: {estado_str}", 
            
            True, 
            
            self.C_ORO_VIEJO
            
        )
        
        
        self.pantalla.blit(
            
            estado_rend, 
            
            (x_izq + 25, 115)
            
        )


        # =====================================
        # BLOQUE 2: MATRIZ DE LOS 5 SENTIDOS
        # =====================================
        
        rect_bloque_cen = pygame.Rect(
            
            x_cen, 
            20, 
            ancho_bloque_cen, 
            145
            
        )
        
        
        self.dibujar_caja_biselada_solida(
            
            rect_bloque_cen, 
            
            self.C_MADERA_BASE, 
            
            self.C_MADERA_LUZ, 
            
            self.C_MADERA_SOMBRA
            
        )
        
        
        tit_sens = self.fuente_subtitulo.render(
            
            "MATRIZ SENSORIAL", 
            
            True, 
            
            self.C_ORO_PURO
            
        )
        
        
        self.pantalla.blit(
            
            tit_sens, 
            
            (x_cen + 20, 30)
            
        )
        
        
        padding_sens = 15
        
        
        ancho_slot = (
            
            (ancho_bloque_cen - (padding_sens * 3)) 
            // 
            2
            
        )
        
        
        x_col1 = x_cen + padding_sens
        
        
        x_col2 = x_col1 + ancho_slot + padding_sens
        
        
        # --- 1. VISIÓN (👁️) ---
        
        si_ve = getattr(
            self.agente.sentidos, 've_puma', False
        )
        
        
        txt_ve = "ALERTA: PUMA" if si_ve else "Despejado"
        
        
        self.dibujar_slot_sentido_animado(
            
            x_col1, 
            55, 
            ancho_slot, 
            "👁️ Visión", 
            txt_ve, 
            si_ve, 
            self.C_NEON_ROJO
            
        )
        
        
        # --- 2. OÍDO (👂) ---
        
        si_escucha = getattr(
            self.agente.sentidos, 'escucha_puma', False
        )
        
        
        dir_son = str(
            getattr(self.agente.sentidos, 'direccion_sonido', 'NULA')
        ).upper()
        
        
        txt_oido = dir_son if si_escucha else "Silencio"
        
        
        self.dibujar_slot_sentido_animado(
            
            x_col1, 
            95, 
            ancho_slot, 
            "👂 Oído", 
            txt_oido, 
            si_escucha, 
            self.C_NEON_AMARILLO
            
        )
        
        
        # --- 3. OLFATO (👃) ---
        
        si_huele = getattr(
            self.agente.sentidos, 'percibe_olor', False
        )
        
        
        txt_huele = "Fuerte" if si_huele else "Normal"
        
        
        self.dibujar_slot_sentido_animado(
            
            x_col2, 
            55, 
            ancho_slot, 
            "👃 Olfato", 
            txt_huele, 
            si_huele, 
            self.C_NEON_MORADO
            
        )
        
        
        # --- 4. TACTO (🖐️) ---
        
        si_siente = getattr(
            self.agente.sentidos, 'siente_vibracion', False
        )
        
        
        txt_siente = "Vibración" if si_siente else "Estable"
        
        
        self.dibujar_slot_sentido_animado(
            
            x_col2, 
            95, 
            ancho_slot, 
            "🖐️ Tacto", 
            txt_siente, 
            si_siente, 
            self.C_NEON_AZUL
            
        )
        
        
        # --- 5. GUSTO (👅) ---
        
        si_sabor = getattr(
            self.agente.sentidos, 'saborea_baya', False
        )
        
        
        txt_sabor = "Ácido" if si_sabor else "Neutro"
        
        
        x_col3 = (
            
            x_cen 
            + 
            (ancho_bloque_cen - ancho_slot) 
            // 
            2
            
        )
        
        
        self.dibujar_slot_sentido_animado(
            
            x_col3, 
            132, 
            ancho_slot, 
            "👅 Gusto", 
            txt_sabor, 
            si_sabor, 
            self.C_NEON_VERDE
            
        )


        # =====================================
        # BLOQUE 3: BARRAS Y CONTROLES
        # =====================================
        
        rect_bloque_der = pygame.Rect(
            
            x_der, 
            20, 
            ancho_bloque_der, 
            145
            
        )
        
        
        self.dibujar_caja_biselada_solida(
            
            rect_bloque_der, 
            
            self.C_MADERA_BASE, 
            
            self.C_MADERA_LUZ, 
            
            self.C_MADERA_SOMBRA
            
        )
        
        
        # ----------- BARRA ENERGÍA -----------
        
        energia = self.agente.energia
        
        
        if energia > 30:
            
            color_en = self.C_ORO_PURO
            
        else:
            
            color_en = self.C_NEON_ROJO
            
            
        self.dibujar_barra_animada(
            
            x_der + 20, 
            35, 
            ancho_bloque_der - 40, 
            28, 
            energia / 100.0, 
            color_en, 
            f"ENERGÍA: {int(energia)}%"
            
        )
        
        
        # ----------- BOTONES INTERACTIVOS -----------
        
        ancho_btn = (
            
            (ancho_bloque_der - 60) 
            // 
            2
            
        )
        
        
        rect_btn_1 = pygame.Rect(
            
            x_der + 20, 
            85, 
            ancho_btn, 
            50
            
        )
        
        
        if self.en_curso:
            
            c_base1 = (200, 50, 50)
            
            c_luz1 = (255, 100, 100)
            
            c_sombra1 = (100, 20, 20)
            
            txt1 = "PAUSAR (ESP)"
            
        else:
            
            c_base1 = (50, 180, 80)
            
            c_luz1 = (100, 255, 120)
            
            c_sombra1 = (20, 80, 30)
            
            txt1 = "INICIAR (ESP)"
            
            
        self.dibujar_boton_interactivo(
            
            rect_btn_1, 
            
            c_base1, 
            
            c_luz1, 
            
            c_sombra1, 
            
            txt1
            
        )
        
        
        rect_btn_2 = pygame.Rect(
            
            x_der + 40 + ancho_btn, 
            85, 
            ancho_btn, 
            50
            
        )
        
        
        c_base2 = (40, 100, 200)
        
        c_luz2 = (100, 180, 255)
        
        c_sombra2 = (20, 40, 100)
        
        txt2 = "REINICIAR (R)"
        
        
        self.dibujar_boton_interactivo(
            
            rect_btn_2, 
            
            c_base2, 
            
            c_luz2, 
            
            c_sombra2, 
            
            txt2
            
        )



    # =========================================
    # TABLERO DE JUEGO (MAPA Y ENTIDADES)
    # =========================================

    def dibujar_tablero(self):

        zona_mundo = pygame.Rect(
            
            self.offset_mapa_x,
            
            self.offset_mapa_y,
            
            self.mundo.ancho,
            
            self.mundo.alto
            
        )


        # =====================================
        # FONDO COMPLETO DE PANTALLA
        # =====================================

        if self.usa_fondo_img:
            
            self.pantalla.blit(
                
                self.fondo_juego, 
                
                (0, 0)
                
            )
            
            
            capa_oscura = pygame.Surface(
                
                (
                    self.mundo.ancho, 
                    self.mundo.alto
                ), 
                
                pygame.SRCALPHA
                
            )
            
            
            capa_oscura.fill(
                
                (10, 20, 15, 140)
                
            )
            
            
            self.pantalla.blit(
                
                capa_oscura, 
                
                (self.offset_mapa_x, self.offset_mapa_y)
                
            )
            
        else:
            
            pygame.draw.rect(
                
                self.pantalla,
                
                (35, 75, 45),
                
                zona_mundo
                
            )


        # =====================================
        # APLICAR CLIPPING
        # =====================================
        
        self.pantalla.set_clip(
            
            zona_mundo
            
        )


        # =====================================
        # CUADRÍCULA DE CRISTAL
        # =====================================

        color_linea = (200, 255, 200, 40)


        for col in range(
            self.mundo.columnas + 1
        ):
            
            px = (
                
                self.offset_mapa_x 
                + 
                (col * self.mundo.tamano_celda)
                
            )
            
            
            pygame.draw.line(
                
                self.pantalla, 
                
                color_linea, 
                
                (px, self.offset_mapa_y), 
                
                (px, self.offset_mapa_y + self.mundo.alto), 
                
                1
                
            )


        for fil in range(
            self.mundo.filas + 1
        ):
            
            py = (
                
                self.offset_mapa_y 
                + 
                (fil * self.mundo.tamano_celda)
                
            )
            
            
            pygame.draw.line(
                
                self.pantalla, 
                
                color_linea, 
                
                (self.offset_mapa_x, py), 
                
                (self.offset_mapa_x + self.mundo.ancho, py), 
                
                1
                
            )
            
            
        # =====================================
        # RANGO DE OÍDO (SONAR AZUL)
        # =====================================

        celdas_oido = self.agente.sentidos.obtener_celdas_oido(
            
            self.agente.posicion
            
        )


        sup_oido = pygame.Surface(
            
            (
                self.mundo.tamano_celda, 
                self.mundo.tamano_celda
            ), 
            
            pygame.SRCALPHA
            
        )
        
        
        sup_oido.fill(
            
            (100, 200, 255, 30)
            
        )
        

        for f, c in celdas_oido:
            
            px = (
                self.offset_mapa_x 
                + 
                (c * self.mundo.tamano_celda)
            )
            
            py = (
                self.offset_mapa_y 
                + 
                (f * self.mundo.tamano_celda)
            )

            self.pantalla.blit(
                
                sup_oido, 
                
                (px, py)
                
            )

            pygame.draw.rect(
                
                self.pantalla,
                
                (100, 200, 255, 100),
                
                (px, py, self.mundo.tamano_celda, self.mundo.tamano_celda),
                
                1
                
            )


        # =====================================
        # RANGO DE VISIÓN (LUZ AMARILLA)
        # =====================================

        celdas_visibles = self.agente.sentidos.obtener_celdas_visibles(
            
            self.agente.posicion
            
        )
        
        
        sup_vis = pygame.Surface(
            
            (
                self.mundo.tamano_celda, 
                self.mundo.tamano_celda
            ), 
            
            pygame.SRCALPHA
            
        )
        
        
        sup_vis.fill(
            
            (255, 220, 50, 45)
            
        )


        for f, c in celdas_visibles:

            px = (
                self.offset_mapa_x 
                + 
                (c * self.mundo.tamano_celda)
            )
            
            py = (
                self.offset_mapa_y 
                + 
                (f * self.mundo.tamano_celda)
            )
            
            self.pantalla.blit(
                
                sup_vis, 
                
                (px, py)
                
            )

            pygame.draw.rect(
                
                self.pantalla,
                
                (255, 200, 50, 150),
                
                (px, py, self.mundo.tamano_celda, self.mundo.tamano_celda),
                
                2
                
            )


        # =====================================
        # ENTIDADES DEL JUEGO
        # =====================================
        
        sup_entidades = pygame.Surface(
            
            (
                self.mundo.ancho, 
                self.mundo.alto
            ), 
            
            pygame.SRCALPHA
            
        )


        for (f, c), tipo in self.mundo.grid.items():

            if tipo == 1:
                
                self.arbol.dibujar(
                    
                    sup_entidades, 
                    f, 
                    c, 
                    0
                    
                )

            elif tipo == 4:
                
                self.arena.dibujar(
                    
                    sup_entidades, 
                    f, 
                    c, 
                    0
                    
                )

            elif tipo == 5:
                
                self.baya.dibujar(
                    
                    sup_entidades, 
                    f, 
                    c, 
                    True, 
                    0
                    
                )

            elif tipo == 6:
                
                self.baya.dibujar(
                    
                    sup_entidades, 
                    f, 
                    c, 
                    False, 
                    0
                    
                )


        # Campamento
        
        fc, cc = self.mundo.campamento
        
        
        self.campamento.dibujar(
            
            sup_entidades, 
            fc, 
            cc, 
            0
            
        )


        # Puma
        
        if self.mundo.puma_vivo:
            
            fp, cp = self.mundo.posicion_puma
            
            self.puma.dibujar(
                
                sup_entidades, 
                fp, 
                cp, 
                0
                
            )


        # Cazador
        
        fa, ca = self.agente.posicion
        
        
        self.cazador.dibujar(
            
            sup_entidades, 
            fa, 
            ca, 
            0
            
        )


        # Pegar entidades
        
        self.pantalla.blit(
            
            sup_entidades, 
            
            (self.offset_mapa_x, self.offset_mapa_y)
            
        )


        # Retirar el clipping
        
        self.pantalla.set_clip(
            
            None
            
        )


        # =====================================
        # MARCO MAJESTUOSO ALREDEDOR DEL MAPA
        # =====================================
        
        # AQUÍ USAMOS LA FUNCIÓN DE MARCO HUECO
        
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