
import pygame
import os


class ArenaMovediza:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # CARGAR SPRITE
        # =========================================

        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        ruta_arena = os.path.join(
            carpeta_recursos,
            "images",
            "arena_movediza.png"
        )

        self.sprite = pygame.image.load(
            ruta_arena
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
            + fila
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
        # DIBUJAR ARENA MOVEDIZA
        # =========================================

        pantalla.blit(
            self.sprite,
            rect_sprite
        )
