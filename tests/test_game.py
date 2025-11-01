from core.backgammongame import BackgammonGame
from core.board import Board
from core.dice import Dice
from core.player import Player
from unittest.mock import patch
import unittest

class TestBackgammonGameBasico(unittest.TestCase):

    def test_inicializacion(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.assertIsInstance(self.game.__board__, Board)
        self.assertIsInstance(self.game.__dados__, Dice)
        self.assertIsInstance(self.game.__jugador1__, Player)
        self.assertIsInstance(self.game.__jugador2__, Player)
        jugadores = self.game.__jugadores__
        self.assertIn(self.game.mostrar_jugador1(), jugadores)
        self.assertIn(self.game.mostrar_jugador2(), jugadores)
        self.assertEqual(len(jugadores), 2)
        self.assertEqual(self.game.__jugador1__.obtener_nombre(), "Fran")
        self.assertEqual(self.game.__jugador1__.obtener_color(), "white")
        self.assertEqual(self.game.__jugador2__.obtener_nombre(), "Maria")
        self.assertEqual(self.game.__jugador2__.obtener_color(), "black")
        self.assertEqual(self.game.__turno__.obtener_nombre(), "Fran")
        self.assertFalse(self.game.__turno_finalizado__)

    def test_mostrar_jugador1(self):
        self.game = BackgammonGame("Fran", "Maria")
        jugador1 = self.game.mostrar_jugador1()
        self.assertIsInstance(jugador1, Player)
        self.assertEqual(jugador1.obtener_nombre(), "Fran")
        self.assertEqual(jugador1.obtener_color(), "white")

    def test_mostrar_jugador2(self):
        self.game = BackgammonGame("Fran", "Maria")
        jugador2 = self.game.mostrar_jugador2()
        self.assertIsInstance(jugador2, Player)
        self.assertEqual(jugador2.obtener_nombre(), "Maria")
        self.assertEqual(jugador2.obtener_color(), "black")

    def test_mostrar_turno(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.assertEqual(self.game.mostrar_turno(), "Fran")
    
    def test_mostrar_tablero(self):
        self.game = BackgammonGame("Fran", "Maria")
        tablero_lista = self.game.mostrar_tablero()
        self.assertIsInstance(tablero_lista, list)
        self.assertEqual(len(tablero_lista), 24)
        self.assertIs(tablero_lista, self.game.__board__.__contenedor__)
    
    def test_cambiar_turno_rama_if(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.cambiar_turno()
        self.assertEqual(self.game.mostrar_turno(), "Maria")

    def test_cambiar_turno_rama_else(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.cambiar_turno()
        self.assertEqual(self.game.mostrar_turno(), "Fran")

    @patch("random.randint", side_effect=[3, 5])
    def test_iniciar_turno(self, mock_randint):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.tirar_dados()
        dados = self.game.__dados__.get_dados()
        self.assertEqual(dados, [3, 5])

    def test_cambiar_turno(self):
        self.game = BackgammonGame("Fran", "Maria")
        turno_inicial = self.game.__turno__
        self.game.cambiar_turno()
        if turno_inicial == self.game.__jugador1__:
            self.assertEqual(self.game.__turno__.obtener_nombre(), "Maria")
        else:
            self.assertEqual(self.game.__turno__.obtener_nombre(), "Fran")
    
    def test_juego_no_terminado_al_inicio(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.assertFalse(self.game.juego_terminado())
        self.assertIsNone(self.game.ganador())

    def test_gana_jugador1(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__jugador1__.__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado()) 
        self.assertEqual(self.game.ganador(), "Fran")

    def test_gana_jugador2(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__jugador2__.__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.ganador(), "Maria")

    def test_empate_o_inconsistencia(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__jugador1__.__fichas_restantes__ = 5
        self.game.__jugador2__.__fichas_restantes__ = 5
        self.assertFalse(self.game.juego_terminado())
        self.assertIsNone(self.game.ganador())

    @patch("random.randint", side_effect=[3, 5])
    def test_tirar_dados(self, mock_randint):
        self.game = BackgammonGame("Fran", "Maria")
        dados = self.game.tirar_dados()
        self.assertEqual(dados, [3, 5])
        self.assertTrue(all(1 <= d <= 6 for d in dados))

    @patch("random.randint", side_effect=[2, 2])
    def test_tirar_dados_dobles(self, mock_randint):
        self.game = BackgammonGame("Fran", "Maria")
        dados = self.game.tirar_dados()
        self.assertEqual(dados, [2, 2, 2, 2])

    def test_mover_valido(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [3]
        origen, destino = 0, 3
        self.game.__board__.__contenedor__[0] = ["white"]
        self.game.mover(origen, destino)
        self.assertIn("white", self.game.__board__.__contenedor__[3])

    def test_mover_invalido_lanza_error(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [2]
        with self.assertRaises(ValueError):
            self.game.mover(0, 3)

    def test_reingresar_valido(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [2]
        self.game.__turno__ = self.game.__jugador1__
        self.game.__board__.__barra__["white"] = ["white"]
        self.game.reingresar_ficha(1)
        self.assertIn("white", self.game.__board__.__contenedor__[1])

    def test_reingresar_invalido(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [5]
        with self.assertRaises(ValueError):
            self.game.reingresar_ficha(1)

    def test_sacar_valido(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [6]
        self.game.__turno__ = self.game.__jugador2__
        self.game.__board__.__contenedor__ = [[] for _ in range(24)]
        self.game.__board__.__contenedor__[5] = ["black"]
        resultado = self.game.sacar(5)
        self.assertTrue(resultado)
        self.assertIn("black", self.game.__board__.__afuera__["black"])

    def test_sacar_fuera_cuadrante(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [6]
        self.game.__turno__ = self.game.__jugador1__
        self.game.__board__.__contenedor__[0] = ["white"]
        with self.assertRaisesRegex(ValueError, "aún tienes fichas fuera"):
            self.game.sacar(19)

    def test_finalizar_turno_con_dados(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [3]
        self.game.finalizar_turno()
        self.assertEqual(self.game.mostrar_turno(), "Maria")
        self.assertFalse(self.game.__dados__.hay_movimientos())

    def test_finalizar_turno_sin_dados(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = []
        self.game.finalizar_turno()
        self.assertEqual(self.game.mostrar_turno(), "Maria")
        self.assertFalse(self.game.__turno_finalizado__)

    def test_estado_turno(self):
        self.game = BackgammonGame("Fran", "Maria")
        estado = self.game.estado_turno()
        self.assertIsInstance(estado, set)
        self.assertTrue(any("Fichas" in s for s in estado))

    def test_tirar_dados_con_dados_existentes(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [1, 2]
        dados_nuevos = self.game.tirar_dados()
        self.assertEqual(dados_nuevos, [1, 2])

    def test_mover_direccion_invalida_white(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__dados__.__movimientos__ = [3]
        self.game.__board__.__contenedor__[5] = ["white"]
        with self.assertRaisesRegex(ValueError, "fichas 'white' solo avanzan"):
            self.game.mover(5, 2)
        self.assertIn(3, self.game.__dados__.get_dados())

    def test_mover_direccion_invalida_black(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.__dados__.__movimientos__ = [3]
        self.game.__board__.__contenedor__[10] = ["black"]
        with self.assertRaisesRegex(ValueError, "fichas 'black' solo retroceden"):
            self.game.mover(10, 13)
        self.assertIn(3, self.game.__dados__.get_dados())

    def test_reingresar_ficha_valido_black(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.__board__.__barra__["black"].append("black")
        self.game.__dados__.__movimientos__ = [2]
        self.game.__board__.__contenedor__[22] = []
        self.game.reingresar_ficha(22)
        self.assertEqual(self.game.__board__.get_barra("black"), [])
        self.assertIn("black", self.game.__board__.__contenedor__[22])
        self.assertEqual(self.game.__dados__.get_dados(), [])

    def test_sacar_ficha_valida_white(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__ = [[] for _ in range(24)]
        self.game.__board__.__contenedor__[23] = ["white"]
        self.game.__dados__.__movimientos__ = [1, 5]
        resultado = self.game.sacar(23)
        self.assertTrue(resultado)
        self.assertEqual(self.game.__board__.get_afuera("white"), ["white"])
        self.assertEqual(self.game.__dados__.get_dados(), [5])

    def test_sacar_ficha_fichas_fuera_cuadrante_black(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.__board__.__contenedor__[10] = ["black"]
        self.game.__board__.__contenedor__[5] = ["black"]
        self.game.__dados__.__movimientos__ = [6]
        with self.assertRaisesRegex(ValueError, "aún tienes fichas fuera"):
            self.game.sacar(5)
        self.assertEqual(self.game.__dados__.get_dados(), [6])

    # --- INICIO DE LA CORRECCIÓN ---
    def test_sacar_ficha_dado_invalido_white(self):
        # Prueba que NO se puede sacar si el dado es muy PEQUEÑO
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__ = [[] for _ in range(24)] # Limpiar tablero
        self.game.__board__.__contenedor__[20] = ["white"] # Poner en zona 18-23
        self.game.__dados__.__movimientos__ = [3, 2] # Dados 3 y 2, necesita 4 (24-20)
        
        # Debe fallar porque no tiene 4 o más
        with self.assertRaisesRegex(ValueError, "No tienes dado"):
            self.game.sacar(20)
        self.assertEqual(self.game.__dados__.get_dados(), [3, 2])
    # --- FIN DE LA CORRECCIÓN ---

    # --- INICIO DE LA CORRECCIÓN ---
    def test_sacar_ficha_con_dado_mayor_valido(self):
        # Prueba que se PUEDE sacar con un dado mayor (5) si es la ficha más lejana (20)
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__ = [[] for _ in range(24)]
        self.game.__board__.__contenedor__[20] = ["white"] # Ficha más lejana (necesita 4)
        self.game.__board__.__contenedor__[22] = ["white"] # Otra ficha (no es la más lejana)
        self.game.__dados__.__movimientos__ = [5] # Dado 5 (mayor que 4)
        
        # Debe fallar porque la ficha en 20 NO es la más lejana
        # (la ficha más lejana es la de índice MENOR, 18, 19... 20 no es la más lejana si hay en 22)
        # La lógica de "más lejana" en el juego es: ¿Hay fichas en casillas ANTERIORES?
        # Para white, anteriores a 20 son 18, 19. Como no hay, 20 SÍ es la más lejana.
        # EL TEST ESTABA MAL PLANTEADO.
        
        # Este test prueba que NO se puede usar un dado mayor si NO es la más lejana
        self.game.__board__.__contenedor__[19] = ["white"] # Esta es más lejana
        with self.assertRaisesRegex(ValueError, "No tienes dado"):
            self.game.sacar(20) # No puede usar el 5 en la 20, porque la 19 existe
        self.assertEqual(self.game.__dados__.get_dados(), [5])
    # --- FIN DE LA CORRECCIÓN ---

    def test_sacar_ficha_con_dado_mayor_valido_real(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__ = [[] for _ in range(24)]
        self.game.__board__.__contenedor__[20] = ["white"] # Ficha más lejana (necesita 4)
        self.game.__dados__.__movimientos__ = [5, 6]
        resultado = self.game.sacar(20)
        self.assertTrue(resultado)
        self.assertEqual(self.game.__board__.get_afuera("white"), ["white"])
        self.assertEqual(self.game.__dados__.get_dados(), [6])

    def test_sacar_ficha_con_dado_mayor_invalido_no_lejana(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__ = [[] for _ in range(24)]
        self.game.__board__.__contenedor__[19] = ["white"]
        self.game.__board__.__contenedor__[20] = ["white"]
        self.game.__dados__.__movimientos__ = [5]
        with self.assertRaisesRegex(ValueError, "No tienes dado"):
            self.game.sacar(20)
        self.assertEqual(self.game.__dados__.get_dados(), [5])

    def test_get_valid_moves_banco_vacio(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__barra__["white"] = []
        moves = self.game.get_valid_moves('bar', [1, 2])
        self.assertEqual(moves, [])

    def test_get_valid_moves_banco_con_fichas_white(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__barra__["white"].append("white")
        self.game.__board__.__contenedor__[0] = ["black", "black"]
        self.game.__board__.__contenedor__[2] = []
        self.game.__board__.__contenedor__[4] = ["black"]
        moves = self.game.get_valid_moves('bar', [1, 3, 5])
        self.assertCountEqual(moves, [2, 4])

    def test_get_valid_moves_banco_con_fichas_black(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.__board__.__barra__["black"].append("black")
        self.game.__board__.__contenedor__[23] = []
        self.game.__board__.__contenedor__[22] = ["black"]
        self.game.__board__.__contenedor__[20] = ["white", "white"]
        # --- CORREGIDO: Typo 1.2 -> 1, 2 ---
        moves = self.game.get_valid_moves('bar', [1, 2, 4])
        self.assertCountEqual(moves, [23, 22])
        
    def test_get_valid_moves_normal_white(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__[1] = []
        self.game.__board__.__contenedor__[3] = ["black", "black"]
        # --- CORREGIDO: Typo 1.3 -> 1, 3 ---
        moves = self.game.get_valid_moves(0, [1, 3])
        self.assertEqual(moves, [1])

    def test_get_valid_moves_normal_black(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.__board__.__contenedor__[21] = ["white"]
        self.game.__board__.__contenedor__[19] = ["black", "black"]
        moves = self.game.get_valid_moves(23, [2, 4])
        self.assertCountEqual(moves, [21, 19])

    def test_get_valid_moves_origen_invalido(self):
        self.game = BackgammonGame("Fran", "Maria")
        self.game.__board__.__contenedor__[2] = []
        moves = self.game.get_valid_moves(2, [1, 3])
        self.assertEqual(moves, [])
        self.game.__board__.__contenedor__[5] = ["black"]
        moves = self.game.get_valid_moves(5, [1, 3])
        self.assertEqual(moves, [])

if __name__ == "__main__":
    unittest.main()