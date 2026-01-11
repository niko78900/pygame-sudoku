# Sudoku Pygame

A Pygame-based Sudoku game with a solver, three difficulty buttons, and locked clue cells (givens) that are shown in a distinct color.

## Features
- Graph-based Sudoku model with backtracking solver and generator.
- Generate easy/medium/hard puzzles (any solvable puzzle; not necessarily unique).
- Locked clues that cannot be edited.
- On-screen activity log and move counter.
- Solver button and keyboard shortcut.
- Dark and light themes (press T to toggle; dark default).

## Project Structure
- `Python_Sudoku.py` Entry point.
- `main.py` Game loop and event handling.
- `sudoku.py` Board logic, solver, and generator.
- `ui.py` Rendering helpers and instructions screen.
- `config.py` UI constants, colors, and layout values.

## Requirements
- Python 3.8+ (recommended)
- Pygame (listed in `requirements.txt`)

## Installation

### Windows (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux (bash/zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
```bash
python Python_Sudoku.py
```

## Controls
- Click a cell to select it.
- Press 1-9 to place a number.
- Press Backspace or 0 to clear a number (if the cell is not a given).
- Press S to solve the current board.
- Press T to toggle the theme.
- Use the buttons for Easy, Medium, Hard, Solve, and Instructions.
- In the Instructions screen, press ESC to return to the game.

## Documentation
- See `DOCUMENTATION.md` for module responsibilities, game flow, and configuration notes.

## Notes
- Starting a new game always resets the board and clears prior user input.
- Given cells are locked and displayed in a darker color.

## Troubleshooting
- If you see `ModuleNotFoundError: No module named 'pygame'`, run `pip install -r requirements.txt` in your active virtual environment.
- If the window does not open, make sure you are running in a local desktop session (not a headless terminal).
