#Requerimientos: guardar nombre/color/fichas

class Player:
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
            self.__fichas_restantes__ -= 1
            return True
        else: 
            return False
    
    def resetear_fichas(self):
        self.__fichas_restantes__ = self.__fichas__
    
    def __str__(self):
        return (f"El jugador: {self.__nombre__}, tiene color: {self.__color__} y le quedan {self.__fichas_restantes__} fichas")