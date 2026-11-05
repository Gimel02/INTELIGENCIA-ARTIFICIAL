
import pygame
import os

from Recursos.cazador import Cazador
from Recursos.campamento import Campamento


# =========================================
# SPRITE DEL INTERCEPTOR
# =========================================

COLOR_INTERCEPTOR = (60, 130, 255)


class Interceptor(Cazador):

    def __init__(self, tamano_celda):

        # Inicializar atributos y comportamiento del cazador
        super().__init__(tamano_celda)

        # Obtener carpeta de imágenes
        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        carpeta_imagenes = os.path.join(
            carpeta_recursos,
            "images"
        )

        # Cargar los cuatro sprites propios del interceptor
        self.sprite_arriba = pygame.image.load(
            os.path.join(carpeta_imagenes, "interceptor_arriba.png")
        ).convert_alpha()

        self.sprite_abajo = pygame.image.load(
            os.path.join(carpeta_imagenes, "interceptor_abajo.png")
        ).convert_alpha()

        self.sprite_izquierda = pygame.image.load(
            os.path.join(carpeta_imagenes, "interceptor_izquierda.png")
        ).convert_alpha()

        self.sprite_derecha = pygame.image.load(
            os.path.join(carpeta_imagenes, "interceptor_derecha.png")
        ).convert_alpha()

        # Ajustar todos los sprites al tamaño de la celda
        self.sprite_arriba = pygame.transform.scale(
            self.sprite_arriba,
            (tamano_celda, tamano_celda)
        )

        self.sprite_abajo = pygame.transform.scale(
            self.sprite_abajo,
            (tamano_celda, tamano_celda)
        )

        self.sprite_izquierda = pygame.transform.scale(
            self.sprite_izquierda,
            (tamano_celda, tamano_celda)
        )

        self.sprite_derecha = pygame.transform.scale(
            self.sprite_derecha,
            (tamano_celda, tamano_celda)
        )

    # =========================================
    # DIBUJAR INTERCEPTOR
    # =========================================

    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # Centro de la celda
        centro = (
            int(columna * self.tamano_celda + self.tamano_celda // 2),
            int(desplazamiento_y + fila * self.tamano_celda + self.tamano_celda // 2)
        )

        # Aro azul para distinguir al interceptor
        pygame.draw.circle(
            pantalla,
            COLOR_INTERCEPTOR,
            centro,
            self.tamano_celda // 2 - 2,
            3
        )

        # Dibujar con sus propios sprites
        super().dibujar(
            pantalla,
            fila,
            columna,
            desplazamiento_y
        )


# =========================================
# CABAÑA DEL INTERCEPTOR
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
