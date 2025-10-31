"""
Módulo de la Interfaz Gráfica del Tablero.

Contiene la clase TableroGrafico, responsable de dibujar
todos los elementos del juego (tablero, fichas, UI) en la
pantalla de Pygame.
"""
import pygame
from pygame_ui import constantes as C

# pylint: disable=no-member

class TableroGrafico:
    """Gestiona el dibujado de todos los elementos visuales del juego."""

    def __init__(self, pantalla):
        """
        Inicializa la interfaz gráfica.

        Args:
            pantalla (pygame.Surface): La superficie principal de Pygame.
        """
        self.pantalla = pantalla
        self.rects_puntos = [None] * 24
        self._inicializar_posiciones()

    def _inicializar_posiciones(self):
        """Calcula y almacena los rectángulos para cada punto del tablero."""
        for i in range(6):
            # Izquierda (desplazado por X_START_TABLERO)
            x_izq = C.X_CENTRO_REAL - C.ANCHO_BARRA_CENTRAL // 2 - \
                (i + 1) * C.ANCHO_TRIANGULO
            # Abajo 6-11
            self.rects_puntos[6 + i] = pygame.Rect(
                x_izq, C.ALTO_TABLERO // 2,
                C.ANCHO_TRIANGULO, C.ALTO_TABLERO // 2
            )
            # Arriba 17-12
            self.rects_puntos[17 - i] = pygame.Rect(
                x_izq, 0, C.ANCHO_TRIANGULO, C.ALTO_TABLERO // 2
            )
            # Derecha (después de barra central)
            x_der = C.X_CENTRO_REAL + C.ANCHO_BARRA_CENTRAL // 2 + \
                i * C.ANCHO_TRIANGULO
            # Abajo 5-0
            self.rects_puntos[5 - i] = pygame.Rect(
                x_der, C.ALTO_TABLERO // 2,
                C.ANCHO_TRIANGULO, C.ALTO_TABLERO // 2
            )
            # Arriba 18-23
            self.rects_puntos[18 + i] = pygame.Rect(
                x_der, 0, C.ANCHO_TRIANGULO, C.ALTO_TABLERO // 2
            )

    def dibujar_tablero(self):
        """Dibuja barras (izquierda, central, home) y triángulos."""
        pygame.draw.rect(self.pantalla, C.COLOR_INFO_BAR, C.INFO_BAR_RECT)

        pygame.draw.rect(
            self.pantalla, C.COLOR_BARRA_Y_HOME, C.ZONA_BARRA_IZQUIERDA
        )
        pygame.draw.rect(
            self.pantalla, C.COLOR_BARRA_Y_HOME, C.ZONA_HOME_BLANCO
        )
        pygame.draw.rect(
            self.pantalla, C.COLOR_BARRA_Y_HOME, C.ZONA_HOME_NEGRO
        )
        pygame.draw.rect(
            self.pantalla, C.COLOR_BARRA_Y_HOME, C.ZONA_BARRA_CENTRAL
        )

        for i in range(24):
            rect = self.rects_puntos[i]
            if not rect:
                continue
            color = C.COLOR_TRIANGULO_1 if i % 2 == 0 else C.COLOR_TRIANGULO_2
            if i < 12:
                puntos = [
                    (rect.left, rect.bottom),
                    (rect.right, rect.bottom),
                    (rect.centerx, rect.bottom - C.ALTO_TRIANGULO)
                ]
            else:
                puntos = [
                    (rect.left, rect.top),
                    (rect.right, rect.top),
                    (rect.centerx, rect.top + C.ALTO_TRIANGULO)
                ]
            pygame.draw.polygon(self.pantalla, color, puntos)

    # pylint: disable=too-many-locals
    def dibujar_fichas(self, board_state, banco_blanco, banco_negro):
        """
        Dibuja fichas en tablero (con contador +n) y banco.
        (Se quitaron home_blanco y home_negro porque no se usan aquí)
        """
        # 1. Fichas en el tablero
        for i, casilla in enumerate(board_state):
            if not casilla:
                continue
            color_ficha = C.COLOR_FICHA_BLANCA if casilla[0] == 'white' \
                else C.COLOR_FICHA_NEGRA
            rect_punto = self.rects_puntos[i]
            if not rect_punto:
                continue
            num_fichas = len(casilla)

            for j in range(num_fichas):
                if j >= C.MAX_FICHAS_APILADAS:
                    break
                y_pos = rect_punto.bottom - C.RADIO_FICHA - \
                    (j * (C.RADIO_FICHA * 2)) if i < 12 \
                    else rect_punto.top + C.RADIO_FICHA + \
                    (j * (C.RADIO_FICHA * 2))

                if (j == C.MAX_FICHAS_APILADAS - 1 and
                        num_fichas > C.MAX_FICHAS_APILADAS):
                    pygame.draw.circle(
                        self.pantalla, color_ficha,
                        (rect_punto.centerx, y_pos), C.RADIO_FICHA
                    )
                    pygame.draw.circle(
                        self.pantalla, C.COLOR_BORDE_FICHA,
                        (rect_punto.centerx, y_pos), C.RADIO_FICHA, 2
                    )
                    fichas_extra = num_fichas - C.MAX_FICHAS_APILADAS
                    texto_contador = f"+{fichas_extra}"
                    color_contador = C.COLOR_COUNTER_B if \
                        color_ficha == C.COLOR_FICHA_NEGRA \
                        else C.COLOR_COUNTER_W
                    contador_surf = C.FONT_COUNTER.render(
                        texto_contador, True, color_contador
                    )
                    contador_rect = contador_surf.get_rect(
                        center=(rect_punto.centerx, y_pos)
                    )
                    self.pantalla.blit(contador_surf, contador_rect)
                else:
                    pygame.draw.circle(
                        self.pantalla, color_ficha,
                        (rect_punto.centerx, y_pos), C.RADIO_FICHA
                    )
                    pygame.draw.circle(
                        self.pantalla, C.COLOR_BORDE_FICHA,
                        (rect_punto.centerx, y_pos), C.RADIO_FICHA, 2
                    )

        # 2. Fichas en el Banco (usando ZONA_BARRA_CENTRAL)
        for i, _ in enumerate(banco_blanco):
            y_pos = (C.ALTO_TABLERO // 2) + 40 + (i * C.RADIO_FICHA * 2)
            pygame.draw.circle(
                self.pantalla, C.COLOR_FICHA_BLANCA,
                (C.ZONA_BARRA_CENTRAL.centerx, y_pos), C.RADIO_FICHA
            )
            pygame.draw.circle(
                self.pantalla, C.COLOR_BORDE_FICHA,
                (C.ZONA_BARRA_CENTRAL.centerx, y_pos), C.RADIO_FICHA, 2
            )
        for i, _ in enumerate(banco_negro):
            y_pos = (C.ALTO_TABLERO // 2) - 40 - (i * C.RADIO_FICHA * 2)
            pygame.draw.circle(
                self.pantalla, C.COLOR_FICHA_NEGRA,
                (C.ZONA_BARRA_CENTRAL.centerx, y_pos), C.RADIO_FICHA
            )
            pygame.draw.circle(
                self.pantalla, C.COLOR_BORDE_FICHA,
                (C.ZONA_BARRA_CENTRAL.centerx, y_pos), C.RADIO_FICHA, 2
            )

    def dibujar_menu(self, nombre_p1, nombre_p2, input_activo):
        """Dibuja la pantalla del menú inicial con fondo marrón."""
        self.pantalla.fill(C.COLOR_FONDO_PRINCIPAL)
        txt_titulo = C.FONT_MENU_TITULO.render("BACKGAMMON", True,
                                               C.COLOR_TEXTO_MENU)
        titulo_pos = (
            C.MENU_RECT_TITULO.x +
            (C.MENU_RECT_TITULO.width - txt_titulo.get_width()) // 2,
            C.MENU_RECT_TITULO.y
        )
        self.pantalla.blit(txt_titulo, titulo_pos)

        label1 = C.FONT_INPUT.render("Jugador 1 (Blancas):", True,
                                      C.COLOR_TEXTO_MENU)
        self.pantalla.blit(label1,
                           (C.MENU_RECT_INPUT1_LABEL.x,
                            C.MENU_RECT_INPUT1_LABEL.y + 5))
        color_input1 = C.COLOR_INPUT_ACTIVO if input_activo == 1 \
            else C.COLOR_INPUT_INACTIVO
        pygame.draw.rect(self.pantalla, color_input1, C.MENU_RECT_INPUT1)
        pygame.draw.rect(self.pantalla, C.COLOR_TEXTO_MENU,
                         C.MENU_RECT_INPUT1, 2)
        input_surf1 = C.FONT_INPUT.render(nombre_p1, True, C.COLOR_TEXTO)
        self.pantalla.blit(input_surf1,
                           (C.MENU_RECT_INPUT1.x + 5,
                            C.MENU_RECT_INPUT1.y + 5))

        label2 = C.FONT_INPUT.render("Jugador 2 (Negras):", True,
                                      C.COLOR_TEXTO_MENU)
        self.pantalla.blit(label2,
                           (C.MENU_RECT_INPUT2_LABEL.x,
                            C.MENU_RECT_INPUT2_LABEL.y + 5))
        color_input2 = C.COLOR_INPUT_ACTIVO if input_activo == 2 \
            else C.COLOR_INPUT_INACTIVO
        pygame.draw.rect(self.pantalla, color_input2, C.MENU_RECT_INPUT2)
        pygame.draw.rect(self.pantalla, C.COLOR_TEXTO_MENU,
                         C.MENU_RECT_INPUT2, 2)
        input_surf2 = C.FONT_INPUT.render(nombre_p2, True, C.COLOR_TEXTO)
        self.pantalla.blit(input_surf2,
                           (C.MENU_RECT_INPUT2.x + 5,
                            C.MENU_RECT_INPUT2.y + 5))

        pygame.draw.rect(self.pantalla, C.COLOR_BOTON,
                         C.MENU_BOTON_START, border_radius=10)
        txt_start = C.FONT_TURNO.render("Empezar Juego", True, C.COLOR_TEXTO)
        start_pos = (
            C.MENU_BOTON_START.x +
            (C.MENU_BOTON_START.width - txt_start.get_width()) // 2,
            C.MENU_BOTON_START.y + 10
        )
        self.pantalla.blit(txt_start, start_pos)

    def dibujar_highlights(self, posibles_destinos):
        """Dibuja resaltado en casillas de destino posibles."""
        if not posibles_destinos:
            return
        for destino_idx in posibles_destinos:
            if 0 <= destino_idx <= 23:
                rect_destino = self.rects_puntos[destino_idx]
                if not rect_destino:
                    continue
                s = pygame.Surface(
                    (C.ANCHO_TRIANGULO, C.ALTO_TABLERO // 2), pygame.SRCALPHA
                )
                s.fill(C.COLOR_HIGHLIGHT)
                pos = (
                    rect_destino.left,
                    C.ALTO_TABLERO // 2 if destino_idx < 12 else 0
                )
                self.pantalla.blit(s, pos)

    # pylint: disable=too-many-arguments, too-many-locals
    def dibujar_ui(self, turno_color, dados, game_state, mensaje_error,
                   origen_seleccionado, posibles_destinos, banco_blanco_len,
                   banco_negro_len, home_blanco_len, home_negro_len):
        """Dibuja selección, resaltados, y los elementos de la BARRA INFERIOR."""
        if origen_seleccionado is not None:
            is_int = isinstance(origen_seleccionado, int)
            s_size = (C.ANCHO_TRIANGULO, C.ALTO_TABLERO // 2) if is_int \
                else (C.ANCHO_BARRA_CENTRAL, C.ALTO_TABLERO)
            s = pygame.Surface(s_size, pygame.SRCALPHA)
            s.fill(C.COLOR_SELECCION)
            pos = (
                self.rects_puntos[origen_seleccionado].left,
                C.ALTO_TABLERO // 2 if origen_seleccionado < 12 else 0
            ) if is_int else (C.ZONA_BARRA_CENTRAL.left, 0)
            self.pantalla.blit(s, pos)
        self.dibujar_highlights(posibles_destinos)

        if game_state == "ROLL_DICE":
            pygame.draw.rect(
                self.pantalla, C.COLOR_BOTON,
                C.BOTON_ROLL_DICE_RECT, border_radius=10
            )
            txt = C.FONT_TURNO.render("Tirar Dados", True, C.COLOR_TEXTO)
            self.pantalla.blit(
                txt, (C.BOTON_ROLL_DICE_RECT.x + 15,
                      C.BOTON_ROLL_DICE_RECT.y + 10)
            )
        elif game_state == "MAKE_MOVE":
            pygame.draw.rect(
                self.pantalla, C.COLOR_BOTON,
                C.BOTON_END_TURN_RECT, border_radius=10
            )
            txt = C.FONT_TURNO.render("Finalizar Turno", True, C.COLOR_TEXTO)
            self.pantalla.blit(
                txt, (C.BOTON_END_TURN_RECT.x + 10,
                      C.BOTON_END_TURN_RECT.y + 10)
            )

        texto_turno = f"Turno de: {'BLANCAS' if turno_color == 'white' else 'NEGRAS'}"
        txt_t = C.FONT_TURNO.render(texto_turno, True, C.COLOR_INFO_TEXT)
        self.pantalla.blit(
            txt_t, (C.POS_TURNO_TEXT[0] - txt_t.get_width() // 2,
                   C.POS_TURNO_TEXT[1])
        )
        if game_state == "MAKE_MOVE":
            texto_dados = f"Dados: {' '.join(map(str, dados))}" if dados else "Dados: -"
            txt_d = C.FONT_DADOS.render(texto_dados, True, C.COLOR_INFO_TEXT)
            self.pantalla.blit(
                txt_d, (C.POS_DADOS_TEXT[0] - txt_d.get_width() // 2,
                       C.POS_DADOS_TEXT[1])
            )

        txt_bw_c = C.FONT_INFO_BAR.render(
            f"Comidas W: {banco_blanco_len}", True, C.COLOR_INFO_TEXT
        )
        self.pantalla.blit(txt_bw_c, C.POS_CONTADOR_W_COMIDAS)
        txt_bw_s = C.FONT_INFO_BAR.render(
            f"Sacadas W: {home_blanco_len}", True, C.COLOR_INFO_TEXT
        )
        self.pantalla.blit(txt_bw_s, C.POS_CONTADOR_W_SACADAS)
        txt_bb_c = C.FONT_INFO_BAR.render(
            f"Comidas B: {banco_negro_len}", True, C.COLOR_INFO_TEXT
        )
        self.pantalla.blit(txt_bb_c, C.POS_CONTADOR_B_COMIDAS)
        txt_bb_s = C.FONT_INFO_BAR.render(
            f"Sacadas B: {home_negro_len}", True, C.COLOR_INFO_TEXT
        )
        self.pantalla.blit(txt_bb_s, C.POS_CONTADOR_B_SACADAS)

        if mensaje_error:
            txt_e = C.FONT_ERROR_CENTRAL.render(
                mensaje_error, True, C.COLOR_ERROR
            )
            error_rect = txt_e.get_rect(center=C.POS_ERROR_CENTRAL)
            self.pantalla.blit(txt_e, error_rect)

    def dibujar_ganador(self, nombre_ganador):
        """Muestra mensaje de ganador."""
        s = pygame.Surface((C.ANCHO, C.ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.pantalla.blit(s, (0, 0))
        txt = C.FONT_GANADOR.render(
            f"¡Gana {nombre_ganador}!", True, C.COLOR_FICHA_BLANCA
        )
        self.pantalla.blit(
            txt, (C.ANCHO // 2 - txt.get_width() // 2,
                  C.ALTO // 2 - txt.get_height() // 2)
        )

    def obtener_casilla_desde_pos(self, pos):
        """Devuelve índice (0-23), 'bar', 'home', o None. IGNORA BARRAS."""
        if pos[1] >= C.ALTO_TABLERO or pos[0] < C.ANCHO_BARRA_LATERAL:
            return None
        for i, rect in enumerate(self.rects_puntos):
            if rect and rect.collidepoint(pos):
                return i
        if C.ZONA_BARRA_CENTRAL.collidepoint(pos):
            return 'bar'
        if C.ZONA_HOME_BLANCO.collidepoint(pos):
            return 'home_white'
        if C.ZONA_HOME_NEGRO.collidepoint(pos):
            return 'home_black'
        return None

    def obtener_boton_desde_pos(self, pos, game_state):
        """Devuelve 'ROLL_DICE', 'END_TURN', o None."""
        if game_state == "ROLL_DICE" and \
           C.BOTON_ROLL_DICE_RECT.collidepoint(pos):
            return "ROLL_DICE"
        if game_state == "MAKE_MOVE" and \
           C.BOTON_END_TURN_RECT.collidepoint(pos):
            return "END_TURN"
        return None

    def obtener_input_menu_activo(self, pos):
        """Devuelve 1 si clic en input P1, 2 si en P2, o None."""
        if C.MENU_RECT_INPUT1.collidepoint(pos):
            return 1
        if C.MENU_RECT_INPUT2.collidepoint(pos):
            return 2
        return None

    def obtener_boton_menu(self, pos):
        """Devuelve 'START' si clic en botón Start, o None."""
        if C.MENU_BOTON_START.collidepoint(pos):
            return "START"
        return None
