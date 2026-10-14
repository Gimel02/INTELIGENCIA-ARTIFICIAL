
import pygame
import os


class Raton:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # RUTA DE LA IMAGEN
        # =========================================

        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        ruta_raton = os.path.join(
            carpeta_recursos,
            "images",
            "raton.png"
        )

        # =========================================
        # CARGAR IMAGEN
        # =========================================

        self.imagen = pygame.image.load(
            ruta_raton
        ).convert_alpha()

        # =========================================
        # AJUSTAR TAMAÑO
        # =========================================

       
        # Los ratones ocuparán el 60% del tamaño de la celda
        tamano_raton = int(self.tamano_celda * 0.6)

        self.imagen = pygame.transform.scale(
        self.imagen,
        (tamano_raton, tamano_raton)
        )


    # =========================================
    # DIBUJAR RATON
    # =========================================

    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # Calcular posición en la pantalla

        x = columna * self.tamano_celda

        y = (
            desplazamiento_y
            + fila * self.tamano_celda
        )

        # Centrar imagen en la celda

        rect_sprite = self.imagen.get_rect(
            center=(
                x + self.tamano_celda // 2,
                y + self.tamano_celda // 2
            )
        )

        # Dibujar imagen

        pantalla.blit(
            self.imagen,
            rect_sprite
        )
