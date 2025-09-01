import random

class dice:
    def __init__(self):
        self.__movimientos__ = []

    def tirar_dados(self):
        dado1 = random.randint(1, 6) #Genera dado 1
        dado2 = random.randint(1, 6) #Genera dado 2

        if dado1 == dado2:
            self.__movimientos__ = [dado1] *4 #Si los dados son iguales se duplican los turnos
        else:
            self.__movimientos__ = [dado1, dado2] #Si los dados son distintos se agregan individualmente