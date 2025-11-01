"""
Módulo CLI (Command Line Interface).

Contiene la clase 'cli' para interactuar con el juego
a través de una terminal de comandos.
"""
from core.backgammongame import BackgammonGame


class cli:
    """Gestiona la interfaz de usuario de línea de comandos."""
    def __init__(self, nombre1: str, nombre2: str):
        """Inicializa la CLI con una instancia del juego."""
        self.__game__ = BackgammonGame(nombre1, nombre2)

    def iniciar_juego(self):
        """Pide los nombres de los jugadores e inicia un nuevo juego."""
        nombre1 = str(input(
            "Ingrese el nombre del primer jugador (Fichas white): "
        ))
        nombre2 = str(input(
            "Ingrese el nombre del segundo jugador (Fichas black): "
        ))
        self.__game__ = BackgammonGame(nombre1, nombre2)
        print(
            f"El juego se inició, {nombre1} (white) vs {nombre2} (black)"
        )

    def _imprimir_tablero_visual(self):
        """Imprime una lista simple del estado de cada casilla (1-24)."""
        board_state = self.__game__.mostrar_tablero()  # Usa __contenedor__

        print("\n--- ESTADO DEL TABLERO ---")
        for i, casilla in enumerate(board_state):
            punto_num = i + 1  # Mostrar 1-24
            if not casilla:
                print(f"{punto_num}: vacío")
            else:
                cantidad = len(casilla)
                color = casilla[0]  # "white" o "black"
                print(f"{punto_num}: {cantidad} {color}")

        # Imprimir Barra y Afuera (usando los nombres de la nueva clase Board)
        print(f"Barra: {self.__game__.__board__.__barra__}")
        print(f"Afuera: {self.__game__.__board__.__afuera__}")

    def mostrar_juego(self):
        """Imprime el estado actual del tablero, turno y dados."""
        print("==========================================================")
        print(f"Turno de: {self.__game__.mostrar_turno()}")
        self._imprimir_tablero_visual()
        if not self.__game__.__dados__.hay_movimientos():
            print("Tirando dados...")
            self.__game__.tirar_dados()
        print("\nDados disponibles:", self.__game__.__dados__.get_dados())
        print("==========================================================")

    def mostrar_banco(self):
        """Imprime la cantidad de fichas comidas en el banco."""
        # --- Usar get_barra ---
        banco_white = self.__game__.__board__.get_barra("white")
        banco_black = self.__game__.__board__.get_barra("black")
        if banco_white or banco_black:
            print("\nFICHAS CAPTURADAS:")
            print(f"  Blancas: {len(banco_white)}")
            print(f"  Negras: {len(banco_black)}")

    def mostrar_home(self):
        """Imprime la cantidad de fichas sacadas (en casa)."""
        # ---Usar get_afuera ---
        home_white = self.__game__.__board__.get_afuera("white")
        home_black = self.__game__.__board__.get_afuera("black")
        print("\nFICHAS EN CASA:")
        print(f"  Blancas: {len(home_white)}")
        print(f"  Negras: {len(home_black)}")

    def mostrar_movimientos_posibles(self):
        """Calcula e imprime los movimientos legales desde la posición actual."""
        dados = self.__game__.__dados__.get_dados()
        color = self.__game__.__turno__.obtener_color()
        tablero = self.__game__.mostrar_tablero()

        print(f"\nMovimientos posibles para {color}:")
        for i, punto in enumerate(tablero):
            if punto and punto[-1] == color:
                for dado in dados:
                    if color == "white":
                        destino = i + dado
                    else:
                        destino = i - dado

                    if 0 <= destino <= 23:
                        # ---Mostrar 1-24 al usuario ---
                        print(f"  {i+1} → {destino+1} (usando dado {dado})")

    def mostrar_estado_completo(self):
        """Imprime un resumen completo del estado del juego."""
        print("="*50)
        print(f"BACKGAMMON - Turno de: {self.__game__.mostrar_turno()}")
        print("="*50)
        self._imprimir_tablero_visual()
        print("\nDados:", self.__game__.__dados__.get_dados())
        print(self.__game__.__board__.estado_jugador("white"))
        print(self.__game__.__board__.estado_jugador("black"))
        self.mostrar_banco()
        self.mostrar_home()
        print("="*50)

    def mostrar_ganador(self):
        """Comprueba e imprime si hay un ganador."""
        ganador = self.__game__.ganador()
        if ganador:
            print(f"El ganador del juego es {ganador}")
        else:
            print("El juego no ha finalizado")

    def jugar_turno(self):
        """Muestra el menú principal y maneja la entrada del usuario."""
        # Mostrar estado al inicio del turno
        self.mostrar_juego()

        while True:
            print("\nOpciones:")
            print("1. Mover ficha (usar números 1-24)")
            print("2. Reingresar ficha (usar números 1-24)")
            print("3. Sacar ficha (usar números 1-24)")
            print("4. Finalizar turno")
            print("5. Mostrar banco")
            print("6. Mostrar home")
            print("7. Mostrar movimientos posibles")
            print("8. Mostrar estado completo")
            print("9. Mostrar ganador")
            print("10. Reiniciar el juego")

            opcion = input("Elija acción: ")
            accion_realizada = False
            color_actual = self.__game__.__turno__.obtener_color()

            try:
                if opcion == "1":
                    # Restar 1 al input del usuario ---
                    origen = int(input("Origen (1-24): ")) - 1
                    destino = int(input("Destino (1-24): ")) - 1
                    self.__game__.mover(origen, destino)
                    accion_realizada = True
                elif opcion == "2":
                    fichas_en_barra = self.__game__.__board__.get_barra(color_actual)
                    if not fichas_en_barra:
                        print("Error: No tienes fichas en el banco para reingresar.")
                    else:
                        destino = int(input("Destino (1-24): ")) - 1
                        self.__game__.reingresar_ficha(destino)
                        accion_realizada = True
                elif opcion == "3":
                    tablero_actual = self.__game__.mostrar_tablero()
                    todas_en_cuadrante = True
                    rango_check = range(18) if color_actual == "white" else range(6, 24)
                    
                    for i in rango_check:
                        if color_actual in tablero_actual[i]:
                            todas_en_cuadrante = False
                            break
                    
                    if not todas_en_cuadrante:
                        print("\nError: No puedes sacar fichas.")
                        print("Aún tienes fichas fuera de tu cuadrante final.")
                    else:
                        origen = int(input("Origen (1-24): ")) - 1
                        self.__game__.sacar(origen)
                        accion_realizada = True
                elif opcion == "4":
                    self.__game__.finalizar_turno()
                    break # Salir del bucle de acciones (finaliza este turno)
                elif opcion == "5":
                    self.mostrar_banco()
                elif opcion == "6":
                    self.mostrar_home()
                elif opcion == "7":
                    self.mostrar_movimientos_posibles()
                elif opcion == "8":
                    self.mostrar_estado_completo()
                elif opcion == "9":
                    self.mostrar_ganador()
                elif opcion == "10":
                    print("El juego se reinició")
                    self.iniciar_juego()
                    break # Salir del bucle actual para reiniciar el turno
                else:
                    print("Opción inválida.")
            except ValueError as e:
                print(f"Error: {e}")
            except EOFError:
                print("\nSaliendo del juego.")
                self.__game__.__juego_terminado__ = True
                break

            if self.__game__.juego_terminado():
                break # Salir del bucle si la acción de sacar ganó

            if accion_realizada:
                # --- Mostrar tablero actualizado después de mover ---
                self._imprimir_tablero_visual()
                print("\nDados disponibles:", self.__game__.__dados__.get_dados())

                if not self.__game__.__dados__.hay_movimientos():
                    print("\nNo quedan más dados. Finalizando turno...")
                    self.__game__.finalizar_turno()
                    break # Salir del bucle de acciones (finaliza este turno)


if __name__ == "__main__":
    juego_cli = cli("Jugador1_temp", "Jugador2_temp")
    juego_cli.iniciar_juego()

    # Bucle de juego principal que llama a jugar_turno() repetidamente
    while not juego_cli.__game__.juego_terminado():
        juego_cli.jugar_turno()
    
    # Cuando el bucle termina (porque el juego terminó), mostrar el ganador final
    print("\n--- ¡PARTIDA FINALIZADA! ---")
    juego_cli.mostrar_ganador()
