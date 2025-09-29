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

    @patch("builtins.print")
    def test_mostrar_home_con_fichas_blancas_y_negras(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__home__["white"].extend(["white", "white", "white"])
        self.juego.__board__.__home__["black"].extend(["black", "black"])
        self.interfaz.mostrar_home()
        mock_print.assert_any_call("\nFICHAS EN CASA:")
        mock_print.assert_any_call("  Blancas: 3")
        mock_print.assert_any_call("  Negras: 2")

    @patch("builtins.print")
    def test_mostrar_home_solo_fichas_blancas(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__home__["white"].extend(["white", "white", "white", "white"])
        self.interfaz.mostrar_home()
        mock_print.assert_any_call("\nFICHAS EN CASA:")
        mock_print.assert_any_call("  Blancas: 4")
        mock_print.assert_any_call("  Negras: 0")

    @patch("builtins.print")
    def test_mostrar_home_solo_fichas_negras(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__home__["black"].extend(["black", "black", "black", "black", "black"])
        self.interfaz.mostrar_home()
        mock_print.assert_any_call("\nFICHAS EN CASA:")
        mock_print.assert_any_call("  Blancas: 0")
        mock_print.assert_any_call("  Negras: 5")

    @patch("builtins.print")
    def test_mostrar_home_vacio(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__home__["white"].clear()
        self.juego.__board__.__home__["black"].clear()
        self.interfaz.mostrar_home()
        mock_print.assert_any_call("\nFICHAS EN CASA:")
        mock_print.assert_any_call("  Blancas: 0")
        mock_print.assert_any_call("  Negras: 0")

    @patch("builtins.print")
    def test_mostrar_home_todas_fichas_sacadas(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__board__.__home__["white"].extend(["white"] * 15)
        self.juego.__board__.__home__["black"].extend(["black"] * 8)
        self.interfaz.mostrar_home()
        mock_print.assert_any_call("\nFICHAS EN CASA:")
        mock_print.assert_any_call("  Blancas: 15")
        mock_print.assert_any_call("  Negras: 8")
    
    @patch("builtins.print")
    def test_movimientos_posibles_fichas_blancas_con_dados(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__turno__ = self.juego.__jugador1__  # jugador blanco
        self.juego.__dados__.__movimientos__ = [2, 3]

        for i in range(24):
            self.juego.mostrar_tablero()[i].clear()
        self.juego.mostrar_tablero()[5].append("white")
        
        self.interfaz.mostrar_movimientos_posibles()

        mock_print.assert_any_call("\nMovimientos posibles para white:")
        mock_print.assert_any_call("  5 → 7 (usando dado 2)")
        mock_print.assert_any_call("  5 → 8 (usando dado 3)")

    @patch("builtins.print")
    def test_movimientos_posibles_fichas_blancas_multiples_posiciones(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__turno__ = self.juego.__jugador1__
        self.juego.__dados__.__movimientos__ = [1]
        for i in range(24):
            self.juego.mostrar_tablero()[i].clear()
        self.juego.mostrar_tablero()[0].append("white")
        self.juego.mostrar_tablero()[10].extend(["white", "white"])
        
        self.interfaz.mostrar_movimientos_posibles()

        mock_print.assert_any_call("\nMovimientos posibles para white:")
        mock_print.assert_any_call("  0 → 1 (usando dado 1)")
        mock_print.assert_any_call("  10 → 11 (usando dado 1)")

    @patch("builtins.print")
    def test_movimientos_posibles_fichas_negras_con_dados(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__turno__ = self.juego.__jugador2__  # jugador negro
        self.juego.__dados__.__movimientos__ = [1, 4]

        for i in range(24):
            self.juego.mostrar_tablero()[i].clear()
        self.juego.mostrar_tablero()[20].append("black")
        
        self.interfaz.mostrar_movimientos_posibles()

        mock_print.assert_any_call("\nMovimientos posibles para black:")
        mock_print.assert_any_call("  20 → 19 (usando dado 1)")
        mock_print.assert_any_call("  20 → 16 (usando dado 4)")

    @patch("builtins.print")  
    def test_movimientos_posibles_fichas_negras_multiples_posiciones(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__turno__ = self.juego.__jugador2__
        self.juego.__dados__.__movimientos__ = [2]

        for i in range(24):
            self.juego.mostrar_tablero()[i].clear()
        self.juego.mostrar_tablero()[15].append("black")
        self.juego.mostrar_tablero()[23].extend(["black", "black"])
        
        self.interfaz.mostrar_movimientos_posibles()

        mock_print.assert_any_call("\nMovimientos posibles para black:")
        mock_print.assert_any_call("  15 → 13 (usando dado 2)")
        mock_print.assert_any_call("  23 → 21 (usando dado 2)")
    
    @patch("builtins.print")
    def test_movimientos_posibles_fichas_blancas_fuera_limite_superior(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__turno__ = self.juego.__jugador1__
        self.juego.__dados__.__movimientos__ = [5]

        for i in range(24):
            self.juego.mostrar_tablero()[i].clear()
        self.juego.mostrar_tablero()[22].append("white")  # 22 + 5 = 27 > 23
        
        self.interfaz.mostrar_movimientos_posibles()

        mock_print.assert_any_call("\nMovimientos posibles para white:") # No debe haber llamadas con "22 → 27"

    @patch("builtins.print")
    def test_movimientos_posibles_fichas_negras_fuera_limite_inferior(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__turno__ = self.juego.__jugador2__
        self.juego.__dados__.__movimientos__ = [3]

        for i in range(24):
            self.juego.mostrar_tablero()[i].clear()
        self.juego.mostrar_tablero()[1].append("black")  # 1 - 3 = -2 < 0
        
        self.interfaz.mostrar_movimientos_posibles()
        mock_print.assert_any_call("\nMovimientos posibles para black:") # No debe haber llamadas con "1 → -2"

    @patch("builtins.print")
    def test_mostrar_estado_basico(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__

        self.interfaz.mostrar_estado_completo()

        mock_print.assert_any_call("="*50)
        mock_print.assert_any_call("BACKGAMMON - Turno de: Fran")
        mock_print.assert_any_call("="*50)

    @patch("builtins.print")
    def test_mostrar_estado_llamadas_reales(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__

        self.juego.__dados__.__movimientos__ = [1, 2]
        self.juego.__board__.__banco__["white"].append("white")

        self.interfaz.mostrar_estado_completo()

        mock_print.assert_any_call("="*50)
        mock_print.assert_any_call("="*50)

    @patch("builtins.print")
    def test_mostrar_estado_con_fichas_en_home_y_banco(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__

        self.juego.__board__.__banco__["black"].append("black")
        self.juego.__board__.__home__["white"].append("white")

        self.interfaz.mostrar_estado_completo()
        mock_print.assert_any_call("="*50)
    
    @patch("builtins.input", side_effect=["9", "4"])  # Mostrar ganador y salir
    @patch("builtins.print")
    def test_menu_mostrar_ganador_jugador1(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        interfaz.__game__.__jugador1__.__fichas_restantes__ = 0
        interfaz.__game__.__jugador2__.__fichas_restantes__ = 5
        interfaz.jugar_turno()
        mock_print.assert_any_call("El ganador del juego es Fran")

    @patch("builtins.input", side_effect=["9", "4"])  # Mostrar ganador y salir
    @patch("builtins.print")
    def test_menu_mostrar_ganador_jugador2(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        interfaz.__game__.__jugador1__.__fichas_restantes__ = 5
        interfaz.__game__.__jugador2__.__fichas_restantes__ = 0
        interfaz.jugar_turno()
        mock_print.assert_any_call("El ganador del juego es Maria")

    @patch("builtins.input", side_effect=["9", "4"])  # Mostrar ganador y salir
    @patch("builtins.print")
    def test_menu_mostrar_ganador_sin_ganador(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        interfaz.__game__.__jugador1__.__fichas_restantes__ = 5
        interfaz.__game__.__jugador2__.__fichas_restantes__ = 5
        interfaz.jugar_turno()
        mock_print.assert_any_call("El juego no ha finalizado")

#===============================================================#

    def test_finalizar_turno(self):

        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__

        # Dejamos sin movimientos
        juego.__dados__.limpiar_dados()

        # Ejecutamos directamente
        juego.finalizar_turno()

        self.assertTrue(juego.__turno_finalizado__)
    
    @patch("builtins.input", side_effect=["1", "0", "1", "4"])
    def test_mover_ficha_valido(self, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        for i in range(24): # Limpiar tablero y dejar una sola ficha blanca
            juego.mostrar_tablero()[i].clear()
        juego.mostrar_tablero()[0].append("white")
        juego.__dados__.__movimientos__ = [1] # Forzamos dados a [1] para permitir movimiento 0 -> 1

        interfaz.jugar_turno()

        self.assertEqual(juego.mostrar_tablero()[0], [])
        self.assertIn("white", juego.mostrar_tablero()[1])

    @patch("builtins.input", side_effect=["1", "0", "3", "4"])
    @patch("builtins.print")
    def test_mover_ficha_dado_invalido(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        
        for i in range(24): # Limpiar tablero y poner ficha
            juego.mostrar_tablero()[i].clear()
        juego.mostrar_tablero()[0].append("white")
        juego.__dados__.__movimientos__ = [2]  # pero intentamos 0->3

        interfaz.jugar_turno()

        mock_print.assert_any_call("Error:", unittest.mock.ANY)

    @patch("builtins.input", side_effect=["2", "1", "4"])
    def test_reingresar_ficha_valido(self, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__board__.__banco__["white"].append("white") # Mandamos una ficha blanca al banco
        juego.__dados__.__movimientos__ = [2]  # destino=1 -> movimiento=2

        interfaz.jugar_turno()

        self.assertIn("white", juego.mostrar_tablero()[1])
        self.assertNotIn("white", juego.__board__.__banco__["white"])

    @patch("builtins.input", side_effect=["2", "1", "4"])
    @patch("builtins.print")
    def test_reingresar_ficha_sin_dado(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__board__.__banco__["white"].append("white")
        juego.__dados__.__movimientos__ = [5]  # distinto al necesario

        interfaz.jugar_turno()

        mock_print.assert_any_call("Error:", unittest.mock.ANY)

    @patch("builtins.input", side_effect=["3", "23", "4"])
    def test_sacar_ficha_valido(self, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        for i in range(24): # Limpiamos tablero y ponemos ficha blanca en 23
            juego.mostrar_tablero()[i].clear()
        juego.mostrar_tablero()[23].append("white")
        juego.__dados__.__movimientos__ = [1]  # origen=23 -> movimiento=1

        interfaz.jugar_turno()

        self.assertIn("white", juego.__board__.__home__["white"])
        self.assertEqual(juego.mostrar_tablero()[23], [])

    @patch("builtins.input", side_effect=["3", "0", "4"])
    @patch("builtins.print")
    def test_sacar_ficha_fuera_cuadrante(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        for i in range(24): # Poner ficha en casilla inicial
            juego.mostrar_tablero()[i].clear()
        juego.mostrar_tablero()[0].append("white")
        juego.__dados__.__movimientos__ = [6]

        interfaz.jugar_turno()

        mock_print.assert_any_call("Error:", unittest.mock.ANY)

    @patch("builtins.input", side_effect=["99", "4"])
    @patch("builtins.print")
    def test_opcion_invalida(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        interfaz.jugar_turno()
        mock_print.assert_any_call("Opción inválida.")

if __name__ == "__main__":
    unittest.main()