import unittest
from unittest.mock import patch
from core.cli import cli
from core.backgammongame import backgammongame

class TestCLI(unittest.TestCase):

    def test_inicializacion(self):
        interfaz = cli("Fran", "Maria")
        self.assertIsInstance(interfaz.__game__, backgammongame)
        self.assertEqual(interfaz.__game__.mostrar_turno(), "Fran")

    @patch("builtins.input", side_effect=["Fran", "Maria"])
    def test_inicar_juego(self, mock_input):
        interfaz = cli("Temp1", "Temp2")
        interfaz.inicar_juego()
        self.assertIsInstance(interfaz.__game__, backgammongame)
        self.assertEqual(interfaz.__game__.mostrar_jugador1().obtener_nombre(), "Fran")
        self.assertEqual(interfaz.__game__.mostrar_jugador2().obtener_nombre(), "Maria")
    
    @patch("random.randint", side_effect=[2, 5])  # simulamos tirada de dados
    @patch("builtins.print")
    def test_mostrar_juego_basico(self, mock_print, mock_randint):
        interfaz = cli("Fran", "Maria")
        interfaz.mostrar_juego()

        llamadas = mock_print.call_args_list

        # verificamos que se imprimió el turno correcto
        self.assertIn(("Turno:", "Fran"), [args[0] for args in llamadas])
        # verificamos que se imprimieron los separadores
        self.assertIn(("=====================================",), [args[0] for args in llamadas])
        # verificamos que se imprimieron los dados
        self.assertTrue(any("Dados disponibles:" in str(a) for a in [args[0] for args in llamadas]))

    @patch("random.randint", side_effect=[6, 3])  # otra tirada
    @patch("builtins.print")
    def test_mostrar_juego_otro_dado(self, mock_print, mock_randint):
        interfaz = cli("Fran", "Maria")
        interfaz.mostrar_juego()

        llamadas = mock_print.call_args_list

        # turno y jugador
        self.assertIn(("Turno:", "Fran"), [args[0] for args in llamadas])
        # separador al inicio
        self.assertEqual(("=====================================",), llamadas[0][0])
        # dados disponibles
        self.assertTrue(any("Dados disponibles:" in str(a) for a in [args[0] for args in llamadas]))