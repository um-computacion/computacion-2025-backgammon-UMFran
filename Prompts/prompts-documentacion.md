Modelo de IA: Gemini 2.5 Pro

Prompt:
    "Necesito que modifiques el JUSTIFIACION.md para que agregues las nuevas funciones que hice al código"

Respuesta:

# JUSTIFICACIÓN DE DISEÑO: Backgammon Computación 2025

## 1. Resumen del Diseño General

El proyecto está implementado en Python siguiendo un diseño basado en el paradigma de Programación Orientada a Objetos (POO). La arquitectura principal sigue el **Principio de Responsabilidad Única (SRP)**, separando estrictamente la lógica de negocio (el "cómo funciona" el Backgammon) de las capas de presentación (el "cómo se ve" o "cómo se interactúa").

La lógica de negocio reside en el paquete `core/`, mientras que las interfaces (CLI y Pygame) residen en `cli/` y `pygame_ui/` respectivamente. La clase `BackgammonGame` actúa como el "director de orquesta" o *Facade*, coordinando el resto de los componentes del `core`.

## 2. Justificación de Clases y Métodos

A continuación, se detallan las clases principales del proyecto y las responsabilidades de sus métodos clave.

### `core/board.py` -> `Board`

* **Responsabilidad:** Representa el estado físico del tablero (casillas, barra, home). Es el "músculo" que ejecuta las acciones físicas sobre las fichas.
* **Métodos Clave:**
    * `__init__()`: Inicializa la estructura de datos del tablero: `__casillas__` (una lista de 24 listas), `__banco__` (un dict para fichas comidas) y `__home__` (un dict para fichas sacadas).
    * `mostrar_tablero()`: Devuelve el estado actual de las casillas.
    * `remover_checker(punto)`: Saca la ficha superior de una casilla específica. Lanza `ValueError` si la casilla está vacía.
    * `mover_checker(origen, destino)`: Mueve una ficha. Primero valida si el destino es legal (no bloqueado por 2+ fichas enemigas). Si el destino es un "blot" (1 ficha enemiga), la mueve al banco. Lanza `ValueError` si el movimiento es ilegal.
    * `move_checker_banco(color, destino)`: Mueve una ficha desde el banco al tablero. Valida que el destino esté en la zona de reingreso correcta (0-5 para blancas, 18-23 para negras) y que no esté bloqueado.
    * `sacar_ficha(color, origen)`: Mueve una ficha de su casilla de origen a la zona `__home__`.
    * `get_banco(color)` / `get_home(color)`: Devuelven una copia de la lista de fichas comidas o sacadas para un jugador.

### `core/dice.py` -> `dice`

* **Responsabilidad:** Gestionar el estado y la lógica de los dados para un turno.
* **Métodos Clave:**
    * `__init__()`: Inicializa `__movimientos__` como una lista vacía.
    * `tirar_dados()`: Usa `random.randint` para generar dos dados. Si son dobles, `__movimientos__` se puebla con 4 instancias del dado. Si no, con los 2 dados diferentes.
    * `get_dados()`: Devuelve una copia de la lista de movimientos (dados) restantes.
    * `usar_dado(valor)`: Elimina un dado de la lista `__movimientos__` una vez que ha sido utilizado.
    * `hay_movimientos()`: Devuelve `True` si quedan dados en la lista, `False` si no.
    * `limpiar_dados()`: Vacía la lista `__movimientos__` (se usa al finalizar un turno).

### `core/player.py` -> `Player`

* **Responsabilidad:** Almacenar el estado de un jugador.
* **Métodos Clave:**
    * `__init__(nombre, color)`: Configura al jugador con su nombre, color ("white" o "black") y 15 fichas iniciales.
    * `mostrar_fichas()`: Devuelve el número de `__fichas_restantes__`.
    * `obtener_nombre()` / `obtener_color()`: Devuelven el nombre y el color.
    * `ganar()`: Devuelve `True` si `__fichas_restantes__` es 0, indicando la victoria.
    * `restar_ficha()`: Reduce el contador `__fichas_restantes__` en uno.
    * `resetear_fichas()`: Restaura el contador a 15 (usado para reiniciar el juego).

### `core/backgammongame.py` -> `backgammongame`

* **Responsabilidad:** Es el motor central y árbitro del juego. Conecta todos los componentes del `core` y aplica las reglas complejas.
* **Métodos Clave:**
    * `__init__(jugador1, jugador2)`: Crea las instancias de `Board`, `dice`, y los dos `Player`.
    * `mostrar_*()`: Métodos "getter" que devuelven el estado del tablero o los jugadores.
    * `tirar_dados()`: Llama a `__dados__.tirar_dados()` solo si no hay movimientos pendientes.
    * `mover(origen, destino)`: Valida la lógica de negocio: 1) que el movimiento sea en la dirección correcta (blancas +, negras -), 2) que el dado necesario (`abs(destino - origen)`) esté disponible. Si todo es válido, llama a `__board__.mover_checker()`.
    * `reingresar_ficha(destino)`: Valida que el dado necesario para el reingreso esté disponible y luego llama a `__board__.move_checker_banco()`.
    * `sacar(origen)`: La lógica más compleja. Valida: 1) que todas las fichas del jugador estén en el cuadrante final, 2) que el dado necesario esté disponible (ya sea el *exacto* o uno *mayor* si es la ficha más lejana). Si es válido, llama a `__board__.sacar_ficha()` y `__player__.restar_ficha()`.
    * `finalizar_turno()` / `cambiar_turno()`: Gestiona el flujo del juego, limpiando los dados y cambiando el jugador activo (`__turno__`).
    * `juego_terminado()` / `ganador()`: Comprueba si algún jugador ha ganado.
    * `get_valid_moves(origen, dados)`: Método de ayuda para la UI. Devuelve una lista de destinos válidos (casillas 0-23) desde un origen (`'bar'` o un índice) usando los dados actuales.

### `pygame_ui/interfaz_tablero.py` -> `TableroGrafico`

* **Responsabilidad:** Sabe cómo dibujar el estado del juego y traducir clics. No tiene lógica de juego.
* **Métodos Clave:**
    * `__init__(pantalla)`: Guarda la pantalla de Pygame y llama a `_inicializar_posiciones()`.
    * `_inicializar_posiciones()`: Calcula y almacena los `pygame.Rect` (rectángulos) para cada una de las 24 casillas, asegurando que coincidan con la lógica interna (0-23) y la disposición visual.
    * `dibujar_tablero()`: Dibuja los elementos estáticos: barras laterales, barra central, barra de home y los 24 triángulos (con sus colores alternados).
    * `dibujar_fichas(...)`: Dibuja las fichas (círculos) en sus casillas, apilándolas. Si hay más de 5, dibuja la quinta ficha y un contador (ej. "+2") encima. También dibuja las fichas en la barra central.
    * `dibujar_menu(...)`: Dibuja la pantalla de inicio, los campos para ingresar nombres y el botón "Empezar".
    * `dibujar_ui(...)`: Dibuja la barra de información inferior, incluyendo botones ("Tirar Dados", "Finalizar Turno"), el texto del turno, los dados, y los contadores de fichas comidas y sacadas. También dibuja el mensaje de error en la barra central.
    * `dibujar_highlights(destinos)`: Dibuja un resaltado verde semi-transparente sobre las casillas válidas recibidas desde `get_valid_moves`.
    * `obtener_casilla_desde_pos(pos)`: Traduce coordenadas (x, y) de un clic en un índice de casilla (0-23), `'bar'`, o `'home_white'`/`'home_black'`.
    * `obtener_boton_desde_pos(pos)`: Comprueba si un clic cayó sobre un botón de la UI.

### `main_pygame.py` -> `main()`

* **Responsabilidad:** El bucle principal de la aplicación gráfica. Es el controlador que une todo.
* **Lógica Principal:**
    * **Máquina de Estados:** Opera con un `game_state` ("MENU", "ROLL_DICE", "MAKE_MOVE", "GAME_OVER").
    * **Bucle de Eventos:** Captura todos los eventos de Pygame (clics, teclado, salir).
    * **Traducción de Eventos:**
        * En "MENU", maneja la entrada de texto y el clic en "Empezar".
        * En "ROLL_DICE", espera el clic en el botón "Tirar Dados".
        * En "MAKE_MOVE", traduce los clics:
            * Si el primer clic es en una ficha válida (o la barra), la selecciona (`origen_seleccionado`) y llama a `game.get_valid_moves()` para obtener y mostrar los resaltados.
            * Si el segundo clic está en un destino resaltado (o en 'home'), llama a la función correspondiente (`game.mover()`, `game.reingresar_ficha()`, `game.sacar()`).
    * **Bucle de Dibujado:** Llama a las funciones de `interfaz` para dibujar el estado actual del juego en cada fotograma.

## 3. Decisiones de Diseño Relevantes

1.  **Separación Core/UI:** La decisión más importante fue adherir al requisito de separar la lógica (core) de la UI. Esto permitió que la misma lógica de `BackgammonGame` funcione tanto para `cli` como para `main_pygame.py` sin cambios.
2.  **Representación del Tablero (`Board`):** Se eligió una `list[list]` para las `__casillas__`. Esto es eficiente y simple, donde el índice (0-23) es el punto y la lista interna contiene las fichas (como strings "white" o "black").
3.  **Manejo de Estado (Pygame):** El `main_pygame.py` usa una máquina de estados simple (`game_state`) para controlar qué se dibuja y qué eventos se procesan.
4.  **Cálculo de Movimientos Válidos:** Se añadió el método `get_valid_moves` a `BackgammonGame` para que la UI de Pygame sea "inteligente", consultando al motor qué movimientos son legales *antes* de que el usuario haga clic. Esto permite resaltar las casillas válidas.

## 4. Manejo de Errores y Excepciones

El manejo de errores se centraliza en la lógica del `core` usando excepciones `ValueError`.

* `Board.remover_checker`: Lanza `ValueError` si la casilla está vacía.
* `Board.mover_checker` / `move_checker_banco`: Lanzan `ValueError` si el destino está bloqueado o si el reingreso es en la zona incorrecta.
* `BackgammonGame.mover` / `reingresar_ficha` / `sacar`: Lanzan `ValueError` si el movimiento no es válido según los dados, la dirección o las reglas del cuadrante final.

Las interfaces (`cli` y `main_pygame.py`) se encargan de *capturar* estas excepciones (`try...except ValueError as e:`) y mostrar el mensaje de error `e` al usuario de forma amigable (en la consola o en la barra central de la UI), sin crashear el juego.

## 5. Estrategias de Testing

La estrategia de testing se enfoca en el `core/`, que contiene toda la lógica.

* Se testean las clases `Board`, `Dice`, `Player`, y `BackgammonGame` de forma aislada.
* **`test_board.py`:** Prueba la configuración inicial, movimientos válidos, comer fichas, bloqueos y reingreso/salida de fichas.
* **`test_dice.py`:** Prueba la tirada normal y los dobles usando `@patch` para simular `random.randint`.
* **`test_player.py`:** Prueba la inicialización, el contador de fichas y la condición de victoria.
* **`test_game.py`:** Prueba la lógica principal, incluyendo el cambio de turnos, la validación de movimientos con dados (usando `@patch`) y las condiciones de victoria.
* El objetivo es alcanzar la cobertura del 90% sobre estos archivos del `core`.

## 6. Cumplimiento de Principios SOLID

Se ha intentado seguir los principios SOLID:

* **S (SRP - Responsabilidad Única):** Es el pilar del diseño. Cada clase (`Board`, `Player`, `Dice`) tiene una única responsabilidad bien definida. `BackgammonGame` coordina, y las UIs solo dibujan o imprimen.
* **O (OCP - Abierto/Cerrado):** El `core` está cerrado a modificaciones (sus reglas son fijas) pero abierto a extensión (se pudo añadir una UI de Pygame sin tocar el `core`).
* **L (LSP - Sustitución de Liskov):** No aplica fuertemente al no haber herencia compleja.
* **I (ISP - Segregación de Interfaces):** Las clases exponen interfaces pequeñas y específicas (ej. `Dice` tiene `tirar_dados`, `usar_dado`, no una única función "gestionar_dados").
* **D (DIP - Inversión de Dependencias):** Este es el punto más débil. Las clases de alto nivel (`BackgammonGame`, `main_pygame`) crean sus propias dependencias de bajo nivel (instancian `Board`, `Dice`, etc.). Un diseño más estricto usaría Inyección de Dependencias, pero para la escala de este proyecto, la instanciación directa se consideró más simple.

## 7. Anexos (Diagrama de Clases)

*(Aquí deberías insertar una imagen de tu diagrama de clases UML)*

Se usa tal cual en el código

------------------------------------------------------------------------------------------------------

Prompt:
    "Necesito que me arregles el README.md para que tenga todo lo necesario para que se pueda usar el código directamente si lo leo desde ahí, como un manual"

Respuesta:

# Backgammon Computación 2025

**Autor: Francisco Martín Gallardo**

Este repositorio contiene la implementación completa del juego de mesa Backgammon, desarrollada como proyecto para la materia Computación 2025. El proyecto cumple con los requisitos de la cátedra, incluyendo una lógica de juego robusta, múltiples interfaces de usuario (CLI y Pygame) y una arquitectura de software orientada a objetos.

## Resumen del Juego

El Backgammon es un juego de estrategia y suerte para dos jugadores. El objetivo es mover las 15 fichas propias a lo largo de 24 triángulos (puntos) en el tablero, llevarlas a tu "cuadrante final" (o casa) y ser el primero en sacarlas todas del juego. Los movimientos se deciden por el lanzamiento de dos dados.

## Lógica del Juego Implementada

El motor del juego maneja todas las reglas clásicas del Backgammon:

1.  **Inicio:** El juego comienza con una pantalla de menú donde los jugadores pueden ingresar sus nombres antes de empezar.
2.  **Turnos:** Los jugadores se turnan para tirar los dados. Un jugador debe usar los números de ambos dados para mover sus fichas. Si saca "dobles" (ambos dados iguales), los movimientos se duplican (4 movimientos).
3.  **Movimiento:** Las fichas blancas avanzan en sentido horario (de la casilla 0 a la 23) y las negras en sentido antihorario (de la 23 a la 0). El juego valida que una ficha no pueda moverse hacia atrás.
4.  **Comer Fichas:** Si un jugador mueve una ficha a una casilla ocupada por *una sola* ficha enemiga (un "blot"), la ficha enemiga es comida y movida a la "barra" central.
5.  **Reingresar Fichas:** Un jugador con fichas en la barra no puede mover otras fichas hasta que todas sus fichas comidas hayan reingresado al tablero. El reingreso se hace en el cuadrante inicial del oponente, usando el valor de los dados.
6.  **Bloqueos:** Un jugador no puede mover una ficha a una casilla que esté "bloqueada" por dos o más fichas enemigas.
7.  **Sacar Fichas (Bear Off):** Una vez que un jugador ha movido sus 15 fichas a su cuadrante final, puede empezar a sacarlas del tablero.
    * Se puede sacar una ficha si el dado coincide exactamente con los pasos que le faltan para salir.
    * Si no hay un dado exacto, se puede usar un dado con un número mayor, *solo si no hay otras fichas en casillas más alejadas*.
8.  **Victoria:** El primer jugador que logra sacar sus 15 fichas del tablero gana la partida.

## Organización del Código

El proyecto está diseñado siguiendo los principios de la Programación Orientada a Objetos, con una clara **separación entre la lógica de negocio y la presentación (UI)**.

### `core/` - El Cerebro del Juego

Este directorio contiene toda la lógica pura del Backgammon, sin ninguna dependencia gráfica o de consola.

* **`backgammongame.py`**: Es el motor principal. Conecta a los jugadores, el tablero y los dados, y aplica las reglas del juego (validar movimientos, cambiar turnos, etc.).
* **`board.py`**: Representa el estado físico del tablero. Sabe dónde está cada ficha, cómo moverlas entre casillas, cómo gestionar la barra (fichas comidas) y la casa (fichas sacadas).
* **`player.py`**: Almacena la información del jugador (nombre, color) y lleva la cuenta de cuántas fichas le quedan por sacar para determinar al ganador.
* **`dice.py`**: Gestiona la lógica de tirar los dados, manejar dobles y llevar la cuenta de los dados usados en un turno.
* **`checker.py`**: Una clase simple que representa una ficha individual (aunque el tablero usa strings por simplicidad, esta clase existe para la estructura de clases).

### `pygame_ui/` - La Interfaz Gráfica (Pygame)

Este paquete se encarga de todo lo visual y la interacción con el mouse.

* **`main_pygame.py`**: Es el punto de entrada que se ejecuta. Contiene el bucle principal del juego, gestiona los eventos de Pygame (clics, teclado) y coordina la lógica del `core` con el dibujado en pantalla.
* **`interfaz_tablero.py`**: Contiene la clase `TableroGrafico`, que sabe cómo dibujar cada elemento (el tablero, las barras, los triángulos, las fichas, los contadores "+n", los resaltados de movimientos válidos, el menú y la barra de información inferior).
* **`constantes.py`**: Almacena todos los valores fijos (tamaños de pantalla, colores, fuentes, posiciones de botones) para mantener el código limpio y fácil de modificar.

### `cli/` - La Interfaz de Consola

* **`cli.py`**: Una interfaz alternativa que permite jugar al juego completo directamente en la terminal, usando comandos de texto.

### `tests/` - Control de Calidad

* Contiene todas las pruebas unitarias que validan el funcionamiento del `core/`. Las pruebas usan `unittest` y `mocking` (especialmente `@patch`) para simular tiradas de dados y asegurar que la lógica del juego es correcta.

Se usa tal cual en el código