from ..config import BOARD_SIZE
from ..pieces.piece_movement import (get_pawn_moves, get_rook_moves, get_knight_moves, 
                                    get_bishop_moves, get_queen_moves, get_king_moves, 
                                    is_square_under_attack)
from ..utils.file_handler import coords_to_algebraic, save_moves_to_file

class ChessBoard:
    def __init__(self):
        self.reset_board()
        self.selected_piece = None
        self.turn = 'w'  # Εκκίνηση με τον λευκό
        self.black_king_pos = (0, 4)
        self.white_king_pos = (7, 4)
        self.in_check = False
        self.checkmate = False
        self.last_move = None
        self.valid_moves = []
        self.message = "Σειρά του Λευκού να κινηθεί"
        self.game_over = False  # Κατάσταση τέλους παιχνιδιού
        self.moves_history = []  # Ιστορικό κινήσεων
    
    def reset_board(self):
        # Αρχικοποίηση του πίνακα
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Τοποθέτηση στρατιωτών
        for col in range(BOARD_SIZE):
            self.board[1][col] = 'bp'  # Black pawns
            self.board[6][col] = 'wp'  # White pawns
        
        # Τοποθέτηση υπόλοιπων πιονιών
        back_row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        for col in range(BOARD_SIZE):
            self.board[0][col] = 'b' + back_row[col]  # μαύρα πιόνια
            self.board[7][col] = 'w' + back_row[col]  # λευκά πιόνια
    
    def get_piece_at(self, row, col):
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col]
        return ''
    
    def select_piece(self, row, col):
        piece = self.get_piece_at(row, col)
        
        # Έλεγχος αν το πιόνι είναι του παίκτη που παίζει
        if piece and piece[0] == self.turn:
            self.selected_piece = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            return True
        return False
    
    def save_moves_to_file(self, filename=None):
        message, success = save_moves_to_file(
            self.moves_history, 
            self.game_over, 
            self.checkmate, 
            self.turn, 
            filename
        )
        self.message = message
        return success
    
    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Εντοπισμός κινούμενου πιονιού
        piece = self.board[from_row][from_col]
        
        # Έλεγχος αν η κίνηση είναι έγκυρη
        if to_pos in self.valid_moves:
            # Καταγραφή κίνησης με αλγεβραική σημειογραφία
            from_algebraic = coords_to_algebraic(from_row, from_col)
            to_algebraic = coords_to_algebraic(to_row, to_col)
            piece_symbol = piece[1].upper() if piece[1] != 'p' else ''
            captured = self.board[to_row][to_col]
            move_notation = f"{piece_symbol}{from_algebraic}-{to_algebraic}"
            
            # Καταγραφή κίνησης "φαγώματος"
            if captured:
                move_notation = f"{piece_symbol}{from_algebraic}x{to_algebraic}"
            
            self.moves_history.append(move_notation)
            
            # Ενημέρωση θέσης βασιλιά
            if piece[1] == 'k':
                if piece[0] == 'w':
                    self.white_king_pos = to_pos
                else:
                    self.black_king_pos = to_pos
            
            # Εκτέλεση κίνησης
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = ''
            self.last_move = (from_pos, to_pos)
            
            # Έλεγχος για αναβάθμιση στρατιώτη
            self.handle_pawn_promotion(to_row, to_col)
            
            # αλλαγή γύρου
            self.turn = 'b' if self.turn == 'w' else 'w'
            
            # Έλεγχος για σαχ
            king_pos = self.white_king_pos if self.turn == 'w' else self.black_king_pos
            self.in_check = is_square_under_attack(self.board, king_pos[0], king_pos[1], self.turn)
            
            if self.in_check:
                # Έλεγχος για checkmate
                self.checkmate = self.is_checkmate()
                if self.checkmate:
                    winner = "Μάυρος" if self.turn == 'w' else "Άσπρος"
                    self.message = f"Ρουά Ματ! Ο {winner} παικτης νίκησε!"
                    self.game_over = True  # Ορισμός κατάστασης τέλους παιχνιδιού
                else:
                    self.message = f"{'Ο άσπρος' if self.turn == 'w' else 'μαύρος'} παίκτης είναι σε σαχ!"
            else:
                # Έλεγχος για πατ
                if self.is_stalemate():
                    self.message = "Πατ! Το παιχνίδι είναι ισοπαλία."
                    self.game_over = True  # Ορισμός κατάστασης τέλους παιχνιδιού
                else:
                    self.message = f"Ο {'Λευκός' if self.turn == 'w' else 'Μαύρος'} παίκτης παίζει"
            
            return True
        else:
            self.message = "Άκυρη κίνηση! Προσπάθησε ξανά."
            return False
    
    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
        
        piece_type = piece[1]
        color = piece[0]
        
        # Εύρεση δυνατών κινήσεων ανάλογα με τον τύπο του πιονιού
        potential_moves = []
        
        if piece_type == 'p':
            potential_moves = get_pawn_moves(self.board, row, col, color)
        elif piece_type == 'r':
            potential_moves = get_rook_moves(self.board, row, col, color)
        elif piece_type == 'n':
            potential_moves = get_knight_moves(self.board, row, col, color)
        elif piece_type == 'b':
            potential_moves = get_bishop_moves(self.board, row, col, color)
        elif piece_type == 'q':
            potential_moves = get_queen_moves(self.board, row, col, color)
        elif piece_type == 'k':
            potential_moves = get_king_moves(self.board, row, col, color)
        
        # Έλεγχος κινήσεων που αφήνουν τον βασιλιά σε σαχ
        valid_moves = []
        for move in potential_moves:
            if self.is_move_safe(row, col, move[0], move[1]):
                valid_moves.append(move)
        
        return valid_moves
    
    def is_move_safe(self, from_row, from_col, to_row, to_col):
        # Προσωρινή εκτέλεση κίνησης
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        # Προσωρινή ενημέρωση της σκακιέρας
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ''
        
        # Ενημέρωση θέσης βασιλιά στην περίπτωση που κινείται
        original_king_pos = None
        if piece[1] == 'k':
            if piece[0] == 'w':
                original_king_pos = self.white_king_pos
                self.white_king_pos = (to_row, to_col)
            else:
                original_king_pos = self.black_king_pos
                self.black_king_pos = (to_row, to_col)
        
        # Έλεγχος αν ο βασιλιάς είναι σε σαχ
        king_pos = self.white_king_pos if piece[0] == 'w' else self.black_king_pos
        is_safe = not is_square_under_attack(self.board, king_pos[0], king_pos[1], piece[0])
        
        # Αποκατάσταση της σκακιέρας
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured
        
        # Αποκατάσταση της θέσης του βασιλιά
        if piece[1] == 'k':
            if piece[0] == 'w':
                self.white_king_pos = original_king_pos
            else:
                self.black_king_pos = original_king_pos
        
        return is_safe
    
    def is_checkmate(self):
        # Έλεγχος αν υπάρχει σαχ πριν το ρουα ματ(για επιβεβαίωση)
        if not self.in_check:
            return False
        
        # Έλεγχος αν κάποιο πιόνι μπορεί να κινηθεί για να αποφευχθεί το ρουα ματ
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece[0] == self.turn:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        return False
        
        # Αν δεν υπάρχει κίνηση που να αποφεύγει το ρουα ματ, τότε υπάρχει ρουα ματ
        return True
    
    def is_stalemate(self):
        # Έλεγχος αν υπάρχει σαχ, δεν υπάρχει πατ στην περίπτωση αυτή
        if self.in_check:
            return False
        
        # Έλεγχος αν υπάρχει κίνηση που να αποφεύγει το πατ(δεν γίνεται τότε να ισχύει πατ)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece[0] == self.turn:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        return False
        
        # Αν δεν υπάρχει κίνηση που να αποφεύγει το πατ και δεν υπάρχει σαχ, τότε υπάρχει πατ
        return True
    
    def handle_pawn_promotion(self, row, col):
        """Συνάρτηση για αναβάθμιση πιονιού"""
        piece = self.board[row][col]
        if piece and piece[1] == 'p':  # If it's a pawn
            # Έλεγχος για λευκό πιόνι στην κορυφή ή μαύρο στη βάση του πίνακα
            if (piece[0] == 'w' and row == 0) or (piece[0] == 'b' and row == 7):
                # Αναβάθμιση σε βασίλισσα μέσω αντικατάστασης
                self.board[row][col] = piece[0] + 'q'
                self.message = f"Ο στρατιώτης αναβαθμίστηκε σε βασίλισσα!"
                return True
        return False