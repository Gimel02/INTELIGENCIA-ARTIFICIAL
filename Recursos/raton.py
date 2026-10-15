import pygame
import os


class Raton:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # RUTAS DE LAS IMAGENES
        # =========================================

        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        carpeta_images = os.path.join(
            carpeta_recursos,
            "images"
        )

        # =========================================
        # CARGAR LAS CUATRO DIRECCIONES
        # =========================================

        nombres = {
            "arriba": "raton_arriba.png",
            "abajo": "raton_abajo.png",
            "izquierda": "raton_izquierda.png",
            "derecha": "raton_derecha.png"
        }

        self.imagenes = {}

        tamano_raton = int(
            self.tamano_celda * 0.6
        )

        for direccion, nombre in nombres.items():

            ruta = os.path.join(
                carpeta_images,
                nombre
            )

            imagen = pygame.image.load(
                ruta
            ).convert_alpha()

            self.imagenes[direccion] = (
                pygame.transform.scale(
                    imagen,
                    (tamano_raton, tamano_raton)
                )
            )

        # Direccion inicial
        self.direccion = "abajo"

    # =========================================
    # DIBUJAR RATON SEGUN SU DIRECCION
    # =========================================

    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0,
        direccion=None
    ):

        # Actualizar direccion si se proporciona
        if direccion in self.imagenes:
            self.direccion = direccion

        # Obtener imagen correspondiente
        imagen = self.imagenes[self.direccion]

        # Calcular posicion en pantalla
        x = columna * self.tamano_celda

        y = (
            desplazamiento_y
            + fila * self.tamano_celda
        )

        # Centrar el raton
        rect_sprite = imagen.get_rect(
            center=(
                int(x + self.tamano_celda / 2),
                int(y + self.tamano_celda / 2)
            )
        )

        # Dibujar imagen transparente
        pantalla.blit(
            imagen,
            rect_sprite
        )
