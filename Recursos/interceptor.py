import pygame

from Recursos.cazador import Cazador
from Recursos.campamento import Campamento


# =========================================
# SPRITE DEL INTERCEPTOR
#
# Usa los mismos dibujos del cazador, pero
# teñidos de azul y con un aro azul debajo
# para distinguirlos.
# =========================================

COLOR_INTERCEPTOR = (60, 130, 255)


class Interceptor(Cazador):

    def __init__(self, tamano_celda):

        super().__init__(tamano_celda)

        for nombre in (
            "sprite_arriba",
            "sprite_abajo",
            "sprite_izquierda",
            "sprite_derecha",
        ):

            sprite = getattr(self, nombre).copy()

            # Tono azul sin oscurecer el dibujo
            sprite.fill(
                (170, 200, 255),
                special_flags=pygame.BLEND_RGB_MULT
            )

            sprite.fill(
                (0, 25, 80),
                special_flags=pygame.BLEND_RGB_ADD
            )

            setattr(self, nombre, sprite)


    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # Aro azul en el suelo

        centro = (
            int(columna * self.tamano_celda + self.tamano_celda // 2),
            int(desplazamiento_y + fila * self.tamano_celda + self.tamano_celda // 2)
        )

        pygame.draw.circle(
            pantalla,
            COLOR_INTERCEPTOR,
            centro,
            self.tamano_celda // 2 - 2,
            3
        )

        super().dibujar(
            pantalla,
            fila,
            columna,
            desplazamiento_y
        )


# =========================================
# CABAÑA DEL INTERCEPTOR
#
# La misma cabaña, teñida de azul y con un
# marco azul.
# =========================================

class CampamentoInterceptor(Campamento):

    def __init__(self, tamano_celda):

        super().__init__(tamano_celda)

        sprite = self.sprite.copy()

        sprite.fill(
            (170, 200, 255),
            special_flags=pygame.BLEND_RGB_MULT
        )

        sprite.fill(
            (0, 25, 80),
            special_flags=pygame.BLEND_RGB_ADD
        )

        self.sprite = sprite


    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        marco = pygame.Rect(
            int(columna * self.tamano_celda) + 1,
            int(desplazamiento_y + fila * self.tamano_celda) + 1,
            self.tamano_celda - 2,
            self.tamano_celda - 2
        )

        pygame.draw.rect(
            pantalla,
            COLOR_INTERCEPTOR,
            marco,
            3,
            border_radius=4
        )

        super().dibujar(
            pantalla,
            fila,
            columna,
            desplazamiento_y
        )
