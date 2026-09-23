import pygame


class ArenaMovediza:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        self.color = (194, 170, 90)
        self.detalle = (145, 115, 60)


    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # POSICIÓN DE LA CELDA
        x = (
            columna * self.tamano_celda
        )

        y = (
            desplazamiento_y
            + fila * self.tamano_celda
        )

        # MARGEN
        margen = 8

        # ARENA
        pygame.draw.rect(
            pantalla,
            self.color,
            (
                x + margen,
                y + margen,
                self.tamano_celda - margen * 2,
                self.tamano_celda - margen * 2
            ),
            border_radius=10
        )

        # ONDAS DE LA ARENA

        for i in range(3):

            pygame.draw.arc(
                pantalla,
                self.detalle,
                (
                    x + 15,
                    y + 20 + i * 10,
                    45,
                    12
                ),
                0,
                3.14,
                2
            )