import pygame


class Arbol:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        self.tronco = (95, 65, 40)
        self.verde_oscuro = (25, 90, 35)
        self.verde = (45, 125, 50)
        self.verde_claro = (65, 145, 55)


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

        x = columna * self.tamano_celda

        y = (
            desplazamiento_y
            + fila * self.tamano_celda
        )


        # =========================================
        # CENTRO DE LA CELDA
        # =========================================

        centro_x = (
            x + self.tamano_celda // 2
        )

        centro_y = (
            y + self.tamano_celda // 2
        )


        # =========================================
        # TAMAÑO
        # =========================================

        radio = int(
            self.tamano_celda * 0.28
        )


        # =========================================
        # TRONCO
        # =========================================

        ancho_tronco = int(
            self.tamano_celda * 0.12
        )

        alto_tronco = int(
            self.tamano_celda * 0.30
        )

        pygame.draw.rect(

            pantalla,

            self.tronco,

            (
                centro_x - ancho_tronco // 2,

                y
                + self.tamano_celda
                - alto_tronco
                - 3,

                ancho_tronco,

                alto_tronco
            )
        )


        # =========================================
        # COPA DEL ÁRBOL
        # =========================================

        centro_copa_y = (
            y
            + int(self.tamano_celda * 0.35)
        )


        # Parte central
        pygame.draw.circle(
            pantalla,
            self.verde_oscuro,
            (
                centro_x,
                centro_copa_y
            ),
            radio
        )


        # Parte izquierda
        pygame.draw.circle(
            pantalla,
            self.verde,
            (
                centro_x
                - int(self.tamano_celda * 0.17),

                centro_copa_y
                + int(self.tamano_celda * 0.04)
            ),
            int(self.tamano_celda * 0.22)
        )


        # Parte derecha
        pygame.draw.circle(
            pantalla,
            self.verde,
            (
                centro_x
                + int(self.tamano_celda * 0.17),

                centro_copa_y
                + int(self.tamano_celda * 0.04)
            ),
            int(self.tamano_celda * 0.22)
        )


        # Parte superior
        pygame.draw.circle(
            pantalla,
            self.verde_claro,
            (
                centro_x,

                centro_copa_y
                - int(self.tamano_celda * 0.10)
            ),
            int(self.tamano_celda * 0.19)
        )