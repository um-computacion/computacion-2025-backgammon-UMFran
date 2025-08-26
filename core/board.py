class Board:
    def __init__(self):
        self.__casillas__: list[list] = [
            ['white','white'], #0
            [], #1
            [], #2
            [], #3
            [], #4
            ['black', 'black', 'black', 'black', 'black'], #5
            #--------------------------------------------
            [], #6
            ['black', 'black', 'black'], #7
            [], #8
            [], #9
            [], #10
            ['white', 'white', 'white', 'white', 'white'], #11
            #--------------------------------------------
            ['black', 'black', 'black', 'black', 'black'], #12
            [], #13
            [], #14
            [], #15
            ['white', 'white', 'white'], #16
            [], #17
            #--------------------------------------------
            ['white', 'white', 'white', 'white', 'white'], #18
            [], #19
            [], #20
            [], #21
            [], #22
            ['black', 'black'], #23
        ] #Definimos el tablero general de 24 casillas como una lista

        self.__banco__ = {"white": [], "black": []} #Lugar donde guardamos las fichas comidas

        self.__home__ = {"white": [], "black": []} #Lugar donde guardamos las fichas al finalizar el juego
    
    def mostrar_tablero(self):
        return self.__casillas__
    
    def remover_checker(self, punto: int):
        if punto < 0 or punto > 23:
            raise ValueError("punto inválido")
        elif not self.__casillas__[punto]:
            raise ValueError("No hay ficha en esta casilla")
        return self.__casillas__[punto].pop()
    
    def mover_checker(self, origen: int, destino: int):
        ficha = self.remover_checker(origen) #Elegimos la ficha que vamos a mover y la eliminamos de la posición en la que está
        if destino < 0 or destino > 23:
            raise ValueError("Punto inválido") #Validamos que el destino esté entre los puntos válidos
        
        if self.__casillas__[destino] and self.__casillas__[destino][0] != ficha and len(self.__casillas__[destino]) > 1:
            raise ValueError("Punto inválido, hay más de 1 ficha de otro color")

        if self.__casillas__[destino] and self.__casillas__[destino][0] != ficha and len(self.__casillas__[destino]) == 1: #Comemos la ficha enemiga si es posible
            enemigo = self.__casillas__[destino].pop()
            self.__banco__[enemigo].append(enemigo)
        
        return self.__casillas__[destino].append(ficha) #Agregamos la ficha a la casilla