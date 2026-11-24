# ==========================================
# PATRÓN LOCAL DEL ENTORNO PARA ART1
#
# Convierte las cuatro casillas ortogonales
# alrededor de un agente en un patrón
# binario de cuatro entradas:
#
#   x1 = arriba
#   x2 = abajo
#   x3 = izquierda
#   x4 = derecha
#
# Cada entrada representa:
#
#   1 = terreno local transitable y seguro
#   0 = obstáculo, peligro o borde
#
# Esta función NO examina todo el mapa.
# Solo observa las cuatro casillas vecinas
# al agente.
#
# El patrón actual funciona como memoria
# de corto plazo (STM).
#
# ART1 almacenará los prototipos aprendidos
# como memoria de largo plazo (LTM).
# ==========================================


# ==========================================
# ORDEN FIJO DE LAS 4 ENTRADAS
# ==========================================

DIRECCIONES = (

    (
        "arriba",
        (-1, 0)
    ),

    (
        "abajo",
        (1, 0)
    ),

    (
        "izquierda",
        (0, -1)
    ),

    (
        "derecha",
        (0, 1)
    ),

)


# ==========================================
# TIPOS DE TERRENO DEL MUNDO
# ==========================================
#
# MundoSelva utiliza:
#
# 0 = terreno libre
# 1 = árbol
# 4 = arena movediza
# 5 = baya
# 6 = baya
#
# Para ART, las bayas siguen siendo
# transitables. No se utiliza aquí si son
# buenas o malas porque eso pertenece al
# conocimiento particular del agente.
# ==========================================

TERRENO_LIBRE = 0
ARBOL = 1
ARENA = 4
BAYA_1 = 5
BAYA_2 = 6


# ==========================================
# POSICIONES VECINAS
# ==========================================

def posiciones_vecinas(
    posicion
):

    fila, columna = posicion

    return {

        nombre: (
            fila + desplazamiento[0],
            columna + desplazamiento[1]
        )

        for nombre, desplazamiento
        in DIRECCIONES

    }


# ==========================================
# ANALIZAR UNA SOLA CASILLA
# ==========================================

def analizar_casilla(
    mundo,
    posicion
):

    # ======================================
    # BORDE DEL MAPA
    # ======================================

    if not mundo.dentro_limites(
        posicion
    ):

        return {
            "valor": 0,
            "tipo": "borde",
            "posicion": posicion,
        }


    tipo = mundo.grid[
        posicion
    ]


    # ======================================
    # ÁRBOL
    #
    # Es obstáculo físico.
    # ======================================

    if tipo == ARBOL:

        return {
            "valor": 0,
            "tipo": "arbol",
            "posicion": posicion,
        }


    # ======================================
    # ARENA MOVEDIZA
    #
    # Es transitable físicamente, pero para
    # la memoria de caminos ART se considera
    # una zona peligrosa.
    # ======================================

    if tipo == ARENA:

        return {
            "valor": 0,
            "tipo": "arena",
            "posicion": posicion,
        }


    # ======================================
    # BAYAS
    #
    # Físicamente se puede caminar sobre
    # ellas, por lo que forman parte de un
    # camino posible.
    # ======================================

    if tipo in (
        BAYA_1,
        BAYA_2
    ):

        return {
            "valor": 1,
            "tipo": "baya",
            "posicion": posicion,
        }


    # ======================================
    # TERRENO LIBRE
    # ======================================

    return {
        "valor": 1,
        "tipo": "libre",
        "posicion": posicion,
    }


# ==========================================
# ANALIZAR ENTORNO COMPLETO
# ==========================================

def analizar_entorno(
    agente
):

    mundo = agente.mundo

    vecinos = posiciones_vecinas(
        agente.posicion
    )


    patron = []

    detalle = {}


    for nombre, _ in DIRECCIONES:

        posicion = vecinos[
            nombre
        ]


        informacion = analizar_casilla(
            mundo,
            posicion
        )


        patron.append(
            informacion[
                "valor"
            ]
        )


        detalle[
            nombre
        ] = informacion


    return {
        "patron": patron,
        "detalle": detalle,
    }


# ==========================================
# OBTENER SOLO LAS 4 ENTRADAS DE ART
# ==========================================

def patron_entorno(
    agente
):

    return analizar_entorno(
        agente
    )["patron"]