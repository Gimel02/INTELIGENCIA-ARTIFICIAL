import pygame


class Campamento:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # Colores
        self.tela = (190, 150, 100)
        self.tela_oscura = (145, 105, 65)
        self.palo = (95, 60, 35)
        self.fuego = (230, 100, 30)
        self.fuego_claro = (255, 180, 50)


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
        # TAMAÑO DEL CAMPAMENTO
        # =========================================

        ancho = int(
            self.tamano_celda * 0.70
        )

        alto = int(
            self.tamano_celda * 0.65
        )

        izquierda = (
            centro_x - ancho // 2
        )

        derecha = (
            centro_x + ancho // 2
        )


        # =========================================
        # TIENDA
        # =========================================

        parte_superior = (
            y + int(self.tamano_celda * 0.12)
        )

        parte_inferior = (
            y + int(self.tamano_celda * 0.62)
        )

        puntos_tienda = [

            (
                centro_x,
                parte_superior
            ),

            (
                izquierda,
                parte_inferior
            ),

            (
                derecha,
                parte_inferior
            )

        ]

        pygame.draw.polygon(
            pantalla,
            self.tela_oscura,
            puntos_tienda
        )


        # =========================================
        # PARTE FRONTAL
        # =========================================

        ancho_frente = int(
            self.tamano_celda * 0.50
        )

        puntos_frente = [

            (
                centro_x,
                y + int(self.tamano_celda * 0.18)
            ),

            (
                centro_x - ancho_frente // 2,
                parte_inferior - 2
            ),

            (
                centro_x + ancho_frente // 2,
                parte_inferior - 2
            )

        ]

        pygame.draw.polygon(
            pantalla,
            self.tela,
            puntos_frente
        )


        # =========================================
        # ENTRADA DE LA TIENDA
        # =========================================

        ancho_entrada = int(
            self.tamano_celda * 0.16
        )

        entrada = [

            (
                centro_x,
                y + int(self.tamano_celda * 0.38)
            ),

            (
                centro_x - ancho_entrada // 2,
                parte_inferior - 2
            ),

            (
                centro_x + ancho_entrada // 2,
                parte_inferior - 2
            )

        ]

        pygame.draw.polygon(
            pantalla,
            self.palo,
            entrada
        )


        # =========================================
        # FOGATA
        # =========================================

        fuego_x = centro_x

        fuego_y = (
            y + int(self.tamano_celda * 0.82)
        )


        # =========================================
        # LEÑA
        # =========================================

        largo_leña = int(
            self.tamano_celda * 0.20
        )

        pygame.draw.line(
            pantalla,
            self.palo,

            (
                fuego_x - largo_leña,
                fuego_y + 2
            ),

            (
                fuego_x + largo_leña,
                fuego_y - 2
            ),

            max(
                2,
                int(self.tamano_celda * 0.06)
            )
        )

        pygame.draw.line(
            pantalla,
            self.palo,

            (
                fuego_x - largo_leña,
                fuego_y - 2
            ),

            (
                fuego_x + largo_leña,
                fuego_y + 2
            ),

            max(
                2,
                int(self.tamano_celda * 0.06)
            )
        )


        # =========================================
        # FUEGO EXTERIOR
        # =========================================

        pygame.draw.circle(
            pantalla,
            self.fuego,

            (
                fuego_x,
                fuego_y - 4
            ),

            max(
                4,
                int(self.tamano_celda * 0.14)
            )
        )


        # =========================================
        # FUEGO INTERIOR
        # =========================================

        pygame.draw.circle(
            pantalla,
            self.fuego_claro,

            (
                fuego_x,
                fuego_y - 5
            ),

            max(
                2,
                int(self.tamano_celda * 0.07)
            )
        )