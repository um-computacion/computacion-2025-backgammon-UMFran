"""
Módulo Principal de Pygame.

Este archivo es el punto de entrada para ejecutar la interfaz gráfica.
Contiene el bucle principal del juego, gestiona los estados (Menú, Juego)
y maneja los eventos de usuario (clics, teclado).
"""
# pylint: disable=no-member
import sys
import pygame
from core.backgammongame import BackgammonGame
from pygame_ui.interfaz_tablero import TableroGrafico
from pygame_ui import constantes as C


def main():
    """Función principal que ejecuta el bucle del juego."""
    # --- 1. Inicialización ---
    pygame.init()
    pantalla = pygame.display.set_mode((C.ANCHO, C.ALTO))
    pygame.display.set_caption("Backgammon - Computación 2025 (UM)")
    clock = pygame.time.Clock()

    # --- 2. Variables de Estado Global ---
    running = True
    game_state = "MENU"  # MENU, ROLL_DICE, MAKE_MOVE, GAME_OVER
    game = None
    interfaz = TableroGrafico(pantalla)

    # --- 3. Variables de Juego ---
    turno_actual_player = None
    dados_disponibles = []
    origen_seleccionado = None  # int (0-23) or 'bar'
    mensaje_error = ""
    ganador = None
    posibles_destinos = []  # Para highlights

    # --- 4. Variables Menú ---
    nombre_p1 = "Jugador 1"
    nombre_p2 = "Jugador 2"
    input_activo = 1  # 1=P1, 2=P2

    # --- 5. Bucle Principal ---
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    # pylint: disable=too-many-nested-blocks
    while running:
        # --- 6. Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            # --- Eventos Menú ---
            if game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    input_sel = interfaz.obtener_input_menu_activo(pos)
                    if input_sel:
                        input_activo = input_sel
                    elif interfaz.obtener_boton_menu(pos) == "START":
                        game = BackgammonGame(nombre_p1, nombre_p2)
                        turno_actual_player = game.mostrar_jugador1()
                        game_state = "ROLL_DICE"
                        mensaje_error = ""
                        continue
                if event.type == pygame.KEYDOWN:
                    campo_activo = nombre_p1 if input_activo == 1 else nombre_p2
                    if event.key == pygame.K_BACKSPACE:
                        campo_activo = campo_activo[:-1]
                    elif event.unicode.isalnum() or event.unicode == ' ':
                        campo_activo += event.unicode
                    if input_activo == 1:
                        nombre_p1 = campo_activo
                    else:
                        nombre_p2 = campo_activo

            # --- Eventos Juego ---
            elif game_state != "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    mensaje_error = ""

                    # A. Botones
                    boton_clicado = interfaz.obtener_boton_desde_pos(
                        pos, game_state
                    )
                    if boton_clicado == "ROLL_DICE":
                        dados_disponibles = game.tirar_dados()
                        color_temp = turno_actual_player.obtener_color()
                        banco_temp = game.__board__.get_banco(color_temp)
                        hay_movimiento = False
                        origen_temporal = 'bar' if banco_temp else None
                        if origen_temporal:
                            moves = game.get_valid_moves(
                                origen_temporal, dados_disponibles
                            )
                            if moves:
                                hay_movimiento = True
                        else:
                            for i in range(24):
                                c_temp = game.mostrar_tablero()[i]
                                if c_temp and c_temp[0] == color_temp:
                                    moves = game.get_valid_moves(
                                        i, dados_disponibles
                                    )
                                    if moves:
                                        hay_movimiento = True
                                        break
                                    in_home = (
                                        (color_temp == "white" and i >= 18) or
                                        (color_temp == "black" and i <= 5)
                                    )
                                    if in_home:
                                        m_exacto = (24 - i) if \
                                            color_temp == "white" \
                                            else (i + 1)
                                        if any(d >= m_exacto
                                               for d in dados_disponibles):
                                            hay_movimiento = True
                                            break
                        if hay_movimiento:
                            game_state = "MAKE_MOVE"
                        else:
                            mensaje_error = "No hay movimientos. Pasa el turno."
                            game_state = "MAKE_MOVE"
                        origen_seleccionado = None
                        posibles_destinos = []
                        continue

                    if boton_clicado == "END_TURN":
                        try:
                            game.finalizar_turno()
                            game_state = "ROLL_DICE"
                            turno_actual_player = game.__turno__
                            dados_disponibles = []
                            origen_seleccionado = None
                            posibles_destinos = []
                        except ValueError as e:
                            mensaje_error = str(e)
                        continue

                    # B. Tablero
                    casilla_clicada = interfaz.obtener_casilla_desde_pos(pos)
                    if casilla_clicada is None:
                        origen_seleccionado = None
                        posibles_destinos = []
                        continue

                    color_actual = turno_actual_player.obtener_color()
                    banco_actual = game.__board__.get_banco(color_actual)

                    # --- Lógica de Clics y Movimientos ---
                    if origen_seleccionado == 'bar':
                        if isinstance(casilla_clicada, int) and \
                           casilla_clicada in posibles_destinos:
                            try:
                                game.reingresar_ficha(casilla_clicada)
                                dados_disponibles = game.__dados__.get_dados()
                            except ValueError as e:
                                mensaje_error = str(e)
                            finally:
                                origen_seleccionado = None
                                posibles_destinos = []
                        else:
                            mensaje_error = "Movimiento inválido"
                            origen_seleccionado = None
                            posibles_destinos = []
                    elif isinstance(origen_seleccionado, int):
                        if isinstance(casilla_clicada, int) and \
                           casilla_clicada in posibles_destinos:
                            try:
                                game.mover(origen_seleccionado,
                                           casilla_clicada)
                                dados_disponibles = game.__dados__.get_dados()
                            except ValueError as e:
                                mensaje_error = str(e)
                            finally:
                                origen_seleccionado = None
                                posibles_destinos = []
                        elif ((color_actual == 'white' and
                               casilla_clicada == 'home_white') or
                              (color_actual == 'black' and
                               casilla_clicada == 'home_black')):
                            try:
                                game.sacar(origen_seleccionado)
                                dados_disponibles = game.__dados__.get_dados()
                            except ValueError as e:
                                mensaje_error = str(e)
                            finally:
                                origen_seleccionado = None
                                posibles_destinos = []
                        else:
                            mensaje_error = "Movimiento inválido"
                            origen_seleccionado = None
                            posibles_destinos = []
                    else:  # Nada seleccionado (primer clic)
                        origen_potencial = None
                        puede_sacar_directo = False
                        if casilla_clicada == 'bar' and len(banco_actual) > 0:
                            origen_potencial = 'bar'
                        elif isinstance(casilla_clicada, int):
                            casilla_origen = game.mostrar_tablero()[
                                casilla_clicada
                            ]
                            if casilla_origen and \
                               casilla_origen[0] == color_actual:
                                if len(banco_actual) > 0:
                                    mensaje_error = "Debes reingresar primero"
                                else:
                                    try:
                                        in_home_board = (
                                            (color_actual == "white" and
                                             casilla_clicada >= 18) or
                                            (color_actual == "black" and
                                             casilla_clicada <= 5)
                                        )
                                        if in_home_board:
                                            todas_en_cuadrante = True
                                            rango_check = range(18) if \
                                                color_actual == "white" \
                                                else range(6, 24)
                                            for i in rango_check:
                                                if color_actual in \
                                                   game.mostrar_tablero()[i]:
                                                    todas_en_cuadrante = False
                                                    break
                                            if todas_en_cuadrante and \
                                               game_state == "MAKE_MOVE":
                                                m_exacto = (24 - casilla_clicada) \
                                                    if color_actual == "white" \
                                                    else (casilla_clicada + 1)
                                                dado_valido = None
                                                d_sim = game.__dados__.get_dados()
                                                if m_exacto in d_sim:
                                                    dado_valido = m_exacto
                                                else:
                                                    d_mayores = sorted(
                                                        [d for d in d_sim
                                                         if d > m_exacto]
                                                    )
                                                    if d_mayores:
                                                        es_mas_lejana = True
                                                        r_lejana = range(
                                                            18, casilla_clicada
                                                        ) if color_actual == "white" \
                                                            else range(
                                                                casilla_clicada + 1, 6
                                                            )
                                                        for i in r_lejana:
                                                            if color_actual in \
                                                               game.mostrar_tablero()[i]:
                                                                es_mas_lejana = False
                                                                break
                                                        if es_mas_lejana:
                                                            dado_valido = d_mayores[0]
                                                if dado_valido is not None:
                                                    game.sacar(casilla_clicada)
                                                    dados_disponibles = \
                                                        game.__dados__.get_dados()
                                                    origen_seleccionado = None
                                                    posibles_destinos = []
                                                    puede_sacar_directo = True
                                                else:
                                                    origen_potencial = casilla_clicada
                                            else:
                                                origen_potencial = casilla_clicada
                                        else:
                                            origen_potencial = casilla_clicada
                                    except ValueError:
                                        origen_potencial = casilla_clicada

                        if origen_potencial and not puede_sacar_directo:
                            if game_state == "MAKE_MOVE":
                                origen_seleccionado = origen_potencial
                                posibles_destinos = []
                                posibles_destinos = game.get_valid_moves(
                                    origen_seleccionado, dados_disponibles
                                )
                                puede_sacar_aqui = False
                                if isinstance(origen_seleccionado, int):
                                    try:
                                        in_home = (
                                            (color_actual == "white" and
                                             origen_seleccionado >= 18) or
                                            (color_actual == "black" and
                                             origen_seleccionado <= 5)
                                        )
                                        if in_home:
                                            todas_home = True
                                            r_fuera = range(18) if \
                                                color_actual == "white" \
                                                else range(6, 24)
                                            for i in r_fuera:
                                                if color_actual in \
                                                   game.mostrar_tablero()[i]:
                                                    todas_home = False
                                                    break
                                            if todas_home:
                                                m_s = (24 - origen_seleccionado) \
                                                    if color_actual == "white" \
                                                    else (origen_seleccionado + 1)
                                                d_sim = game.__dados__.get_dados()
                                                if m_s in d_sim:
                                                    puede_sacar_aqui = True
                                                else:
                                                    d_may = sorted(
                                                        [d for d in d_sim
                                                         if d > m_s]
                                                    )
                                                    if d_may:
                                                        es_lej = True
                                                        r_lej = range(
                                                            18, origen_seleccionado
                                                        ) if color_actual == "white" \
                                                            else range(
                                                                origen_seleccionado + 1, 6
                                                            )
                                                        for i in r_lej:
                                                            if color_actual in \
                                                               game.mostrar_tablero()[i]:
                                                                es_lej = False
                                                                break
                                                        if es_lej:
                                                            puede_sacar_aqui = True
                                    except ValueError:
                                        pass
                                if not posibles_destinos and \
                                   not puede_sacar_aqui:
                                    mensaje_error = "No hay movimientos válidos"
                                    origen_seleccionado = None
                            else:
                                mensaje_error = "Debes tirar los dados"
                        elif not puede_sacar_directo:
                            origen_seleccionado = None
                            posibles_destinos = []

        # --- Actualización Lógica (Ganador) ---
        if game and game_state != "GAME_OVER":
            if game.juego_terminado():
                ganador = game.ganador()
                if ganador:
                    game_state = "GAME_OVER"

        # --- Dibujado ---
        pantalla.fill(C.COLOR_FONDO_PRINCIPAL)

        if game_state == "MENU":
            interfaz.dibujar_menu(nombre_p1, nombre_p2, input_activo)
        else:
            interfaz.dibujar_tablero()  # Dibuja barras, home y triángulos
            banco_w = game.__board__.get_banco("white")
            banco_b = game.__board__.get_banco("black")
            home_w = game.__board__.get_home("white")
            home_b = game.__board__.get_home("black")
            interfaz.dibujar_fichas(
                game.mostrar_tablero(), banco_w, banco_b
            )
            interfaz.dibujar_ui(
                turno_actual_player.obtener_color() if
                turno_actual_player else 'white',
                dados_disponibles, game_state, mensaje_error,
                origen_seleccionado, posibles_destinos,
                len(banco_w), len(banco_b), len(home_w), len(home_b)
            )
            if game_state == "GAME_OVER":
                interfaz.dibujar_ganador(ganador)

        pygame.display.flip()
        clock.tick(30)

    # --- Salir ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
