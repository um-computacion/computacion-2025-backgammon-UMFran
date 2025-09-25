import unittest
from unittest.mock import patch
from core.cli import cli
from core.backgammongame import backgammongame

class TestCLI(unittest.TestCase):

    def test_inicializacion(self):
        interfaz = cli("Fran", "Maria")
        self.assertIsInstance(interfaz.game, backgammongame)
        self.assertEqual(interfaz.game.mostrar_turno(), "Fran")

    @patch("builtins.input", side_effect=["Fran", "Maria"])
    def test_inicar_juego(self, mock_input):
        interfaz = cli("Temp1", "Temp2")
        interfaz.inicar_juego()
        self.assertIsInstance(interfaz.game, backgammongame)
        self.assertEqual(interfaz.game.mostrar_jugador1().obtener_nombre(), "Fran")
        self.assertEqual(interfaz.game.mostrar_jugador2().obtener_nombre(), "Maria")