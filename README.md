
# ChessGame
Chess Game using Python and the pygame library

## Installation

To run this game, you need to have Python and pygame installed. You can install pygame using pip:

```bash
pip install pygame
```

## Running the Game

To start the game, simply run the `MainGame.py` script:

```bash
python MainGame.py
```

## Features

### Graphical User Interface

The game features a graphical user interface built with pygame. It includes a chessboard, chess pieces, and a message panel to display game status and instructions.

### Chess Timer

A chess timer is implemented to manage each player's time. The timer has a main period and a secondary period, and it switches turns automatically.

### Pawn Promotion

When a pawn reaches the opposite side of the board, it is promoted to a queen.

### Piece Movement

Players can move pieces by clicking and dragging them to the desired position on the board. Valid moves are highlighted, and invalid moves are rejected with a message.

### Game Status

The game checks for check, checkmate, and stalemate conditions and updates the game status accordingly.

## Code Overview

### Main Components

- **ChessBoard**: Manages the state of the chessboard, including piece positions, valid moves, and game status.
- **ChessTimer**: Manages the chess timers for both players, including switching turns and updating remaining time.
- **Piece Loading**: Loads chess piece images or creates placeholder pieces if the images are not available.

### Main Functions and Classes

#### load_pieces

```python
def load_pieces():
    # Loads chess piece images from the 'pieces' directory and returns them in a dictionary.
```

#### create_placeholder_pieces

```python
def create_placeholder_pieces():
    # Creates placeholder pieces with symbols if the images are not available and returns them in a dictionary.
```

#### handle_pawn_promotion

```python
def handle_pawn_promotion(chess_board, row, col):
    # Promotes a pawn to a queen when it reaches the opposite side of the board.
```

#### ChessBoard

```python
class ChessBoard:
    def __init__(self):
        # Initializes the chessboard with the default setup.
    
    def reset_board(self):
        # Resets the chessboard to the initial setup.
    
    def draw_board(self, surface):
        # Draws the chessboard on the given surface.
    
    def draw_pieces(self, surface, pieces):
        # Draws the chess pieces on the given surface.
    
    def draw_dragged_piece(self, surface, pieces, piece, pos):
        # Draws the piece being dragged on the given surface.
    
    def draw_message_panel(self, surface):
        # Draws the message panel on the given surface.
    
    def get_piece_at(self, row, col):
        # Returns the piece at the given board position.
    
    def select_piece(self, row, col):
        # Selects the piece at the given board position if it belongs to the current player.
    
    def move_piece(self, from_pos, to_pos):
        # Moves the piece from one position to another, checks for promotions, and updates the game status.
    
    def get_valid_moves(self, row, col):
        # Returns a list of valid moves for the piece at the given board position.
    
    def is_move_safe(self, from_row, from_col, to_row, to_col):
        # Checks if moving from one position to another puts the king in check.
    
    def is_square_under_attack(self, row, col, color):
        # Checks if the given square is under attack by the opponent.
    
    def is_checkmate(self):
        # Checks if the current player is in checkmate.
    
    def is_stalemate(self):
        # Checks if the game is in stalemate.
    
    def save_moves_to_file(self, filename=None):
        # Saves the move history to a file.
```

#### ChessTimer

```python
class ChessTimer:
    def __init__(self, main_time=DEFAULT_MAIN_TIME, secondary_time=DEFAULT_SECONDARY_TIME):
        # Initializes the chess timers for both players.
    
    def update(self):
        # Updates the remaining time for the active player.
    
    def switch_turn(self):
        # Switches the active player and updates the move counter.
    
    def format_time(self, seconds):
        # Formats the given time in seconds to a readable string.
    
    def draw(self, surface):
        # Draws the timer information on the given surface.
```

## License

This project is licensed under the MIT License.
```
