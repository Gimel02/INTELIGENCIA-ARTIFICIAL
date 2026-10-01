
import pygame
import os


class Campamento:

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
        ruta_campamento = os.path.join(
            carpeta_recursos,
            "images",
            "campamento.png"
        )

        # Cargar imagen conservando
        # el fondo transparente
        self.sprite = pygame.image.load(
            ruta_campamento
        ).convert_alpha()

        # =========================================
        # CAMBIAR TAMAÑO
        # =========================================

        # Adaptar el sprite de 64x64
        # al tamaño de la celda.
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
        # DIBUJAR CAMPAMENTO
        # =========================================

        pantalla.blit(
            self.sprite,
            rect_sprite
        )
