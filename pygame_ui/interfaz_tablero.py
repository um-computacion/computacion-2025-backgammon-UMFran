import pygame
from core.backgammongame import backgammongame

class TableroGrafico:
    def __init__(self, pantalla):
        juego = backgammongame("jugador1", "Jugador2")
        self.pantalla = pantalla
        self.ancho = self.pantalla.get_width()
        self.alto = self.pantalla.get_height()
        
        # Ajustamos dimensiones para dejar espacio para info
        self.ancho_tablero = self.ancho * 0.9
        self.margen_x = (self.ancho - self.ancho_tablero) / 2
        
        self.ancho_triangulo = self.ancho_tablero / 13
        self.ancho_barra = self.ancho_triangulo
        self.alto_triangulo = self.alto * 0.4
        self.radio_ficha = (self.ancho_triangulo / 2) * 0.8
        
        # Fuentes
        self.fuente_dados = pygame.font.SysFont("arial", 40, bold=True)
        self.fuente_info = pygame.font.SysFont("arial", 24)
    
    def dibujar_tablero(self):
        colores= [(180, 100, 80), (250, 220, 200)] #Color triangulos

        color_barra_central = (139, 69, 19)
        color_borde = (60, 40, 30)
        color_fondo = (220, 190, 160)
        self.pantalla.fill(color_fondo)

        #Barra central
        x_barra = x_barra = (self.ancho / 2) - (self.ancho_barra / 2)
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(x_barra, 0, self.ancho_barra, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(x_barra, 0, self.ancho_barra, self.alto),2)
        
        #Parte superior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte superior derecha(6 triangulos)
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)
        
           #Parte inferior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte inferior derecha (6 triangulos)
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame.draw.polygon(self.pantalla, colores[i % 2], puntos)
        
        # Barra exterior izquierda
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(0, 0, self.ancho_barra // 2, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(0, 0, self.ancho_barra // 2, self.alto),2)

        # Barra exterior derecha
        pygame.draw.rect(self.pantalla,color_barra_central,
            pygame.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto))
        pygame.draw.rect(self.pantalla,color_borde,
            pygame.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto),2)
    
    def _get_coords_from_point(self, punto: int):
        """Función clave: Convierte un número de punto (1-24) a coordenadas de píxel (x, y)"""
        if not (1 <= punto <= 24): return None, None
        
        # Parte superior (puntos 1 a 12)
        if 1 <= punto <= 12:
            y_base = self.radio_ficha + 10
            step = self.radio_ficha * 2
            
            if 1 <= punto <= 6: # Cuadrante superior derecho
                col = 6 - punto
                x = self.margen_x + (6 * self.ancho_triangulo) + self.ancho_barra + (col * self.ancho_triangulo) + self.ancho_triangulo / 2
            else: # Cuadrante superior izquierdo
                col = 12 - punto
                x = self.margen_x + (col * self.ancho_triangulo) + self.ancho_triangulo / 2
        # Parte inferior (puntos 13 a 24)
        else:
            y_base = self.alto - self.radio_ficha - 10
            step = -self.radio_ficha * 2

            if 13 <= punto <= 18: # Cuadrante inferior izquierdo
                col = punto - 13
                x = self.margen_x + (col * self.ancho_triangulo) + self.ancho_triangulo / 2
            else: # Cuadrante inferior derecho
                col = punto - 19
                x = self.margen_x + (6 * self.ancho_triangulo) + self.ancho_barra + (col * self.ancho_triangulo) + self.ancho_triangulo / 2

        return int(x), (y_base, step)

    def resaltar_ficha_seleccionada(self, punto: int, cantidad_fichas: int):
        x, (y_base, step) = self._get_coords_from_point(punto)
        y = y_base + step * (cantidad_fichas - 1)
        pygame.draw.circle(self.pantalla, (255, 255, 0), (x, y), self.radio_ficha + 4, 4)

    def dibujar_movimientos_posibles(self, puntos_destino: list):
        color_resaltado = (0, 200, 0, 150)
        for punto in puntos_destino:
            x, (y_base, _) = self._get_coords_from_point(punto)
            superficie = pygame.Surface((self.radio_ficha * 2, self.radio_ficha * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie, color_resaltado, (self.radio_ficha, self.radio_ficha), self.radio_ficha)
            self.pantalla.blit(superficie, (x - self.radio_ficha, y_base - self.radio_ficha))

    def dibujar_fichas(self, estado: dict):
        """Dibuja las fichas en el tablero según el estado del juego con punto 1 arriba a la derecha"""
        for punto, datos in estado.items():
            color = (255, 255, 255) if datos["color"] == "Blanca" else (0, 0, 0)
            cantidad = datos["cantidad"]

            # parte superior
            if punto <= 12:
                # Los triángulos van de derecha a izquierda
                if punto <= 6:
                    # Triángulos de la derecha
                    x = (6 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                else:
                    # Triángulos de la izquierda
                    x = (12 - punto) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2
                y_base = self.radio_ficha
                step = self.radio_ficha * 2
            
            # parte inferior
            else:
                # Los triángulos van de derecha a izquierda
                if punto <= 18:
                    # Triángulos de la izquierda (19–24)
                    x = (punto - 13) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2
                else:
                    # Triángulos de la derecha (13–18)
                    x = (punto - 19) * self.ancho_triangulo + self.ancho_triangulo // 2 \
                        + self.ancho_barra // 2 + (7 * self.ancho_triangulo)
                y_base = self.alto - self.radio_ficha
                step = -self.radio_ficha * 2
            
             # Dibujar fichas en pila
            for i in range(cantidad):
                y = y_base + step * i
                pygame.draw.circle(self.pantalla, color, (x, y), self.radio_ficha)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), self.radio_ficha, 2)

    def obtener_punto_desde_click(self, pos):

        x, y = pos
        
        # Usar las mismas dimensiones que al dibujar
        margen_lateral = self.ancho_barra // 2
        ancho_barra_central = self.ancho_barra

        # Determina si el clic está en la parte superior o inferior
        parte_superior = y < self.alto / 2

        # Calcula la columna según x, ignorando los márgenes laterales
        if x < margen_lateral or x > self.ancho - margen_lateral:
            return None  # Clic fuera del área de juego

        # Ajusta la coordenada x para el cálculo del índice
        x_rel = x - margen_lateral
        # Si el clic fue en la mitad derecha del tablero, resta el ancho de la barra central
        if x > self.ancho / 2:
            x_rel -= ancho_barra_central

        # Calcula el índice del triángulo (de 0 a 11)
        indice = int(x_rel // self.ancho_triangulo)
        if not (0 <= indice <= 11):
            return None

        # Convierte el índice al número de punto del backgammon
        if parte_superior:
            # Puntos 1 a 12 (se leen de derecha a izquierda en el tablero)
            punto = 12 - indice
        else:
            # Puntos 13 a 24 (se leen de izquierda a derecha en el tablero)
            punto = 13 + indice
            
        return punto
    
    def dibujar_dados(self, dados: list):
        texto_dados = " ".join(map(str, dados)) if dados else " "
        COLOR_TEXTO = (0, 0, 0)
        superficie = self.fuente_dados.render(texto_dados, True, COLOR_TEXTO)
        rect = superficie.get_rect(center=(self.ancho / 2, self.alto / 2))
        pygame.draw.rect(self.pantalla, (250, 220, 200), rect.inflate(20,10))
        pygame.draw.rect(self.pantalla, COLOR_TEXTO, rect.inflate(20,10), 2)
        self.pantalla.blit(superficie, rect)

    def adaptar_estado_tablero(board_casillas: list):
        estado_grafico = {}
        for indice, casilla in enumerate(board_casillas):
            if casilla:  # Solo procesa las casillas que tienen fichas
                punto = indice + 1  # Convierte el índice (0-23) a punto (1-24)
                estado_grafico[punto] = {
                    "color": casilla[0],
                    "cantidad": len(casilla)
                }
        return estado_grafico