from core.backgammongame import backgammongame

class cli:
    def __init__(self, nombre1: str, nombre2: str):
        self.__game__ = backgammongame(nombre1, nombre2)
    
    def inicar_juego(self):
        nombre1 = str(input("Ingrese el nombre del primer jugador (fichas blancas): "))
        nombre2 = str(input("Ingrese el nombre del segundo jugador (fichas negras): "))
        self.__game__ = backgammongame(nombre1, nombre2)
        print(f"El juego se inició, {nombre1} le tocan fichas blancas y {nombre2} le tocan fichas negras")
    
    def mostrar_juego(self):
        print("=====================================")
        print("Turno:", self.__game__.mostrar_turno())
        print("Tablero:", self.__game__.mostrar_tablero())
        # Solo tira dados si no hay movimientos disponibles
        if not self.__game__.__dados__.hay_movimientos():
            self.__game__.tirar_dados()
        print("Dados disponibles:", self.__game__.__dados__.get_dados())
        print("=====================================")
    
    def jugar_turno(self):
        self.mostrar_juego()
        while True:
            print("\nOpciones:")
            print("1. Mover ficha")
            print("2. Reingresar ficha")
            print("3. Sacar ficha")
            print("4. Finalizar turno")
            opcion = input("Elija acción: ")

            try:
                if opcion == "1":
                    origen = int(input("Origen: "))
                    destino = int(input("Destino: "))
                    # Validación de dirección eliminada - se maneja en la lógica del juego
                    self.__game__.mover(origen, destino)

                elif opcion == "2":
                    destino = int(input("Destino: "))
                    self.__game__.reingresar_ficha(destino)

                elif opcion == "3":
                    origen = int(input("Origen: "))
                    self.__game__.sacar(origen)

                elif opcion == "4":
                    self.__game__.finalizar_turno()
                    break
                else:
                    print("Opción inválida.")
            except Exception as e:
                print("Error:", str(e))