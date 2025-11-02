import unittest
from core.board import Board

class TestBoard(unittest.TestCase):

    def test_tablero_tiene_24_casillas(self):
        self.board = Board()
        # --- CORREGIDO: Usar __contenedor__ ---
        self.assertEqual(len(self.board.__contenedor__), 24)

    # --- CORREGIDO: Pruebas actualizadas a la nueva configuración inicial ---
    def test_configuracion_inicial_casilla_0(self):
        self.board = Board()
        # "white" (antes Negra)
        self.assertEqual(self.board.__contenedor__[0], ['white']*2)

    def test_configuracion_inicial_casilla_5(self):
        self.board = Board()
        # "black" (antes Blanca)
        self.assertEqual(self.board.__contenedor__[5], ['black']*5)

    def test_configuracion_inicial_casilla_7(self):
        self.board = Board()
        # "black" (antes Blanca)
        self.assertEqual(self.board.__contenedor__[7], ['black']*3)

    def test_configuracion_inicial_casilla_11(self):
        self.board = Board()
        # "white" (antes Negra)
        self.assertEqual(self.board.__contenedor__[11], ['white']*5)

    def test_configuracion_inicial_casilla_12(self):
        self.board = Board()
        # "black" (antes Blanca)
        self.assertEqual(self.board.__contenedor__[12], ['black']*5)

    def test_configuracion_inicial_casilla_16(self):
        self.board = Board()
        # "white" (antes Negra)
        self.assertEqual(self.board.__contenedor__[16], ['white']*3)

    def test_configuracion_inicial_casilla_18(self):
        self.board = Board()
        # "white" (antes Negra)
        self.assertEqual(self.board.__contenedor__[18], ['white']*5)

    def test_configuracion_inicial_casilla_23(self):
        self.board = Board()
        # "black" (antes Blanca)
        self.assertEqual(self.board.__contenedor__[23], ['black']*2)
    # --- FIN CORRECCIÓN CONFIGURACIÓN ---

    def test_banco_empieza_vacio(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ ---
        self.assertEqual(self.board.__barra__['white'], [])
        self.assertEqual(self.board.__barra__['black'], [])

    def test_home_empieza_vacio(self):
        self.board = Board()
        # --- CORREGIDO: Usar __afuera__ ---
        self.assertEqual(self.board.__afuera__['white'], [])
        self.assertEqual(self.board.__afuera__['black'], [])
    
    def test_remove_checker_color_correcto(self):
        self.board = Board()
        color = self.board.remover_checker(0)
        self.assertEqual(color, 'white')
        # --- CORREGIDO: Usar __contenedor__ ---
        self.assertEqual(len(self.board.__contenedor__[0]), 1)
    
    def test_remove_checker_casilla_vacia(self):
        self.board = Board()
        self.board.remover_checker(0)
        self.board.remover_checker(0)
        # --- CORREGIDO: Usar __contenedor__ ---
        self.assertEqual(len(self.board.__contenedor__[0]), 0)
    
    def test_remove_checker_casilla_vacia_error(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.remover_checker(1) # Casilla 1 empieza vacía
    
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
        # --- CORREGIDO: Usar __contenedor__ ---
        self.assertEqual(self.board.__contenedor__[origen], ['white'])
        self.assertEqual(self.board.__contenedor__[destino], ['white'])
    
    def test_mover_checker_mismo_color(self):
        self.board = Board()
        # --- CORREGIDO: Usar __contenedor__ ---
        self.board.__contenedor__[0] = ['white']
        self.board.__contenedor__[2] = ['white', 'white']
        self.board.mover_checker(0, 2)
        self.assertEqual(self.board.__contenedor__[2], ['white', 'white', 'white'])

    def test_mover_checker_comer_ficha(self):
        self.board = Board()
        # --- CORREGIDO: Usar __contenedor__ y __barra__ ---
        self.board.__contenedor__[0] = ['white']
        self.board.__contenedor__[3] = ['black']
        self.board.mover_checker(0, 3)
        self.assertEqual(self.board.__contenedor__[3], ['white'])
        self.assertEqual(self.board.__barra__['black'], ['black'])

    def test_mover_checker_bloqueado(self):
        self.board = Board()
        # --- CORREGIDO: Usar __contenedor__ ---
        self.board.__contenedor__[0] = ['white']
        self.board.__contenedor__[4] = ['black', 'black']
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
            self.board.mover_checker(2, 5) # Casilla 2 empieza vacía

    def test_consultar_checker_vacia(self):
        self.board = Board()
        self.assertEqual(self.board.consultar_checker(2), (None, 0))

    def test_consultar_checker_con_fichas(self):
        self.board = Board()
        resultado = self.board.consultar_checker(0)
        # --- CORREGIDO: Usar 'white' ---
        self.assertIn("hay 2 del color white", str(resultado))

    def test_consultar_checker_otro_color(self):
        self.board = Board()
        resultado = self.board.consultar_checker(5)
        # --- CORREGIDO: Usar 'black' ---
        self.assertIn("hay 5 del color black", str(resultado))

    def test_estado_jugador_inicial_white(self):
        self.board = Board()
        resultado = self.board.estado_jugador("white")
        self.assertIn("Fichas de white: 15 en el tablero, 0 guardadas, 0 comidas", str(resultado))

    def test_estado_jugador_inicial_black(self):
        self.board = Board()
        resultado = self.board.estado_jugador("black")
        self.assertIn("Fichas de black: 15 en el tablero, 0 guardadas, 0 comidas", str(resultado))

    # --- INICIO DE LA CORRECCIÓN (Lógica del test) ---
    def test_estado_jugador_con_fichas_en_home_y_banco(self):
        self.board = Board()
        # Configurar 2 en home, 1 en banco
        self.board.__afuera__["white"].extend(["white", "white"])
        self.board.__barra__["white"].append("white")
        
        # Simular tablero con 12 fichas (15 - 2 - 1)
        self.board.__contenedor__ = [[] for _ in range(24)] # Limpiar tablero
        self.board.__contenedor__[0] = ["white"] * 12 # Poner 12 fichas en un lugar
        
        # Ahora, en_tablero debe ser 12
        en_tablero = sum(1 for p in self.board.__contenedor__ for f in p if f == "white")
        self.assertEqual(en_tablero, 12) 
        
        resultado = self.board.estado_jugador("white")
        self.assertIn(f"Fichas de white: 12 en el tablero, 2 guardadas, 1 comidas", str(resultado))
    # --- FIN DE LA CORRECCIÓN ---

    def test_get_banco_inicial_vacio(self):
        self.board = Board()
        # --- CORREGIDO: Usar get_barra ---
        self.assertEqual(self.board.get_barra("white"), [])
        self.assertEqual(self.board.get_barra("black"), [])

    def test_get_banco_con_fichas(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ y get_barra ---
        self.board.__barra__["white"].extend(["white", "white"])
        self.assertEqual(self.board.get_barra("white"), ["white", "white"])

    def test_get_banco_devuelve_copia(self):
        self.board = Board()
        # --- CORREGIDO: Usar get_barra y __barra__ ---
        resultado = self.board.get_barra("black")
        resultado.append("black")
        self.assertNotEqual(resultado, self.board.__barra__["black"])

    def test_get_home_inicial_vacio(self):
        self.board = Board()
        # --- CORREGIDO: Usar get_afuera ---
        self.assertEqual(self.board.get_afuera("white"), [])
        self.assertEqual(self.board.get_afuera("black"), [])

    def test_get_home_con_fichas(self):
        self.board = Board()
        # --- CORREGIDO: Usar __afuera__ y get_afuera ---
        self.board.__afuera__["black"].extend(["black", "black", "black"])
        self.assertEqual(self.board.get_afuera("black"), ["black", "black", "black"])

    def test_get_home_devuelve_copia(self):
        self.board = Board()
        # --- CORREGIDO: Usar get_afuera y __afuera__ ---
        resultado = self.board.get_afuera("white")
        resultado.append("white")
        self.assertNotEqual(resultado, self.board.__afuera__["white"])
    
    def test_reingreso_normal(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ y __contenedor__ ---
        self.board.__barra__["white"].append("white")
        self.board.move_checker_banco("white", 2) # white reingresa en 0-5
        self.assertEqual(self.board.__contenedor__[2], ["white"])
        self.assertEqual(self.board.__barra__["white"], [])

    def test_destino_invalido(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ ---
        self.board.__barra__["white"].append("white")
        # Probar reingreso en zona incorrecta (white no puede en 20)
        with self.assertRaisesRegex(ValueError, "Fichas blancas sólo reingresan"):
            self.board.move_checker_banco("white", 20)

    def test_casilla_bloqueada_por_enemigos(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ y __contenedor__ ---
        self.board.__barra__["white"].append("white")
        self.board.__contenedor__[5] = ["black", "black"]  # casilla 5 (zona válida) bloqueada
        with self.assertRaises(ValueError):
            self.board.move_checker_banco("white", 5)

    def test_casilla_con_un_enemigo(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__, __contenedor__ y zona válida (0-5) ---
        self.board.__barra__["white"].append("white")
        self.board.__contenedor__[4] = ["black"]  # un enemigo en zona 0-5
        self.board.move_checker_banco("white", 4)
        self.assertEqual(self.board.__contenedor__[4], ["white"])
        self.assertEqual(self.board.__barra__["black"], ["black"])

    def test_banco_vacio_lanza_error(self):
        self.board = Board()
        with self.assertRaises(ValueError):
            self.board.move_checker_banco("white", 3)
    
    def test_sacar_ficha_valida(self):
        self.board = Board()
        # --- CORREGIDO: Usar __afuera__ y __contenedor__ (white saca de 18-23) ---
        self.board.__contenedor__[18] = ["white", "white"] # Sobreescribir
        resultado = self.board.sacar_ficha("white", 18)
        self.assertTrue(resultado)
        self.assertEqual(self.board.__afuera__["white"], ["white"])
        self.assertEqual(self.board.__contenedor__[18], ["white"]) # Queda una

    def test_sacar_ficha_casilla_vacia(self):
        self.board = Board()
        resultado = self.board.sacar_ficha("white", 3)
        self.assertFalse(resultado)
        # --- CORREGIDO: Usar __afuera__ ---
        self.assertEqual(self.board.__afuera__["white"], [])

    def test_sacar_ficha_color_incorrecto(self):
        self.board = Board()
        resultado = self.board.sacar_ficha("white", 5) # Casilla 5 es 'black'
        self.assertFalse(resultado)
        # --- CORREGIDO: Usar __afuera__ y __contenedor__ ---
        self.assertEqual(self.board.__afuera__["white"], [])
        self.assertEqual(self.board.__contenedor__[5], ["black"]*5)

    def test_sacar_ficha_modifica_home_y_tablero(self):
        self.board = Board()
        # --- CORREGIDO: Usar __contenedor__ y __afuera__ ---
        self.board.__contenedor__[18] = ["white", "white"]
        cantidad_inicial = len(self.board.__contenedor__[18])
        self.board.sacar_ficha("white", 18)
        self.assertEqual(len(self.board.__contenedor__[18]), cantidad_inicial - 1)
        self.assertEqual(self.board.__afuera__["white"], ["white"])

    def test_reingresar_ficha_apilando_mismo_color(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ y __contenedor__ ---
        self.board.__barra__["white"].append("white")
        self.board.__contenedor__[2] = ["white", "white"]
        self.board.move_checker_banco("white", 2)
        self.assertEqual(len(self.board.__contenedor__[2]), 3)
        self.assertEqual(self.board.__contenedor__[2], ["white", "white", "white"])
        self.assertEqual(self.board.get_barra("white"), [])

    def test_reingresar_ficha_zona_invalida_blancas(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ ---
        self.board.__barra__["white"].append("white")
        with self.assertRaisesRegex(ValueError, "Fichas blancas sólo reingresan"):
            self.board.move_checker_banco("white", 10)
        self.assertEqual(len(self.board.get_barra("white")), 1)

    def test_reingresar_ficha_zona_invalida_negras(self):
        self.board = Board()
        # --- CORREGIDO: Usar __barra__ ---
        self.board.__barra__["black"].append("black")
        with self.assertRaisesRegex(ValueError, "Fichas negras sólo reingresan"):
            self.board.move_checker_banco("black", 10)
        self.assertEqual(len(self.board.get_barra("black")), 1)

    def test_sacar_ficha_valida_negras(self):
        self.board = Board()
        # --- CORREGIDO: Usar get_afuera y __contenedor__ ---
        # "black" saca de 0-5. Usamos 5.
        resultado = self.board.sacar_ficha("black", 5)
        self.assertTrue(resultado)
        self.assertEqual(self.board.get_afuera("black"), ["black"])
        self.assertEqual(len(self.board.__contenedor__[5]), 4)


if __name__ == '__main__':
    unittest.main()