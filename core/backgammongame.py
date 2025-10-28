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
        self.__juego_terminado__ = False # Añadir estado para controlar fin

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
        return self.__dados__.get_dados()

    def mover(self, origen: int, destino: int):
        # Validar dirección
        color = self.__turno__.obtener_color()
        if color == "white" and destino <= origen:
            raise ValueError("Movimiento inválido (blancas solo avanzan)")
        if color == "black" and destino >= origen:
            raise ValueError("Movimiento inválido (negras solo retroceden)")

        movimiento = abs(destino - origen)
        if movimiento not in self.__dados__.__movimientos__:
            raise ValueError(f"Movimiento {movimiento} no disponible en dados {self.__dados__.__movimientos__}")

        self.__board__.mover_checker(origen, destino)
        self.__dados__.usar_dado(movimiento)

    def reingresar_ficha(self, destino: int):
        color = self.__turno__.obtener_color()
        movimiento = destino + 1 if color == "white" else 24 - destino

        if movimiento not in self.__dados__.__movimientos__:
            raise ValueError(f"Movimiento {movimiento} no disponible en dados {self.__dados__.__movimientos__}")

        # La función del board valida la zona de reingreso
        self.__board__.move_checker_banco(color, destino)
        self.__dados__.usar_dado(movimiento)

    def sacar(self, origen: int):
        color = self.__turno__.obtener_color()
        tablero_actual = self.__board__.mostrar_tablero()
        dados_actuales = self.__dados__.get_dados() # Obtener copia

        # 1. Validar que todas las fichas estén en el cuadrante final
        if color == "white":
            fichas_fuera_cuadrante = any(color in punto for i, punto in enumerate(tablero_actual) if i < 18)
        else: # black
            fichas_fuera_cuadrante = any(color in punto for i, punto in enumerate(tablero_actual) if i > 5)

        if fichas_fuera_cuadrante:
            raise ValueError("No puedes sacar: aún tienes fichas fuera del cuadrante final")

        # 2. Calcular el valor exacto necesario para sacar
        movimiento_exacto = (24 - origen) if color == "white" else (origen + 1)

        dado_a_usar = None

        # 3. ¿Está el dado exacto disponible?
        if movimiento_exacto in dados_actuales:
            dado_a_usar = movimiento_exacto
        else:
            # 4. No está el exacto. ¿Hay un dado mayor disponible?
            dados_mayores_disponibles = [d for d in dados_actuales if d > movimiento_exacto]
            if dados_mayores_disponibles:
                # 5. Sí hay dados mayores. ¿Es esta la ficha más lejana?
                es_la_mas_lejana = True
                if color == "white":
                    # Chequear si hay fichas blancas ANTES de 'origen' (índices menores) en el cuadrante
                    for i in range(18, origen):
                        if "white" in tablero_actual[i]:
                            es_la_mas_lejana = False
                            break
                else: # black
                    # Chequear si hay fichas negras DESPUÉS de 'origen' (índices mayores) en el cuadrante
                    for i in range(origen + 1, 6):
                         if "black" in tablero_actual[i]:
                            es_la_mas_lejana = False
                            break

                # Si es la ficha más lejana, podemos usar un dado mayor
                if es_la_mas_lejana:
                    # Usamos el dado mayor más PEQUEÑO disponible
                    dado_a_usar = min(dados_mayores_disponibles)

        # 6. Validar si encontramos un dado válido
        if dado_a_usar is None:
            raise ValueError(f"No tienes dado ({movimiento_exacto} o > aplicable) para sacar desde {origen}")

        # 7. Intentar sacar ficha usando el dado encontrado
        if self.__board__.sacar_ficha(color, origen):
            restado = self.__turno__.restar_ficha() # Guardar el resultado por si acaso
            if not restado:
                 print(f"Advertencia: restar_ficha() devolvió False al sacar de {origen}") # Para depuración
            self.__dados__.usar_dado(dado_a_usar)
            # Verificar si este movimiento ganó el juego
            if self.__turno__.ganar():
                self.__juego_terminado__ = True
            return True

        return False # Fallback

    # Funciones del turno
    def cambiar_turno(self):
        self.__dados__.limpiar_dados()
        self.__turno__ = self.__jugador2__ if self.__turno__ == self.__jugador1__ else self.__jugador1__
        self.__turno_finalizado__ = False # Reiniciar estado para el nuevo turno

    def finalizar_turno(self):
        self.__turno_finalizado__ = True
        self.cambiar_turno()

    def estado_turno(self):
        color = self.__turno__.obtener_color()
        return self.__board__.estado_jugador(color)

    # Funciones para ganar
    def ganador(self):
        # Devuelve el nombre del ganador si el juego ha terminado, sino None
        if self.__juego_terminado__:
             # Determinar quién ganó (quien tiene 0 fichas)
             if self.__jugador1__.mostrar_fichas() == 0:
                 return self.__jugador1__.obtener_nombre()
             elif self.__jugador2__.mostrar_fichas() == 0:
                 return self.__jugador2__.obtener_nombre()
             else:
                 # Esto no debería pasar si juego_terminado es True
                 return "Error: Juego terminado sin ganador claro"
        return None

    def juego_terminado(self):
        # Verifica si algún jugador tiene 0 fichas restantes
        # y actualiza el estado interno si es necesario.
        j1_fichas = self.__jugador1__.mostrar_fichas()
        j2_fichas = self.__jugador2__.mostrar_fichas()
        
        terminado = (j1_fichas == 0) or (j2_fichas == 0)
        
        if terminado and not self.__juego_terminado__:
            #print(f"Debug: Juego terminado detectado. Fichas: J1={j1_fichas}, J2={j2_fichas}") # Debug
            self.__juego_terminado__ = True
        
        # Devuelve el estado actual (puede ser True aunque no se haya detectado antes)
        return self.__juego_terminado__


    def get_valid_moves(self, origen, dados):
        """Calcula los posibles destinos válidos desde un origen dado los dados."""
        valid_destinos = []
        color = self.__turno__.obtener_color()
        tablero = self.__board__.mostrar_tablero()
        banco_propio = self.__board__.get_banco(color)

        if origen == 'bar':
            if not banco_propio: return []
            for dado in dados:
                destino = (dado - 1) if color == "white" else (24 - dado)
                zona_valida = (0 <= destino <= 5) if color == "white" else (18 <= destino <= 23)
                if not zona_valida: continue

                casilla_destino = tablero[destino]
                # Puede mover si está vacía, es blot enemigo, o es propia
                if not casilla_destino or \
                   (len(casilla_destino) == 1 and casilla_destino[0] != color) or \
                   (casilla_destino and casilla_destino[0] == color):
                    valid_destinos.append(destino)

        elif isinstance(origen, int):
            if banco_propio: return [] # No puede mover si hay fichas en banco
            if not tablero[origen] or tablero[origen][0] != color: return [] # Origen inválido

            for dado in dados:
                destino = (origen + dado) if color == "white" else (origen - dado)
                if not (0 <= destino <= 23): continue # Fuera del tablero

                casilla_destino = tablero[destino]
                # Puede mover si está vacía, es blot enemigo, o es propia
                if not casilla_destino or \
                   (len(casilla_destino) == 1 and casilla_destino[0] != color) or \
                   (casilla_destino and casilla_destino[0] == color):
                     valid_destinos.append(destino)

        return list(set(valid_destinos)) # Eliminar duplicados