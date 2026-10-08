# ==========================================
# PERSONALIDAD DEL AGENTE CAZADOR
# ==========================================


class PersonalidadCazador:

    def __init__(self):

        # Nombre del perfil
        self.nombre = "Estratégico"


        # ======================================
        # RASGOS DE PERSONALIDAD
        #
        # Valores entre 0.0 y 1.0
        # ======================================

        # Qué tanto busca acercarse al Jaguar
        self.agresividad = 0.80

        # Qué tanto evita obstáculos y riesgos
        self.precaucion = 0.90

        # Qué tanto favorece explorar zonas nuevas
        self.exploracion = 0.60

        # Qué tanto intenta conservar energía
        self.ahorro_energia = 0.70


    def obtener_descripcion(self):

        return (
            "Cazador estratégico: persigue activamente "
            "al objetivo, pero prioriza rutas seguras, "
            "evita riesgos innecesarios y adapta sus "
            "decisiones al entorno."
        )


    def obtener_rasgos(self):

        return {
            "agresividad": self.agresividad,
            "precaucion": self.precaucion,
            "exploracion": self.exploracion,
            "ahorro_energia": self.ahorro_energia
        }