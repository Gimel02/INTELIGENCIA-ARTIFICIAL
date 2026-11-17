# ==========================================
# GRÁFICAS DE LA RED NEURONAL (SVG)
#
#   funciones_transferencia.svg  las 5
#       funciones de transferencia del PDF
#   curva_aprendizaje.svg  cómo baja el error
#       en cada época del entrenamiento
#       offline
#   pesos.svg  qué aprendió la red: el peso
#       de cada entrada (la sinapsis)
#
# Se guardan en Redes_Neuronales/reporte/.
#
# Cómo correrlo (desde la carpeta del
# proyecto):
#
#   python3 -m Redes_Neuronales.graficas
# ==========================================

import json
import os

from Redes_Neuronales.funciones_transferencia import (
    escalon,
    lineal,
    lineal_mixta,
    sigmoidal,
    gaussiana,
)
from Redes_Neuronales.predictor_ataque import (
    CARPETA_PESOS,
    ARCHIVO_PESOS,
    NOMBRES_ENTRADAS,
)


CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reporte")

COLORES = ["#1f6feb", "#d1242f", "#2da44e", "#bf8700", "#8250df"]

FUENTE = "font-family='Helvetica, Arial, sans-serif'"


def _svg(ancho, alto, contenido):

    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {ancho} {alto}' "
        f"width='{ancho}' height='{alto}' {FUENTE}>"
        f"<rect width='{ancho}' height='{alto}' fill='white'/>"
        + "".join(contenido)
        + "</svg>"
    )


# ==========================================
# FUNCIONES DE TRANSFERENCIA
# ==========================================

def _panel(x0, y0, titulo, funcion, ymin, ymax, color):

    ancho, alto = 220, 150
    xmin, xmax = -4, 4

    def px(x):
        return x0 + 30 + (x - xmin) / (xmax - xmin) * (ancho - 40)

    def py(y):
        return y0 + 30 + (ymax - y) / (ymax - ymin) * (alto - 50)

    partes = [
        f"<text x='{x0 + ancho / 2}' y='{y0 + 18}' text-anchor='middle' "
        f"font-size='14' font-weight='600'>{titulo}</text>",
        # ejes
        f"<line x1='{px(xmin)}' y1='{py(0)}' x2='{px(xmax)}' y2='{py(0)}' stroke='#999'/>",
        f"<line x1='{px(0)}' y1='{py(ymin)}' x2='{px(0)}' y2='{py(ymax)}' stroke='#999'/>",
        f"<text x='{px(xmax)}' y='{py(0) + 14}' text-anchor='end' font-size='11' fill='#555'>net</text>",
        f"<text x='{px(0) + 4}' y='{py(ymax) + 10}' font-size='11' fill='#555'>y</text>",
    ]

    for valor in (ymin, ymax):

        if valor != 0:

            partes.append(
                f"<text x='{px(0) - 4}' y='{py(valor) + 4}' text-anchor='end' "
                f"font-size='10' fill='#555'>{valor:g}</text>"
            )

    puntos = []

    pasos = 160

    for i in range(pasos + 1):

        x = xmin + (xmax - xmin) * i / pasos

        y = max(ymin, min(ymax, funcion(x)))

        puntos.append(f"{px(x):.1f},{py(y):.1f}")

    partes.append(
        f"<polyline points='{' '.join(puntos)}' fill='none' "
        f"stroke='{color}' stroke-width='2.5'/>"
    )

    return partes


def grafica_funciones():

    paneles = [
        ("Escalón", escalon, -0.2, 1.2),
        ("Lineal (identidad)", lineal, -4, 4),
        ("Lineal-mixta (0 a 1)", lambda x: lineal_mixta(x, 2), -0.2, 1.2),
        ("Lineal-mixta (-1 a 1)", lambda x: lineal_mixta(x, 2, bipolar=True), -1.2, 1.2),
        ("Lineal-mixta (b, B)", lambda x: lineal_mixta(x, inferior=-1.5, superior=2.5), -2, 3),
        ("Sigmoidal", sigmoidal, -0.2, 1.2),
        ("Gaussiana", gaussiana, -0.2, 1.2),
    ]

    contenido = [
        "<text x='20' y='28' font-size='17' font-weight='600'>"
        "Funciones de transferencia: y = f(net)</text>",
        "<text x='20' y='48' font-size='12' fill='#555'>"
        "La red del jaguar usa la sigmoidal (riesgo de 0 a 1) y "
        "luego un escalón para decidir sí o no</text>",
    ]

    for i, (titulo, funcion, ymin, ymax) in enumerate(paneles):

        x0 = 20 + (i % 3) * 230
        y0 = 60 + (i // 3) * 165

        contenido += _panel(x0, y0, titulo, funcion, ymin, ymax, COLORES[i % len(COLORES)])

    return _svg(720, 565, contenido)


# ==========================================
# CURVA DE APRENDIZAJE
# ==========================================

def grafica_curva(errores):

    ancho, alto = 640, 300
    izq, der, arriba, abajo = 60, 20, 60, 50

    ymax = max(errores) * 1.05
    ymin = min(errores) * 0.95

    def px(i):
        return izq + i / max(1, len(errores) - 1) * (ancho - izq - der)

    def py(e):
        return arriba + (ymax - e) / (ymax - ymin) * (alto - arriba - abajo)

    contenido = [
        "<text x='20' y='28' font-size='17' font-weight='600'>"
        "Curva de aprendizaje: el error baja y se estabiliza</text>",
        f"<text x='20' y='46' font-size='12' fill='#555'>"
        f"Error cuadrático medio por época (entrenamiento offline, regla delta)</text>",
        f"<line x1='{izq}' y1='{alto - abajo}' x2='{ancho - der}' y2='{alto - abajo}' stroke='#999'/>",
        f"<line x1='{izq}' y1='{arriba}' x2='{izq}' y2='{alto - abajo}' stroke='#999'/>",
        f"<text x='{(ancho + izq) / 2}' y='{alto - 12}' text-anchor='middle' "
        f"font-size='12' fill='#555'>época</text>",
    ]

    for i in range(0, len(errores), 5):

        contenido.append(
            f"<text x='{px(i)}' y='{alto - abajo + 16}' text-anchor='middle' "
            f"font-size='10' fill='#555'>{i + 1}</text>"
        )

    for valor in (ymin, (ymin + ymax) / 2, ymax):

        contenido.append(
            f"<text x='{izq - 6}' y='{py(valor) + 4}' text-anchor='end' "
            f"font-size='10' fill='#555'>{valor:.3f}</text>"
        )

    puntos = " ".join(f"{px(i):.1f},{py(e):.1f}" for i, e in enumerate(errores))

    contenido.append(
        f"<polyline points='{puntos}' fill='none' stroke='{COLORES[0]}' stroke-width='2.5'/>"
    )

    return _svg(ancho, alto, contenido)


# ==========================================
# PESOS APRENDIDOS
# ==========================================

def grafica_pesos(pesos, umbral):

    ancho = 640
    nombres = list(NOMBRES_ENTRADAS) + ["umbral θ"]
    valores = list(pesos) + [umbral]

    alto = 80 + 40 * len(valores)
    centro = 360
    escala = 200 / max(abs(v) for v in valores)

    contenido = [
        "<text x='20' y='28' font-size='17' font-weight='600'>"
        "Lo que aprendió la red: el peso de cada entrada</text>",
        "<text x='20' y='46' font-size='12' fill='#555'>"
        "Positivo = sube el riesgo de ataque; negativo = lo baja</text>",
        f"<line x1='{centro}' y1='60' x2='{centro}' y2='{alto - 10}' stroke='#999'/>",
    ]

    for i, (nombre, valor) in enumerate(zip(nombres, valores)):

        y = 70 + 40 * i

        largo = valor * escala

        x = centro if largo >= 0 else centro + largo

        color = COLORES[1] if valor > 0 else COLORES[0]

        if nombre == "umbral θ":

            color = "#777"

        contenido += [
            f"<text x='{centro - 230}' y='{y + 17}' font-size='13'>{nombre}</text>",
            f"<rect x='{x:.1f}' y='{y}' width='{abs(largo):.1f}' height='24' rx='4' "
            f"fill='{color}' fill-opacity='0.8'/>",
            f"<text x='{centro + largo + (6 if largo >= 0 else -6):.1f}' y='{y + 17}' "
            f"font-size='12' text-anchor='{'start' if largo >= 0 else 'end'}'>{valor:.2f}</text>",
        ]

    return _svg(ancho, alto, contenido)


if __name__ == "__main__":

    os.makedirs(CARPETA, exist_ok=True)

    graficas = {"funciones_transferencia.svg": grafica_funciones()}

    ruta_pesos = os.path.join(CARPETA_PESOS, ARCHIVO_PESOS)

    if os.path.exists(ruta_pesos):

        with open(ruta_pesos, encoding="utf-8") as f:

            datos = json.load(f)

        graficas["curva_aprendizaje.svg"] = grafica_curva(
            datos["entrenamiento"]["error_por_epoca"]
        )

        neurona = datos["neurona"]

        graficas["pesos.svg"] = grafica_pesos(neurona["pesos"], -neurona["w0"])

    else:

        print("Primero corre: python3 -m Redes_Neuronales.entrenar_red")

    for nombre, svg in graficas.items():

        ruta = os.path.join(CARPETA, nombre)

        with open(ruta, "w", encoding="utf-8") as f:

            f.write(svg)

        print("Creada", os.path.relpath(ruta))
