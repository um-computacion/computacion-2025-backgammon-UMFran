import unittest
from core.dice import dice
from unittest.mock import patch

class TestsDice(unittest.TestCase): #CONSULTAR EN CLASE!!!

    @patch("random.randint", side_effect=[3, 5])
    def test_tirada_normal(self, mock_randint):
        self.dice = dice()
        self.dice.tirar_dados()
        self.assertEqual(self.dice.__movimientos__, [3, 5])

    @patch("random.randint", side_effect=[4, 4])
    def test_tirada_doble(self, mock_randint):
        self.dice = dice()
        self.dice.tirar_dados()
        self.assertEqual(self.dice.__movimientos__, [4, 4, 4, 4])

    def test_movimientos_se_reemplazan(self):
        self.dice = dice()
        self.dice.__movimientos__ = [1, 2, 3]
        with patch("random.randint", side_effect=[6, 2]):
            self.dice.tirar_dados()
        self.assertEqual(self.dice.__movimientos__, [6, 2])

    def test_get_dado(self):
        self.dice = dice()
        self.dice.__movimientos__ = [1, 3]
        resultado = self.dice.get_dados()
        self.assertEqual(resultado, [1, 3])

    def test_usar_dado_valido(self):
        self.dice = dice()
        self.dice.__movimientos__ = [3, 5]
        self.dice.usar_dado(3)
        self.assertEqual(self.dice.__movimientos__, [5])

    def test_usar_dado_invalido(self):
        self.dice = dice()
        self.dice.__movimientos__ = [2, 6]
        with self.assertRaises(ValueError):
            self.dice.usar_dado(4)

    def test_usar_dado_con_dobles(self):
        self.dice = dice()
        self.dice.__movimientos__ = [4, 4, 4, 4]
        self.dice.usar_dado(4)
        self.assertEqual(self.dice.__movimientos__, [4, 4, 4])
    
    def test_hay_movimientos_true(self):
        self.dice = dice()
        self.dice.__movimientos__ = [3, 5]
        self.assertTrue(self.dice.hay_movimientos())

    def test_hay_movimientos_false(self):
        self.dice = dice()
        self.dice.__movimientos__ = []
        self.assertFalse(self.dice.hay_movimientos())

    def test_reset_vacia_lista(self):
        self.dice = dice()
        self.dice.__movimientos__ = [2, 6]
        self.dice.limpiar_dados()
        self.assertEqual(self.dice.__movimientos__, [])
    
if __name__ == "__main__":
    unittest.main()