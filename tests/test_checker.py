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
    
    def test_posicion_nueva_true(self):
        ficha = Checker("white", 5)
        self.assertTrue(ficha.posicion_nueva(5))

    def test_posicion_nueva_false(self):
        ficha = Checker("black", 10)
        self.assertFalse(ficha.posicion_nueva(7))

    def test_esta_banco_true(self):
        ficha = Checker("white", "banco")
        self.assertTrue(ficha.esta_banco())

    def test_esta_banco_false(self):
        ficha = Checker("black", 8)
        self.assertFalse(ficha.esta_banco())

    def test_esta_home_true(self):
        ficha = Checker("white", "home")
        self.assertTrue(ficha.esta_home())

    def test_esta_home_false(self):
        ficha = Checker("black", 3)
        self.assertFalse(ficha.esta_home())