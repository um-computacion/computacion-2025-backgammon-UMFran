"""
Módulo Dice.

Contiene la clase Dice, que gestiona la lógica de
lanzamiento y uso de los dados.
"""
import random


class Dice:
    """
    Representa un par de dados de Backgammon.
    Gestiona tiradas, dobles y el consumo de movimientos.
    """
    def __init__(self):
        """Inicializa la lista de movimientos (dados) disponibles."""
        self.__movimientos__ = []

    def tirar_dados(self):
        """
        Simula la tirada de dos dados.
        Si son dobles, genera 4 movimientos.
        """
        dado1 = random.randint(1, 6)  # Genera dado 1
        dado2 = random.randint(1, 6)  # Genera dado 2

        if dado1 == dado2:
            self.__movimientos__ = [dado1] * 4  # Si son iguales se duplican
        else:
            self.__movimientos__ = [dado1, dado2]  # Si son distintos se agregan

    def get_dados(self):
        """Devuelve una copia de la lista de dados disponibles."""
        return list(self.__movimientos__)

    def usar_dado(self, valor: int):
        """
        Consume (elimina) un dado de la lista de movimientos.
        Lanza ValueError si el dado no está disponible.
        """
        if valor not in self.__movimientos__:
            raise ValueError(
                f"El valor {valor} no se encuentra entre los generados"
            )
        self.__movimientos__.remove(valor)  # Elimina el valor usado

    def hay_movimientos(self):
        """Devuelve True si quedan dados, False si no."""
        return len(self.__movimientos__) > 0

    def limpiar_dados(self):
        """Limpia la lista de movimientos (al final del turno)."""
        self.__movimientos__.clear()
