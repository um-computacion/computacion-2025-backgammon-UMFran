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
    def mostrar_jugador1(self):
        return self.__jugador1__
    
    def mostrar_jugador2(self):
        return self.__jugador2__
    
    def mostrar_turno(self):
        return self.__turno__.obtener_nombre()
    
    def mostrar_tablero(self):
        return self.__board__.mostrar_tablero()
    
    # Funciones de dados
    def tirar_dados(self):
        # Solo tira dados si no hay movimientos disponibles
        if not self.__dados__.hay_movimientos():
            self.__dados__.tirar_dados()
        return self.__dados__.get_dados()  # Me devuelve los números que salieron
    
    def mover(self, origen: int, destino: int):
        movimiento = abs(destino - origen)

        # Verificamos si está disponible el movimiento
        if movimiento not in self.__dados__.__movimientos__:
            raise ValueError(f"Movimiento {movimiento} no está disponible en los dados {self.__dados__.__movimientos__}")

        self.__board__.mover_checker(origen, destino)  # Movemos la ficha
        self.__dados__.usar_dado(movimiento)  # Sacamos el movimiento de los dados
    
    def reingresar_ficha(self, destino: int):
        color = self.__turno__.obtener_color() 
        movimiento = destino + 1

        # Verificamos si está disponible el movimiento
        if movimiento not in self.__dados__.__movimientos__:
            raise ValueError(f"Movimiento {movimiento} no está disponible en los dados {self.__dados__.__movimientos__}")
        
        self.__board__.move_checker_banco(color, destino)
        self.__dados__.usar_dado(movimiento)
    
    def sacar(self, origen: int):
        color = self.__turno__.obtener_color()

        if color == "white":
            fichas_fuera_cuadrante = any(
                color in punto for i, punto in enumerate(self.__board__.mostrar_tablero()) if i < 18
            )
        else:  # black
            fichas_fuera_cuadrante = any(
                color in punto for i, punto in enumerate(self.__board__.mostrar_tablero()) if i > 5
            )

        if fichas_fuera_cuadrante:
            raise ValueError(f"El jugador {color} no puede sacar fichas: todavía tiene piezas fuera de su cuadrante final")

        # Calcular el valor necesario para sacar
        movimiento = 24 - origen if color == "white" else origen + 1

        # Validar dado
        if movimiento not in self.__dados__.__movimientos__:
            raise ValueError(f"No puedes sacar desde {origen}, el valor {movimiento} no está en los dados {self.__dados__.__movimientos__}")

        # Intentar sacar ficha
        if self.__board__.sacar_ficha(color, origen):
            self.__turno__.restar_ficha()
            self.__dados__.usar_dado(movimiento)
            return True
        return False

    # Funciones del turno
    def cambiar_turno(self):
        if self.__turno__ == self.__jugador1__:
            self.__dados__.limpiar_dados()  # Elimina los dados del turno anterior
            self.__turno__ = self.__jugador2__  # Cambia de jugador
        else:
            self.__dados__.limpiar_dados()  # Elimina los dados del turno anterior
            self.__turno__ = self.__jugador1__  # Cambia de jugador
    
    def finalizar_turno(self):
        self.__turno_finalizado__ = True
        if not self.__dados__.hay_movimientos():  # Corrobora que no quedan movimientos posibles
            self.cambiar_turno()
        else:
            self.__turno_finalizado__ = False
    
    def estado_turno(self):
        color = self.__turno__.obtener_color()
        return self.__board__.estado_jugador(color)

    # Funciones para ganar
    def ganador(self):
        for jugador in self.__jugadores__:  # Revisa la lista de jugadores
            if jugador.ganar():  # Corrobora condición de ganar
                self.__juego_terminado__ = True 
                return jugador.obtener_nombre()  # Me devuelve el nombre del ganador
        return None
    
    def juego_terminado(self):
        return self.__jugador1__.ganar() or self.__jugador2__.ganar()  # Finaliza el juego si cualquiera de los jugadores gana