import pygame


class Baya:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        self.buena = (130, 70, 170)
        self.mala = (180, 60, 50)
        self.hoja = (35, 110, 45)


    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        buena=True,
        desplazamiento_y=0
    ):

        # =========================================
        # CENTRO DE LA CELDA
        # =========================================

        centro_x = (
            columna * self.tamano_celda
            + self.tamano_celda // 2
        )

        centro_y = (
            desplazamiento_y
            + fila * self.tamano_celda
            + self.tamano_celda // 2
        )


        # =========================================
        # COLOR
        # =========================================

        color = (
            self.buena
            if buena
            else self.mala
        )


        # =========================================
        # TAMAÑO
        # =========================================

        radio = max(
            3,
            int(self.tamano_celda * 0.11)
        )

        separacion = int(
            self.tamano_celda * 0.14
        )


        # =========================================
        # BAYAS
        # =========================================

        pygame.draw.circle(
            pantalla,
            color,
            (
                centro_x - separacion,
                centro_y
            ),
            radio
        )

        pygame.draw.circle(
            pantalla,
            color,
            (
                centro_x + separacion,
                centro_y
            ),
            radio
        )

        pygame.draw.circle(
            pantalla,
            color,
            (
                centro_x,
                centro_y - separacion
            ),
            radio
        )


        # =========================================
        # HOJA
        # =========================================

        ancho_hoja = int(
            self.tamano_celda * 0.20
        )

        alto_hoja = int(
            self.tamano_celda * 0.10
        )

        pygame.draw.ellipse(
            pantalla,
            self.hoja,
            (
                centro_x
                - ancho_hoja // 2,

                centro_y
                - int(self.tamano_celda * 0.38),

                ancho_hoja,
                alto_hoja
            )
        )