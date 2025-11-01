"""
Módulo del Tablero de Backgammon.

Contiene la clase Board, que gestiona el estado de las casillas,
la barra de fichas comidas y la zona home de fichas sacadas.
"""


class Board:
    """
    Representa el tablero de Backgammon con sus 24 puntos,
    barra (banco) y zona final (home).
    """
    def __init__(self):
        """Inicializa el tablero con las posiciones iniciales del Backgammon."""
        # Contenedor principal: lista de 24 puntos
        self.__contenedor__ = [[] for _ in range(24)]

        # --- Configuración con tus colores "white" y "black" ---
        # Jugador "white" (mueve 0 -> 23)
        self.__contenedor__[0] = ["white"] * 2
        self.__contenedor__[11] = ["white"] * 5
        self.__contenedor__[16] = ["white"] * 3
        self.__contenedor__[18] = ["white"] * 5

        # Jugador "black" (mueve 23 -> 0)
        self.__contenedor__[23] = ["black"] * 2
        self.__contenedor__[12] = ["black"] * 5
        self.__contenedor__[7] = ["black"] * 3
        self.__contenedor__[5] = ["black"] * 5
        # --- Fin de la configuración ---

        # Diccionario para fichas capturadas (en la barra)
        self.__barra__ = {"white": [], "black": []}

        # Diccionario para fichas que ya salieron del tablero
        self.__afuera__ = {"white": [], "black": []}

    def mostrar_tablero(self):
        """Devuelve la lista de listas que representa las casillas."""
        return self.__contenedor__

    def remover_checker(self, punto: int):
        """
        Saca la ficha superior de una casilla (punto).
        Lanza ValueError si el punto es inválido o está vacío.
        """
        if not 0 <= punto <= 23:
            raise ValueError("punto inválido")
        if not self.__contenedor__[punto]:
            raise ValueError("No hay ficha en esta casilla")
        return self.__contenedor__[punto].pop()

    def mover_checker(self, origen: int, destino: int):
        """
        Mueve una ficha de origen a destino.
        Valida que el destino no esté bloqueado.
        Come fichas enemigas si es un 'blot'.
        """
        if not self.__contenedor__[origen]:
            raise ValueError("No hay ficha en esta casilla")

        ficha_color = self.__contenedor__[origen][-1]

        if not 0 <= destino <= 23:
            raise ValueError("Punto inválido")

        casilla_destino = self.__contenedor__[destino]
        if casilla_destino:
            color_destino = casilla_destino[0]
            cantidad_destino = len(casilla_destino)

            if color_destino != ficha_color and cantidad_destino > 1:
                raise ValueError(
                    "Punto inválido, hay más de 1 ficha de otro color"
                )

        ficha = self.remover_checker(origen)

        if casilla_destino and casilla_destino[0] != ficha:
            # Es un 'blot' (una sola ficha).
            enemigo = self.__contenedor__[destino].pop()
            self.__barra__[enemigo].append(enemigo)

        return self.__contenedor__[destino].append(ficha)

    def move_checker_banco(self, color: str, destino: int):
        """
        Mueve una ficha desde el banco (barra) al destino.
        Valida la zona de reingreso y que no esté bloqueado.
        """
        if not self.__barra__[color]:
            raise ValueError("No hay fichas en el banco")

        ficha_color = self.__barra__[color][0]

        # "white" (antes Negra) reingresa en 0-5
        if ficha_color == "white" and not 0 <= destino <= 5:
            raise ValueError("Fichas blancas sólo reingresan en casillas 0-5")

        # "black" (antes Blanca) reingresa en 18-23
        if ficha_color == "black" and not 18 <= destino <= 23:
            raise ValueError("Fichas negras sólo reingresan en casillas 18-23")

        casilla_destino = self.__contenedor__[destino]
        if casilla_destino:
            color_destino = casilla_destino[0]
            cantidad_destino = len(casilla_destino)

            if color_destino != ficha_color and cantidad_destino > 1:
                raise ValueError(
                    "Punto inválido, hay más de 1 ficha de otro color"
                )

        ficha = self.__barra__[color].pop()

        if casilla_destino and casilla_destino[0] != ficha:
            enemigo = self.__contenedor__[destino].pop()
            self.__barra__[enemigo].append(enemigo)

        return self.__contenedor__[destino].append(ficha)

    def sacar_ficha(self, color: str, origen: int):
        """
        Mueve una ficha del origen a la zona 'afuera' (sacar del juego).
        Devuelve True si tuvo éxito, False si no.
        """
        if self.__contenedor__[origen] and \
           self.__contenedor__[origen][-1] == color:
            ficha = self.__contenedor__[origen].pop()
            self.__afuera__[color].append(ficha)
            return True
        return False

    def consultar_checker(self, punto: int):
        """
        Devuelve el estado de una casilla (color y cantidad).
        Devuelve (None, 0) si está vacía.
        """
        if not self.__contenedor__[punto]:
            return None, 0
        casilla = self.__contenedor__[punto]
        msg = (
            f"En la posición {casilla} hay {len(casilla)} "
            f"del color {casilla[0]}"
        )
        return {msg}

    def estado_jugador(self, color: str):
        """
        Devuelve un resumen del estado de todas las fichas de un jugador
        (en tablero, en afuera, en barra).
        """
        en_tablero = sum(
            1 for punto in self.__contenedor__ for ficha in punto
            if ficha == color
        )
        en_afuera = len(self.__afuera__[color])
        en_barra = len(self.__barra__[color])

        msg = (
            f"Fichas de {color}: {en_tablero} en el tablero, "
            f"{en_afuera} guardadas, {en_barra} comidas sin sacar"
        )
        return {msg}

    def get_barra(self, color: str):
        """Devuelve una copia de la lista de fichas en el banco."""
        return list(self.__barra__[color])

    def get_afuera(self, color: str):
        """Devuelve una copia de la lista de fichas en el home."""
        return list(self.__afuera__[color])
