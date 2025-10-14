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
        
        # Calcular el valor del dado necesario para este movimiento
        if color == "black":
            movimiento_necesario = destino + 1 # Asumiendo que los puntos 1-6 son indices 0-5
        else: # "white"
            movimiento_necesario = 24 - destino # Asumiendo que los puntos 19-24 son indices 18-23
        
        # Verificamos si el dado está disponible
        if movimiento_necesario not in self.__dados__.get_dados(): # Usar un getter si es posible
            raise ValueError(f"Movimiento {movimiento_necesario} no está disponible.")
        
        # Mover la ficha y usar el dado
        self.__board__.move_checker_banco(color, destino)
        self.__dados__.usar_dado(movimiento_necesario)
    
    def sacar(self, origen: int):
        color = self.__turno__.obtener_color()
        dados_disponibles = self.__dados__.get_dados() # ej: [5, 2]

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

        movimiento_exacto = 0
        if color == "white":
            # Las blancas sacan desde 19-24
            if not (19 <= origen <= 24):
                raise ValueError("Las fichas blancas solo pueden sacar desde los puntos 19 a 24.")
            movimiento_exacto = 25 - origen
        else: # "black"
            # Las negras sacan desde 1-6
            if not (1 <= origen <= 6):
                raise ValueError("Las fichas negras solo pueden sacar desde los puntos 1 a 6.")
            movimiento_exacto = origen
            
        dado_a_usar = 0
        
        if movimiento_exacto in dados_disponibles:
            dado_a_usar = movimiento_exacto
        else:
            dado_mayor_disponible = max(dados_disponibles) if dados_disponibles else 0
            if dado_mayor_disponible > movimiento_exacto:
                punto_mas_alto = self.__board__.obtener_punto_mas_alto(color)
                if origen == punto_mas_alto:
                    dado_a_usar = dado_mayor_disponible
        
        if dado_a_usar == 0:
            raise ValueError(f"No tienes un dado válido para sacar una ficha desde el punto {origen}.")

        if self.__board__.sacar_ficha(color, origen):
            self.__turno__.restar_ficha()      # El jugador tiene una ficha menos en el tablero
            self.__dados__.usar_dado(dado_a_usar) # Se consume el dado utilizado
            print(f"Ficha {color} sacada desde {origen} usando un dado de {dado_a_usar}")
            return True
        
        return False
    
    def mostrar_movimientos_posibles(self):
        dados = self.__dados__.get_dados()
        color = self.__turno__.obtener_color()
        tablero = self.mostrar_tablero()
        
        print(f"\nMovimientos posibles para {color}:")
        for i, punto in enumerate(tablero):
            if punto and punto[-1] == color:  # Si hay ficha del color actual
                for dado in dados:
                    if color == "white":
                        destino = i + dado
                    else:
                        destino = i - dado
                    
                    if 0 <= destino <= 23:
                        print(f"  {i} → {destino} (usando dado {dado})")
    

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