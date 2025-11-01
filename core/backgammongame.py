"""
Módulo principal del juego Backgammon.

Contiene la clase BackgammonGame, que actúa como el motor
principal del juego, coordinando el tablero, los dados y los jugadores.
"""
from core.board import Board
from core.dice import Dice
from core.player import Player


class BackgammonGame:
    """
    Clase principal que gestiona la lógica y el estado del juego Backgammon.

    Atributos:
        __board__ (Board): Instancia del tablero de juego.
        __dados__ (Dice): Instancia de los dados.
        __jugador1__ (Player): Jugador 1 (fichas blancas).
        __jugador2__ (Player): Jugador 2 (fichas negras).
        __jugadores__ (set): Conjunto de los dos jugadores.
        __turno__ (Player): El jugador cuyo turno está activo.
        __turno_finalizado__ (bool): Estado del turno.
        __juego_terminado__ (bool): Estado del juego.
    """
    def __init__(self, jugador1: str, jugador2: str):
        """Inicializa el juego creando el tablero, dados y jugadores."""
        self.__board__ = Board()
        self.__dados__ = Dice()
        # --- Asignar "white" y "black" según la nueva lógica del tablero ---
        # "white" (antes "Negra") se mueve 0 -> 23
        self.__jugador1__ = Player(jugador1, "white")
        # "black" (antes "Blanca") se mueve 23 -> 0
        self.__jugador2__ = Player(jugador2, "black")
        self.__jugadores__ = {self.__jugador1__, self.__jugador2__}
        self.__turno__ = self.__jugador1__
        self.__turno_finalizado__ = False
        self.__juego_terminado__ = False

    def mostrar_jugador1(self):
        """Devuelve el objeto del jugador 1."""
        return self.__jugador1__

    def mostrar_jugador2(self):
        """Devuelve el objeto del jugador 2."""
        return self.__jugador2__

    def mostrar_turno(self):
        """Devuelve el nombre del jugador del turno actual."""
        return self.__turno__.obtener_nombre()

    def mostrar_tablero(self):
        """Devuelve la representación de la lista del tablero."""
        return self.__board__.mostrar_tablero()

    def tirar_dados(self):
        """
        Tira los dados si no hay movimientos pendientes.
        Devuelve la lista de dados disponibles.
        """
        if not self.__dados__.hay_movimientos():
            self.__dados__.tirar_dados()
        return self.__dados__.get_dados()

    # --- INICIO CORRECCIÓN 1: Método público para obtener dados ---
    def get_dados(self):
        """Devuelve la lista de dados disponibles."""
        return self.__dados__.get_dados()
    # --- FIN CORRECCIÓN 1 ---

    def mover(self, origen: int, destino: int):
        """
        Intenta mover una ficha de un origen a un destino.
        Valida la dirección, el dado y llama al tablero.
        """
        color = self.__turno__.obtener_color()
        # --- Lógica de dirección invertida ---
        # "white" (antes Negra) se mueve 0 -> 23 (destino > origen)
        if color == "white" and destino <= origen:
            raise ValueError("Movimiento inválido (fichas 'white' solo avanzan)")
        # "black" (antes Blanca) se mueve 23 -> 0 (destino < origen)
        if color == "black" and destino >= origen:
            raise ValueError("Movimiento inválido (fichas 'black' solo retroceden)")

        movimiento = abs(destino - origen)
        
        # --- INICIO CORRECCIÓN 2: Usar get_dados() en lugar de __movimientos__ ---
        if movimiento not in self.__dados__.get_dados():
        # --- FIN CORRECCIÓN 2 ---
            raise ValueError(
                f"Movimiento {movimiento} no disponible en dados "
                f"{self.__dados__.get_dados()}"
            )

        self.__board__.mover_checker(origen, destino)
        self.__dados__.usar_dado(movimiento)

    def reingresar_ficha(self, destino: int):
        """
        Intenta reingresar una ficha comida desde el banco al destino.
        Valida el dado y llama al tablero.
        """
        color = self.__turno__.obtener_color()
        
        # --- Lógica de dado invertida ---
        # "white" (antes Negra) reingresa en 0-5. Dado 1 -> destino 0.
        if color == "white":
            movimiento = destino + 1
        # "black" (antes Blanca) reingresa en 18-23. Dado 1 -> destino 23.
        else:  # black
            movimiento = 24 - destino

        # --- INICIO CORRECCIÓN 3: Usar get_dados() en lugar de __movimientos__ ---
        if movimiento not in self.__dados__.get_dados():
        # --- FIN CORRECCIÓN 3 ---
            raise ValueError(
                f"Movimiento {movimiento} no disponible en dados "
                f"{self.__dados__.get_dados()}"
            )

        self.__board__.move_checker_banco(color, destino)
        self.__dados__.usar_dado(movimiento)

    # pylint: disable=too-many-branches
    def sacar(self, origen: int):
        """
        Intenta sacar (bear off) una ficha del tablero.
        Valida que todas las fichas estén en el cuadrante final
        y que se tenga el dado correcto (exacto o mayor aplicable).
        """
        color = self.__turno__.obtener_color()
        tablero_actual = self.__board__.mostrar_tablero()
        
        # --- CORRECCIÓN 4: Usar el método público ---
        dados_actuales = self.get_dados()
        # --- FIN CORRECCIÓN 4 ---

        # --- Lógica de cuadrante invertida ---
        if color == "white":
            # "white" (antes Negra) saca de 18-23
            fichas_fuera_cuadrante = any(
                color in punto for i, punto in enumerate(tablero_actual)
                if i < 18
            )
        else:  # black
            # "black" (antes Blanca) saca de 0-5
            fichas_fuera_cuadrante = any(
                color in punto for i, punto in enumerate(tablero_actual)
                if i > 5
            )

        if fichas_fuera_cuadrante:
            msg = "No puedes sacar: aún tienes fichas fuera del cuadrante final"
            raise ValueError(msg)

        # --- Lógica de dado invertida ---
        # "white" (antes Negra) saca de 18-23. Ficha en 23 necesita 1 (24-23).
        movimiento_exacto = (24 - origen) if color == "white" else (origen + 1)
        # "black" (antes Blanca) saca de 0-5. Ficha en 0 necesita 1 (0+1).

        dado_a_usar = None

        if movimiento_exacto in dados_actuales:
            dado_a_usar = movimiento_exacto
        else:
            dados_mayores_disponibles = [
                d for d in dados_actuales if d > movimiento_exacto
            ]
            if dados_mayores_disponibles:
                es_la_mas_lejana = True
                # --- Lógica de "más lejana" invertida ---
                if color == "white":
                    # "white" (antes Negra): más lejana es la de índice menor (ej. 18)
                    for i in range(18, origen):
                        if "white" in tablero_actual[i]:
                            es_la_mas_lejana = False
                            break
                else:  # black
                    # "black" (antes Blanca): más lejana es la de índice mayor (ej. 5)
                    for i in range(origen + 1, 6):
                        if "black" in tablero_actual[i]:
                            es_la_mas_lejana = False
                            break

                if es_la_mas_lejana:
                    dado_a_usar = min(dados_mayores_disponibles)

        if dado_a_usar is None:
            msg = (
                f"No tienes dado ({movimiento_exacto} o > aplicable) "
                f"para sacar desde {origen}"
            )
            raise ValueError(msg)

        if self.__board__.sacar_ficha(color, origen):
            self.__turno__.restar_ficha()
            self.__dados__.usar_dado(dado_a_usar)
            if self.__turno__.ganar():
                self.__juego_terminado__ = True
            return True
        return False

    def cambiar_turno(self):
        """Cambia el jugador activo y limpia los dados."""
        self.__dados__.limpiar_dados()
        self.__turno__ = (
            self.__jugador2__ if self.__turno__ == self.__jugador1__
            else self.__jugador1__
        )
        self.__turno_finalizado__ = False

    def finalizar_turno(self):
        """Marca el turno como finalizado y lo cambia."""
        self.__turno_finalizado__ = True
        self.cambiar_turno()

    def estado_turno(self):
        """Devuelve el estado (fichas) del jugador activo."""
        color = self.__turno__.obtener_color()
        return self.__board__.estado_jugador(color)

    def ganador(self):
        """
        Devuelve el nombre del ganador si el juego ha terminado.
        Devuelve None si no hay ganador.
        """
        if self.__juego_terminado__:
            if self.__jugador1__.mostrar_fichas() == 0:
                return self.__jugador1__.obtener_nombre()
            if self.__jugador2__.mostrar_fichas() == 0:
                return self.__jugador2__.obtener_nombre()
        return None

    def juego_terminado(self):
        """
        Verifica si el juego ha terminado (un jugador tiene 0 fichas).
        Actualiza el estado interno del juego.
        """
        terminado = (
            self.__jugador1__.mostrar_fichas() == 0 or
            self.__jugador2__.mostrar_fichas() == 0
        )
        if terminado:
            self.__juego_terminado__ = True
        return self.__juego_terminado__

    def get_valid_moves(self, origen, dados):
        """
        Calcula los posibles destinos válidos desde un origen dado los dados.
        Args:
            origen (int or 'bar'): La casilla de origen (0-23) o 'bar'.
            dados (list): Lista de enteros con los valores de los dados.
        Returns:
            list: Lista de índices de casillas de destino válidas (int).
        """
        valid_destinos = []
        color = self.__turno__.obtener_color()
        tablero = self.__board__.mostrar_tablero()
        # --- Usar get_barra ---
        banco_propio = self.__board__.get_barra(color)

        if origen == 'bar':
            if not banco_propio:
                return []
            for dado in dados:
                # --- Lógica de reingreso invertida ---
                if color == "white": # "white" (antes Negra)
                    destino = dado - 1 # Dado 1 va a casilla 0
                    zona_valida = 0 <= destino <= 5
                else: # "black" (antes Blanca)
                    destino = 24 - dado # Dado 1 va a casilla 23
                    zona_valida = 18 <= destino <= 23

                if not zona_valida:
                    continue
                casilla_destino = tablero[destino]
                if (not casilla_destino or
                   (len(casilla_destino) == 1 and casilla_destino[0] != color) or
                   (casilla_destino and casilla_destino[0] == color)):
                    valid_destinos.append(destino)
        elif isinstance(origen, int):
            if banco_propio:
                return []
            if not tablero[origen] or tablero[origen][0] != color:
                return []
            for dado in dados:
                # ---Lógica de movimiento invertida ---
                if color == "white": # "white" (antes Negra)
                    destino = origen + dado
                else: # "black" (antes Blanca)
                    destino = origen - dado

                if not 0 <= destino <= 23:
                    continue
                casilla_destino = tablero[destino]
                if (not casilla_destino or
                   (len(casilla_destino) == 1 and casilla_destino[0] != color) or
                   (casilla_destino and casilla_destino[0] == color)):
                    valid_destinos.append(destino)

        return list(set(valid_destinos))
