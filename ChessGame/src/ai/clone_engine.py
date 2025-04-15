import random
from copy import deepcopy
import time
from ..utils.pgn_parser import PGNParser
from ..config import BOARD_SIZE

class CloneEngine:
    """
    A chess engine that attempts to mimic the play style of a specific player
    by analyzing their previous games from PGN files.
    """
    
    def __init__(self):
        self.pgn_parser = PGNParser()
        self.loaded = False
        self.player_name = "Unknown Player"
        self.fallback_difficulty = 2  #Επίπεδο δυσκολίας για την εναλλακτική μηχανή σκακιού	
        self.move_history = []  # Διατήρηση ιστορικού κινήσεων
        
        # Μετατροπή αλγεβρικής σημειογραφίας σε συντεταγμένες πίνακα
        self.file_to_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self.rank_to_row = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        
    def load_player_data(self):
        """Load and analyze PGN data for a player"""
        file_path = self.pgn_parser.select_pgn_file()
        if file_path:
            success = self.pgn_parser.parse_pgn_file(file_path)
            if success:
                self.loaded = True
                self.player_name = self.pgn_parser.get_player_name()
                return self.pgn_parser.get_style_summary()
            else:
                return "Failed to parse the PGN file."
        return "No file selected."
    
    def get_best_move(self, board):
        """
        Get the best move based on the player's style.
        If no matching position is found, fall back to a standard algorithm.
        """
        # Add a small delay to simulate thinking
        time.sleep(0.5)
        
        if not self.loaded:
            # If no player data is loaded, use standard algorithm
            from .chess_engine import ChessEngine
            fallback_engine = ChessEngine(difficulty=self.fallback_difficulty)
            return fallback_engine.get_best_move(board)
        
        # Update move history with the last white move
        if board.last_move and board.turn == 'b':
            from_pos, to_pos = board.last_move
            from_algebraic = self._coords_to_algebraic(from_pos)
            to_algebraic = self._coords_to_algebraic(to_pos)
            piece = board.board[to_pos[0]][to_pos[1]]
            piece_type = piece[1].upper() if piece[1] != 'p' else ''
            
            # Add the white move to history
            white_move = f"{piece_type}{from_algebraic}-{to_algebraic}"
            if self.move_history and self.move_history[-1][0] == 'b':
                self.move_history.append(('w', white_move))
        
        # Create a simplified position key from recent moves
        position_key = str(self.move_history[-6:]) if len(self.move_history) >= 6 else str(self.move_history)
        
        # Try to get a move from the player's style
        pgn_move = self.pgn_parser.get_most_likely_move(position_key)
        
        if pgn_move:
            # Try to convert the PGN move to board coordinates
            try:
                move_coords = self._pgn_move_to_coords(board, pgn_move)
                if move_coords:
                    from_pos, to_pos = move_coords
                    
                    # Verify if this is a valid move
                    valid_moves = board.get_valid_moves(from_pos[0], from_pos[1])
                    if to_pos in valid_moves:
                        # Add the move to history
                        self.move_history.append(('b', pgn_move))
                        return from_pos, to_pos
            except:
                # If conversion fails, fall back to standard algorithm
                pass
        
        # Fallback to standard algorithm if no matching style move is found
        from .chess_engine import ChessEngine
        fallback_engine = ChessEngine(difficulty=self.fallback_difficulty)
        best_move = fallback_engine.get_best_move(board)
        
        # If a move was found, add to history in PGN format
        if best_move:
            from_pos, to_pos = best_move
            from_algebraic = self._coords_to_algebraic(from_pos)
            to_algebraic = self._coords_to_algebraic(to_pos)
            piece = board.board[from_pos[0]][from_pos[1]]
            piece_type = piece[1].upper() if piece[1] != 'p' else ''
            
            captured = board.board[to_pos[0]][to_pos[1]]
            if captured:
                black_move = f"{piece_type}{from_algebraic}x{to_algebraic}"
            else:
                black_move = f"{piece_type}{from_algebraic}-{to_algebraic}"
                
            self.move_history.append(('b', black_move))
            
        return best_move
    
    def _coords_to_algebraic(self, coords):
        """Convert board coordinates to algebraic notation"""
        row, col = coords
        files = "abcdefgh"
        ranks = "87654321"
        return files[col] + ranks[row]
    
    def _algebraic_to_coords(self, algebraic):
        """Convert algebraic notation to board coordinates"""
        if len(algebraic) < 2:
            return None
        col = self.file_to_col.get(algebraic[0].lower())
        row = self.rank_to_row.get(algebraic[1])
        if col is not None and row is not None:
            return row, col
        return None
    
    def _pgn_move_to_coords(self, board, pgn_move):
        """
        Convert a PGN move to board coordinates.
        This is a simplified implementation and doesn't handle all PGN formats.
        """
        # Remove check/mate symbols
        pgn_move = pgn_move.replace('+', '').replace('#', '')
        
        # Handle castling
        if pgn_move == "O-O" or pgn_move == "0-0":  # Kingside castling
            return (0, 4), (0, 6) if board.turn == 'b' else (7, 4), (7, 6)
        elif pgn_move == "O-O-O" or pgn_move == "0-0-0":  # Queenside castling
            return (0, 4), (0, 2) if board.turn == 'b' else (7, 4), (7, 2)
        
        # Handle standard moves (this is a simplified version)
        # For simplicity, we'll just look for a piece of the right type that can move to the target square
        
        # Extract piece type, if any
        piece_type = 'p'  # Default to pawn
        if pgn_move[0].upper() in "RNBQK":
            piece_type = pgn_move[0].lower()
            pgn_move = pgn_move[1:]
        
        # Handle captures
        capture = 'x' in pgn_move
        if capture:
            parts = pgn_move.split('x')
            from_part = parts[0]
            to_part = parts[1]
        else:
            # Try to identify the destination square
            to_part = pgn_move[-2:] if len(pgn_move) >= 2 else ""
            from_part = pgn_move[:-2] if len(pgn_move) > 2 else ""
        
        # Get destination coordinates
        to_coords = self._algebraic_to_coords(to_part)
        if not to_coords:
            return None
        
        # Find a piece that can move to the destination
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.board[row][col]
                if piece and piece[0] == board.turn and piece[1] == piece_type:
                    # Check if this piece can move to the destination
                    valid_moves = board.get_valid_moves(row, col)
                    if to_coords in valid_moves:
                        # If there's disambiguation info, make sure it matches
                        if from_part:
                            algebraic = self._coords_to_algebraic((row, col))
                            if from_part in algebraic:
                                return (row, col), to_coords
                        else:
                            return (row, col), to_coords
        
        return None