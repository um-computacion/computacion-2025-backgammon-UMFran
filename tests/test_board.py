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
        # La forma en que se construye el set es sensible, usemos una comparación de string
        self.assertIn("hay 2 del color white", str(resultado))

    def test_consultar_checker_otro_color(self):
        self.board = Board()
        resultado = self.board.consultar_checker(5)
        self.assertIn("hay 5 del color black", str(resultado))

    def test_estado_jugador_inicial_white(self):
        self.board = Board()
        resultado = self.board.estado_jugador("white")
        self.assertIn("Fichas de white: 15 en el tablero, 0 guardadas, 0 comidas", str(resultado))

    def test_estado_jugador_inicial_black(self):
        self.board = Board()
        resultado = self.board.estado_jugador("black")
        self.assertIn("Fichas de black: 15 en el tablero, 0 guardadas, 0 comidas", str(resultado))

    def test_estado_jugador_con_fichas_en_home_y_banco(self):
        self.board = Board()
        self.board.__home__["white"].extend(["white", "white"]) # 2 en home
        self.board.__banco__["white"].append("white") # 1 en banco
        # Total 15: 2 en home + 1 en banco + 12 en tablero
        self.board.__casillas__[0] = [] # Quitamos 2 de la pos 0
        self.board.__casillas__[11] = ['white'] # Quitamos 4 de la pos 11
        # Ahora hay 15 - 2 - 4 = 9 fichas en tablero
        
        resultado = self.board.estado_jugador("white")
        # El test original no restaba las fichas del tablero, esta es una mejor prueba
        en_tablero = sum(1 for p in self.board.__casillas__ for f in p if f == "white")
        
        self.assertEqual(en_tablero, 9) # 15 iniciales - 2 (home) - 1 (banco) - 3 (quitadas para test) = 9
        self.assertIn(f"Fichas de white: {en_tablero} en el tablero, 2 guardadas, 1 comidas", str(resultado))


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
        self.assertEqual(self.board.__banco__["black"], []) # El original sigue vacío

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
        self.assertEqual(self.board.__home__["white"], []) # El original sigue vacío
    
    def test_reingreso_normal(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.move_checker_banco("white", 2)
        self.assertEqual(self.board.__casillas__[2], ["white"])
        self.assertEqual(self.board.__banco__["white"], [])

    def test_destino_invalido(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        with self.assertRaisesRegex(ValueError, "blancas sólo reingresan"):
            self.board.move_checker_banco("white", 23)

    def test_casilla_bloqueada_por_enemigos(self):
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.__casillas__[5] = ["black", "black"]  # casilla bloqueada
        with self.assertRaises(ValueError):
            self.board.move_checker_banco("white", 5)

    def test_casilla_con_un_enemigo(self):
        # --- CORREGIDO ---
        # El test original fallaba porque intentaba reingresar en la casilla 7,
        # lo cual es ilegal para las blancas.
        # Lo movemos a la casilla 4 (que está en la zona 0-5).
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.__casillas__[4] = ["black"]  # un enemigo en la zona de reingreso
        self.board.move_checker_banco("white", 4)
        self.assertEqual(self.board.__casillas__[4], ["white"]) # Come a la negra
        self.assertEqual(self.board.__banco__["black"], ["black"]) # Negra va al banco
        # --- FIN CORRECCIÓN ---

    def test_banco_vacio_lanza_error(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.move_checker_banco("white", 3)
    
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

    # --- Tests Adicionales Añadidos ---

    def test_reingresar_ficha_apilando_mismo_color(self):
        # Prueba reingresar en una casilla que ya tiene fichas propias
        self.board = Board()
        self.board.__banco__["white"].append("white")
        self.board.__casillas__[2] = ["white", "white"] # Casilla ya tiene 2 blancas
        self.board.move_checker_banco("white", 2)
        # Debería apilarse
        self.assertEqual(len(self.board.__casillas__[2]), 3)
        self.assertEqual(self.board.__casillas__[2], ["white", "white", "white"])
        self.assertEqual(self.board.get_banco("white"), [])

    def test_reingresar_ficha_zona_invalida_blancas(self):
        # Prueba que las blancas no pueden reingresar fuera de 0-5
        self.board = Board()
        self.board.__banco__["white"].append("white")
        with self.assertRaisesRegex(ValueError, "blancas sólo reingresan en casillas 0-5"):
            self.board.move_checker_banco("white", 10)
        # La ficha debe seguir en el banco
        self.assertEqual(len(self.board.get_banco("white")), 1)

    def test_reingresar_ficha_zona_invalida_negras(self):
        # Prueba que las negras no pueden reingresar fuera de 18-23
        self.board = Board()
        self.board.__banco__["black"].append("black")
        with self.assertRaisesRegex(ValueError, "negras sólo reingresan en casillas 18-23"):
            self.board.move_checker_banco("black", 10)
        # La ficha debe seguir en el banco
        self.assertEqual(len(self.board.get_banco("black")), 1)

    def test_sacar_ficha_valida_negras(self):
        # Prueba el 'bear off' para las fichas negras
        self.board = Board()
        # La casilla 5 (cuadrante final negro) tiene fichas negras por defecto
        resultado = self.board.sacar_ficha("black", 5)
        self.assertTrue(resultado)
        self.assertEqual(self.board.get_home("black"), ["black"])
        self.assertEqual(len(self.board.__casillas__[5]), 4) # Eran 5, queda 1 menos


if __name__ == '__main__':
    unittest.main()