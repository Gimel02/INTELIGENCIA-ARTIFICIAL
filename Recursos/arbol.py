
import pygame
import os


class Arbol:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # CARGAR SPRITE
        # =========================================

        # Obtener la carpeta donde está este archivo
        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Ruta de la imagen del árbol
        ruta_arbol = os.path.join(
            carpeta_recursos,
            "images",
            "arbol.png"
        )

        # Cargar imagen conservando
        # el fondo transparente
        self.sprite = pygame.image.load(
            ruta_arbol
        ).convert_alpha()

        # =========================================
        # CAMBIAR TAMAÑO
        # =========================================

        # Adaptar el sprite al tamaño de la celda
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
        # DIBUJAR ÁRBOL
        # =========================================

        pantalla.blit(
            self.sprite,
            rect_sprite
        )
