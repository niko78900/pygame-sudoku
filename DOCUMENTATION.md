# Sudoku Pygame Documentation

## Overview
This project is a Pygame Sudoku game split into small modules for clarity. The game generates a solvable puzzle, locks the original clues, and lets the player fill the rest.

## Module Responsibilities
- `Python_Sudoku.py` Entry point that calls `main.main()`.
- `main.py` Initializes Pygame, owns the main loop, and handles input and state updates.
- `sudoku.py` Encapsulates board state, validation rules, the solver, and puzzle generation.
- `ui.py` Draws the grid, buttons, the console log, and the instructions screen.
- `config.py` Centralized constants for sizes, colors, and UI layout.

## Game Flow
1. App starts in `main.main()` and initializes fonts, buttons, and an empty `SudokuBoard`.
2. Clicking Easy/Medium/Hard generates a new puzzle, sets givens, and clears the move counter.
3. Clicking Solve (or pressing S) runs the backtracking solver on the current board.
4. Each frame, UI elements are drawn and the board is checked for a win.

## Board Model
- Cell values live in a dict keyed by `(row, col)` with `0` representing empty.
- `givens` is a set of locked cells that cannot be edited.
- `is_valid(row, col, num)` enforces row/col/subgrid constraints.

## Puzzle Generation
- A full valid board is created by randomized backtracking.
- A fixed number of cells are removed based on difficulty.
- Uniqueness is not enforced; puzzles are guaranteed solvable, not necessarily unique.

## UI Notes
- Themes live in `config.THEMES` and the default is `config.DEFAULT_THEME` (dark).
- Press T in-game to toggle between dark and light themes.
- Given clues use the theme `given_text` color; user entries use `user_text`.
- The selected cell outline uses the theme `selected` color.
- The activity log keeps the most recent messages and drops the oldest beyond the limit.

## Configuration
Update `config.py` to customize:
- Window and grid sizes
- Theme colors and fonts
- Button layout
- Console size and message limits

## Extending the Project
- Add difficulty levels by changing removal counts.
- Add conflict highlighting by checking neighbors during rendering.
- Persist puzzles by serializing `values` and `givens` to a file.
