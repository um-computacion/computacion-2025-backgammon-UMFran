from core.board import Board
from core.dice import dice
from core.player import Player

class backgammongame:
    def __init__(self, jugador1, jugador2):
        self.__board__ = Board()
        self.__dados__ = dice()
        self.__jugador1__ = Player(jugador1, "white")
        self.__jugador2__ = Player(jugador2, "black")
        self.__turno__ = jugador1
        self.__turno_finalizado__ = False

# Funciones básicas:

    def mostrar_jugador1 (self):
        return self.__jugador1__
    
    def mostrar_jugador2 (self):
        return self.__jugador2__
    
    def mostrar_turno(self):
        return self.__turno__
