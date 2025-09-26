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

    @patch("builtins.print")
    def test_mostrar_banco_con_fichas_blancas_y_negras(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__banco__["white"].extend(["white", "white"])
        self.juego.__board__.__banco__["black"].extend(["black", "black", "black"])
        
        self.interfaz.mostrar_banco()
        
        mock_print.assert_any_call("\nFICHAS CAPTURADAS:")
        mock_print.assert_any_call("  Blancas: 2")
        mock_print.assert_any_call("  Negras: 3")

    @patch("builtins.print")
    def test_mostrar_banco_solo_fichas_blancas(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__banco__["white"].extend(["white", "white", "white"])
        self.interfaz.mostrar_banco()
        mock_print.assert_any_call("\nFICHAS CAPTURADAS:")
        mock_print.assert_any_call("  Blancas: 3")
        mock_print.assert_any_call("  Negras: 0")

    @patch("builtins.print")
    def test_mostrar_banco_solo_fichas_negras(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__banco__["black"].extend(["black"])
        self.interfaz.mostrar_banco()
        mock_print.assert_any_call("\nFICHAS CAPTURADAS:")
        mock_print.assert_any_call("  Blancas: 0")
        mock_print.assert_any_call("  Negras: 1")

    @patch("builtins.print")
    def test_mostrar_banco_vacio(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__banco__["white"].clear()
        self.juego.__board__.__banco__["black"].clear()
        self.interfaz.mostrar_banco()
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_mostrar_banco_muchas_fichas(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__banco__["white"].extend(["white"] * 10)
        self.juego.__board__.__banco__["black"].extend(["black"] * 15)
        self.interfaz.mostrar_banco()
        mock_print.assert_any_call("\nFICHAS CAPTURADAS:")
        mock_print.assert_any_call("  Blancas: 10")
        mock_print.assert_any_call("  Negras: 15")

    @patch("builtins.input", side_effect=["4"])  
    def test_finalizar_turno(self, mock_input):
        """Debe finalizar turno con la opción 4"""
        self.interfaz = cli("Fran", "Maria")
        self.interfaz.jugar_turno()
        self.assertTrue(self.interfaz.__game__.__turno_finalizado__)

    @patch("builtins.input", side_effect=["1", "0", "1", "4"])
    def test_mover_ficha_valido(self, mock_input):
        """Debe mover una ficha usando un dado válido"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        # Forzamos dados a [1] para permitir movimiento 0 -> 1
        juego.__dados__.__movimientos__ = [1]

        self.interfaz.jugar_turno()

        # La casilla 0 pierde una ficha blanca
        self.assertLess(len(juego.mostrar_tablero()[0]), 2)
        # La casilla 1 recibe una ficha blanca
        self.assertIn("white", juego.mostrar_tablero()[1])

    @patch("builtins.input", side_effect=["2", "1", "4"])
    def test_reingresar_ficha_valido(self, mock_input):
        """Debe reingresar una ficha desde el banco"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        # Mandamos una ficha blanca al banco
        juego.__board__.__banco__["white"].append("white")
        juego.__dados__.__movimientos__ = [2]  # destino=1 -> movimiento=2

        self.interfaz.jugar_turno()

        self.assertIn("white", juego.mostrar_tablero()[1])
        self.assertNotIn("white", juego.__board__.__banco__["white"])

    @patch("builtins.input", side_effect=["3", "11", "4"])
    def test_sacar_ficha_valido(self, mock_input):
        """Debe poder sacar ficha blanca desde cuadrante final"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        # Forzamos dados
        juego.__dados__.__movimientos__ = [13]  # origen=11 -> movimiento=13
        # Ponemos fichas blancas solo en cuadrante final
        for i in range(24):
            juego.mostrar_tablero()[i].clear()
        juego.mostrar_tablero()[23].append("white")
        juego.__dados__.__movimientos__ = [1]  # origen=23 -> movimiento=1

        self.interfaz.jugar_turno()

        self.assertIn("white", juego.__board__.__home__["white"])
        self.assertEqual(juego.mostrar_tablero()[11], [])
    
    @patch("builtins.input", side_effect=["4"])  
    def test_finalizar_turno(self, mock_input):
        """Debe finalizar turno con la opción 4"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        juego.__dados__.limpiar_dados()
        juego.finalizar_turno()
        self.assertTrue(juego.__turno_finalizado__)

    @patch("builtins.input", side_effect=["1", "0", "1", "4"])
    def test_mover_ficha_valido(self, mock_input):
        """Debe mover una ficha usando un dado válido"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        juego.__dados__.__movimientos__ = [1]
        self.interfaz.jugar_turno()
        self.assertIn("white", juego.mostrar_tablero()[1])

    @patch("builtins.input", side_effect=["1", "0", "3", "4"])  # opción mover -> origen 0 -> destino 3 -> finalizar
    @patch("builtins.print")
    def test_mover_ficha_dado_invalido(self, mock_print, mock_input):
        self.interfaz = cli("Fran", "Maria")
        self.interfaz.jugar_turno()
        mock_print.assert_any_call("Error:", unittest.mock.ANY)

    @patch("builtins.input", side_effect=["2", "1", "4"])  # opción 2 -> destino 1 -> finalizar
    @patch("builtins.print")
    def test_reingresar_ficha_valido(self, mock_print, mock_input):
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        juego.__board__.__banco__["white"].append("white")
        juego.__dados__.__movimientos__ = [2]

        self.interfaz.jugar_turno()
        self.assertIn("white", juego.mostrar_tablero()[1])

    @patch("builtins.input", side_effect=["2", "1", "4"])
    def test_reingresar_ficha_sin_dado(self, mock_input):
        """Debe fallar si no hay un dado válido para reingresar"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        juego.__board__.__banco__["white"].append("white")
        juego.__dados__.__movimientos__ = [5]  # distinto
        with patch("builtins.print") as mock_print:
            self.interfaz.jugar_turno()
            mock_print.assert_any_call("Error:", unittest.mock.ANY)

    @patch("builtins.input", side_effect=["3", "23", "4"])  # opción 3 -> origen 23 -> finalizar
    @patch("builtins.print")
    def test_sacar_ficha_valido(self, mock_print, mock_input):
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        for i in range(24):
            juego.mostrar_tablero()[i].clear()
        juego.mostrar_tablero()[23].append("white")
        juego.__dados__.__movimientos__ = [1]
        self.interfaz.jugar_turno()
        self.assertIn("white", juego.__board__.__home__["white"])

    @patch("builtins.input", side_effect=["3", "0", "4"])
    def test_sacar_ficha_fuera_cuadrante(self, mock_input):
        """Debe fallar al intentar sacar ficha que no está en cuadrante final"""
        self.interfaz = cli("Fran", "Maria")
        juego = self.interfaz.__game__
        juego.__dados__.__movimientos__ = [24]
        juego.mostrar_tablero()[0].append("white")
        with patch("builtins.print") as mock_print:
            self.interfaz.jugar_turno()
            mock_print.assert_any_call("Error:", unittest.mock.ANY)

    @patch("builtins.input", side_effect=["9", "4"])
    def test_opcion_invalida(self, mock_input):
        """Debe imprimir error si la opción no existe"""
        self.interfaz = cli("Fran", "Maria")
        with patch("builtins.print") as mock_print:
            self.interfaz.jugar_turno()
            mock_print.assert_any_call("Opción inválida.")