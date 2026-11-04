
import pygame
import os


class Cueva:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # CARGAR SPRITE
        # =========================================

        # Obtener la carpeta donde está este archivo
        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Ruta de la imagen
        ruta_cueva = os.path.join(
            carpeta_recursos,
            "images",
            "cueva.png"
        )

        # Cargar imagen conservando
        # el fondo transparente
        self.sprite = pygame.image.load(
            ruta_cueva
        ).convert_alpha()

        # =========================================
        # CAMBIAR TAMAÑO
        # =========================================

        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # =========================================
        # POSICIÓN DE LA CELDA
        # =========================================

        x = (
            columna
            * self.tamano_celda
        )

        y = (
            desplazamiento_y
            +
            fila
            * self.tamano_celda
        )

        # =========================================
        # CENTRAR SPRITE
        # =========================================

        rect_sprite = self.sprite.get_rect(
            center=(
                x + self.tamano_celda // 2,
                y + self.tamano_celda // 2
            )
        )

        # =========================================
        # DIBUJAR CUEVA
        # =========================================

        pantalla.blit(
            self.sprite,
            rect_sprite
        )
