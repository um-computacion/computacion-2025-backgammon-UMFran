## [1.1.1] - 2025-23-08

### Added

- core/
-   backgammongame.py
-   board.py
-   checker.py
-   cli.py
-   dice.py
-   player.py
-   pygame.py

## [1.1.2] - 2025-24-08

### Added

- class backgammongame
- class board
- class checker
- class cli
- class dice
- class player
- class pygame

## [1.1.3] - 2025-25-08

### Added

- board/__init__
- tests/
- tests/test_board.py
- .coverage

## [1.1.4] - 2025-26-08

### Added

- board/remove-checker

### Changed

- tests/test_board.py

## [1.1.5] - 2025-27-08

### Added

- board/move-checker
- CHANGELOG.md
- READEME.md
- prompts-desarrollo.md
- prompts-documentacion.md
- prompts-testing.md

### Changed

- tests/test_board.py

## [1.1.6] - 2025-29-08

### Added

- board/consulta-checker
- board/estado-jugador

### Changed

- tests/test_board.py

## [1.1.7] - 2025-31-08

### Added

- board/get-home
- board/get-banco
- dice/__init__
- dice/tirar_dados
- tests/test_dice.py

### Changed

- tests/test_board.py

## [1.1.8] - 2025-02-09

### Added

- dice/usar_dados
- dice/get_dados
- dice/hay_movimientos
- dice/limpiar_dados

### Changed

- tests/test_dice.py

## [1.1.9.1] - 2025-05-09

### Changed

- prompts-desarrollo.md

## [1.1.9.2] - 2025-09-09

### Changed

- CHANGELOG.md
- core/board.py
- tests/test_board.py

## [1.2.1] - 2025-09-09

### Added

- player/mostrar_fichas
- player/obtener_nombre
- player/obtener_color
- player/ganar
- player/restar_ficha
- player/__str__
- tests/test_player.py
- checket/obtener_color
- checket/obtener_posicion
- checket/posicion_nueva
- checket/esta_banco
- checket/esta_home
- tests/test_checker.py

## [1.2.2] - 2025-09-15

### Added

- backgammongame/__init__
- backgammongame/mostrar_jugador1
- backgammongame/mostrar_jugador2
- backgammongame/mostrar_turno
- backgammongame/tirar_dados
- backgammongame/cambiar_turno
- backgammongame/ganador
- backgammongame/juego_terminado
- tests/test_game.py

### Changed

- tests/test_board.py
- README.md

## [1.2.2] - 2025-09-16

### Added

- backgammongame/mover
- backgammongame/reingresar_ficha
- backgammongame/sacar
- backgammongame/finalizar_turno
- backgammongame/estado_turno
- player/resetear_fichas
- tests/test_game.py

### Changed

- backgammongame/cambiar_turno
- tests/test_game.py
- tests/test_player.py

## [1.3.1] - 2025-09-24

### Added

- cli/__init__
- cli/iniciar_juego
- tests/test_cli.py

### Changed

- CHANGELOG
- prompts-testing.md

## [1.3.2] - 2025-09-25

### Added

- cli/jugar_turno
- cli/mostrar_banco
- cli/mostar_home

### Changed

- tests/test_cli.py

## [1.3.3] - 2025-09-26

### Added

- cli/mostrar_estado_completo
- cli/mostrar_movimientos:posibles

### Changed

- cli/jugar_turno
- tests/test_cli.py