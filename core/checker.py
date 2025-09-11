class Checker:
    def __init__(self, color: str, posicion = None):
        self.__color__ = color
        self.__posicion__ = posicion

    def obtener_color(self):
        return self.__color__
    
    def obtener_posicion(self):
        return self.__posicion__
    
