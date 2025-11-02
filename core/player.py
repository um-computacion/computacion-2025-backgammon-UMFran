"""
Módulo Player.

Contiene la clase Player, que representa a un jugador.
"""

class Player:
    """
    Representa a un jugador con nombre, color y contador de fichas.
    """
    def __init__(self, nombre, color):
        """Inicializa al jugador."""
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas__ = 15
        self.__fichas_restantes__ = 15

    def mostrar_fichas(self):
        """Devuelve la cantidad de fichas que le quedan al jugador."""
        return self.__fichas_restantes__

    def obtener_nombre(self):
        """Devuelve el nombre del jugador."""
        return self.__nombre__

    def obtener_color(self):
        """Devuelve el color del jugador ('white' o 'black')."""
        return self.__color__

    def ganar(self):
        """Comprueba si el jugador ha ganado (no le quedan fichas)."""
        return self.__fichas_restantes__ == 0

    def restar_ficha(self):
        """
        Resta una ficha del contador.
        Devuelve True si tuvo éxito, False si ya estaba en 0.
        """
        if self.__fichas_restantes__ > 0:
            self.__fichas_restantes__ -= 1
            return True
        return False

    def resetear_fichas(self):
        """Restaura el contador de fichas a 15 (para un juego nuevo)."""
        self.__fichas_restantes__ = self.__fichas__

    def __str__(self):
        """Devuelve una representación en string del jugador."""
        return (
            f"El jugador: {self.__nombre__}, tiene color: {self.__color__} "
            f"y le quedan {self.__fichas_restantes__} fichas"
        )
