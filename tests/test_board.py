import unittest
from core.board import Board

class TestBoard(unittest.TestCase):

    def test_tablero_tiene_24_casillas(self):
        self.board = Board()
        #El tablero debe tener exactamente 24 casillas
        self.assertEqual(len(self.board.__casillas__), 24)

    def test_configuracion_inicial_casilla_0(self):
        self.board = Board()
        #La casilla 0 debe comenzar con 2 fichas blancas
        self.assertEqual(self.board.__casillas__[0], ['white','white'])

    def test_configuracion_inicial_casilla_5(self):
        self.board = Board()
        #La casilla 5 debe comenzar con 5 fichas negras
        self.assertEqual(self.board.__casillas__[5], ['black']*5)

    def test_configuracion_inicial_casilla_11(self):
        self.board = Board()
        #La casilla 11 debe comenzar con 5 fichas blancas
        self.assertEqual(self.board.__casillas__[11], ['white']*5)

    def test_configuracion_inicial_casilla_12(self):
        self.board = Board()
        #La casilla 12 debe comenzar con 5 fichas negras
        self.assertEqual(self.board.__casillas__[12], ['black']*5)

    def test_configuracion_inicial_casilla_16(self):
        self.board = Board()
        #La casilla 16 debe comenzar con 3 fichas blancas
        self.assertEqual(self.board.__casillas__[16], ['white']*3)

    def test_configuracion_inicial_casilla_18(self):
        self.board = Board()
        #La casilla 18 debe comenzar con 5 fichas blancas
        self.assertEqual(self.board.__casillas__[18], ['white']*5)

    def test_configuracion_inicial_casilla_23(self):
        self.board = Board()
        #La casilla 23 debe comenzar con 2 fichas negras
        self.assertEqual(self.board.__casillas__[23], ['black']*2)

    def test_banco_empieza_vacio(self):
        self.board = Board()
        #El banco debe empezar vacío para ambos colores
        self.assertEqual(self.board.__banco__['white'], [])
        self.assertEqual(self.board.__banco__['black'], [])

    def test_home_empieza_vacio(self):
        self.board = Board()
        #El home debe empezar vacío para ambos colores
        self.assertEqual(self.board.__home__['white'], [])
        self.assertEqual(self.board.__home__['black'], [])
    
    def test_remove_checker_color_correcto(self):
        self.board = Board()
        color = self.board.remover_checker(0)
        self.assertEqual(color, 'white')
        self.assertEqual(len(self.board.__casillas__[0]), 1)
    
    def test_remove_checker_casilla_vacia(self):
        self.board = Board()
        self.board.remover_checker(0)
        self.board.remover_checker(0)
        self.assertEqual(len(self.board.__casillas__[0]), 0)
    
    def test_remove_checker_casilla_vacia_error(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(1)
    
    def test_remove_checker_casilla_fuera_rango(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(24)
    
    def test_remove_checker_casilla_negativa(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(-1)
    
    def test_move_checker_valido(self):
        self.board = Board()
        origen, destino = 0, 2
        self.board.mover_checker(0, 2)
        self.assertEqual(self.board.__casillas__[origen], ['white'])
        self.assertEqual(self.board.__casillas__[destino], ['white'])
    
    def test_mover_checker_mismo_color(self):
        self.board = Board()
        self.board.__casillas__[0] = ['white']
        self.board.__casillas__[2] = ['white', 'white']
        self.board.mover_checker(0, 2)
        self.assertEqual(self.board.__casillas__[2], ['white', 'white', 'white'])

    def test_mover_checker_comer_ficha(self):
        self.board = Board()
        self.board.__casillas__[0] = ['white']
        self.board.__casillas__[3] = ['black']
        self.board.mover_checker(0, 3)

        self.assertEqual(self.board.__casillas__[3], ['white']) #Ficha blanca come a ficha negra
        self.assertEqual(self.board.__banco__['black'], ['black']) #Ficha negra se agrega al banco

    def test_mover_checker_bloqueado(self):
        self.board = Board()
        self.board.__casillas__[0] = ['white']
        self.board.__casillas__[4] = ['black', 'black']
        with self.assertRaises(ValueError):
            self.board.mover_checker(0, 4)

    def test_mover_checker_destino_invalido(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.mover_checker(0, -1)
        with self.assertRaises(ValueError):
            self.board.mover_checker(0, 24)

    def test_mover_checker_origen_vacio(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.mover_checker(2, 5)

if __name__ == '__main__':
    unittest.main()