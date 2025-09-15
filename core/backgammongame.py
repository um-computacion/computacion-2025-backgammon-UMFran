from core.board import Board
from core.dice import dice
from core.player import Player

class backgammongame:
    def __init__(self, jugador1: str, jugador2: str):
        self.__board__ = Board()
        self.__dados__ = dice()
        self.__jugador1__ = Player(jugador1, "white")
        self.__jugador2__ = Player(jugador2, "black")
        self.__jugadores__ = {self.__jugador1__, self.__jugador2__}
        self.__turno__ = self.__jugador1__
        self.__turno_finalizado__ = False

# Funciones básicas:

    def mostrar_jugador1 (self):
        return self.__jugador1__
    
    def mostrar_jugador2 (self):
        return self.__jugador2__
    
    def mostrar_turno(self):
        return self.__turno__.obtener_nombre()
    
    def mostrar_tablero(self):
        return self.__board__
    
#Funciones de dados

    def tirar_dados(self):
        self.__dados__.tirar_dados()
        return self.__dados__.get_dados()
    
    def cambiar_turno(self):
        if self.__turno__ == self.__jugador1__:
            self.__turno__ = self.__jugador2__
        else:
            self.__turno__ = self.__jugador1__

    def ganador(self):
        for jugador in self.__jugadores__: 
            if jugador.ganar():
                self.__juego_terminado__ = True
                return jugador.obtener_nombre()
        return None
    
    def juego_terminado(self):
        return self.__jugador1__.ganar() or self.__jugador2__.ganar()