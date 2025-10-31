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
    
    def mostrar_banco(self):
        banco_white = self.__game__.__board__.get_banco("white")
        banco_black = self.__game__.__board__.get_banco("black")
        if banco_white or banco_black:
            print(f"\nFICHAS CAPTURADAS:")
            print(f"  Blancas: {len(banco_white)}")
            print(f"  Negras: {len(banco_black)}")
    
    def mostrar_home(self):
        home_white = self.__game__.__board__.get_home("white")
        home_black = self.__game__.__board__.get_home("black")
        print(f"\nFICHAS EN CASA:")
        print(f"  Blancas: {len(home_white)}")
        print(f"  Negras: {len(home_black)}")
    
    def mostrar_movimientos_posibles(self):
        dados = self.__game__.__dados__.get_dados()
        color = self.__game__.__turno__.obtener_color()
        tablero = self.__game__.mostrar_tablero()
        
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
    
    def mostrar_estado_completo(self):
        print("="*50)
        print(f"BACKGAMMON - Turno de: {self.__game__.mostrar_turno()}")
        print("="*50)
        self.__game__.mostrar_tablero()
        self.__game__.__dados__.get_dados()
        self.__game__.__board__.estado_jugador("white")
        self.__game__.__board__.estado_jugador("black")
        self.mostrar_banco()
        print("="*50)
    
    def mostrar_ganador(self):
        ganador = self.__game__.ganador()
        if ganador:
            print(f"El ganador del juego es {ganador}")
        else:
            print("El juego no ha finalizado")

    def jugar_turno(self):
        self.mostrar_juego()
        while True:
            print("\nOpciones:")
            print("1. Mover ficha")
            print("2. Reingresar ficha")
            print("3. Sacar ficha")
            print("4. Finalizar turno")
            print("5. Mostrar banco")
            print("6. Mostrar home")
            print("7. Mostrar movimientos posibles")
            print("8. Mostrar estado completo")
            print("9. Mostrar ganador")
            print("10. Reiniciar el juego")

            opcion = input("Elija acción: ")

            try:
                if opcion == "1":
                    origen = int(input("Origen: "))
                    destino = int(input("Destino: "))
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
                    self.inicar_juego()

                else:
                    print("Opción inválida.")

            except Exception as e:
                print("Error:", e)