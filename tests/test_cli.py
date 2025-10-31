import unittest
from unittest.mock import patch, ANY
from cli.cli import cli
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
        self.assertIn(("Turno:", "Fran"), [args[0] for args in llamadas if args])
        # verificamos que se imprimieron los separadores
        self.assertIn(("=====================================",), [args[0] for args in llamadas if args])
        # verificamos que se imprimieron los dados
        self.assertTrue(any("Dados disponibles:" in str(a) for a in [args[0] for args in llamadas if args]))

    @patch("random.randint", side_effect=[6, 3])  # otra tirada
    @patch("builtins.print")
    def test_mostrar_juego_otro_dado(self, mock_print, mock_randint):
        interfaz = cli("Fran", "Maria")
        interfaz.mostrar_juego()

        llamadas = mock_print.call_args_list

        # turno y jugador
        self.assertIn(("Turno:", "Fran"), [args[0] for args in llamadas if args])
        # separador al inicio
        self.assertEqual(("=====================================",), llamadas[0][0])
        # dados disponibles
        self.assertTrue(any("Dados disponibles:" in str(a) for a in [args[0] for args in llamadas if args]))

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
        # --- CORREGIDO: El método ahora no imprime nada si ambos están vacíos ---
        mock_print.assert_not_called()
        # --- FIN CORRECCIÓN ---

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
        # No debe haber llamadas con "22 → 27"
        call_strings = [str(call[0]) for call in mock_print.call_args_list]
        self.assertFalse(any("22 → 27" in s for s in call_strings))


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
        # No debe haber llamadas con "1 → -2"
        call_strings = [str(call[0]) for call in mock_print.call_args_list]
        self.assertFalse(any("1 → -2" in s for s in call_strings))

    @patch("builtins.print")
    def test_mostrar_estado_basico(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.interfaz.mostrar_estado_completo()
        mock_print.assert_any_call("="*50)
        mock_print.assert_any_call("BACKGAMMON - Turno de: Fran")

    @patch("builtins.print")
    def test_mostrar_estado_llamadas_reales(self, mock_print):
        self.interfaz = cli("Fran", "Maria")
        self.juego = self.interfaz.__game__
        self.juego.__dados__.__movimientos__ = [1, 2]
        self.juego.__board__.__banco__["white"].append("white")
        self.interfaz.mostrar_estado_completo()
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
        # --- CORREGIDO: Simular un estado de juego terminado ---
        interfaz.__game__.__jugador1__.__fichas_restantes__ = 0
        interfaz.__game__.__juego_terminado__ = True # Añadir esto
        # --- FIN CORRECCIÓN ---
        interfaz.jugar_turno()
        mock_print.assert_any_call("El ganador del juego es Fran")

    @patch("builtins.input", side_effect=["9", "4"])  # Mostrar ganador y salir
    @patch("builtins.print")
    def test_menu_mostrar_ganador_jugador2(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        # --- CORREGIDO: Simular un estado de juego terminado ---
        interfaz.__game__.__jugador1__.__fichas_restantes__ = 5
        interfaz.__game__.__jugador2__.__fichas_restantes__ = 0
        interfaz.__game__.__juego_terminado__ = True # Añadir esto
        # --- FIN CORRECCIÓN ---
        interfaz.jugar_turno()
        mock_print.assert_any_call("El ganador del juego es Maria")

    @patch("builtins.input", side_effect=["9", "4"])  # Mostrar ganador y salir
    @patch("builtins.print")
    def test_menu_mostrar_ganador_sin_ganador(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        interfaz.__game__.__jugador1__.__fichas_restantes__ = 5
        interfaz.__game__.__jugador2__.__fichas_restantes__ = 5
        # juego_terminado es False por defecto
        interfaz.jugar_turno()
        mock_print.assert_any_call("El juego no ha finalizado")
    
    @patch("builtins.input", side_effect=["10", "Nuevo1", "Nuevo2", "4"])
    @patch("builtins.print")
    def test_menu_reiniciar_juego(self, mock_print, mock_input):
        """Debe reiniciar el juego y pedir nuevamente los nombres"""
        interfaz = cli("Fran", "Maria")
        interfaz.jugar_turno()
        mock_print.assert_any_call("El juego se reinició")
        self.assertEqual(interfaz.__game__.__jugador1__.__nombre__, "Nuevo1")
        self.assertEqual(interfaz.__game__.__jugador2__.__nombre__, "Nuevo2")

    @patch("builtins.input", side_effect=["4"]) # Opción 4: Finalizar turno
    def test_finalizar_turno(self, mock_input):
        # --- CORREGIDO ---
        # El test original probaba un detalle de implementación obsoleto.
        # Ahora probamos que el turno realmente cambia.
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__dados__.limpiar_dados() # Sin dados, finalizar es válido
        
        turno_inicial = juego.mostrar_turno()
        self.assertEqual(turno_inicial, "Fran")
        
        interfaz.jugar_turno() # Esto llamará a finalizar_turno()
        
        turno_final = juego.mostrar_turno()
        self.assertNotEqual(turno_inicial, turno_final)
        self.assertEqual(turno_final, "Maria")
        # --- FIN CORRECCIÓN ---
    
    @patch("builtins.input", side_effect=["1", "0", "1", "4"]) # Mover 0->1, Salir
    @patch.object(backgammongame, 'mover') # Mockear el método mover
    def test_mover_ficha_valido(self, mock_mover, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__dados__.__movimientos__ = [1] # Forzamos dados
        
        interfaz.jugar_turno()

        # Probamos que la CLI llamó a la lógica del juego con los params correctos
        mock_mover.assert_called_with(0, 1)

    @patch("builtins.input", side_effect=["1", "0", "3", "4"]) # Mover 0->3, Salir
    @patch("builtins.print")
    def test_mover_ficha_dado_invalido(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__dados__.__movimientos__ = [2]  # Dado 2
        
        interfaz.jugar_turno()
        # Debería fallar porque el dado 3 no está (movimiento = abs(3-0))
        mock_print.assert_any_call("Error:", ANY) # ANY matchea cualquier ValueError

    @patch("builtins.input", side_effect=["2", "1", "4"]) # Reingresar a 1, Salir
    @patch.object(backgammongame, 'reingresar_ficha')
    def test_reingresar_ficha_valido(self, mock_reingresar, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__board__.__banco__["white"].append("white")
        juego.__dados__.__movimientos__ = [2]  # destino=1 -> movimiento=2
        
        interfaz.jugar_turno()
        
        # Probamos que la CLI llamó a la lógica del juego
        mock_reingresar.assert_called_with(1)

    @patch("builtins.input", side_effect=["2", "1", "4"]) # Reingresar a 1, Salir
    @patch("builtins.print")
    def test_reingresar_ficha_sin_dado(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        juego.__board__.__banco__["white"].append("white")
        juego.__dados__.__movimientos__ = [5]  # Dado 5 (no 2)
        
        interfaz.jugar_turno()
        mock_print.assert_any_call("Error:", ANY)

    @patch("builtins.input", side_effect=["3", "23", "4"]) # Sacar de 23, Salir
    @patch.object(backgammongame, 'sacar')
    def test_sacar_ficha_valido(self, mock_sacar, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        # Simular estado válido para sacar
        self.setup_sacar_valido(juego, "white", 23)
        juego.__dados__.__movimientos__ = [1]  # origen=23 -> movimiento=1
        
        interfaz.jugar_turno()
        mock_sacar.assert_called_with(23)

    # Helper para tests de sacar
    def setup_sacar_valido(self, juego, color, origen):
         for i in range(24):
            juego.mostrar_tablero()[i].clear()
         if color == "white":
             juego.mostrar_tablero()[origen] = ["white"]
         else:
             juego.__turno__ = juego.__jugador2__
             juego.mostrar_tablero()[origen] = ["black"]


    @patch("builtins.input", side_effect=["3", "0", "4"]) # Sacar de 0, Salir
    @patch("builtins.print")
    def test_sacar_ficha_fuera_cuadrante(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        juego = interfaz.__game__
        # Poner ficha en casilla 0 (fuera de cuadrante 18-23)
        self.setup_sacar_valido(juego, "white", 0)
        juego.__dados__.__movimientos__ = [6]
        
        interfaz.jugar_turno()
        mock_print.assert_any_call("Error:", ANY)

    @patch("builtins.input", side_effect=["99", "4"]) # Opción inválida, Salir
    @patch("builtins.print")
    def test_opcion_invalida(self, mock_print, mock_input):
        interfaz = cli("Fran", "Maria")
        interfaz.jugar_turno()
        mock_print.assert_any_call("Opción inválida.")

if __name__ == "__main__":
    unittest.main()