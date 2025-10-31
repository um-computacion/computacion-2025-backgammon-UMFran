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