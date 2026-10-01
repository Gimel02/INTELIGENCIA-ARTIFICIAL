
import pygame
import os


class Cazador:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # CARGAR SPRITES
        # =========================================

        # Obtener la carpeta donde está este archivo
        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Rutas de los sprites
        ruta_arriba = os.path.join(
            carpeta_recursos,
            "images",
            "cazador_arriba.png"
        )

        ruta_abajo = os.path.join(
            carpeta_recursos,
            "images",
            "cazador_abajo.png"
        )

        ruta_izquierda = os.path.join(
            carpeta_recursos,
            "images",
            "cazador_izquierda.png"
        )

        ruta_derecha = os.path.join(
            carpeta_recursos,
            "images",
            "cazador_derecha.png"
        )

        # =========================================
        # CARGAR IMÁGENES
        # =========================================

        self.sprite_arriba = pygame.image.load(
            ruta_arriba
        ).convert_alpha()

        self.sprite_abajo = pygame.image.load(
            ruta_abajo
        ).convert_alpha()

        self.sprite_izquierda = pygame.image.load(
            ruta_izquierda
        ).convert_alpha()

        self.sprite_derecha = pygame.image.load(
            ruta_derecha
        ).convert_alpha()

        # =========================================
        # CAMBIAR TAMAÑO
        # =========================================

        self.sprite_arriba = pygame.transform.scale(
            self.sprite_arriba,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_abajo = pygame.transform.scale(
            self.sprite_abajo,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_izquierda = pygame.transform.scale(
            self.sprite_izquierda,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_derecha = pygame.transform.scale(
            self.sprite_derecha,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        # =========================================
        # DIRECCIÓN INICIAL
        # =========================================

        self.direccion = "abajo"

        # =========================================
        # POSICIÓN ANTERIOR
        # =========================================

        self.posicion_anterior = None


    # =========================================
    # ACTUALIZAR DIRECCIÓN
    # =========================================

    def actualizar_direccion(
        self,
        fila,
        columna
    ):

        # Primera posición
        if self.posicion_anterior is None:

            self.posicion_anterior = (
                fila,
                columna
            )

            return

        fila_anterior, columna_anterior = (
            self.posicion_anterior
        )

        # =========================================
        # MOVIMIENTO HACIA ARRIBA
        # =========================================

        if fila < fila_anterior:

            self.direccion = "arriba"


        # =========================================
        # MOVIMIENTO HACIA ABAJO
        # =========================================

        elif fila > fila_anterior:

            self.direccion = "abajo"


        # =========================================
        # MOVIMIENTO HACIA IZQUIERDA
        # =========================================

        elif columna < columna_anterior:

            self.direccion = "izquierda"


        # =========================================
        # MOVIMIENTO HACIA DERECHA
        # =========================================

        elif columna > columna_anterior:

            self.direccion = "derecha"


        # Guardar posición actual
        self.posicion_anterior = (
            fila,
            columna
        )


    # =========================================
    # OBTENER SPRITE ACTUAL
    # =========================================

    def obtener_sprite(self):

        if self.direccion == "arriba":

            return self.sprite_arriba


        elif self.direccion == "izquierda":

            return self.sprite_izquierda


        elif self.direccion == "derecha":

            return self.sprite_derecha


        # Por defecto: abajo
        return self.sprite_abajo


    # =========================================
    # DIBUJAR CAZADOR
    # =========================================

    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # =========================================
        # ACTUALIZAR DIRECCIÓN
        # =========================================

        self.actualizar_direccion(
            fila,
            columna
        )


        # =========================================
        # OBTENER SPRITE
        # =========================================

        sprite = self.obtener_sprite()


        # =========================================
        # POSICIÓN DE LA CELDA
        # =========================================

        x = (
            columna
            *
            self.tamano_celda
        )

        y = (
            desplazamiento_y
            +
            fila
            *
            self.tamano_celda
        )


        # =========================================
        # CENTRAR SPRITE
        # =========================================

        rect_sprite = sprite.get_rect(

            center=(

                x
                +
                self.tamano_celda // 2,

                y
                +
                self.tamano_celda // 2

            )

        )


        # =========================================
        # DIBUJAR
        # =========================================

        pantalla.blit(
            sprite,
            rect_sprite
        )
