Modelo de IA: Chat GPT 

Prompt:
    dame los tests necesarios para obtener un 95% de cobertura para el código:

class player:
    def __init__(self, nombre, color):
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas__ = 15
        self.__fichas_restantes__ = 15

    def mostrar_fichas(self):
        return self.__fichas_restantes__
    
    def obtener_nombre(self):
        return self.__nombre__
    
    def obtener_color(self):
        return self.__color__
    
    def ganar(self):
        if self.__fichas_restantes__ == 0:
            return True
        else:
            return False
    
    def restar_ficha(self):
        if self.__fichas_restantes__ > 0:
            self.__fichas_restantes__ - 1
            return True
        else: 
            return False
    
    def __str__(self):
        return (f"El jugador: {self.__nombre__}, tiene color: {self.__color__} y le quedan {self.__fichas_restantes__} fichas")

Respuesta:
    import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.jugador = player("Fran", "white")

    def test_inicializacion(self):
        """El jugador debe iniciar con nombre, color y 15 fichas"""
        self.assertEqual(self.jugador.obtener_nombre(), "Fran")
        self.assertEqual(self.jugador.obtener_color(), "white")
        self.assertEqual(self.jugador.mostrar_fichas(), 15)

    def test_mostrar_fichas(self):
        """Debe devolver la cantidad de fichas restantes"""
        self.assertEqual(self.jugador.mostrar_fichas(), 15)

    def test_ganar_false(self):
        """Si quedan fichas, no debe haber ganado"""
        self.assertFalse(self.jugador.ganar())

    def test_ganar_true(self):
        """Si no quedan fichas, debe haber ganado"""
        self.jugador._player__fichas_restantes__ = 0
        self.assertTrue(self.jugador.ganar())

    def test_restar_ficha_valida(self):
        """Debe restar una ficha y devolver True si quedan fichas"""
        self.jugador._player__fichas_restantes__ = 3
        resultado = self.jugador.restar_ficha()
        self.assertTrue(resultado)
        self.assertEqual(self.jugador.mostrar_fichas(), 2)

    def test_restar_ficha_ultima(self):
        """Debe restar la última ficha y permitir que gane"""
        self.jugador._player__fichas_restantes__ = 1
        resultado = self.jugador.restar_ficha()
        self.assertTrue(resultado)
        self.assertEqual(self.jugador.mostrar_fichas(), 0)
        self.assertTrue(self.jugador.ganar())

    def test_restar_ficha_sin_fichas(self):
        """Debe devolver False si ya no quedan fichas"""
        self.jugador._player__fichas_restantes__ = 0
        resultado = self.jugador.restar_ficha()
        self.assertFalse(resultado)

    def test_str(self):
        """Debe mostrar correctamente la representación en string"""
        esperado = "El jugador: Fran, tiene color: white y le quedan 15 fichas"
        self.assertEqual(str(self.jugador), esperado)

No se utilizó el código exacto ya que a fines de asegurarnos que se inicie una instancia propia de cada clase player se modifica eliminando set_up y agregando una inicialización porpia por test

tets/test_player.py

Prompt:
    "

Respuesta:
    import unittest
    from unittest.mock import patch
    from core.cli import cli
    from core.backgammongame import backgammongame

    class TestCLI(unittest.TestCase):

        def test_inicializacion(self):
            interfaz = cli("Fran", "Maria")
            self.assertIsInstance(interfaz.game, backgammongame)
            self.assertEqual(interfaz.game.mostrar_turno(), "Fran")

        @patch("builtins.input", side_effect=["Fran", "Maria"])
        def test_inicar_juego(self, mock_input):
            interfaz = cli("Temp1", "Temp2")
            interfaz.inicar_juego()
            self.assertIsInstance(interfaz.game, backgammongame)
            self.assertEqual(interfaz.game.mostrar_jugador1().obtener_nombre(), "Fran")
            self.assertEqual(interfaz.game.mostrar_jugador2().obtener_nombre(), "Maria")

Se utiliza el código exacto
tets/test_cli.py