import pygame
import sys
from pygame.locals import *
import time
from datetime import datetime
from datetime import datetime

# Initialize pygame
pygame.init()
# Function to handle pawn promotion
def handle_pawn_promotion(chess_board, row, col):
    """Automatically promote a pawn to a queen if it reaches the end of the board"""
    piece = chess_board.board[row][col]
    if piece and piece[1] == 'p':  # If it's a pawn
        # Check if white pawn reached top row or black pawn reached bottom row
        if (piece[0] == 'w' and row == 0) or (piece[0] == 'b' and row == 7):
            # Promote to queen
            chess_board.board[row][col] = piece[0] + 'q'
            chess_board.message = f"Pawn promoted to Queen!"
            return True
    return False
# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_PX = BOARD_SIZE * SQUARE_SIZE
WINDOW_WIDTH = BOARD_PX + 300  # Extra space for messages
WINDOW_HEIGHT = BOARD_PX
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (118, 150, 86)
LIGHT = (238, 238, 210)
HIGHLIGHT = (186, 202, 68)
MOVE_HIGHLIGHT = (255, 255, 0, 100)
CHECK_HIGHLIGHT = (255, 0, 0, 100)

# Timer settings (in seconds)
DEFAULT_MAIN_TIME = 2 * 60 * 60  # 2 hours for first 40 moves
DEFAULT_SECONDARY_TIME = 30 * 60  # 30 minutes for remainder of the game
MOVES_THRESHOLD = 40  # Number of moves before switching to secondary time

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Python Chess Game')
clock = pygame.time.Clock()

# Timer class to manage chess clock
class ChessTimer:
    def __init__(self, main_time=DEFAULT_MAIN_TIME, secondary_time=DEFAULT_SECONDARY_TIME):
        self.white_main_time = main_time
        self.black_main_time = main_time
        self.white_secondary_time = secondary_time
        self.black_secondary_time = secondary_time
        self.white_moves = 0
        self.black_moves = 0
        self.active_color = 'w'  # White starts
        self.last_update = time.time()
        self.game_over = False
    
    def update(self):
        if self.game_over:
            return
            
        current = time.time()
        elapsed = current - self.last_update
        self.last_update = current
        
        # Subtract elapsed time from active player's clock
        if self.active_color == 'w':
            # Use main time if under move threshold, otherwise use secondary time
            if self.white_moves < MOVES_THRESHOLD:
                self.white_main_time -= elapsed
                if self.white_main_time <= 0:
                    # If main time expires, start using secondary time
                    elapsed_overflow = -self.white_main_time
                    self.white_main_time = 0
                    self.white_secondary_time -= elapsed_overflow
            else:
                self.white_secondary_time -= elapsed
            
            # Check if time is out
            if self.white_moves < MOVES_THRESHOLD and self.white_main_time <= 0 and self.white_secondary_time <= 0:
                self.white_secondary_time = 0
                self.game_over = True
            elif self.white_moves >= MOVES_THRESHOLD and self.white_secondary_time <= 0:
                self.white_secondary_time = 0
                self.game_over = True
        else:
            # Same logic for black
            if self.black_moves < MOVES_THRESHOLD:
                self.black_main_time -= elapsed
                if self.black_main_time <= 0:
                    elapsed_overflow = -self.black_main_time
                    self.black_main_time = 0
                    self.black_secondary_time -= elapsed_overflow
            else:
                self.black_secondary_time -= elapsed
            
            # Check if time is out
            if self.black_moves < MOVES_THRESHOLD and self.black_main_time <= 0 and self.black_secondary_time <= 0:
                self.black_secondary_time = 0
                self.game_over = True
            elif self.black_moves >= MOVES_THRESHOLD and self.black_secondary_time <= 0:
                self.black_secondary_time = 0
                self.game_over = True
    
    def switch_turn(self):
        # Increment move counter for the player who just moved
        if self.active_color == 'w':
            self.white_moves += 1
        else:
            self.black_moves += 1
        
        # Switch active player
        self.active_color = 'b' if self.active_color == 'w' else 'w'
        self.last_update = time.time()
    
    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def draw(self, surface):
        # Update the clock
        self.update()
        
        # Create font
        font = pygame.font.SysFont('Arial', 22, bold=True)
        small_font = pygame.font.SysFont('Arial', 18)
        
        # Draw white's clock
        y_pos = 180
        
        # White's move counter
        move_text = f"Moves: {self.white_moves}/{MOVES_THRESHOLD}"
        move_surface = small_font.render(move_text, True, BLACK)
        surface.blit(move_surface, (BOARD_PX + 20, y_pos))
        y_pos += 25
        
        # White's main time (if still under move threshold)
        if self.white_moves < MOVES_THRESHOLD:
            main_color = (255, 0, 0) if self.white_main_time < 300 else BLACK  # Red if < 5 min
            main_text = f"Main: {self.format_time(self.white_main_time)}"
            main_surface = font.render(main_text, True, main_color)
            surface.blit(main_surface, (BOARD_PX + 20, y_pos))
            y_pos += 25
        
        # White's secondary time
        second_color = (255, 0, 0) if self.white_secondary_time < 300 else BLACK
        second_text = f"Rest: {self.format_time(self.white_secondary_time)}"
        second_surface = font.render(second_text, True, second_color)
        surface.blit(second_surface, (BOARD_PX + 20, y_pos))
        y_pos += 35
        
        # Draw black's clock
        # Black's move counter
        move_text = f"Moves: {self.black_moves}/{MOVES_THRESHOLD}"
        move_surface = small_font.render(move_text, True, BLACK)
        surface.blit(move_surface, (BOARD_PX + 20, y_pos))
        y_pos += 25
        
        # Black's main time (if still under move threshold)
        if self.black_moves < MOVES_THRESHOLD:
            main_color = (255, 0, 0) if self.black_main_time < 300 else BLACK
            main_text = f"Main: {self.format_time(self.black_main_time)}"
            main_surface = font.render(main_text, True, main_color)
            surface.blit(main_surface, (BOARD_PX + 20, y_pos))
            y_pos += 25
        
        # Black's secondary time
        second_color = (255, 0, 0) if self.black_secondary_time < 300 else BLACK
        second_text = f"Rest: {self.format_time(self.black_secondary_time)}"
        second_surface = font.render(second_text, True, second_color)
        surface.blit(second_surface, (BOARD_PX + 20, y_pos))
        
        # Indicate active timer
        active_text = "▶ WHITE" if self.active_color == 'w' else "▶ BLACK"
        active = font.render(active_text, True, BLACK)
        surface.blit(active, (BOARD_PX + 20, 150))
        
        # Show time-out message if game is over
        if self.game_over:
            winner = "BLACK" if (self.white_moves < MOVES_THRESHOLD and self.white_main_time <= 0 and self.white_secondary_time <= 0) or (self.white_moves >= MOVES_THRESHOLD and self.white_secondary_time <= 0) else "WHITE"
            timeout_text = font.render(f"{winner} WINS ON TIME!", True, (255, 0, 0))
            surface.blit(timeout_text, (BOARD_PX + 20, y_pos + 30))

# Load chess piece images
def load_pieces():
    pieces = {}
    for color in ['w', 'b']:
        for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
            img = pygame.image.load(f'pieces/{color}{piece}.png')
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            pieces[f'{color}{piece}'] = img
    return pieces

# Create placeholders for piece images (would normally be loaded from files)
def create_placeholder_pieces():
    pieces = {}
    symbols = {
        'wp': '♙', 'wr': '♖', 'wn': '♘', 'wb': '♗', 'wq': '♕', 'wk': '♔',
        'bp': '♟', 'br': '♜', 'bn': '♞', 'bb': '♝', 'bq': '♛', 'bk': '♚'
    }
    
    font = pygame.font.SysFont('segoeuisymbol', 60)
    
    for piece, symbol in symbols.items():
        color = WHITE if piece.startswith('w') else BLACK
        bg_color = (200, 200, 200) if piece.startswith('w') else (50, 50, 50)
        
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surface, bg_color, (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//2.5)
        text = font.render(symbol, True, color)
        text_rect = text.get_rect(center=(SQUARE_SIZE//2, SQUARE_SIZE//2))
        surface.blit(text, text_rect)
        
        pieces[piece] = surface
    
    return pieces

class ChessBoard:
    def __init__(self):
        self.reset_board()
        self.selected_piece = None
        self.turn = 'w'  # White starts
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.in_check = False
        self.checkmate = False
        self.last_move = None
        self.valid_moves = []
        self.message = "White's turn to move"
        self.game_over = False  # Add this to track game over state
    
    def reset_board(self):
        # Initialize empty board
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Set up pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = 'bp'  # Black pawns
            self.board[6][col] = 'wp'  # White pawns
        
        # Set up back rows
        back_row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        for col in range(BOARD_SIZE):
            self.board[0][col] = 'b' + back_row[col]  # Black pieces
            self.board[7][col] = 'w' + back_row[col]  # White pieces
    
    def draw_board(self, surface):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
                color = LIGHT if (row + col) % 2 == 0 else DARK
                
                # Draw the square
                pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight the last move
                if self.last_move and ((row, col) == self.last_move[0] or (row, col) == self.last_move[1]):
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((255, 255, 0, 50))  # Semi-transparent yellow
                    surface.blit(highlight, (x, y))
                
                # Highlight the selected piece
                if self.selected_piece and self.selected_piece[0] == row and self.selected_piece[1] == col:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((100, 100, 255, 100))  # Semi-transparent blue
                    surface.blit(highlight, (x, y))
                
                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((0, 255, 0, 70))  # Semi-transparent green
                    surface.blit(highlight, (x, y))
                
                # Highlight king in check
                if self.in_check:
                    king_pos = self.white_king_pos if self.turn == 'w' else self.black_king_pos
                    if (row, col) == king_pos:
                        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill((255, 0, 0, 100))  # Semi-transparent red
                        surface.blit(highlight, (x, y))
    
    def draw_pieces(self, surface, pieces):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE
                    surface.blit(pieces[piece], (x, y))
    
    def draw_dragged_piece(self, surface, pieces, piece, pos):
        if piece:
            piece_img = pieces[piece]
            rect = piece_img.get_rect(center=pos)
            surface.blit(piece_img, rect)
    
    def draw_message_panel(self, surface):
        # Draw the message panel background
        pygame.draw.rect(surface, (240, 240, 240), (BOARD_PX, 0, 300, WINDOW_HEIGHT))
        pygame.draw.line(surface, BLACK, (BOARD_PX, 0), (BOARD_PX, WINDOW_HEIGHT), 2)
        
        # Create fonts
        title_font = pygame.font.SysFont('Arial', 28, bold=True)
        msg_font = pygame.font.SysFont('Arial', 22)
        turn_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Draw title
        title = title_font.render("Chess Game", True, BLACK)
        surface.blit(title, (BOARD_PX + 20, 30))
        
        # Draw current turn or game over status
        if not self.game_over:
            turn_text = "White's Turn" if self.turn == 'w' else "Black's Turn"
            turn_color = BLACK
        else:
            turn_text = "Game Over"
            turn_color = (255, 0, 0)  # Red for game over
            
        turn_label = turn_font.render(turn_text, True, turn_color)
        surface.blit(turn_label, (BOARD_PX + 20, 80))
        
        # Draw status message
        y_pos = 130
        words = self.message.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if msg_font.size(test_line)[0] < 280:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Add emphasis to checkmate message
        if self.checkmate:
            for i, line in enumerate(lines):
                if "Checkmate" in line:
                    text = msg_font.render(line, True, (255, 0, 0))  # Red for checkmate
                    text_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 6))
                    text_bg.fill((255, 255, 200))  # Light yellow background
                    surface.blit(text_bg, (BOARD_PX + 15, y_pos - 3))
                    surface.blit(text, (BOARD_PX + 20, y_pos))
                else:
                    text = msg_font.render(line, True, BLACK)
                    surface.blit(text, (BOARD_PX + 20, y_pos))
                y_pos += 30
        else:
            for line in lines:
                text = msg_font.render(line, True, BLACK)
                surface.blit(text, (BOARD_PX + 20, y_pos))
                y_pos += 30
        
        # Draw congratulatory message for checkmate
        if self.checkmate:
            winner = "Black" if self.turn == 'w' else "White"
            
            # Draw a celebration box
            pygame.draw.rect(surface, (240, 220, 130), (BOARD_PX + 15, y_pos + 20, 270, 100), 0, 10)
            pygame.draw.rect(surface, (200, 160, 30), (BOARD_PX + 15, y_pos + 20, 270, 100), 3, 10)
            
            congrats_font = pygame.font.SysFont('Arial', 24, bold=True)
            congrats_text = congrats_font.render(f"Congratulations!", True, (180, 0, 0))
            surface.blit(congrats_text, (BOARD_PX + 20, y_pos + 35))
            
            winner_font = pygame.font.SysFont('Arial', 26, bold=True)
            winner_text = winner_font.render(f"{winner} wins!", True, (0, 100, 0))
            surface.blit(winner_text, (BOARD_PX + 20, y_pos + 75))
    
    def get_piece_at(self, row, col):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col]
        return ''
    
    def select_piece(self, row, col):
        piece = self.get_piece_at(row, col)
        
        # Can only select your own pieces
        if piece and piece[0] == self.turn:
            self.selected_piece = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            return True
        return False
    def __init__(self):
        self.reset_board()
        self.selected_piece = None
        self.turn = 'w'  # White starts
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.in_check = False
        self.checkmate = False
        self.last_move = None
        self.valid_moves = []
        self.message = "White's turn to move"
        self.game_over = False  # Track game over state
        self.moves_history = []  # Track moves history

    def coords_to_algebraic(self, row, col):
        """Convert board coordinates to algebraic notation (e.g., e4)"""
        cols = 'abcdefgh'
        rows = '87654321'
        return cols[col] + rows[row]

    def save_moves_to_file(self, filename=None):
        """Save all moves played in the game to a text file"""
        if not self.moves_history:
            self.message = "No moves to save!"
            return
        
        # Generate default filename if none provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chess_game_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                # Write header
                f.write("Chess Game Moves\n")
                f.write("===============\n\n")
                
                # Write date and time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Game played on: {current_time}\n\n")
                
                # Write the moves in a nice format
                f.write("Moves:\n")
                for i, move in enumerate(self.moves_history):
                    move_number = i // 2 + 1
                    if i % 2 == 0:  # White's move
                        f.write(f"{move_number}. {move} ")
                    else:  # Black's move
                        f.write(f"{move}\n")
                
                # Add a newline if the last move was white's
                if len(self.moves_history) % 2 == 1:
                    f.write("\n")
                
                # Write game result if applicable
                if self.game_over:
                    f.write("\nResult: ")
                    if self.checkmate:
                        winner = "Black" if self.turn == 'w' else "White"
                        f.write(f"{winner} wins by checkmate")
                    else:
                        f.write("Draw")
            
            self.message = f"Game moves saved to {filename}"
        except Exception as e:
            self.message = f"Error saving moves: {str(e)}"
    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Get the piece being moved
        piece = self.board[from_row][from_col]
        
        # Check if it's a valid move
        if to_pos in self.valid_moves:
            # Record the move in algebraic notation
            from_algebraic = self.coords_to_algebraic(from_row, from_col)
            to_algebraic = self.coords_to_algebraic(to_row, to_col)
            piece_symbol = piece[1].upper() if piece[1] != 'p' else ''
            captured = self.board[to_row][to_col]
            move_notation = f"{piece_symbol}{from_algebraic}-{to_algebraic}"
            
            # Add capture indication
            if captured:
                move_notation = f"{piece_symbol}{from_algebraic}x{to_algebraic}"
            
            self.moves_history.append(move_notation)
            
            # Update king position if king is moved
            if piece[1] == 'k':
                if piece[0] == 'w':
                    self.white_king_pos = to_pos
                else:
                    self.black_king_pos = to_pos
            
            # Make the move
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = ''
            self.last_move = (from_pos, to_pos)
            
            # Check for pawn promotion
            handle_pawn_promotion(self, to_row, to_col)
            
            # Switch turns
            self.turn = 'b' if self.turn == 'w' else 'w'
            
            # Check if the opponent is in check or checkmate
            king_pos = self.white_king_pos if self.turn == 'w' else self.black_king_pos
            self.in_check = self.is_square_under_attack(king_pos[0], king_pos[1], self.turn)
            
            if self.in_check:
                # Check for checkmate
                self.checkmate = self.is_checkmate()
                if self.checkmate:
                    winner = "Black" if self.turn == 'w' else "White"
                    self.message = f"Checkmate! {winner} wins!"
                    self.game_over = True  # Set game over state
                else:
                    self.message = f"{'White' if self.turn == 'w' else 'Black'} is in check!"
            else:
                # Check for stalemate
                if self.is_stalemate():
                    self.message = "Stalemate! Game is a draw."
                    self.game_over = True  # Set game over state
                else:
                    self.message = f"{'White' if self.turn == 'w' else 'Black'}'s turn to move"
            
            return True
        else:
            self.message = "Invalid move! Try again."
            return False
    
    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
        
        piece_type = piece[1]
        color = piece[0]
        valid_moves = []
        
        # Get all theoretically valid moves based on piece type
        potential_moves = []
        
        if piece_type == 'p':  # Pawn
            direction = -1 if color == 'w' else 1
            
            # Move forward one square
            if 0 <= row + direction < BOARD_SIZE and not self.board[row + direction][col]:
                potential_moves.append((row + direction, col))
                
                # Move forward two squares from starting position
                if (color == 'w' and row == 6) or (color == 'b' and row == 1):
                    if not self.board[row + 2*direction][col]:
                        potential_moves.append((row + 2*direction, col))
            
            # Capture diagonally
            for dcol in [-1, 1]:
                if 0 <= row + direction < BOARD_SIZE and 0 <= col + dcol < BOARD_SIZE:
                    target = self.board[row + direction][col + dcol]
                    if target and target[0] != color:
                        potential_moves.append((row + direction, col + dcol))
        
        elif piece_type == 'r':  # Rook
            # Horizontal and vertical moves
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                for dist in range(1, BOARD_SIZE):
                    r, c = row + dr * dist, col + dc * dist
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    target = self.board[r][c]
                    if not target:
                        potential_moves.append((r, c))
                    elif target[0] != color:
                        potential_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'n':  # Knight
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    target = self.board[r][c]
                    if not target or target[0] != color:
                        potential_moves.append((r, c))
        
        elif piece_type == 'b':  # Bishop
            # Diagonal moves
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for dist in range(1, BOARD_SIZE):
                    r, c = row + dr * dist, col + dc * dist
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    target = self.board[r][c]
                    if not target:
                        potential_moves.append((r, c))
                    elif target[0] != color:
                        potential_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'q':  # Queen (combines rook and bishop moves)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                for dist in range(1, BOARD_SIZE):
                    r, c = row + dr * dist, col + dc * dist
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    target = self.board[r][c]
                    if not target:
                        potential_moves.append((r, c))
                    elif target[0] != color:
                        potential_moves.append((r, c))
                        break
                    else:
                        break
        
        elif piece_type == 'k':  # King
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    target = self.board[r][c]
                    if not target or target[0] != color:
                        potential_moves.append((r, c))
        
        # Filter moves that would leave the king in check
        for move in potential_moves:
            if self.is_move_safe(row, col, move[0], move[1]):
                valid_moves.append(move)
        
        return valid_moves
    
    def is_move_safe(self, from_row, from_col, to_row, to_col):
        # Make temporary move
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        # Update board temporarily
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ''
        
        # Update king position if king is moved
        original_king_pos = None
        if piece[1] == 'k':
            if piece[0] == 'w':
                original_king_pos = self.white_king_pos
                self.white_king_pos = (to_row, to_col)
            else:
                original_king_pos = self.black_king_pos
                self.black_king_pos = (to_row, to_col)
        
        # Check if king is in check after move
        king_pos = self.white_king_pos if piece[0] == 'w' else self.black_king_pos
        is_safe = not self.is_square_under_attack(king_pos[0], king_pos[1], piece[0])
        
        # Restore board
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured
        
        # Restore king position if king was moved
        if piece[1] == 'k':
            if piece[0] == 'w':
                self.white_king_pos = original_king_pos
            else:
                self.black_king_pos = original_king_pos
        
        return is_safe
    
    def is_square_under_attack(self, row, col, color):
        # Check if square (row, col) is attacked by any piece of the opposite color
        opposite_color = 'b' if color == 'w' else 'w'
        
        # Check pawns
        pawn_dir = 1 if color == 'w' else -1
        for dcol in [-1, 1]:
            r, c = row + pawn_dir, col + dcol
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                piece = self.board[r][c]
                if piece == opposite_color + 'p':
                    return True
        
        # Check knights
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                piece = self.board[r][c]
                if piece == opposite_color + 'n':
                    return True
        
        # Check king
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                piece = self.board[r][c]
                if piece == opposite_color + 'k':
                    return True
        
        # Check rooks, bishops, queens (along lines)
        directions = {
            'straight': [(1, 0), (-1, 0), (0, 1), (0, -1)],
            'diagonal': [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        
        # Check straight lines (rooks and queens)
        for dr, dc in directions['straight']:
            for dist in range(1, BOARD_SIZE):
                r, c = row + dr * dist, col + dc * dist
                if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                    break
                piece = self.board[r][c]
                if piece:
                    if piece[0] == opposite_color and (piece[1] == 'r' or piece[1] == 'q'):
                        return True
                    break
        
        # Check diagonals (bishops and queens)
        for dr, dc in directions['diagonal']:
            for dist in range(1, BOARD_SIZE):
                r, c = row + dr * dist, col + dc * dist
                if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                    break
                piece = self.board[r][c]
                if piece:
                    if piece[0] == opposite_color and (piece[1] == 'b' or piece[1] == 'q'):
                        return True
                    break
        
        return False
    
    def is_checkmate(self):
        # If not in check, can't be checkmate
        if not self.in_check:
            return False
        
        # Check if any piece can make a valid move
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece[0] == self.turn:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        return False
        
        # No valid moves and in check means checkmate
        return True
        
    def is_stalemate(self):
        # If in check, can't be stalemate
        if self.in_check:
            return False
        
        # Check if any piece can make a valid move
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece[0] == self.turn:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        return False
        
        # No valid moves and not in check means stalemate
        return True

def main():
    # Set up the game
    board = ChessBoard()
    # Create the timer
    timer = ChessTimer()
    
    try:
        # Try to load actual piece images
        pieces = load_pieces()
    except:
        # Use placeholder pieces if images aren't available
        pieces = create_placeholder_pieces()
    
    dragging = False
    drag_piece = None
    drag_pos = (0, 0)
    orig_pos = (0, 0)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Convert mouse position to board coordinates
                mouseX, mouseY = event.pos
                
                # Only handle clicks on the board and if the game is not over
                if mouseX < BOARD_PX and not board.game_over:
                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE
                    piece = board.get_piece_at(row, col)
                    
                    if piece and piece[0] == board.turn:
                        dragging = True
                        drag_piece = piece
                        orig_pos = (row, col)
                        drag_pos = event.pos
                        board.select_piece(row, col)
            
            elif event.type == MOUSEMOTION and dragging:
                drag_pos = event.pos
            
            elif event.type == MOUSEBUTTONUP and event.button == 1 and dragging:
                mouseX, mouseY = event.pos
                
                # Only handle drops on the board
                if mouseX < BOARD_PX:
                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE
                    to_pos = (row, col)
                    
                    # Try to move the piece
                    if orig_pos != to_pos:  # Only if it's actually moving
                        if board.move_piece(orig_pos, to_pos):
                            # Switch the timer when a successful move is made
                            if not board.game_over:  # Only switch if game is not over
                                timer.switch_turn()
                            else:
                                # If game is over due to checkmate, stop the timer
                                timer.game_over = True
                
                # Reset dragging state
                dragging = False
                drag_piece = None
                board.selected_piece = None
                board.valid_moves = []
        
        # Draw everything
        window.fill(WHITE)
        board.draw_board(window)
        board.draw_pieces(window, pieces)
        
        # Draw the dragged piece on top
        if dragging and drag_piece:
            board.draw_dragged_piece(window, pieces, drag_piece, drag_pos)
        
        # Draw message panel
        board.draw_message_panel(window)
        
        # Draw the timer
        timer.draw(window)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    def show_checkmate_modal(window, winner):
        """Display a modal dialog for checkmate"""
        modal_width = 400
        modal_height = 250
        
        # Calculate position to center the modal
        modal_x = (WINDOW_WIDTH - modal_width) // 2
        modal_y = (WINDOW_HEIGHT - modal_height) // 2
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        window.blit(overlay, (0, 0))
        
        # Draw modal background
        pygame.draw.rect(window, (240, 240, 210), (modal_x, modal_y, modal_width, modal_height), 0, 10)
        pygame.draw.rect(window, (218, 165, 32), (modal_x, modal_y, modal_width, modal_height), 3, 10)
        
        # Create fonts
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        message_font = pygame.font.SysFont('Arial', 28, bold=True)
        instruction_font = pygame.font.SysFont('Arial', 18)
        
        # Draw congratulations title
        title = title_font.render("Checkmate!", True, (180, 0, 0))
        title_rect = title.get_rect(center=(modal_x + modal_width // 2, modal_y + 70))
        window.blit(title, title_rect)
        
        # Draw winner message
        winner_msg = message_font.render(f"{winner} wins!", True, (0, 100, 0))
        winner_rect = winner_msg.get_rect(center=(modal_x + modal_width // 2, modal_y + 130))
        window.blit(winner_msg, winner_rect)
        
        # Draw instruction
        instruction = instruction_font.render("Click anywhere to continue", True, (100, 100, 100))
        instruction_rect = instruction.get_rect(center=(modal_x + modal_width // 2, modal_y + 200))
        window.blit(instruction, instruction_rect)
        
        # Update display
        pygame.display.flip()
        
        # Wait for click to dismiss
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    waiting_for_click = False

    def main():
        # Set up the game
        board = ChessBoard()
        # Create the timer
        timer = ChessTimer()
        
        try:
            # Try to load actual piece images
            pieces = load_pieces()
        except:
            # Use placeholder pieces if images aren't available
            pieces = create_placeholder_pieces()
        
        dragging = False
        drag_piece = None
        drag_pos = (0, 0)
        orig_pos = (0, 0)
        
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Convert mouse position to board coordinates
                    mouseX, mouseY = event.pos
                    
                    # Only handle clicks on the board and if the game is not over
                    if mouseX < BOARD_PX and not board.game_over:
                        col = mouseX // SQUARE_SIZE
                        row = mouseY // SQUARE_SIZE
                        piece = board.get_piece_at(row, col)
                        
                        if piece and piece[0] == board.turn:
                            dragging = True
                            drag_piece = piece
                            orig_pos = (row, col)
                            drag_pos = event.pos
                            board.select_piece(row, col)
                
                elif event.type == MOUSEMOTION and dragging:
                    drag_pos = event.pos
                
                elif event.type == MOUSEBUTTONUP and event.button == 1 and dragging:
                    mouseX, mouseY = event.pos
                    
                    # Only handle drops on the board
                    if mouseX < BOARD_PX:
                        col = mouseX // SQUARE_SIZE
                        row = mouseY // SQUARE_SIZE
                        to_pos = (row, col)
                        
                        # Try to move the piece
                        if orig_pos != to_pos:  # Only if it's actually moving
                            move_successful = board.move_piece(orig_pos, to_pos)
                            if move_successful:
                                # Switch the timer when a successful move is made
                                if not board.game_over:  # Only switch if game is not over
                                    timer.switch_turn()
                                else:
                                    # If game is over due to checkmate, stop the timer
                                    timer.game_over = True
                                    
                                    # Show checkmate modal if checkmate occurred
                                    if board.checkmate:
                                        winner = "Black" if board.turn == 'w' else "White"
                                        show_checkmate_modal(window, winner)
                    
                    # Reset dragging state
                    dragging = False
                    drag_piece = None
                    board.selected_piece = None
                    board.valid_moves = []
            
            # Draw everything
            window.fill(WHITE)
            board.draw_board(window)
            board.draw_pieces(window, pieces)
            
            # Draw the dragged piece on top
            if dragging and drag_piece:
                board.draw_dragged_piece(window, pieces, drag_piece, drag_pos)
            
            # Draw message panel
            board.draw_message_panel(window)
            
            # Draw the timer
            timer.draw(window)
            
            # Update the display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

    if __name__ == "__main__":
        main()