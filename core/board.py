class Board:
    def __init__(self):
        self.__casillas__: list[list] = [
            ['white','white'], #0
            [], #1
            [], #2
            [], #3
            [], #4
            ['black', 'black', 'black', 'black', 'black'], #5
            #--------------------------------------------
            [], #6
            ['black', 'black', 'black'], #7
            [], #8
            [], #9
            [], #10
            ['white', 'white', 'white', 'white', 'white'], #11
            #--------------------------------------------
            ['black', 'black', 'black', 'black', 'black'], #12
            [], #13
            [], #14
            [], #15
            ['white', 'white', 'white'], #16git branch
            [], #17
            #--------------------------------------------
            ['white', 'white', 'white', 'white', 'white'], #18
            [], #19
            [], #20
            [], #21
            [], #22
            ['black', 'black'], #23
        ] #Definimos el tablero general de 24 casillas como una lista

        self.__banco__ = {"white": [], "black": []} #Lugar donde guardamos las fichas comidas

        self.__home__ = {"white": [], "black": []} #Lugar donde guardamos las fichas al finalizar el juego
    
    def mostrar_tablero(self):
        return self.__casillas__
    
    def remover_checker(self, punto: int):
        if punto < 0 or punto > 23:
            raise ValueError("punto inválido")
        elif not self.__casillas__[punto]:
            raise ValueError("No hay ficha en esta casilla")
        return self.__casillas__[punto].pop()
    
    def mover_checker(self, origen: int, destino: int):
        # --- INICIO DE LA CORRECCIÓN (Evitar ficha fantasma) ---
        
        # 1. Validar origen (asegurarse de que hay fichas)
        if not self.__casillas__[origen]:
            raise ValueError("No hay ficha en esta casilla")

        # 2. Obtener el color de la ficha SIN removerla
        ficha_color = self.__casillas__[origen][-1] # -1 para la de arriba

        # 3. Validar destino ANTES de mover nada
        if destino < 0 or destino > 23:
            raise ValueError("Punto inválido")
        
        casilla_destino = self.__casillas__[destino]
        if casilla_destino: # Si no está vacía
            color_destino = casilla_destino[0]
            cantidad_destino = len(casilla_destino)
            
            if color_destino != ficha_color and cantidad_destino > 1:
                # Esta es la validación de bloqueo
                raise ValueError("Punto inválido, hay más de 1 ficha de otro color")

        # 4. AHORA SÍ, remover la ficha
        ficha = self.remover_checker(origen) # Saca la ficha del origen

        # 5. Comer ficha enemiga (si aplica)
        if casilla_destino and casilla_destino[0] != ficha and len(casilla_destino) == 1: 
            enemigo = self.__casillas__[destino].pop()
            self.__banco__[enemigo].append(enemigo)
        
        # 6. Poner la ficha en el destino
        return self.__casillas__[destino].append(ficha)
        # --- FIN DE LA CORRECCIÓN ---
    
    def move_checker_banco(self, color: str, destino:int):
        
        if not self.__banco__[color]:
            raise ValueError("No hay fichas en el banco")

        # 1. Obtener el color SIN remover la ficha
        ficha_color = self.__banco__[color][0]

        # --- INICIO DE LA CORRECCIÓN (ZONA DE REINGRESO) ---
        # 2. Validar que el destino es la zona correcta
        if ficha_color == "white" and (destino < 0 or destino > 5):
             raise ValueError("Fichas blancas sólo reingresan en casillas 0-5")
        
        if ficha_color == "black" and (destino < 18 or destino > 23):
            raise ValueError("Fichas negras sólo reingresan en casillas 18-23")
        # --- FIN DE LA CORRECCIÓN ---

        # 3. Validar destino ANTES de mover nada
        if destino < 0 or destino > 23:
             # Esta validación es redundante ahora, pero la dejamos por seguridad
            raise ValueError("Punto inválido")

        casilla_destino = self.__casillas__[destino]
        if casilla_destino: # Si no está vacía
            color_destino = casilla_destino[0]
            cantidad_destino = len(casilla_destino)

            if color_destino != ficha_color and cantidad_destino > 1:
                # Esta es la validación de bloqueo
                raise ValueError("Punto inválido, hay más de 1 ficha de otro color")

        # 4. AHORA SÍ, remover la ficha del banco
        ficha = self.__banco__[color].pop()

        # 5. Comer ficha enemiga (si aplica)
        if casilla_destino and casilla_destino[0] != ficha and len(casilla_destino) == 1:
            enemigo = self.__casillas__[destino].pop()
            self.__banco__[enemigo].append(enemigo)
        
        # 6. Poner la ficha en el destino
        return self.__casillas__[destino].append(ficha)

    def sacar_ficha(self, color: str, origen: int):
        if self.__casillas__[origen] and self.__casillas__[origen][-1] == color:
            ficha = self.__casillas__[origen].pop()
            self.__home__[color].append(ficha)
            return True
        return False

    def consultar_checker(self, punto: int):
        if not self.__casillas__[punto]: #En caso que no haya ninguna ficha
            return None, 0
        return {f"En la posición {self.__casillas__[punto]} hay {len(self.__casillas__[punto])} del color {self.__casillas__[punto][0]}"} #Nos devuelve el estado de la casilla
    
    def estado_jugador(self, color: str):
        en_tablero = sum(1 for punto in self.__casillas__ for ficha in punto if ficha == color) #Cuenta fichas en el tablero
        en_home = len(self.__home__[color]) #Cuenta fichas guardadas
        en_banco = len(self.__banco__[color]) #Cuenta fichas comidas sin sacar

        return {f"Fichas de {color}: {en_tablero} en el tablero, {en_home} guardadas, {en_banco} comidas sin sacar"}
    
    def get_banco(self, color: str):
        return list(self.__banco__[color])

    def get_home(self, color: str):
        return list(self.__home__[color])