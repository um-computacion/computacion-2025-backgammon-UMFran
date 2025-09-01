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