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

    def test_consultar_checker_vacia(self):
        self.board = Board()
        self.assertEqual(self.board.consultar_checker(2), (None, 0))

    def test_consultar_checker_con_fichas(self):
        self.board = Board()
        resultado = self.board.consultar_checker(0)
        esperado = {f"En la posición {self.board.__casillas__[0]} hay 2 del color white"}
        self.assertEqual(resultado, esperado)

    def test_consultar_checker_otro_color(self):
        self.board = Board()
        resultado = self.board.consultar_checker(5)
        esperado = {f"En la posición {self.board.__casillas__[5]} hay 5 del color black"}
        self.assertEqual(resultado, esperado)

    def test_estado_jugador_inicial_white(self):
        self.board = Board()
        resultado = self.board.estado_jugador("white")
        en_tablero = sum(1 for punto in self.board.__casillas__ for ficha in punto if ficha == "white")
        en_home = len(self.board.__home__["white"])
        en_banco = len(self.board.__banco__["white"])
        esperado = {f"Fichas de white: {en_tablero} en el tablero, {en_home} guardadas, {en_banco} comidas sin sacar"}
        self.assertEqual(resultado, esperado)

    def test_estado_jugador_inicial_black(self):
        self.board = Board()
        resultado = self.board.estado_jugador("black")
        en_tablero = sum(1 for punto in self.board.__casillas__ for ficha in punto if ficha == "black")
        en_home = len(self.board.__home__["black"])
        en_banco = len(self.board.__banco__["black"])
        esperado = {f"Fichas de black: {en_tablero} en el tablero, {en_home} guardadas, {en_banco} comidas sin sacar"}
        self.assertEqual(resultado, esperado)

    def test_estado_jugador_con_fichas_en_home_y_banco(self):
        self.board = Board()
        self.board.__home__["white"].extend(["white", "white"]) # agregamos 2 blancas al home y 1 blanca al banco
        self.board.__banco__["white"].append("white")

        resultado = self.board.estado_jugador("white")
        en_tablero = sum(1 for punto in self.board.__casillas__ for ficha in punto if ficha == "white")
        en_home = len(self.board.__home__["white"])
        en_banco = len(self.board.__banco__["white"])
        esperado = {f"Fichas de white: {en_tablero} en el tablero, {en_home} guardadas, {en_banco} comidas sin sacar"}
        self.assertEqual(resultado, esperado)

    def test_get_banco_inicial_vacio(self):
        self.board = Board()
        self.assertEqual(self.board.get_banco("white"), [])
        self.assertEqual(self.board.get_banco("black"), [])

    def test_get_banco_con_fichas(self):
        self.board = Board()
        self.board.__banco__["white"].extend(["white", "white"])
        self.assertEqual(self.board.get_banco("white"), ["white", "white"])

    def test_get_banco_devuelve_copia(self):
        self.board = Board()
        resultado = self.board.get_banco("black")
        resultado.append("black")
        self.assertNotEqual(resultado, self.board.__banco__["black"])

    def test_get_home_inicial_vacio(self):
        self.board = Board()
        self.assertEqual(self.board.get_home("white"), [])
        self.assertEqual(self.board.get_home("black"), [])

    def test_get_home_con_fichas(self):
        self.board = Board()
        self.board.__home__["black"].extend(["black", "black", "black"])
        self.assertEqual(self.board.get_home("black"), ["black", "black", "black"])

    def test_get_home_devuelve_copia(self):
        self.board = Board()
        resultado = self.board.get_home("white")
        resultado.append("white")
        self.assertNotEqual(resultado, self.board.__home__["white"])
    
    def test_reingreso_normal(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.move_checker_banco("white", 2)
        self.assertEqual(self.board.__casillas__[2], ["white"])
        self.assertEqual(self.board.__banco__["white"], [])

    def test_destino_invalido(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        with self.assertRaises(ValueError):
            self.board.move_checker_banco("white", 30)

    def test_casilla_bloqueada_por_enemigos(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.__casillas__[5] = ["black", "black"]  # casilla bloqueada
        with self.assertRaises(ValueError):
            self.board.move_checker_banco("white", 5)

    def test_casilla_con_un_enemigo(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.__casillas__[7] = ["black"]  # un enemigo
        self.board.move_checker_banco("white", 7)
        self.assertEqual(self.board.__casillas__[7], ["white"])
        self.assertEqual(self.board.__banco__["black"], ["black"])

    def test_banco_vacio_no_hace_nada(self):
        self.board = Board()
        estado_inicial = [list(c) for c in self.board.__casillas__]
        self.board.move_checker_banco("white", 3)  # no hay fichas en banco
        self.assertEqual(self.board.__casillas__, estado_inicial)
    
    def test_sacar_ficha_valida(self):
        self.board = Board()
        resultado = self.board.sacar_ficha("white", 0)
        self.assertTrue(resultado)
        self.assertEqual(self.board.__home__["white"], ["white"])
        self.assertEqual(self.board.__casillas__[0], ["white"])  # quedó una sola

    def test_sacar_ficha_casilla_vacia(self):
        self.board = Board()
        resultado = self.board.sacar_ficha("white", 3)  # casilla 3 arranca vacía
        self.assertFalse(resultado)
        self.assertEqual(self.board.__home__["white"], [])

    def test_sacar_ficha_color_incorrecto(self):
        self.board = Board()
        resultado = self.board.sacar_ficha("white", 5)
        self.assertFalse(resultado)
        self.assertEqual(self.board.__home__["white"], [])
        self.assertEqual(self.board.__casillas__[5], ["black"]*5)

    def test_sacar_ficha_modifica_home_y_tablero(self):
        self.board = Board()
        cantidad_inicial = len(self.board.__casillas__[0])
        self.board.sacar_ficha("white", 0)
        self.assertEqual(len(self.board.__casillas__[0]), cantidad_inicial - 1)
        self.assertEqual(self.board.__home__["white"], ["white"])


if __name__ == '__main__':
    unittest.main()