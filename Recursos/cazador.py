import pygame


class Cazador:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # Colores
        self.piel = (210, 160, 110)
        self.camisa = (70, 105, 65)
        self.camisa_oscura = (45, 75, 45)
        self.pantalon = (75, 65, 50)
        self.botas = (55, 40, 30)

        self.sombrero = (120, 85, 45)
        self.sombrero_oscuro = (90, 60, 30)

        self.mochila = (100, 65, 35)
        self.negro = (30, 30, 30)


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
            columna * self.tamano_celda
        )

        y = (
            desplazamiento_y
            + fila * self.tamano_celda
        )

        centro_x = (
            x + self.tamano_celda // 2
        )

        # =========================================
        # TAMAÑOS
        # =========================================

        cabeza = int(
            self.tamano_celda * 0.20
        )

        # =========================================
        # MOCHILA
        # =========================================

        pygame.draw.rect(
            pantalla,
            self.mochila,
            (
                centro_x
                - int(self.tamano_celda * 0.30),

                y
                + int(self.tamano_celda * 0.38),

                int(self.tamano_celda * 0.18),

                int(self.tamano_celda * 0.30)
            ),
            border_radius=4
        )

        # =========================================
        # PIERNAS
        # =========================================

        pygame.draw.rect(
            pantalla,
            self.pantalon,
            (
                centro_x
                - int(self.tamano_celda * 0.17),

                y
                + int(self.tamano_celda * 0.68),

                int(self.tamano_celda * 0.13),

                int(self.tamano_celda * 0.20)
            ),
            border_radius=3
        )

        pygame.draw.rect(
            pantalla,
            self.pantalon,
            (
                centro_x
                + int(self.tamano_celda * 0.04),

                y
                + int(self.tamano_celda * 0.68),

                int(self.tamano_celda * 0.13),

                int(self.tamano_celda * 0.20)
            ),
            border_radius=3
        )

        # =========================================
        # BOTAS
        # =========================================

        pygame.draw.rect(
            pantalla,
            self.botas,
            (
                centro_x
                - int(self.tamano_celda * 0.19),

                y
                + int(self.tamano_celda * 0.84),

                int(self.tamano_celda * 0.17),

                int(self.tamano_celda * 0.08)
            ),
            border_radius=3
        )

        pygame.draw.rect(
            pantalla,
            self.botas,
            (
                centro_x
                + int(self.tamano_celda * 0.02),

                y
                + int(self.tamano_celda * 0.84),

                int(self.tamano_celda * 0.17),

                int(self.tamano_celda * 0.08)
            ),
            border_radius=3
        )

        # =========================================
        # CUERPO
        # =========================================

        pygame.draw.rect(
            pantalla,
            self.camisa,
            (
                centro_x
                - int(self.tamano_celda * 0.25),

                y
                + int(self.tamano_celda * 0.35),

                int(self.tamano_celda * 0.50),

                int(self.tamano_celda * 0.38)
            ),
            border_radius=7
        )

        # =========================================
        # BRAZO IZQUIERDO
        # =========================================

        pygame.draw.line(
            pantalla,
            self.camisa_oscura,
            (
                centro_x
                - int(self.tamano_celda * 0.23),

                y
                + int(self.tamano_celda * 0.42)
            ),
            (
                centro_x
                - int(self.tamano_celda * 0.32),

                y
                + int(self.tamano_celda * 0.68)
            ),
            max(
                3,
                int(self.tamano_celda * 0.10)
            )
        )

        # =========================================
        # BRAZO DERECHO
        # =========================================

        pygame.draw.line(
            pantalla,
            self.camisa_oscura,
            (
                centro_x
                + int(self.tamano_celda * 0.23),

                y
                + int(self.tamano_celda * 0.42)
            ),
            (
                centro_x
                + int(self.tamano_celda * 0.32),

                y
                + int(self.tamano_celda * 0.68)
            ),
            max(
                3,
                int(self.tamano_celda * 0.10)
            )
        )

        # =========================================
        # CABEZA
        # =========================================

        pygame.draw.circle(
            pantalla,
            self.piel,
            (
                centro_x,
                y
                + int(self.tamano_celda * 0.27)
            ),
            cabeza
        )

        # =========================================
        # SOMBRERO
        # =========================================

        sombrero_y = (
            y
            + int(self.tamano_celda * 0.08)
        )

        pygame.draw.ellipse(
            pantalla,
            self.sombrero,
            (
                centro_x
                - int(self.tamano_celda * 0.32),

                sombrero_y,

                int(self.tamano_celda * 0.64),

                int(self.tamano_celda * 0.16)
            )
        )

        pygame.draw.rect(
            pantalla,
            self.sombrero,
            (
                centro_x
                - int(self.tamano_celda * 0.20),

                sombrero_y
                - int(self.tamano_celda * 0.08),

                int(self.tamano_celda * 0.40),

                int(self.tamano_celda * 0.15)
            ),
            border_radius=4
        )

        # =========================================
        # CINTA DEL SOMBRERO
        # =========================================

        pygame.draw.rect(
            pantalla,
            self.sombrero_oscuro,
            (
                centro_x
                - int(self.tamano_celda * 0.20),

                sombrero_y
                + int(self.tamano_celda * 0.06),

                int(self.tamano_celda * 0.40),

                int(self.tamano_celda * 0.05)
            )
        )

        # =========================================
        # OJOS
        # =========================================

        ojo_y = (
            y
            + int(self.tamano_celda * 0.27)
        )

        pygame.draw.circle(
            pantalla,
            self.negro,
            (
                centro_x
                - int(self.tamano_celda * 0.07),
                ojo_y
            ),
            2
        )

        pygame.draw.circle(
            pantalla,
            self.negro,
            (
                centro_x
                + int(self.tamano_celda * 0.07),
                ojo_y
            ),
            2
        )