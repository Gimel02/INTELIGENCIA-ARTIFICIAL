# ==========================================
# LÓGICA DIFUSA (MÉTODO DE MAMDANI)
#
# Este paquete es el que "mueve los hilos"
# del cazador: decide QUÉ hacer en cada turno
# (huir, recargar, explorar, perseguir o
# atacar).
#
# Archivos:
#   funciones_membresia.py  grado, grado inversa,
#                           triangular, trapezoidal
#   operadores.py           AND, OR, NOT,
#                           implicación y AGG
#   variables.py            variables lingüísticas
#   base_conocimiento.py    reglas IF-THEN y su
#                           carga/guardado (JSON)
#   motor_mamdani.py        fuzzificación,
#                           inferencia y centroide
#   dios.py                 orquestador de agentes
#   simulador.py            partidas sin ventana
#                           las reglas
# ==========================================
