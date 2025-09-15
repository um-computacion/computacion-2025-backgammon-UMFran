from core.backgammongame import backgammongame
from core.board import Board
from core.dice import dice
from core.player import Player
from unittest.mock import patch
import unittest

class TestBackgammonGameBasico(unittest.TestCase):

    def test_inicializacion(self):
        self.game = backgammongame("Fran", "Maria")
        self.assertIsInstance(self.game.__board__, Board)
        self.assertIsInstance(self.game.__dados__, dice)
        self.assertIsInstance(self.game.__jugador1__, Player)
        self.assertIsInstance(self.game.__jugador2__, Player)
        jugadores = self.game.__jugadores__
        self.assertIn(self.game.mostrar_jugador1(), jugadores)
        self.assertIn(self.game.mostrar_jugador2(), jugadores)
        self.assertEqual(len(jugadores), 2)
        self.assertEqual(self.game.__jugador1__.obtener_nombre(), "Fran")
        self.assertEqual(self.game.__jugador2__.obtener_nombre(), "Maria")
        self.assertEqual(self.game.__turno__.obtener_nombre(), "Fran") # turno inicial debe ser jugador1
        self.assertFalse(self.game.__turno_finalizado__)

    def test_mostrar_jugador1(self):
        self.game = backgammongame("Fran", "Maria")        
        jugador1 = self.game.mostrar_jugador1()
        self.assertIsInstance(jugador1, Player)
        self.assertEqual(jugador1.obtener_nombre(), "Fran")
        self.assertEqual(jugador1.obtener_color(), "white")

    def test_mostrar_jugador2(self):
        self.game = backgammongame("Fran", "Maria")
        jugador2 = self.game.mostrar_jugador2()
        self.assertIsInstance(jugador2, Player)
        self.assertEqual(jugador2.obtener_nombre(), "Maria")
        self.assertEqual(jugador2.obtener_color(), "black")

    def test_mostrar_turno(self):
        self.game = backgammongame("Fran", "Maria")
        self.assertEqual(self.game.mostrar_turno(), "Fran")
    
    def test_mostrar_tablero(self):
        self.game = backgammongame("Fran", "Maria")
        tablero = self.game.mostrar_tablero()
        self.assertIsInstance(tablero, Board)
        self.assertIs(tablero, self.game.__board__)
    
    def test_cambiar_turno_rama_if(self):
        self.game = backgammongame("Fran", "Maria")
        self.game.cambiar_turno()
        self.assertEqual(self.game.mostrar_turno(), "Maria")

    def test_cambiar_turno_rama_else(self):
        self.game = backgammongame("Fran", "Maria")
        self.game.__turno__ = self.game.__jugador2__
        self.game.cambiar_turno()
        self.assertEqual(self.game.mostrar_turno(), "Fran")

    @patch("random.randint", side_effect=[3, 5])
    def test_iniciar_turno(self, mock_randint):
        self.game = backgammongame("Fran", "Maria")
        self.game.__dados__.tirar_dados()
        dados = self.game.__dados__.get_dados()
        self.assertEqual(dados, [3, 5])

    def test_cambiar_turno(self):
        self.game = backgammongame("Fran", "Maria")
        turno_inicial = self.game.__turno__
        if turno_inicial == self.game.__jugador1__:
            self.game.__turno__ = self.game.__jugador2__
            self.assertEqual(self.game.__turno__.obtener_nombre(), "Maria")
        else:
            self.game.__turno__ = self.game.__jugador1__
            self.assertEqual(self.game.__turno__.obtener_nombre(), "Fran")
    
    def test_juego_no_terminado_al_inicio(self):
        self.game = backgammongame("Fran", "Maria")
        self.assertFalse(self.game.juego_terminado())
        self.assertIsNone(self.game.ganador())

    def test_gana_jugador1(self):
        self.game = backgammongame("Fran", "Maria")
        self.game.__jugador1__.__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.ganador(), "Fran")

    def test_gana_jugador2(self):
        self.game = backgammongame("Fran", "Maria")
        self.game.__jugador2__.__fichas_restantes__ = 0
        self.assertTrue(self.game.juego_terminado())
        self.assertEqual(self.game.ganador(), "Maria")

    def test_empate_o_inconsistencia(self):
        self.game = backgammongame("Fran", "Maria")
        self.game.__jugador1__.__fichas_restantes__ = 5
        self.game.__jugador2__.__fichas_restantes__ = 5
        self.assertFalse(self.game.juego_terminado())
        self.assertIsNone(self.game.ganador())