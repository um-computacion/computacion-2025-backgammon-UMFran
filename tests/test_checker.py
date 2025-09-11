import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):
    def test_get_color_white(self):
        ficha = Checker("white", 0)
        self.assertEqual(ficha.obtener_color(), "white")

    def test_get_color_black(self):
        ficha = Checker("black", 5)
        self.assertEqual(ficha.obtener_color(), "black")

    def test_get_posicion_inicial(self):
        ficha = Checker("white", 12)
        self.assertEqual(ficha.obtener_posicion(), 12)

    def test_get_posicion_none(self):
        ficha = Checker("black")
        self.assertIsNone(ficha.obtener_posicion())