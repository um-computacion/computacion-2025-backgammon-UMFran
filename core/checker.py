class Checker:
    def __init__(self, color: str, posicion = None):
        self.__color__ = color
        self.__posicion__ = posicion

    def obtener_color(self):
        return self.__color__
    
    def obtener_posicion(self):
        return self.__posicion__
    
    def posicion_nueva(self, nueva_posicion):
        return self.__posicion__ == nueva_posicion
    
    def esta_banco(self):
        return self.__posicion__ == "banco"
    
    def esta_home(self):
        return self.__posicion__ == "home"