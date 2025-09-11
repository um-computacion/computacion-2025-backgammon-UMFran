import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def test_inicializacion(self):
        self.jugador = Player("Fran", "white")
        self.assertEqual(self.jugador.obtener_nombre(), "Fran")
        self.assertEqual(self.jugador.obtener_color(), "white")
        self.assertEqual(self.jugador.mostrar_fichas(), 15)

    def test_mostrar_fichas(self):
        self.jugador = Player("Fran", "white")
        self.assertEqual(self.jugador.mostrar_fichas(), 15)

    def test_ganar_false(self):
        self.jugador = Player("Fran", "white")
        self.assertFalse(self.jugador.ganar())

    def test_ganar_true(self):
        self.jugador = Player("Fran", "white")
        self.jugador.__fichas_restantes__ = 0
        self.assertTrue(self.jugador.ganar())

    def test_restar_ficha_valida(self):
        self.jugador = Player("Fran", "white")        
        self.jugador.__fichas_restantes__ = 3
        resultado = self.jugador.restar_ficha()
        self.assertTrue(resultado)
        self.assertEqual(self.jugador.mostrar_fichas(), 2)

    def test_restar_ficha_ultima(self):
        self.jugador = Player("Fran", "white")
        self.jugador.__fichas_restantes__ = 1
        resultado = self.jugador.restar_ficha()
        self.assertTrue(resultado)
        self.assertEqual(self.jugador.mostrar_fichas(), 0)
        self.assertTrue(self.jugador.ganar())

    def test_restar_ficha_sin_fichas(self):
        self.jugador = Player("Fran", "white")
        self.jugador.__fichas_restantes__ = 0
        resultado = self.jugador.restar_ficha()
        self.assertFalse(resultado)

    def test_str(self):
        self.jugador = Player("Fran", "white")
        esperado = "El jugador: Fran, tiene color: white y le quedan 15 fichas"
        self.assertEqual(str(self.jugador), esperado)
