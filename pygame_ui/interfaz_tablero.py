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
    
    