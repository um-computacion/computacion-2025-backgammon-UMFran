JUSTIFICACIÓN DE DISEÑO: Backgammon Computación 2025
1. Resumen del Diseño General
El proyecto está implementado en Python siguiendo un diseño basado en el paradigma de Programación Orientada a Objetos (POO). La arquitectura principal sigue el Principio de Responsabilidad Única (SRP), separando estrictamente:

Lógica Central (core/): Maneja todas las reglas, estado del juego, y la mecánica del tablero, sin depender de ninguna interfaz visual.

Interfaces de Usuario (cli/ y pygame_ui/): Dos implementaciones de presentación (consola y gráfica) que consumen la lógica del core pero no la modifican.

Esta separación permite que el motor del juego (core) sea reutilizable y testeable de forma aislada, permitiendo intercambiar o agregar nuevas interfaces (como una web) sin alterar las reglas del juego.

2. Justificación de Clases y Atributos
A continuación, se detallan las clases principales del proyecto y sus responsabilidades.

Lógica Central (Core)
core/backgammongame.py -> BackgammonGame
Responsabilidad: Es el motor central y "árbitro" del juego. Actúa como una fachada (Facade), coordinando a los jugadores, el tablero y los dados para aplicar las reglas complejas.

Atributos Clave:

__board__ (Board): Instancia del tablero.

__dados__ (Dice): Instancia de los dados.

__jugador1__ / __jugador2__ (Player): Los dos jugadores.

__turno__ (Player): Referencia al jugador que tiene el turno activo.

__juego_terminado__ (bool): Bandera para detener el juego.

Métodos Clave:

mover(origen, destino): Valida la lógica de negocio (dirección del movimiento, dado disponible) y llama a __board__.mover_checker.

reingresar_ficha(destino): Valida el dado para reingresar y llama a __board__.move_checker_banco.

sacar(origen): Contiene la lógica más compleja, validando que todas las fichas estén en el cuadrante final y que se use un dado exacto o uno mayor aplicable.

get_valid_moves(origen, dados): Método de ayuda crucial para la UI. Devuelve una lista de destinos válidos, permitiendo a la UI (Pygame) resaltar los movimientos legales.

core/board.py -> Board
Responsabilidad: Representa el estado físico del tablero. Es el "músculo" que ejecuta las acciones físicas sobre las fichas, sin conocer las reglas de turnos o dados.

Atributos Clave:

__contenedor__: Una list[list] de 24 elementos que representa los puntos del tablero.

__barra__: Un dict que almacena las fichas comidas (ej. {"white": [], "black": []}).

__afuera__: Un dict que almacena las fichas sacadas del tablero (home).

Justificación: Se eligió una lista de listas para __contenedor__ por eficiencia y simplicidad de acceso por índice (0-23). Los diccionarios para __barra__ y __afuera__ permiten una gestión sencilla por color.

core/player.py -> Player
Responsabilidad: Almacenar el estado de un jugador.

Atributos Clave:

__nombre__ (str): Nombre del jugador para la UI.

__color__ (str): "white" o "black", para identificar sus fichas.

__fichas_restantes__ (int): Contador (inicia en 15) que se decrementa al sacar fichas. Necesario para determinar la victoria.

Métodos Clave: ganar() (comprueba si __fichas_restantes__ es 0), restar_ficha().

core/dice.py -> Dice
Responsabilidad: Gestionar el estado y la lógica de los dados para un turno.

Atributos Clave: __movimientos__ (list): Almacena los dados disponibles (ej. [5, 3] o [6, 6, 6, 6]).

Justificación: Separar esta lógica simplifica el motor del juego; BackgammonGame solo necesita pedir los dados (get_dados) y reportar cuáles usó (usar_dado).

Interfaces de Usuario (UI)
pygame_ui/interfaz_tablero.py -> TableroGrafico
Responsabilidad: Renderizar todos los elementos visuales del juego en la pantalla de Pygame (tablero, fichas, botones, texto).

Atributos Clave:

pantalla (Surface): La superficie principal de Pygame donde se dibuja.

rects_puntos (list): Lista de pygame.Rect que mapea las casillas lógicas (0-23) a coordenadas en pantalla. Se calcula en _inicializar_posiciones.

Justificación: Esta clase encapsula todo el código de pygame.draw. El bucle principal en main_pygame.py simplemente le dice qué dibujar (basado en el estado del juego), pero TableroGrafico decide cómo y dónde dibujarlo.

pygame_ui/main_pygame.py
Responsabilidad: Contiene el bucle principal del juego, gestiona la máquina de estados (game_state) y maneja los eventos del usuario (clics, teclado).

Justificación: A diferencia del ejemplo, esta implementación no separa el manejo de eventos en otra clase, sino que lo centraliza en main(). Este script actúa como el Controlador, traduciendo los eventos de Pygame (como un clic en (x, y)) en acciones lógicas del juego (como game.mover(5, 10)), después de consultar a TableroGrafico (obtener_casilla_desde_pos).

cli/cli.py -> cli
Responsabilidad: Implementación alternativa de la UI para la consola.

Métodos Clave: iniciar_juego() (pide nombres) y jugar_turno() (muestra el menú de opciones 1-10 y captura la entrada del usuario).

3. Decisiones de Diseño Relevantes
Separación Core/UI: La decisión más importante fue adherir al requisito de separar la lógica (core) de la presentación (pygame_ui, cli). Esto se comprueba por el hecho de que core no importa pygame ni cli, permitiendo que la misma lógica funcione para ambas interfaces.

Representación del Tablero: Se eligió una list[list] (__contenedor__) para las casillas, indexadas de 0 a 23. Esto es eficiente y mapea directamente a la lógica del juego. Se usan dict (__barra__, __afuera__) para las zonas fuera del tablero, permitiendo un acceso rápido por color.

Manejo de Estado (Pygame): main_pygame.py utiliza una máquina de estados simple (la variable game_state) para controlar el flujo del juego ("MENU", "ROLL_DICE", "MAKE_MOVE", "GAME_OVER"). Esto define qué eventos se procesan y qué elementos de la UI se dibujan en cada momento.

UI "Inteligente" (Highlights): Para mejorar la experiencia de Pygame, se añadió el método get_valid_moves a BackgammonGame. La UI llama a este método cuando se selecciona una ficha, y el core le devuelve los destinos legales. La UI luego usa esta lista para dibujar los resaltados (dibujar_highlights), guiando al usuario.

4. Manejo de Errores y Excepciones
A diferencia del ejemplo, este proyecto no utiliza excepciones personalizadas, sino que centraliza el manejo de errores lógicos mediante la excepción incorporada ValueError.

Lógica (core): Las clases Board, Dice, y BackgammonGame son las únicas que lanzan excepciones ValueError cuando se viola una regla.

Board.remover_checker: Lanza ValueError si la casilla está vacía.

Board.mover_checker / move_checker_banco: Lanza ValueError si el destino está bloqueado.

BackgammonGame.mover / sacar: Lanza ValueError si el movimiento no es válido según los dados, la dirección o las reglas del cuadrante final.

Interfaces (UI): Las interfaces (cli.py y main_pygame.py) son responsables de capturar estas excepciones (try...except ValueError as e:) y mostrar el mensaje de error e al usuario de forma amigable (en la consola o en la UI gráfica), sin que el programa colapse.

5. Estrategias de Testing
La estrategia de testing se enfoca en validar la lógica de negocio en el directorio core/.

Se testean las clases Board, Dice, Player, y BackgammonGame de forma aislada.

test_board.py: Prueba la configuración inicial, movimientos válidos, comer fichas ("blots"), bloqueos, y el reingreso/salida de fichas.

test_dice.py: Prueba la tirada normal y los dobles, usando @patch para simular random.randint y asegurar resultados predecibles.

test_player.py: Prueba la inicialización, el contador de fichas y la condición de victoria.

test_game.py: Prueba la lógica principal, incluyendo el cambio de turnos, la validación de movimientos con dados (usando @patch) y las reglas de "sacar".

El objetivo es alcanzar una alta cobertura (objetivo del 90%) sobre estos archivos del core.

6. Cumplimiento de Principios SOLID
Se ha intentado seguir los principios SOLID en el diseño:

S (SRP - Responsabilidad Única): Es el pilar del diseño. Board solo maneja el estado de las fichas. Dice solo maneja los dados. Player solo el estado del jugador. BackgammonGame coordina las reglas. TableroGrafico solo dibuja.

O (OCP - Abierto/Cerrado): El core está cerrado a modificaciones (sus reglas son fijas) pero abierto a extensión (se pudo añadir una UI de Pygame sin tocar el core).

I (ISP - Segregación de Interfaces): Las clases exponen interfaces pequeñas y específicas (ej. Dice tiene tirar_dados, usar_dado, no una única función "gestionar_dados").

D (DIP - Inversión de Dependencias): Este es el punto más débil. Las clases de alto nivel (BackgammonGame, main_pygame) crean (instancian) sus propias dependencias de bajo nivel (Board, Dice). Para la escala de este proyecto, se consideró más simple que implementar Inyección de Dependencias.