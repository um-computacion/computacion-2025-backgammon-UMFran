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
        """Inicializa el tablero con la configuración estándar de fichas."""
        self.__casillas__: list[list] = [
            ['white', 'white'],  # 0
            [],  # 1
            [],  # 2
            [],  # 3
            [],  # 4
            ['black', 'black', 'black', 'black', 'black'],  # 5
            # --------------------------------------------
            [],  # 6
            ['black', 'black', 'black'],  # 7
            [],  # 8
            [],  # 9
            [],  # 10
            ['white', 'white', 'white', 'white', 'white'],  # 11
            # --------------------------------------------
            ['black', 'black', 'black', 'black', 'black'],  # 12
            [],  # 13
            [],  # 14
            [],  # 15
            ['white', 'white', 'white'],  # 16
            [],  # 17
            # --------------------------------------------
            ['white', 'white', 'white', 'white', 'white'],  # 18
            [],  # 19
            [],  # 20
            [],  # 21
            [],  # 22
            ['black', 'black'],  # 23
        ]  # Tablero general de 24 casillas

        # Lugar donde guardamos las fichas comidas
        self.__banco__ = {"white": [], "black": []}

        # Lugar donde guardamos las fichas al finalizar el juego
        self.__home__ = {"white": [], "black": []}

    def mostrar_tablero(self):
        """Devuelve la lista de listas que representa las casillas."""
        return self.__casillas__

    def remover_checker(self, punto: int):
        """
        Saca la ficha superior de una casilla (punto).
        Lanza ValueError si el punto es inválido o está vacío.
        """
        if not 0 <= punto <= 23:
            raise ValueError("punto inválido")
        if not self.__casillas__[punto]:
            raise ValueError("No hay ficha en esta casilla")
        return self.__casillas__[punto].pop()

    def mover_checker(self, origen: int, destino: int):
        """
        Mueve una ficha de origen a destino.
        Valida que el destino no esté bloqueado.
        Come fichas enemigas si es un 'blot'.
        """
        if not self.__casillas__[origen]:
            raise ValueError("No hay ficha en esta casilla")

        ficha_color = self.__casillas__[origen][-1]

        if not 0 <= destino <= 23:
            raise ValueError("Punto inválido")

        casilla_destino = self.__casillas__[destino]
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
            enemigo = self.__casillas__[destino].pop()
            self.__banco__[enemigo].append(enemigo)

        return self.__casillas__[destino].append(ficha)

    def move_checker_banco(self, color: str, destino: int):
        """
        Mueve una ficha desde el banco (barra) al destino.
        Valida la zona de reingreso y que no esté bloqueado.
        """
        if not self.__banco__[color]:
            raise ValueError("No hay fichas en el banco")

        ficha_color = self.__banco__[color][0]

        if ficha_color == "white" and not 0 <= destino <= 5:
            raise ValueError("Fichas blancas sólo reingresan en casillas 0-5")

        if ficha_color == "black" and not 18 <= destino <= 23:
            raise ValueError("Fichas negras sólo reingresan en casillas 18-23")

        casilla_destino = self.__casillas__[destino]
        if casilla_destino:
            color_destino = casilla_destino[0]
            cantidad_destino = len(casilla_destino)

            if color_destino != ficha_color and cantidad_destino > 1:
                raise ValueError(
                    "Punto inválido, hay más de 1 ficha de otro color"
                )

        ficha = self.__banco__[color].pop()

        if casilla_destino and casilla_destino[0] != ficha:
            enemigo = self.__casillas__[destino].pop()
            self.__banco__[enemigo].append(enemigo)

        return self.__casillas__[destino].append(ficha)

    def sacar_ficha(self, color: str, origen: int):
        """
        Mueve una ficha del origen a la zona 'home' (sacar del juego).
        Devuelve True si tuvo éxito, False si no.
        """
        if self.__casillas__[origen] and self.__casillas__[origen][-1] == color:
            ficha = self.__casillas__[origen].pop()
            self.__home__[color].append(ficha)
            return True
        return False

    def consultar_checker(self, punto: int):
        """
        Devuelve el estado de una casilla (color y cantidad).
        Devuelve (None, 0) si está vacía.
        """
        if not self.__casillas__[punto]:  # En caso que no haya ninguna ficha
            return None, 0
        # Nos devuelve el estado de la casilla
        casilla = self.__casillas__[punto]
        msg = (
            f"En la posición {casilla} hay {len(casilla)} "
            f"del color {casilla[0]}"
        )
        return {msg}

    def estado_jugador(self, color: str):
        """
        Devuelve un resumen del estado de todas las fichas de un jugador
        (en tablero, en home, en banco).
        """
        en_tablero = sum(
            1 for punto in self.__casillas__ for ficha in punto
            if ficha == color
        )
        en_home = len(self.__home__[color])
        en_banco = len(self.__banco__[color])

        msg = (
            f"Fichas de {color}: {en_tablero} en el tablero, "
            f"{en_home} guardadas, {en_banco} comidas sin sacar"
        )
        return {msg}

    def get_banco(self, color: str):
        """Devuelve una copia de la lista de fichas en el banco."""
        return list(self.__banco__[color])

    def get_home(self, color: str):
        """Devuelve una copia de la lista de fichas en el home."""
        return list(self.__home__[color])
