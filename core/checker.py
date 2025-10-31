"""
Módulo Checker.

Contiene la clase Checker, que representa una ficha individual del juego.
"""


class Checker:
    """
    Representa una ficha de Backgammon con un color y posición.
    """
    def __init__(self, color: str, posicion=None):
        """Inicializa la ficha con su color y posición opcional."""
        self.__color__ = color
        self.__posicion__ = posicion

    def obtener_color(self):
        """Devuelve el color de la ficha."""
        return self.__color__

    def obtener_posicion(self):
        """Devuelve la posición actual de la ficha."""
        return self.__posicion__

    def posicion_nueva(self, nueva_posicion):
        """Comprueba si la posición dada es la actual."""
        return self.__posicion__ == nueva_posicion

    def esta_banco(self):
        """Comprueba si la ficha está en el banco."""
        return self.__posicion__ == "banco"

    def esta_home(self):
        """Comprueba si la ficha está en el home."""
        return self.__posicion__ == "home"
