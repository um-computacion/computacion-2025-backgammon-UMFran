from core.backgammongame import backgammongame
from core.board import Board
from core.dice import dice
from core.player import Player
import unittest

class TestBackgammonGameBasico(unittest.TestCase):

    def test_inicializacion(self):
        self.game = backgammongame("Fran", "Maria")
        # Verificamos tipos
        self.assertIsInstance(self.game.__board__, Board)
        self.assertIsInstance(self.game.__dados__, dice)
        self.assertIsInstance(self.game.__jugador1__, Player)
        self.assertIsInstance(self.game.__jugador2__, Player)
        # Verificamos turno inicial
        self.assertEqual(self.game.__turno__, "Fran")
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