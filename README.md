# Backgammon Computación 2025

**Autor: Francisco Martín Gallardo**

Este repositorio contiene la implementación completa del juego de mesa Backgammon, desarrollada como proyecto para la materia Computación 2025. El proyecto cumple con los requisitos de la cátedra, incluyendo una lógica de juego robusta, múltiples interfaces de usuario (CLI y Pygame) y una arquitectura de software orientada a objetos.

## Resumen del Juego

El Backgammon es un juego de estrategia y suerte para dos jugadores. El objetivo es mover las 15 fichas propias a lo largo de 24 triángulos (puntos) en el tablero, llevarlas a tu "cuadrante final" (o casa) y ser el primero en sacarlas todas del juego. Los movimientos se deciden por el lanzamiento de dos dados.

## Lógica del Juego Implementada

El motor del juego maneja todas las reglas clásicas del Backgammon:

1.  **Inicio:** El juego comienza con una pantalla de menú donde los jugadores pueden ingresar sus nombres antes de empezar.
2.  **Turnos:** Los jugadores se turnan para tirar los dados. Un jugador debe usar los números de ambos dados para mover sus fichas. Si saca "dobles" (ambos dados iguales), los movimientos se duplican (4 movimientos).
3.  **Movimiento:** Las fichas **blancas** avanzan en sentido horario (de la casilla 0 a la 23) y las **negras** en sentido antihorario (de la 23 a la 0). El juego valida que una ficha no pueda moverse hacia atrás.
4.  **Comer Fichas:** Si un jugador mueve una ficha a una casilla ocupada por *una sola* ficha enemiga (un "blot"), la ficha enemiga es comida y movida a la "barra" central.
5.  **Reingresar Fichas:** Un jugador con fichas en la barra no puede mover otras fichas hasta que todas sus fichas comidas hayan reingresado al tablero. El reingreso se hace en el cuadrante inicial del oponente, usando el valor de los dados.
6.  **Bloqueos:** Un jugador no puede mover una ficha a una casilla que esté "bloqueada" por dos o más fichas enemigas.
7.  **Sacar Fichas (Bear Off):** Una vez que un jugador ha movido sus 15 fichas a su cuadrante final, puede empezar a sacarlas del tablero.
      * Se puede sacar una ficha si el dado coincide exactamente con los pasos que le faltan para salir.
      * Si no hay un dado exacto, se puede usar un dado con un número mayor, *solo si no hay otras fichas en casillas más alejadas*.
8.  **Victoria:** El primer jugador que logra sacar sus 15 fichas del tablero gana la partida.

## Organización del Código

El proyecto está diseñado siguiendo los principios de la Programación Orientada a Objetos, con una clara **separación entre la lógica de negocio y la presentación (UI)**.

### Estructura del Proyecto

```
computacion-2025-backgammon-UMFran/
├── core/                 # Lógica central del juego
│   ├── backgammongame.py # Controlador principal (motor)
│   ├── board.py         # Lógica del tablero
│   ├── player.py        # Clase jugador
│   ├── dice.py          # Manejo de dados
│   └── checker.py       # Clase ficha
│
├── cli/                 # Interfaz de línea de comandos
│   └── cli.py           # Implementación CLI
│
├── pygame_ui/           # Interfaz gráfica
│   ├── main_pygame.py   # Punto de entrada GUI (bucle principal)
│   ├── interfaz_tablero.py # Renderizado del tablero y UI
│   └── constantes.py    # Constantes (colores, fuentes, tamaños)
│
├── tests/               # Pruebas unitarias
│   ├── test_board.py
│   ├── test_game.py
│   ├── test_dice.py
│   ├── test_player.py
│   ├── test_checker.py
│   └── test_cli.py
│
├── .github/workflows/   # Integración Continua
│   └── ci.yml
│
├── README.md            # Documentación principal (este archivo)
├── CHANGELOG.md         # Historial de cambios
├── JUSTIFICACION.md     # Justificación de diseño
├── requirements.txt     # Dependencias
└── .pylintrc            # Configuración de Pylint
```

## Diagrama de clases


```text
          ┌───────────────────────────┐         ┌───────────────────────────┐
          │    main_pygame.py (UI)    │         │         cli.py (UI)         │
          │  (Bucle principal Pygame) │         │ (Interfaz de Línea de Comandos) │
          │      usa TableroGrafico   │         │      ATRIBUTOS:             │
          └─────────────┬─────────────┘         │       - __game__: BackgammonGame
                        │ usa                   └─────────────┬─────────────┘
                        │                                     │ usa
                        └───────────────┐   ┌───────────────┘
                                        │   │
                                        ▼   ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                 BackgammonGame                                   │
│                           (Motor principal - core/backgammongame.py)             │
├──────────────────────────────────────────────────────────────────────────────────┤
│ ATRIBUTOS:                                                                       │
│  - __board__: Board              (La instancia del tablero)                      │
│  - __dados__: Dice                (La instancia de los dados)                     │
│  - __jugador1__: Player           (Jugador de fichas 'white')                     │
│  - __jugador2__: Player           (Jugador de fichas 'black')                     │
│  - __jugadores__: set             (Conjunto de los dos jugadores)                 │
│  - __turno__: Player              (Referencia a jugador1 o jugador2)              │
│  - __turno_finalizado__: bool     (Control de estado del turno)                   │
│  - __juego_terminado__: bool      (Controla si el juego acabó)                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ MÉTODOS CLAVE:                                                                   │
│  + mover(origen, destino)        (Valida y mueve la ficha)                       │
│  + reingresar_ficha(destino)     (Valida y saca ficha de la barra)               │
│  + sacar(origen)                 (Valida y saca ficha del tablero)               │
│  + finalizar_turno()             (Pasa el turno al otro jugador)                 │
│  + tirar_dados()                 (Llama a __dados__.tirar_dados())               │
│  + ganador()                     (Revisa si alguien ganó)                        │
│  + get_valid_moves(origen, dados) (Para ayudar a la UI a mostrar resaltados)     │
└─────────────────────────────────────┬────────────────────────────────────────────┘
                                      │
                                      │ Coordina / Posee (Composición)
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────┐
│        Player         │   │            Board            │   │         Dice          │
│    (core/player.py)   │   │       (core/board.py)       │   │     (core/dice.py)    │
├───────────────────────┤   ├───────────────────────────┤   ├───────────────────────┤
│ ATRIBUTOS:            │   │ ATRIBUTOS:                │   │ ATRIBUTOS:            │
│  - __nombre__: str    │   │  - __contenedor__: list[24] │   │  - __movimientos__: list│
│  - __color__: str     │   │  - __barra__: dict          │   │                       │
│  - __fichas__: int (15) │   │  - __afuera__: dict         │   │ MÉTODOS CLAVE:        │
│  - __fichas_restantes__ │   │                           │   │  + tirar_dados()      │
│                       │   │ MÉTODOS CLAVE:            │   │  + get_dados()        │
│ MÉTODOS CLAVE:        │   │  + mover_checker(o, d)    │   │  + usar_dado(v)       │
│  + obtener_nombre()   │   │  + move_checker_banco(c, d) │   │  + hay_movimientos()  │
│  + obtener_color()    │   │  + sacar_ficha(c, o)      │   │  + limpiar_dados()    │
│  + restar_ficha()     │   │  + get_barra(c)           │   │                       │
│  + ganar()            │   │  + get_afuera(c)          │   │                       │
└───────────────────────┘   └───────────────────────────┘   └───────────────────────┘
```

### `core/` - El Cerebro del Juego

Este directorio contiene toda la lógica pura del Backgammon, sin ninguna dependencia gráfica o de consola.

  * **`backgammongame.py`**: Es el motor principal. Conecta a los jugadores, el tablero y los dados, y aplica las reglas del juego (validar movimientos, cambiar turnos, etc.).
  * **`board.py`**: Representa el estado físico del tablero. Sabe dónde está cada ficha, cómo moverlas entre casillas, cómo gestionar la barra (fichas comidas) y la casa (fichas sacadas).
  * **`player.py`**: Almacena la información del jugador (nombre, color) y lleva la cuenta de cuántas fichas le quedan por sacar para determinar al ganador.
  * **`dice.py`**: Gestiona la lógica de tirar los dados, manejar dobles y llevar la cuenta de los dados usados en un turno.
  * **`checker.py`**: Una clase simple que representa una ficha individual.

### `pygame_ui/` - La Interfaz Gráfica (Pygame)

Este paquete se encarga de todo lo visual y la interacción con el mouse.

  * **`main_pygame.py`**: Es el punto de entrada que se ejecuta. Contiene el bucle principal del juego, gestiona los eventos de Pygame (clics, teclado) y coordina la lógica del `core` con el dibujado en pantalla.
  * **`interfaz_tablero.py`**: Contiene la clase `TableroGrafico`, que sabe cómo dibujar cada elemento (el tablero, las barras, los triángulos, las fichas, los contadores "+n", los resaltados de movimientos válidos, el menú y la barra de información inferior).
  * **`constantes.py`**: Almacena todos los valores fijos (tamaños de pantalla, colores, fuentes, posiciones de botones) para mantener el código limpio y fácil de modificar.

### `cli/` - La Interfaz de Consola

  * **`cli.py`**: Una interfaz alternativa que permite jugar al juego completo directamente en la terminal, usando comandos de texto.

### `tests/` - Control de Calidad

  * Contiene todas las pruebas unitarias que validan el funcionamiento del `core/`. Las pruebas usan `unittest` y `mocking` (especialmente `@patch`) para simular tiradas de dados y asegurar que la lógica del juego es correcta.

-----

## Requerimientos

  * Python 3.10 (o superior)
  * **Para la Interfaz Gráfica:** `pygame`
  * **Para Desarrollo:** `pylint`, `coverage`

Todas las dependencias necesarias están listadas en `requirements.txt`.

## Instalación

1.  **Clonar el repositorio:**

    ```sh
    git clone https://github.com/UM-AD/computacion-2025-backgammon-UMFran.git
    cd computacion-2025-backgammon-UMFran
    ```

2.  **(Recomendado) Crear un entorno virtual:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    .\venv\Scripts\activate   # En Windows
    ```

3.  **Instalar las dependencias:**

    ```sh
    pip install -r requirements.txt
    ```

## Cómo Jugar

Puede ejecutar el juego usando la interfaz gráfica (Pygame) o la interfaz de línea de comandos (CLI).

### 1\. Interfaz Gráfica (Pygame)

Es la experiencia de juego recomendada.

**Ejecución:**
Corra el siguiente comando desde la raíz del proyecto:

```sh
python pygame_ui/main_pygame.py
```

**Controles:**

  * **Menú:** Escriba los nombres de los jugadores en los campos de texto y haga clic en **"START"**.
  * **Tirar Dados:** Haga clic en el botón **"ROLL\_DICE"** cuando sea su turno.
  * **Mover Ficha:**
    1.  Haga clic en la ficha (o en la barra central si tiene fichas comidas) que desea mover. La casilla se resaltará en amarillo.
    2.  Los destinos válidos se resaltarán en verde.
    3.  Haga clic en un destino resaltado para mover la ficha.
  * **Sacar Ficha:** Cuando todas sus fichas estén en el cuadrante final, puede hacer clic en una ficha y luego en la zona "home" (la barra lateral derecha) si el movimiento es válido.
  * **Finalizar Turno:** Si no tiene más movimientos o desea ceder el turno, haga clic en **"END\_TURN"**.

### 2\. Interfaz de Línea de Comandos (CLI)

Una versión más simple que se ejecuta en su terminal.

**Ejecución:**

```
Powershell: 
  python -m cli.cli
```

**Controles:**
El juego le pedirá los nombres y luego le presentará un menú de opciones en cada turno.

  * **1. Mover ficha:** Ingrese el número de la casilla de origen (1-24) y luego el destino (1-24).
  * **2. Reingresar ficha:** Si tiene fichas en la barra, ingrese la casilla de destino (1-24) para reingresar.
  * **3. Sacar ficha:** Si puede sacar fichas, ingrese la casilla de origen (1-24).
  * **4. Finalizar turno:** Pasa el turno al siguiente jugador.
  * **5-10:** Opciones para mostrar el estado, reiniciar o ver al ganador.

## Pruebas (Testing)

El proyecto incluye un conjunto de pruebas unitarias en el directorio `tests/` para garantizar el correcto funcionamiento de la lógica del `core`.

**Ejecutar todas las pruebas:**

```
Powershell:
  python -m unittest discover
```

**Generar reporte de cobertura:**
El archivo `ci.yml` está configurado para correr las pruebas y generar un reporte de cobertura.

```
CMD: (HABIENDO ACTIVADO EL ENTORNO VIRTUAL PREVIAMENTE)
  coverage run -m unittest discover
  coverage report -m
```

## Desarrollo

Este proyecto usa `pylint` para el control de calidad y el formateo del código, con la configuración definida en `.pylintrc`.

**Ejecutar Pylint:**

```
CMD: (HABIENDO ACTIVADO EL ENTORNO VIRTUAL PREVIAMENTE)
  pylint --rcfile=.pylintrc core cli pygame_ui
```