
import pygame
import os


class Baya:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # CARGAR SPRITES
        # =========================================

        # Obtiene la carpeta donde está este archivo
        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Rutas de las imágenes
        ruta_baya_buena = os.path.join(
            carpeta_recursos,
            "images",
            "bayas_buenas.png"
        )

        ruta_baya_mala = os.path.join(
            carpeta_recursos,
            "images",
            "bayas_malas.png"
        )

        # =========================================
        # CARGAR IMÁGENES
        # =========================================

        # Baya buena
        self.sprite_buena = pygame.image.load(
            ruta_baya_buena
        ).convert_alpha()

        # Baya mala
        self.sprite_mala = pygame.image.load(
            ruta_baya_mala
        ).convert_alpha()

        # =========================================
        # CAMBIAR TAMAÑO
        # =========================================

        self.sprite_buena = pygame.transform.scale(
            self.sprite_buena,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_mala = pygame.transform.scale(
            self.sprite_mala,
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
        buena=True,
        desplazamiento_y=0
    ):

        # =========================================
        # ELEGIR SPRITE
        # =========================================

        if buena:
            sprite = self.sprite_buena
        else:
            sprite = self.sprite_mala

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

        rect_sprite = sprite.get_rect(
            center=(
                x + self.tamano_celda // 2,
                y + self.tamano_celda // 2
            )
        )

        # =========================================
        # DIBUJAR BAYA
        # =========================================

        pantalla.blit(
            sprite,
            rect_sprite
        )
