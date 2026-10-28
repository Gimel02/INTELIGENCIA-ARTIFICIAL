# ==========================================
# GRÁFICAS PARA EL REPORTE (SVG, sin librerías)
#
#   python3 -m Logica_Difusa.graficas
#
# Crea en Logica_Difusa/reporte/:
#   membresia_<variable>.svg  traslape de los
#                             términos de cada
#                             variable
#   centroide_ejemplo.svg     área agregada del
#                             ejemplo y su x*
# ==========================================

import os

from Logica_Difusa.variables import (
    ENTRADAS_CAZADOR,
    ENTRADAS_JAGUAR,
    ACCION,
    ACCION_JAGUAR
)
from Logica_Difusa.base_conocimiento import base_equipo
from Logica_Difusa.motor_mamdani import ControladorDifuso


CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reporte")

COLORES = ["#1f6feb", "#d1242f", "#2da44e", "#bf8700", "#8250df"]

ANCHO, ALTO = 640, 260
IZQ, DER, ARRIBA, ABAJO = 50, 35, 40, 50

EJEMPLO = {"reserva": 30, "distancia": 4, "peligro": 70}


def _x(valor, variable):

    rango = variable.maximo - variable.minimo

    return IZQ + (valor - variable.minimo) / rango * (ANCHO - IZQ - DER)


def _y(mu):

    return ARRIBA + (1 - mu) * (ALTO - ARRIBA - ABAJO)


def _ejes(variable, titulo):

    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" '
        f'width="{ANCHO}" height="{ALTO}" font-family="Arial" font-size="12">',
        f'<rect width="{ANCHO}" height="{ALTO}" fill="white"/>',
        f'<text x="{IZQ}" y="22" font-size="15" font-weight="bold">{titulo}</text>',
    ]

    for mu in (0, 0.5, 1):

        partes.append(
            f'<line x1="{IZQ}" y1="{_y(mu)}" x2="{ANCHO - DER}" y2="{_y(mu)}" '
            f'stroke="#ddd"/>'
            f'<text x="{IZQ - 8}" y="{_y(mu) + 4}" text-anchor="end">{mu}</text>'
        )

    paso = (variable.maximo - variable.minimo) / 10

    for i in range(11):

        valor = variable.minimo + i * paso

        partes.append(
            f'<text x="{_x(valor, variable)}" y="{ALTO - ABAJO + 18}" '
            f'text-anchor="middle">{valor:g}</text>'
        )

    partes.append(
        f'<text x="{(ANCHO + IZQ) / 2}" y="{ALTO - 8}" text-anchor="middle">'
        f'{variable.nombre} ({variable.unidad})</text>'
        f'<text x="14" y="{(ALTO - ABAJO + ARRIBA) / 2}" text-anchor="middle" '
        f'transform="rotate(-90 14 {(ALTO - ABAJO + ARRIBA) / 2})">μ (grado)</text>'
    )

    return partes


def _curva(termino, variable, color, ancho=2, relleno=None, tope=1.0):

    puntos = []

    pasos = 300

    for i in range(pasos + 1):

        valor = variable.minimo + (variable.maximo - variable.minimo) * i / pasos

        puntos.append(
            f"{_x(valor, variable):.1f},{_y(min(tope, termino.grado(valor))):.1f}"
        )

    if relleno:

        base = f"{_x(variable.maximo, variable):.1f},{_y(0):.1f} {_x(variable.minimo, variable):.1f},{_y(0):.1f}"

        return (
            f'<polygon points="{" ".join(puntos)} {base}" fill="{relleno}" '
            f'fill-opacity="0.35" stroke="none"/>'
        )

    return (
        f'<polyline points="{" ".join(puntos)}" fill="none" '
        f'stroke="{color}" stroke-width="{ancho}"/>'
    )


def grafica_variable(variable, marcar=None):

    partes = _ejes(
        variable,
        f"Funciones de membresía: {variable.nombre} "
        f"[{variable.minimo}, {variable.maximo}]"
    )

    for i, termino in enumerate(variable.terminos.values()):

        color = COLORES[i % len(COLORES)]

        partes.append(_curva(termino, variable, color))

        # Nombre del término sobre su punto más alto

        centro = (termino.puntos[0] + termino.puntos[-1]) / 2

        anclaje = "middle"

        if termino.tipo == "grado_inversa":

            centro, anclaje = variable.minimo, "start"

        elif termino.tipo == "grado":

            centro = (termino.puntos[-1] + variable.maximo) / 2

        partes.append(
            f'<text x="{_x(centro, variable)}" y="{ARRIBA - 4}" fill="{color}" '
            f'text-anchor="{anclaje}" font-weight="bold">{termino.nombre}</text>'
        )

    if marcar is not None:

        partes.append(
            f'<line x1="{_x(marcar, variable)}" y1="{ARRIBA}" '
            f'x2="{_x(marcar, variable)}" y2="{_y(0)}" stroke="black" '
            f'stroke-dasharray="5,4"/>'
            f'<text x="{_x(marcar, variable) + 4}" y="{_y(0) - 6}">'
            f'ejemplo = {marcar}</text>'
        )

    partes.append("</svg>")

    return "\n".join(partes)


def grafica_centroide(controlador, entradas):

    controlador.decidir(entradas)

    traza = controlador.ultima_traza

    variable = controlador.salida

    partes = _ejes(
        variable,
        f"Agregación (max) y centroide: x* = {traza['x_estrella']:.2f} "
        f"-> {traza['accion']}"
    )

    # Términos completos en gris claro

    for termino in variable.terminos.values():

        partes.append(_curva(termino, variable, "#bbb", ancho=1))

    # Área agregada

    puntos = [
        f"{_x(x, variable):.1f},{_y(mu):.1f}"
        for x, mu in zip(traza["xs"], traza["agregado"])
    ]

    partes.append(
        f'<polygon points="{" ".join(puntos)} {_x(variable.maximo, variable):.1f},{_y(0):.1f} '
        f'{_x(variable.minimo, variable):.1f},{_y(0):.1f}" fill="#1f6feb" fill-opacity="0.35" '
        f'stroke="#1f6feb" stroke-width="2"/>'
    )

    for i, (nombre, termino) in enumerate(variable.terminos.items()):

        centro = (termino.puntos[0] + termino.puntos[-1]) / 2

        if termino.tipo == "grado_inversa":

            centro = (variable.minimo + termino.puntos[0]) / 2

        elif termino.tipo == "grado":

            centro = (termino.puntos[-1] + variable.maximo) / 2

        partes.append(
            f'<text x="{_x(centro, variable)}" y="{ARRIBA - 4}" fill="#555" '
            f'text-anchor="middle">{nombre}</text>'
        )

    x_estrella = traza["x_estrella"]

    partes.append(
        f'<line x1="{_x(x_estrella, variable)}" y1="{ARRIBA}" x2="{_x(x_estrella, variable)}" '
        f'y2="{_y(0)}" stroke="black" stroke-width="2"/>'
        f'<text x="{_x(x_estrella, variable) + 5}" y="{ARRIBA + 14}" font-weight="bold">'
        f'x* = {x_estrella:.2f}</text>'
    )

    partes.append("</svg>")

    return "\n".join(partes)


if __name__ == "__main__":

    os.makedirs(CARPETA, exist_ok=True)

    todas = (
        list(ENTRADAS_CAZADOR.items()) + [(ACCION.nombre, ACCION)]
        + list(ENTRADAS_JAGUAR.items()) + [(ACCION_JAGUAR.nombre, ACCION_JAGUAR)]
    )

    for nombre, variable in todas:

        ruta = os.path.join(CARPETA, f"membresia_{nombre}.svg")

        with open(ruta, "w", encoding="utf-8") as f:

            f.write(grafica_variable(variable, EJEMPLO.get(nombre)))

        print("Creada", os.path.relpath(ruta))

    ruta = os.path.join(CARPETA, "centroide_ejemplo.svg")

    with open(ruta, "w", encoding="utf-8") as f:

        f.write(grafica_centroide(ControladorDifuso(base_equipo("cazador")), EJEMPLO))

    print("Creada", os.path.relpath(ruta))
