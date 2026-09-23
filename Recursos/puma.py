import pygame


class Puma:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # Colores
        self.color_cuerpo = (190, 110, 45)
        self.color_oscuro = (120, 70, 30)
        self.color_claro = (220, 150, 70)
        self.negro = (25, 25, 25)


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
        # CENTRO
        # =========================================

        centro_x = (
            x
            +
            self.tamano_celda // 2
        )

        centro_y = (
            y
            +
            self.tamano_celda // 2
        )


        # =========================================
        # CUERPO
        # =========================================

        ancho_cuerpo = int(
            self.tamano_celda * 0.48
        )

        alto_cuerpo = int(
            self.tamano_celda * 0.28
        )


        pygame.draw.ellipse(

            pantalla,

            self.color_cuerpo,

            (
                centro_x
                - ancho_cuerpo // 2,

                centro_y,

                ancho_cuerpo,

                alto_cuerpo
            )

        )


        # =========================================
        # CABEZA
        # =========================================

        radio_cabeza = int(
            self.tamano_celda * 0.17
        )


        cabeza_x = (
            centro_x
            +
            int(
                self.tamano_celda * 0.20
            )
        )

        cabeza_y = (
            centro_y
            -
            int(
                self.tamano_celda * 0.05
            )
        )


        pygame.draw.circle(

            pantalla,

            self.color_claro,

            (
                cabeza_x,
                cabeza_y
            ),

            radio_cabeza

        )


        # =========================================
        # OREJAS
        # =========================================

        radio_oreja = max(
            2,
            int(
                self.tamano_celda * 0.06
            )
        )


        pygame.draw.circle(

            pantalla,

            self.color_oscuro,

            (
                cabeza_x
                -
                int(
                    self.tamano_celda * 0.10
                ),

                cabeza_y
                -
                int(
                    self.tamano_celda * 0.13
                )
            ),

            radio_oreja

        )


        pygame.draw.circle(

            pantalla,

            self.color_oscuro,

            (
                cabeza_x
                +
                int(
                    self.tamano_celda * 0.10
                ),

                cabeza_y
                -
                int(
                    self.tamano_celda * 0.13
                )
            ),

            radio_oreja

        )


        # =========================================
        # OJOS
        # =========================================

        pygame.draw.circle(

            pantalla,

            self.negro,

            (
                cabeza_x
                -
                int(
                    self.tamano_celda * 0.05
                ),

                cabeza_y
                -
                int(
                    self.tamano_celda * 0.02
                )
            ),

            2

        )


        pygame.draw.circle(

            pantalla,

            self.negro,

            (
                cabeza_x
                +
                int(
                    self.tamano_celda * 0.05
                ),

                cabeza_y
                -
                int(
                    self.tamano_celda * 0.02
                )
            ),

            2

        )


        # =========================================
        # NARIZ
        # =========================================

        pygame.draw.circle(

            pantalla,

            self.negro,

            (
                cabeza_x,

                cabeza_y
                +
                int(
                    self.tamano_celda * 0.06
                )
            ),

            2

        )


        # =========================================
        # PATAS
        # =========================================

        ancho_pata = max(
            3,
            int(
                self.tamano_celda * 0.07
            )
        )

        alto_pata = int(
            self.tamano_celda * 0.18
        )


        pygame.draw.rect(

            pantalla,

            self.color_oscuro,

            (
                centro_x
                -
                int(
                    self.tamano_celda * 0.16
                ),

                centro_y
                +
                int(
                    self.tamano_celda * 0.20
                ),

                ancho_pata,

                alto_pata
            ),

            border_radius=3

        )


        pygame.draw.rect(

            pantalla,

            self.color_oscuro,

            (
                centro_x
                +
                int(
                    self.tamano_celda * 0.08
                ),

                centro_y
                +
                int(
                    self.tamano_celda * 0.20
                ),

                ancho_pata,

                alto_pata
            ),

            border_radius=3

        )


        # =========================================
        # COLA
        # =========================================

        pygame.draw.arc(

            pantalla,

            self.color_oscuro,

            (
                centro_x
                -
                int(
                    self.tamano_celda * 0.45
                ),

                centro_y
                -
                int(
                    self.tamano_celda * 0.05
                ),

                int(
                    self.tamano_celda * 0.35
                ),

                int(
                    self.tamano_celda * 0.40
                )
            ),

            1.2,

            4.5,

            max(
                2,
                int(
                    self.tamano_celda * 0.05
                )
            )

        )