import pygame
from pygame_ui import constantes as C

class TableroGrafico:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.rects_puntos = [None] * 24
        self._inicializar_posiciones()

    def _inicializar_posiciones(self):
        """Calcula rectángulos para cada punto del tablero."""
        for i in range(6):
            # Izquierda
            x_izq = (C.ANCHO // 2) - C.ANCHO_BARRA // 2 - (i + 1) * C.ANCHO_TRIANGULO
            self.rects_puntos[6 + i] = pygame.Rect(x_izq, C.ALTO // 2, C.ANCHO_TRIANGULO, C.ALTO // 2) # Abajo 6-11
            self.rects_puntos[17 - i] = pygame.Rect(x_izq, 0, C.ANCHO_TRIANGULO, C.ALTO // 2)      # Arriba 17-12
            # Derecha
            x_der = (C.ANCHO // 2) + C.ANCHO_BARRA // 2 + i * C.ANCHO_TRIANGULO
            self.rects_puntos[5 - i] = pygame.Rect(x_der, C.ALTO // 2, C.ANCHO_TRIANGULO, C.ALTO // 2)  # Abajo 5-0
            self.rects_puntos[18 + i] = pygame.Rect(x_der, 0, C.ANCHO_TRIANGULO, C.ALTO // 2)       # Arriba 18-23

    def dibujar_tablero(self):
        """Dibuja el fondo, triángulos, barra y zonas home."""
        self.pantalla.fill(C.COLOR_FONDO)
        pygame.draw.rect(self.pantalla, C.COLOR_HOME, C.ZONA_HOME_BLANCO)
        pygame.draw.rect(self.pantalla, C.COLOR_HOME, C.ZONA_HOME_NEGRO)
        pygame.draw.rect(self.pantalla, C.COLOR_BARRA, C.ZONA_BARRA)

        for i in range(24):
            rect = self.rects_puntos[i]
            color = C.COLOR_TRIANGULO_1 if i % 2 == 0 else C.COLOR_TRIANGULO_2
            puntos = [(rect.left, rect.bottom), (rect.right, rect.bottom), (rect.centerx, rect.bottom - C.ALTO_TRIANGULO)] if i < 12 else [(rect.left, rect.top), (rect.right, rect.top), (rect.centerx, rect.top + C.ALTO_TRIANGULO)]
            pygame.draw.polygon(self.pantalla, color, puntos)

    def dibujar_fichas(self, board_state, banco_blanco, banco_negro, home_blanco, home_negro):
        """Dibuja fichas en tablero, banco y contadores en home."""
        for i, casilla in enumerate(board_state):
            if not casilla: continue
            color_ficha = C.COLOR_FICHA_BLANCA if casilla[0] == 'white' else C.COLOR_FICHA_NEGRA
            rect_punto = self.rects_puntos[i]
            for j in range(len(casilla)):
                if j >= C.MAX_FICHAS_APILADAS: break
                y_pos = rect_punto.bottom - C.RADIO_FICHA - (j * (C.RADIO_FICHA * 2)) if i < 12 else rect_punto.top + C.RADIO_FICHA + (j * (C.RADIO_FICHA * 2))
                pygame.draw.circle(self.pantalla, color_ficha, (rect_punto.centerx, y_pos), C.RADIO_FICHA)
                pygame.draw.circle(self.pantalla, C.COLOR_BORDE_FICHA, (rect_punto.centerx, y_pos), C.RADIO_FICHA, 2)

        for i, color in enumerate(banco_blanco):
            y_pos = (C.ALTO // 2) + 40 + (i * C.RADIO_FICHA * 2)
            pygame.draw.circle(self.pantalla, C.COLOR_FICHA_BLANCA, (C.ZONA_BARRA.centerx, y_pos), C.RADIO_FICHA)
            pygame.draw.circle(self.pantalla, C.COLOR_BORDE_FICHA, (C.ZONA_BARRA.centerx, y_pos), C.RADIO_FICHA, 2)
        for i, color in enumerate(banco_negro):
            y_pos = (C.ALTO // 2) - 40 - (i * C.RADIO_FICHA * 2)
            pygame.draw.circle(self.pantalla, C.COLOR_FICHA_NEGRA, (C.ZONA_BARRA.centerx, y_pos), C.RADIO_FICHA)
            pygame.draw.circle(self.pantalla, C.COLOR_BORDE_FICHA, (C.ZONA_BARRA.centerx, y_pos), C.RADIO_FICHA, 2)
        
        txt_h_w = C.FONT_MENSAJE.render(f"{len(home_blanco)}", True, C.COLOR_FICHA_BLANCA)
        txt_h_b = C.FONT_MENSAJE.render(f"{len(home_negro)}", True, C.COLOR_FICHA_NEGRA)
        self.pantalla.blit(txt_h_w, (C.ZONA_HOME_BLANCO.centerx - txt_h_w.get_width()//2, C.ZONA_HOME_BLANCO.centery - txt_h_w.get_height()//2))
        self.pantalla.blit(txt_h_b, (C.ZONA_HOME_NEGRO.centerx - txt_h_b.get_width()//2, C.ZONA_HOME_NEGRO.centery - txt_h_b.get_height()//2))

    def dibujar_menu(self, nombre_p1, nombre_p2, input_activo):
        """Dibuja la pantalla del menú inicial."""
        self.pantalla.fill(C.COLOR_FONDO)
        txt_titulo = C.FONT_MENU_TITULO.render("BACKGAMMON", True, C.COLOR_TEXTO)
        self.pantalla.blit(txt_titulo, (C.MENU_RECT_TITULO.x + (C.MENU_RECT_TITULO.width - txt_titulo.get_width()) // 2, C.MENU_RECT_TITULO.y))

        label1 = C.FONT_INPUT.render("Jugador 1 (Blancas):", True, C.COLOR_TEXTO)
        self.pantalla.blit(label1, (C.MENU_RECT_INPUT1_LABEL.x, C.MENU_RECT_INPUT1_LABEL.y + 5))
        color_input1 = C.COLOR_INPUT_ACTIVO if input_activo == 1 else C.COLOR_INPUT_INACTIVO
        pygame.draw.rect(self.pantalla, color_input1, C.MENU_RECT_INPUT1)
        pygame.draw.rect(self.pantalla, C.COLOR_TEXTO, C.MENU_RECT_INPUT1, 2)
        input_surf1 = C.FONT_INPUT.render(nombre_p1, True, C.COLOR_TEXTO)
        self.pantalla.blit(input_surf1, (C.MENU_RECT_INPUT1.x + 5, C.MENU_RECT_INPUT1.y + 5))

        label2 = C.FONT_INPUT.render("Jugador 2 (Negras):", True, C.COLOR_TEXTO)
        self.pantalla.blit(label2, (C.MENU_RECT_INPUT2_LABEL.x, C.MENU_RECT_INPUT2_LABEL.y + 5))
        color_input2 = C.COLOR_INPUT_ACTIVO if input_activo == 2 else C.COLOR_INPUT_INACTIVO
        pygame.draw.rect(self.pantalla, color_input2, C.MENU_RECT_INPUT2)
        pygame.draw.rect(self.pantalla, C.COLOR_TEXTO, C.MENU_RECT_INPUT2, 2)
        input_surf2 = C.FONT_INPUT.render(nombre_p2, True, C.COLOR_TEXTO)
        self.pantalla.blit(input_surf2, (C.MENU_RECT_INPUT2.x + 5, C.MENU_RECT_INPUT2.y + 5))

        pygame.draw.rect(self.pantalla, C.COLOR_BOTON, C.MENU_BOTON_START, border_radius=10)
        txt_start = C.FONT_TURNO.render("Empezar Juego", True, C.COLOR_TEXTO)
        self.pantalla.blit(txt_start, (C.MENU_BOTON_START.x + (C.MENU_BOTON_START.width - txt_start.get_width()) // 2, C.MENU_BOTON_START.y + 10))

    def dibujar_highlights(self, posibles_destinos):
        """Dibuja resaltado en casillas de destino posibles."""
        if not posibles_destinos: return
        for destino_idx in posibles_destinos:
            if 0 <= destino_idx <= 23:
                rect_destino = self.rects_puntos[destino_idx]
                s = pygame.Surface((C.ANCHO_TRIANGULO, C.ALTO // 2), pygame.SRCALPHA)
                s.fill(C.COLOR_HIGHLIGHT)
                pos = (rect_destino.left, C.ALTO // 2 if destino_idx < 12 else 0)
                self.pantalla.blit(s, pos)

    def dibujar_ui(self, turno_color, dados, game_state, mensaje_error, origen_seleccionado, posibles_destinos):
        """Dibuja UI: selección, resaltados, botones, dados, turno, errores."""
        if origen_seleccionado is not None:
            s = pygame.Surface((C.ANCHO_TRIANGULO, C.ALTO // 2) if isinstance(origen_seleccionado, int) else (C.ANCHO_BARRA, C.ALTO), pygame.SRCALPHA)
            s.fill(C.COLOR_SELECCION)
            pos = (self.rects_puntos[origen_seleccionado].left, C.ALTO // 2 if origen_seleccionado < 12 else 0) if isinstance(origen_seleccionado, int) else (C.ZONA_BARRA.left, 0)
            self.pantalla.blit(s, pos)

        self.dibujar_highlights(posibles_destinos)

        if game_state == "ROLL_DICE":
            pygame.draw.rect(self.pantalla, C.COLOR_BOTON, C.BOTON_ROLL_DICE, border_radius=10)
            txt = C.FONT_TURNO.render("Tirar Dados", True, C.COLOR_TEXTO)
            self.pantalla.blit(txt, (C.BOTON_ROLL_DICE.x + 15, C.BOTON_ROLL_DICE.y + 5))
        elif game_state == "MAKE_MOVE":
            pygame.draw.rect(self.pantalla, C.COLOR_BOTON, C.BOTON_END_TURN, border_radius=10)
            txt = C.FONT_TURNO.render("Finalizar", True, C.COLOR_TEXTO)
            self.pantalla.blit(txt, (C.BOTON_END_TURN.x + 30, C.BOTON_END_TURN.y + 5))
            txt_dados = " ".join(map(str, dados))
            txt = C.FONT_DADOS.render(txt_dados, True, C.COLOR_TEXTO)
            self.pantalla.blit(txt, (C.BOTON_ROLL_DICE.x + 40, C.BOTON_ROLL_DICE.y + 5))

        texto_turno = f"Turno de: {'BLANCAS' if turno_color == 'white' else 'NEGRAS'}"
        txt = C.FONT_TURNO.render(texto_turno, True, C.COLOR_TEXTO)
        self.pantalla.blit(txt, (20, C.ALTO // 2 - 15))
        
        if mensaje_error:
            txt = C.FONT_MENSAJE.render(mensaje_error, True, C.COLOR_ERROR)
            self.pantalla.blit(txt, (C.ANCHO // 2 - txt.get_width() // 2, C.ALTO - C.MARGEN_INFERIOR + 5))

    def dibujar_ganador(self, nombre_ganador):
        """Muestra mensaje de ganador."""
        s = pygame.Surface((C.ANCHO, C.ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.pantalla.blit(s, (0, 0))
        txt = C.FONT_GANADOR.render(f"¡Gana {nombre_ganador}!", True, C.COLOR_FICHA_BLANCA)
        self.pantalla.blit(txt, (C.ANCHO // 2 - txt.get_width() // 2, C.ALTO // 2 - txt.get_height() // 2))

    def obtener_casilla_desde_pos(self, pos):
        """Devuelve índice (0-23), 'bar', 'home_white', 'home_black', o None."""
        for i, rect in enumerate(self.rects_puntos):
            if rect and rect.collidepoint(pos): return i
        if C.ZONA_BARRA.collidepoint(pos): return 'bar'
        if C.ZONA_HOME_BLANCO.collidepoint(pos): return 'home_white'
        if C.ZONA_HOME_NEGRO.collidepoint(pos): return 'home_black'
        return None

    def obtener_boton_desde_pos(self, pos, game_state):
        """Devuelve 'ROLL_DICE', 'END_TURN', o None."""
        if game_state == "ROLL_DICE" and C.BOTON_ROLL_DICE.collidepoint(pos): return "ROLL_DICE"
        if game_state == "MAKE_MOVE" and C.BOTON_END_TURN.collidepoint(pos): return "END_TURN"
        return None

    def obtener_input_menu_activo(self, pos):
        """Devuelve 1 si clic en input P1, 2 si en P2, o None."""
        if C.MENU_RECT_INPUT1.collidepoint(pos): return 1
        if C.MENU_RECT_INPUT2.collidepoint(pos): return 2
        return None

    def obtener_boton_menu(self, pos):
        """Devuelve 'START' si clic en botón Start, o None."""
        if C.MENU_BOTON_START.collidepoint(pos): return "START"
        return None