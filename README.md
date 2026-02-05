# Tetris

Pygame implementation of Tetris using my minimal python framework.

## How to run

1. Install Python 3.x
2. run `python -m venv .venv` (change `python` to `python3` for Linux here and forward)
3. run `.\.venv\Scripts\activate` for Windows or `source .venv/bin/activate` for Linux
4. run `python -m pip install -r requirements.txt`
5. run `python -m main` to run the game
6. (Optional) run `pyinstaller --clean Tetris.spec` to create a standalone executable

## How to play

- Use the arrow keys to move the block left and right
- Use the up arrow key to rotate the block
- Use the down arrow key to fall faster
- Press space to drop the block all the way down
- Press Left Control to swap between the on hold and current piece
- Press ESC to go back to the main menu
