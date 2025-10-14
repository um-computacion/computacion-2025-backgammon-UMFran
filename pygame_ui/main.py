import pygame
from pygame_ui.interfaz_tablero import TableroGrafico
from core.backgammongame import backgammongame
import sys

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Backgammon")
    reloj = pygame.time.Clock()

    # --- Inicialización de objetos del juego ---
    juego = backgammongame("Jugador 1", "Jugador 2")
    tablero_grafico = TableroGrafico(pantalla)

    # --- Variables de estado de la UI ---
    ficha_seleccionada = None
    movimientos_posibles = []
    dados_tirados = False

    running = True
    while running:
        # --- Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Tirar los dados
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not dados_tirados:
                    juego.tirar_dados()
                    dados_tirados = True
                    # Aquí se debería comprobar si hay movimientos posibles. Si no, pasar turno.
            
            # Clic del ratón
            if event.type == pygame.MOUSEBUTTONDOWN and dados_tirados:
                pos = pygame.mouse.get_pos()
                punto_clic = tablero_grafico.obtener_punto_desde_click(pos)

                if not ficha_seleccionada:
                    # 1. INTENTAR SELECCIONAR UNA FICHA
                    if punto_clic:
                        casillas = juego.mostrar_tablero()
                        if casillas[punto_clic - 1] and casillas[punto_clic - 1][0] == juego.__turno__.obtener_color():
                            ficha_seleccionada = punto_clic
                            movimientos_posibles = juego.mostrar_movimientos_posibles(ficha_seleccionada)
                            print(f"Ficha en {ficha_seleccionada} seleccionada. Movimientos: {movimientos_posibles}")
                else:
                    # 2. INTENTAR MOVER LA FICHA SELECCIONADA
                    if punto_clic and punto_clic in movimientos_posibles:
                        try:
                            juego.mover(ficha_seleccionada, punto_clic)
                        except ValueError as e:
                            print(f"Error: {e}")
                    
                    # Deseleccionar después de cualquier clic
                    ficha_seleccionada = None
                    movimientos_posibles = []

        # --- Lógica de fin de turno ---
        if dados_tirados and not juego.__dados__.get_dados():
            juego.cambiar_turno()
            dados_tirados = False
            ficha_seleccionada = None
            movimientos_posibles = []

        # --- Sección de Dibujo ---
        tablero_grafico.dibujar_tablero()


        # Dibujar feedback visual
        if ficha_seleccionada:
            tablero_grafico.resaltar_ficha_seleccionada(ficha_seleccionada)
            tablero_grafico.dibujar_movimientos_posibles(movimientos_posibles)
            
        # Dibujar elementos de UI
        tablero_grafico.dibujar_dados(juego.__dados__.get_dados())
        estado_para_dibujar = tablero_grafico.adaptar_estado_tablero(juego.mostrar_tablero())
        tablero_grafico.dibujar_fichas(estado_para_dibujar)

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()