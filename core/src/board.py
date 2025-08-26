import unittest

class Board:
    def __init__(self):
        self.__casillas__ = [
            ['white','white'], #0
            [], #1
            [], #2
            [], #3
            [], #4
            ['black', 'black', 'black', 'black', 'black'], #5
            #--------------------------------------------
            [], #6
            ['black', 'black', 'black'], #7
            [], #8
            [], #9
            [], #10
            ['white', 'white', 'white', 'white', 'white'], #11
            #--------------------------------------------
            ['black', 'black', 'black', 'black', 'black'], #12
            [], #13
            [], #14
            [], #15
            ['white', 'white', 'white'], #16
            [], #17
            #--------------------------------------------
            ['white', 'white', 'white', 'white', 'white'], #18
            [], #19
            [], #20
            [], #21
            [], #22
            ['black', 'black'], #23
        ] #Definimos el tablero general de 24 casillas como una lista

        self.__banco__ = {"white": [], "black": []} #Lugar donde guardamos las fichas comidas

        self.__home__ = {"white": [], "black": []} #Lugar donde guardamos las fichas al finalizar el juego
    
    def remover_checker(self, punto: int):
        if punto < 0 or punto > 23:
            raise ValueError("punto inválido")
        elif not self.__casillas__[punto]:
            raise ValueError("No hay ficha en esta casilla")
        return self.__casillas__[punto].pop()
    

#-----------------TESTS--------------------------

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
    
    def tet_remove_checker_casilla_vacia(self):
        self.board = Board()
        self.board.remover_checker(0)
        self.board.remover_checker(0)
        self.assertEqual(len(self.board.__casillas__[0]), [])
    
    def tet_remove_checker_casilla_vacia_error(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(1)
    
    def tet_remove_checker_casilla_fuera_rango(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(24)
    
    def tet_remove_checker_casilla_negativa(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(-1)
        

if __name__ == '__main__':
    unittest.main()