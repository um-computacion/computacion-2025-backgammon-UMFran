from core.backgammongame import backgammongame

class cli:
    def __init__(self, nombre1: str, nombre2:str):
        self.game = backgammongame(nombre1, nombre2)
    
    def inicar_juego(self):
        nombre1 = str(input("Ingrese el nombre del primer jugador (fichas blancas): "))
        nombre2 = str(input("Ingrese el nombre del segundo jugador (fichas negras): "))
        self.game = backgammongame(nombre1, nombre2)
        print(f"El juego se inició, {nombre1} le tocan fichas blancas y {nombre2} le tocan fichas negras")
