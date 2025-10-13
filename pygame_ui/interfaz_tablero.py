import pygame_ui

class TableroGrafico:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho = self.pantalla.get_width()
        self.alto = self.pantalla.get_heigth()
        self.ancho_triangulo = self.ancho // 14
        self.ancho_barra = self.ancho_triangulo
        self.alto_triangulo = self.alto // 2
        self.radio_ficha = self.ancho_triangulo // 3
    
    def dibujar_tablero(self):
        colores= [(180, 100, 80), (250, 220, 200)] #Color triangulos

        color_barra_central = (139, 69, 19)
        color_borde = (60, 40, 30)
        color_fondo = (220, 190, 160)
        self.pantalla.fill(color_fondo)

        #Barra central
        x_barra = x_barra = (self.ancho / 2) - (self.ancho_barra / 2)
        pygame_ui.draw.rect(self.pantalla,color_barra_central,
            pygame_ui.Rect(x_barra, 0, self.ancho_barra, self.alto))
        pygame_ui.draw.rect(self.pantalla,color_borde,
            pygame_ui.Rect(x_barra, 0, self.ancho_barra, self.alto),2)
        
        #Parte superior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame_ui.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte superior derecha(6 triangulos)
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            puntos = [(x, 0),
                    (x + self.ancho_triangulo, 0),
                    (x + self.ancho_triangulo // 2, self.alto_triangulo)]
            pygame_ui.draw.polygon(self.pantalla, colores[i % 2], puntos)
        
           #Parte inferior izquierda(6 triangulos)
        for i in range(6):
            x = i * self.ancho_triangulo + self.ancho_barra // 2
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame_ui.draw.polygon(self.pantalla, colores[i % 2], puntos)

        #Parte inferior derecha (6 triangulos)
        for i in range(6):
            x = x_barra + self.ancho_barra + (i * self.ancho_triangulo)
            puntos = [(x, self.alto),
                    (x + self.ancho_triangulo, self.alto),
                    (x + self.ancho_triangulo // 2, self.alto - self.alto_triangulo)]
            pygame_ui.draw.polygon(self.pantalla, colores[i % 2], puntos)
        
        # Barra exterior izquierda
        pygame_ui.draw.rect(self.pantalla,color_barra_central,
            pygame_ui.Rect(0, 0, self.ancho_barra // 2, self.alto))
        pygame_ui.draw.rect(self.pantalla,color_borde,
            pygame_ui.Rect(0, 0, self.ancho_barra // 2, self.alto),2)

        # Barra exterior derecha
        pygame_ui.draw.rect(self.pantalla,color_barra_central,
            pygame_ui.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto))
        pygame_ui.draw.rect(self.pantalla,color_borde,
            pygame_ui.Rect(self.ancho - self.ancho_barra // 2, 0, self.ancho_barra // 2, self.alto),2)
    
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
                pygame_ui.draw.circle(self.pantalla, color, (x, y), self.radio_ficha)
                pygame_ui.draw.circle(self.pantalla, (0, 0, 0), (x, y), self.radio_ficha, 2)
