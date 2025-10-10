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