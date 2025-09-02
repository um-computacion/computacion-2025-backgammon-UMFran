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
    
    def get_dados(self):
        return list(self.__movimientos__)

    def usar_dado(self, valor: int):
        
        if valor not in self.__movimientos__:
            raise ValueError(f"El valor {valor} no se encuentra entre los generados")
        else:
            self.__movimientos__.remove(valor) #Elimina el valor usado por el jugador
    
    def hay_movimientos(self):
        if len(self.__movimientos__)> 0: #Verifica que hay moivimientos 
            return True
        else:
            return False
    
    def limpiar_dados(self): 
        self.__movimientos__.clear() #Limpia la lista de movimientos