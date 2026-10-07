import pygame
import os


class Jaguar:

    def __init__(self, tamano_celda):

        self.tamano_celda = tamano_celda

        # =========================================
        # CARGAR SPRITES
        # =========================================

        # Obtiene la carpeta donde está este archivo jaguar.py
        carpeta_recursos = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Rutas de los sprites
        ruta_arriba = os.path.join(
            carpeta_recursos,
            "images",
            "jaguar_arriba.png"
        )

        ruta_abajo = os.path.join(
            carpeta_recursos,
            "images",
            "jaguar_abajo.png"
        )

        ruta_izquierda = os.path.join(
            carpeta_recursos,
            "images",
            "jaguar_izquierda.png"
        )

        ruta_derecha = os.path.join(
            carpeta_recursos,
            "images",
            "jaguar_derecha.png"
        )

        # =========================================
        # CARGAR IMÁGENES
        # =========================================

        self.sprite_arriba = pygame.image.load(
            ruta_arriba
        ).convert_alpha()

        self.sprite_abajo = pygame.image.load(
            ruta_abajo
        ).convert_alpha()

        self.sprite_izquierda = pygame.image.load(
            ruta_izquierda
        ).convert_alpha()

        self.sprite_derecha = pygame.image.load(
            ruta_derecha
        ).convert_alpha()

        # =========================================
        # CAMBIAR TAMAÑO
        # =========================================

        # El tablero utiliza celdas de 50x50,
        # por eso adaptamos los sprites de 64x64
        # al tamaño de la celda.

        self.sprite_arriba = pygame.transform.scale(
            self.sprite_arriba,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_abajo = pygame.transform.scale(
            self.sprite_abajo,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_izquierda = pygame.transform.scale(
            self.sprite_izquierda,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        self.sprite_derecha = pygame.transform.scale(
            self.sprite_derecha,
            (
                self.tamano_celda,
                self.tamano_celda
            )
        )

        # =========================================
        # DIRECCIÓN INICIAL
        # =========================================

        self.direccion = "abajo"

        # Guarda la posición anterior del jaguar
        # para detectar hacia dónde se movió.
        self.posicion_anterior = None


    def actualizar_direccion(
        self,
        fila,
        columna
    ):

        # Si es la primera vez que dibujamos
        # al jaguar, todavía no sabemos hacia
        # dónde se movió.
        if self.posicion_anterior is None:

            self.posicion_anterior = (
                fila,
                columna
            )

            return

        # Obtener posición anterior
        fila_anterior, columna_anterior = (
            self.posicion_anterior
        )

        # =========================================
        # DETECTAR DIRECCIÓN
        # =========================================

        # Se movió hacia arriba
        if fila < fila_anterior:

            self.direccion = "arriba"

        # Se movió hacia abajo
        elif fila > fila_anterior:

            self.direccion = "abajo"

        # Se movió hacia la izquierda
        elif columna < columna_anterior:

            self.direccion = "izquierda"

        # Se movió hacia la derecha
        elif columna > columna_anterior:

            self.direccion = "derecha"

        # Guardamos la posición actual
        # para compararla en el siguiente movimiento.
        self.posicion_anterior = (
            fila,
            columna
        )


    def obtener_sprite(self):

        # =========================================
        # SELECCIONAR SPRITE
        # =========================================

        if self.direccion == "arriba":

            return self.sprite_arriba

        elif self.direccion == "izquierda":

            return self.sprite_izquierda

        elif self.direccion == "derecha":

            return self.sprite_derecha

        # Por defecto mira hacia abajo
        return self.sprite_abajo


    def dibujar(
        self,
        pantalla,
        fila,
        columna,
        desplazamiento_y=0
    ):

        # =========================================
        # ACTUALIZAR DIRECCIÓN
        # =========================================

        self.actualizar_direccion(
            fila,
            columna
        )

        # Obtener el sprite correspondiente
        sprite = self.obtener_sprite()

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
        # CENTRAR SPRITE EN LA CELDA
        # =========================================

        rect_sprite = sprite.get_rect(
            center=(
                x + self.tamano_celda // 2,
                y + self.tamano_celda // 2
            )
        )

        # =========================================
        # DIBUJAR JAGUAR
        # =========================================

        pantalla.blit(
            sprite,
            rect_sprite
        )
