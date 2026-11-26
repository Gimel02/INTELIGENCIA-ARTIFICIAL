import unittest

from Logica_Difusa import dios as modulo_dios
from Logica_Difusa.dios import Dios


def partida_tranquila():
    """Partida de DIOS sin Jaguar ni peleas, para aislar
    el ciclo de los cazadores."""

    dios = Dios()
    dios.guardar_aprendizaje = False
    dios.nueva_partida()

    dios.turno_jaguar = lambda dt: None
    dios.resolver_encuentro = lambda: None

    return dios


def avanzar(dios, condicion, dt=0.1, maximo=1500):

    for _ in range(maximo):

        if condicion():
            return True

        if not dios.paso(dt):
            break

    return condicion()


class TestCicloDios(unittest.TestCase):

    def test_turno_dios_no_depende_de_rodrigo_muerto(self):

        dios = partida_tranquila()

        dios.cazador.vidas = 0

        avanzar(
            dios,
            lambda: dios.turno_actual() >= 10,
            maximo=600
        )

        self.assertEqual(dios.cazador.turno, 0)
        self.assertGreaterEqual(dios.turno_actual(), 10)
        self.assertNotEqual(
            dios.turno_actual(),
            dios.cazador.turno
        )

    def test_gonzalo_no_decide_mientras_cuerpo_en_movimiento(self):

        dios = partida_tranquila()

        fallos = []

        for _, agente, cuerpo in dios.cazadores():

            original = agente.tomar_decision

            def envuelta(
                *args,
                _o=original,
                _a=agente,
                _c=cuerpo
            ):
                if not _c.en_reposo():
                    fallos.append(_a.nombre)

                return _o(*args)

            agente.tomar_decision = envuelta

        for _ in range(800):

            if not dios.paso(0.05):
                break

        self.assertEqual(fallos, [])

    def test_agotamiento_retira_o_activa_estado_agotado(self):

        dios = partida_tranquila()

        agente = dios.cazador
        cuerpo = dios.cuerpo_cazador

        lejos = avanzar(
            dios,
            lambda: agente.posicion != agente.campamento
        )

        self.assertTrue(lejos)

        # Mientras no llegue a su cabaña, la energía se
        # mantiene en 0 (así una baya en el camino no
        # cancela el estado de la prueba).
        vio_agotado = False
        llego_a_cabana = False
        recupero = False

        for _ in range(8000):

            if not llego_a_cabana:
                agente.energia = 0

            if not dios.paso(0.1):
                break

            if agente.agotado:
                vio_agotado = True

                self.assertGreater(agente.vidas, 0)
                self.assertNotIn("Murió", agente.estado)
                self.assertEqual(
                    cuerpo.factor_velocidad,
                    modulo_dios.FACTOR_VELOCIDAD_AGOTADO
                )

            if agente.posicion == agente.campamento:
                llego_a_cabana = True

            if (
                llego_a_cabana
                and agente.energia == agente.energia_max
            ):
                recupero = True
                break

        self.assertTrue(vio_agotado)
        self.assertTrue(llego_a_cabana)
        self.assertTrue(recupero)
        self.assertGreater(agente.vidas, 0)
        self.assertFalse(agente.agotado)
        self.assertEqual(cuerpo.factor_velocidad, 1.0)

    def test_refugio_jaguar_tiene_comportamiento_de_recuperacion_definido(self):

        dios = partida_tranquila()

        agente = dios.cazador

        agente.energia = 10
        agente.en_refugio_jaguar = True
        agente.tiempo_refugio_restante = 0.1

        dios.paso(0.2)

        self.assertFalse(agente.en_refugio_jaguar)
        self.assertEqual(agente.energia, agente.energia_max)

    def test_recuperacion_herido_termina_en_tiempo_esperado(self):

        dios = partida_tranquila()

        agente = dios.cazador

        agente.energia = 10
        agente.vidas = 1

        agente.recibir_herida_rival(
            modulo_dios.DURACION_RECUPERACION
        )

        dt = 0.25
        transcurrido = 0.0

        while agente.herido and transcurrido < 20:

            dios.paso(dt)
            transcurrido += dt

        self.assertFalse(agente.herido)
        self.assertLessEqual(
            transcurrido,
            modulo_dios.DURACION_RECUPERACION + 2 * dt
        )
        self.assertEqual(agente.energia, agente.energia_max)
        self.assertEqual(agente.vidas, agente.vidas_max)


if __name__ == "__main__":
    unittest.main()
