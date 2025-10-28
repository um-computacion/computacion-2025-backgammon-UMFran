import pygame
import sys
from core.backgammongame import backgammongame
from pygame_ui.interfaz_tablero import TableroGrafico
from pygame_ui import constantes as C

def main():
    # --- 1. Inicialización ---
    pygame.init()
    pantalla = pygame.display.set_mode((C.ANCHO, C.ALTO))
    pygame.display.set_caption("Backgammon - Computación 2025 (UM)")
    clock = pygame.time.Clock()

    # --- 2. Variables de Estado Global ---
    running = True
    game_state = "MENU" # MENU, ROLL_DICE, MAKE_MOVE, GAME_OVER
    game = None
    interfaz = TableroGrafico(pantalla)

    # --- 3. Variables de Juego ---
    turno_actual_player = None
    dados_disponibles = []
    origen_seleccionado = None # int (0-23) or 'bar'
    mensaje_error = ""
    ganador = None
    posibles_destinos = [] # Para highlights

    # --- 4. Variables Menú ---
    nombre_p1 = "Jugador 1"
    nombre_p2 = "Jugador 2"
    input_activo = 1 # 1=P1, 2=P2

    # --- 5. Bucle Principal ---
    while running:
        # --- 6. Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False; continue

            # --- Eventos Menú ---
            if game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    input_sel = interfaz.obtener_input_menu_activo(pos)
                    if input_sel: input_activo = input_sel
                    elif interfaz.obtener_boton_menu(pos) == "START":
                        game = backgammongame(nombre_p1, nombre_p2)
                        turno_actual_player = game.mostrar_jugador1()
                        game_state = "ROLL_DICE"; mensaje_error = ""; continue
                if event.type == pygame.KEYDOWN:
                    campo_activo = nombre_p1 if input_activo == 1 else nombre_p2
                    if event.key == pygame.K_BACKSPACE: campo_activo = campo_activo[:-1]
                    elif event.unicode.isalnum() or event.unicode == ' ': campo_activo += event.unicode
                    if input_activo == 1: nombre_p1 = campo_activo
                    else: nombre_p2 = campo_activo

            # --- Eventos Juego ---
            elif game_state != "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos; mensaje_error = ""

                    # A. Botones
                    boton_clicado = interfaz.obtener_boton_desde_pos(pos, game_state)
                    if boton_clicado == "ROLL_DICE":
                        dados_disponibles = game.tirar_dados()
                        # Chequear si hay movimientos posibles tras tirar
                        color_actual_temp = turno_actual_player.obtener_color()
                        banco_actual_temp = game.__board__.get_banco(color_actual_temp)
                        hay_movimiento = False
                        origen_temporal = 'bar' if banco_actual_temp else None
                        
                        if origen_temporal: # Prioridad reingreso
                            moves = game.get_valid_moves(origen_temporal, dados_disponibles)
                            if moves: hay_movimiento = True
                        else: # Buscar movimientos normales o sacar
                            for i in range(24):
                                casilla_temp = game.mostrar_tablero()[i]
                                if casilla_temp and casilla_temp[0] == color_actual_temp:
                                    moves = game.get_valid_moves(i, dados_disponibles)
                                    if moves: hay_movimiento = True; break
                                    # Simplificado: chequear si puede sacar (la función get_valid_moves no lo hace)
                                    # Verificamos si está en el cuadrante final y hay un dado potencialmente válido
                                    in_home_board = (color_actual_temp == "white" and i >= 18) or \
                                                    (color_actual_temp == "black" and i <= 5)
                                    if in_home_board:
                                        mov_exacto = (24 - i) if color_actual_temp == "white" else (i + 1)
                                        if any(d >= mov_exacto for d in dados_disponibles):
                                            # Comprobación básica, la lógica completa está en game.sacar()
                                            # Necesitaríamos simular si es la más lejana para ser 100% preciso
                                            hay_movimiento = True; break
                        
                        if hay_movimiento:
                             game_state = "MAKE_MOVE"
                        else:
                             mensaje_error = "No hay movimientos posibles. Pasa el turno."
                             # Permanece en MAKE_MOVE para permitir pulsar "Finalizar"
                             game_state = "MAKE_MOVE" 

                        origen_seleccionado = None; posibles_destinos = []; continue

                    if boton_clicado == "END_TURN":
                        try:
                            game.finalizar_turno() # Siempre finaliza y cambia el turno
                            game_state = "ROLL_DICE"; turno_actual_player = game.__turno__
                            dados_disponibles = []; origen_seleccionado = None; posibles_destinos = []
                        except Exception as e: mensaje_error = str(e)
                        continue

                    # B. Tablero
                    casilla_clicada = interfaz.obtener_casilla_desde_pos(pos)
                    if casilla_clicada is None:
                         origen_seleccionado = None; posibles_destinos = []; continue

                    color_actual = turno_actual_player.obtener_color()
                    banco_actual = game.__board__.get_banco(color_actual)

                    # --- Lógica de Clics y Movimientos ---
                    if origen_seleccionado == 'bar': # Ya seleccionó la barra
                        if isinstance(casilla_clicada, int) and casilla_clicada in posibles_destinos:
                            try:
                                game.reingresar_ficha(casilla_clicada); dados_disponibles = game.__dados__.get_dados()
                                origen_seleccionado = None; posibles_destinos = []
                            except ValueError as e: mensaje_error = str(e); origen_seleccionado = None; posibles_destinos = []
                        else:
                            mensaje_error = "Movimiento inválido"
                            origen_seleccionado = None; posibles_destinos = []

                    elif isinstance(origen_seleccionado, int): # Ya seleccionó una casilla
                        # Intenta mover? (Clic en otra casilla válida)
                        if isinstance(casilla_clicada, int) and casilla_clicada in posibles_destinos:
                            try:
                                game.mover(origen_seleccionado, casilla_clicada); dados_disponibles = game.__dados__.get_dados()
                                origen_seleccionado = None; posibles_destinos = []
                            except ValueError as e: mensaje_error = str(e); origen_seleccionado = None; posibles_destinos = []
                        # Intenta sacar? (Clic en la zona home correcta)
                        elif ((color_actual == 'white' and casilla_clicada == 'home_white') or \
                              (color_actual == 'black' and casilla_clicada == 'home_black')):
                             try:
                                 # La función sacar valida si es posible con los dados actuales
                                 game.sacar(origen_seleccionado); dados_disponibles = game.__dados__.get_dados()
                                 origen_seleccionado = None; posibles_destinos = []
                             except ValueError as e: mensaje_error = str(e); origen_seleccionado = None; posibles_destinos = []
                        else: # Clic inválido
                            mensaje_error = "Movimiento inválido"
                            origen_seleccionado = None; posibles_destinos = []

                    else: # Nada seleccionado (primer clic)
                        origen_potencial = None
                        puede_sacar_directo = False # Flag para evitar seleccionar si se saca directo

                        if casilla_clicada == 'bar' and len(banco_actual) > 0:
                            origen_potencial = 'bar'
                        elif isinstance(casilla_clicada, int):
                            casilla_origen = game.mostrar_tablero()[casilla_clicada]
                            if casilla_origen and casilla_origen[0] == color_actual:
                                if len(banco_actual) > 0:
                                    mensaje_error = "Debes reingresar primero"
                                else:
                                    # --- Lógica para intentar sacar en el PRIMER clic ---
                                    try:
                                        # ¿Está en cuadrante final y todas las demás también?
                                        in_home_board = (color_actual == "white" and casilla_clicada >= 18) or \
                                                        (color_actual == "black" and casilla_clicada <= 5)
                                        if in_home_board:
                                            todas_en_cuadrante = True
                                            tablero_actual_temp = game.mostrar_tablero()
                                            rango_check_fuera = range(18) if color_actual == "white" else range(6, 24)
                                            for i in rango_check_fuera:
                                                if color_actual in tablero_actual_temp[i]:
                                                    todas_en_cuadrante = False; break
                                            
                                            if todas_en_cuadrante and game_state == "MAKE_MOVE": # Solo si hay dados
                                                # Simular si algún dado permite sacar (sin consumirlo aquí)
                                                mov_exacto = (24 - casilla_clicada) if color_actual == "white" else (casilla_clicada + 1)
                                                dado_valido_para_sacar = None
                                                dados_simulacion = game.__dados__.get_dados() # Usar copia

                                                if mov_exacto in dados_simulacion:
                                                    dado_valido_para_sacar = mov_exacto
                                                else:
                                                    dados_mayores = sorted([d for d in dados_simulacion if d > mov_exacto]) # Ordenar ascendente
                                                    if dados_mayores:
                                                         es_mas_lejana = True
                                                         rango_check_lejana = range(18, casilla_clicada) if color_actual == "white" else range(casilla_clicada + 1, 6)
                                                         for i in rango_check_lejana:
                                                             if color_actual in tablero_actual_temp[i]: es_mas_lejana = False; break
                                                         if es_mas_lejana: dado_valido_para_sacar = dados_mayores[0] # El menor de los mayores

                                                if dado_valido_para_sacar is not None:
                                                    # Sí puede sacar, ejecutarlo directamente
                                                    game.sacar(casilla_clicada)
                                                    dados_disponibles = game.__dados__.get_dados()
                                                    origen_seleccionado = None; posibles_destinos = []
                                                    puede_sacar_directo = True # Marcar que ya se hizo la acción
                                                else:
                                                     origen_potencial = casilla_clicada # No puede sacar, seleccionar para mover
                                            else:
                                                 origen_potencial = casilla_clicada # No todas en cuadrante (o no hay dados), seleccionar
                                        else:
                                             origen_potencial = casilla_clicada # No en cuadrante, seleccionar
                                    except Exception as e:
                                        # Si sacar falla por cualquier motivo (ej. regla no contemplada), solo seleccionar
                                        mensaje_error = f"Error al intentar sacar: {e}" # Opcional: mostrar error
                                        origen_potencial = casilla_clicada


                        # Si se encontró un origen Y NO se sacó ficha directo, seleccionar y calcular movimientos
                        if origen_potencial is not None and not puede_sacar_directo:
                             if game_state == "MAKE_MOVE":
                                origen_seleccionado = origen_potencial
                                posibles_destinos = game.get_valid_moves(origen_seleccionado, dados_disponibles)
                                if not posibles_destinos:
                                     # Comprobar si al menos podría sacar (aunque no haya clicado home)
                                     puede_sacar_desde_aqui = False
                                     if isinstance(origen_seleccionado, int):
                                         try:
                                             # Simular si 'sacar' sería posible (sin ejecutarlo)
                                              in_home_board = (color_actual == "white" and origen_seleccionado >= 18) or \
                                                              (color_actual == "black" and origen_seleccionado <= 5)
                                              if in_home_board:
                                                 todas_en_cuadrante = True # Re-verificar por si acaso
                                                 rango_check_fuera = range(18) if color_actual == "white" else range(6, 24)
                                                 for i in rango_check_fuera:
                                                     if color_actual in game.mostrar_tablero()[i]: todas_en_cuadrante = False; break
                                                 
                                                 if todas_en_cuadrante:
                                                     mov_exacto = (24 - origen_seleccionado) if color_actual == "white" else (origen_seleccionado + 1)
                                                     dados_sim = game.__dados__.get_dados()
                                                     if mov_exacto in dados_sim: puede_sacar_desde_aqui = True
                                                     else:
                                                         dados_mayores = sorted([d for d in dados_sim if d > mov_exacto])
                                                         if dados_mayores:
                                                             es_mas_lejana = True # Re-verificar
                                                             rango_check_lejana = range(18, origen_seleccionado) if color_actual == "white" else range(origen_seleccionado + 1, 6)
                                                             for i in rango_check_lejana:
                                                                 if color_actual in game.mostrar_tablero()[i]: es_mas_lejana = False; break
                                                             if es_mas_lejana: puede_sacar_desde_aqui = True
                                         except: pass # Ignorar errores de simulación

                                     if not puede_sacar_desde_aqui: # Si no puede mover NI sacar
                                        mensaje_error = "No hay movimientos válidos"; origen_seleccionado = None
                                     # Si puede sacar pero no mover, mantener seleccionado para clic en home
                             else: mensaje_error = "Debes tirar los dados"
                        # Si clic no fue válido Y no se sacó, deseleccionar
                        elif not puede_sacar_directo:
                            origen_seleccionado = None
                            posibles_destinos = []


        # --- Actualización Lógica (Ganador) ---
        if game and game_state != "GAME_OVER":
            # Usar la lógica corregida en backgammongame.py
            if game.juego_terminado():
                ganador = game.ganador() # Obtener el nombre del ganador
                if ganador: # Asegurarse de que ganador no sea None
                    game_state = "GAME_OVER"


        # --- Dibujado ---
        pantalla.fill(C.COLOR_FONDO)
        if game_state == "MENU":
            interfaz.dibujar_menu(nombre_p1, nombre_p2, input_activo)
        else:
            interfaz.dibujar_tablero()
            interfaz.dibujar_fichas(
                game.mostrar_tablero(), game.__board__.get_banco("white"), game.__board__.get_banco("black"),
                game.__board__.get_home("white"), game.__board__.get_home("black")
            )
            interfaz.dibujar_ui(
                turno_actual_player.obtener_color() if turno_actual_player else 'white',
                dados_disponibles, game_state, mensaje_error, origen_seleccionado, posibles_destinos
            )
            if game_state == "GAME_OVER": interfaz.dibujar_ganador(ganador)

        pygame.display.flip()
        clock.tick(30)

    # --- Salir ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()