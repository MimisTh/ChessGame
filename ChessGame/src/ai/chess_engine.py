import random
import time
from copy import deepcopy
from ..config import BOARD_SIZE

class ChessEngine:
    """
    Μια απλή υλοποίηση μηχανής σκακιού που χρησιμοποιεί τον αλγόριθμο Minimax 
    με alpha-beta κλάδεμα για αναζήτηση κινήσεων.
    """
    
    def __init__(self, difficulty=2):
        """
        Αρχικοποίηση της μηχανής σκακιού
        difficulty: επίπεδο δυσκολίας (1-3)
            - 1: Εύκολο (βάθος αναζήτησης 1)
            - 2: Μεσαίο (βάθος αναζήτησης 2)
            - 3: Δύσκολο (βάθος αναζήτησης 3)
        """
        self.difficulty = difficulty
        self.search_depth = difficulty
        # Αξίες κομματιών για την αξιολόγηση θέσης
        self.piece_values = {
            'p': 10,    # Στρατιώτης
            'n': 30,    # Ίππος
            'b': 30,    # Αξιωματικός
            'r': 50,    # Πύργος
            'q': 90,    # Βασίλισσα
            'k': 900    # Βασιλιάς
        }
        
    def get_best_move(self, board, is_maximizing=False):
        """
        Αναζήτηση καλύτερης κίνησης για τον μαύρο παίκτη (AI)
        """
        # Κάνουμε μια μικρή καθυστέρηση για να φαίνεται πιο φυσικό
        time.sleep(0.5)
        
        # Σε πολύ χαμηλό επίπεδο δυσκολίας, επιλέγουμε τυχαία κίνηση από τις δυνατές
        if self.difficulty == 0:
            return self.get_random_move(board)
        
        # Συλλογή όλων των δυνατών κινήσεων - χρησιμοποιώντας τον κανονικό έλεγχο του board
        all_moves = []
        
        # Διατρέχουμε όλα τα πιόνια του μαύρου παίκτη και παίρνουμε έγκυρες κινήσεις
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece[0] == 'b':
                    # Παίρνουμε έγκυρες κινήσεις (που δεν οδηγούν σε σαχ) από τη μέθοδο του board
                    valid_moves = board.get_valid_moves(row, col)
                    for move in valid_moves:
                        all_moves.append(((row, col), move))
        
        # Αν δεν υπάρχουν κινήσεις, επιστρέφουμε None
        if not all_moves:
            return None
            
        best_move = None
        best_score = float('-inf')
        
        # Αναζήτηση καλύτερης κίνησης με minimax
        for from_pos, to_pos in all_moves:
            # Δημιουργία αντιγράφου της σκακιέρας για δοκιμή κίνησης
            temp_board = deepcopy(board)
            
            # Εκτέλεση κίνησης στο αντίγραφο
            self.make_temp_move(temp_board, from_pos, to_pos)
            
            # Αξιολόγηση κίνησης με minimax
            score = self.minimax(temp_board, self.search_depth - 1, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
        
        return best_move
    
    def get_random_move(self, board):
        """Επιλογή τυχαίας κίνησης από τις διαθέσιμες"""
        all_moves = []
        
        # Διατρέχουμε όλα τα πιόνια του μαύρου παίκτη και παίρνουμε έγκυρες κινήσεις
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece[0] == 'b':
                    # Παίρνουμε έγκυρες κινήσεις από τη μέθοδο του board
                    valid_moves = board.get_valid_moves(row, col)
                    for move in valid_moves:
                        all_moves.append(((row, col), move))
                        
        return random.choice(all_moves) if all_moves else None
    
    def get_all_moves(self, board, color):
        """Συλλογή όλων των δυνατών κινήσεων για τον παίκτη με το συγκεκριμένο χρώμα"""
        moves = []
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.get_piece_at(row, col)
                if piece and piece[0] == color:
                    # Παίρνουμε όλες τις έγκυρες κινήσεις για το πιόνι
                    valid_moves = board.get_valid_moves(row, col)
                    # Προσθέτουμε τις κινήσεις στη λίστα
                    for move in valid_moves:
                        moves.append(((row, col), move))
        
        return moves
    
    def make_temp_move(self, board, from_pos, to_pos):
        """Εκτελεί προσωρινή κίνηση στη σκακιέρα για αξιολόγηση"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Αποθήκευση πιονιού που κινείται
        moving_piece = board.board[from_row][from_col]
        
        # Αποθήκευση του πιονιού στη θέση προορισμού (αν υπάρχει)
        captured_piece = board.board[to_row][to_col]
        
        # Έλεγχος για αποφυγή λήψης βασιλιά (αυτό είναι παράνομη κίνηση)
        if captured_piece and captured_piece[1] == 'k':
            # Προσθήκη κώδικα επιβεβαίωσης για αποφυγή λήψης βασιλιά
            board.in_check = True
            board.checkmate = True
            board.game_over = True
            
            # Καθορισμός του νικητή με βάση το χρώμα του βασιλιά που θα έπαιρνε
            if captured_piece[0] == 'w':
                board.turn = 'w'  # Για να δείξει ότι ο λευκός έχασε
            else:
                board.turn = 'b'  # Για να δείξει ότι ο μαύρος έχασε
            return
        
        # Ενημέρωση θέσης βασιλιά εάν κινείται
        if moving_piece[1] == 'k':
            if moving_piece[0] == 'w':
                board.white_king_pos = (to_row, to_col)
            else:
                board.black_king_pos = (to_row, to_col)
        
        # Εκτέλεση κίνησης
        board.board[to_row][to_col] = moving_piece
        board.board[from_row][from_col] = ''
        
        # Αλλαγή γύρου
        board.turn = 'w' if board.turn == 'b' else 'b'
        
        # Απλοποιημένος έλεγχος για προαγωγή πιονιού
        if moving_piece[1] == 'p':
            if (moving_piece[0] == 'w' and to_row == 0) or (moving_piece[0] == 'b' and to_row == 7):
                board.board[to_row][to_col] = moving_piece[0] + 'q'  # Προαγωγή σε βασίλισσα
    
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """Αλγόριθμος Minimax με κλάδεμα alpha-beta για αναζήτηση καλύτερης κίνησης"""
        # Βασική περίπτωση: φτάσαμε στο μέγιστο βάθος ή τέλος παιχνιδιού
        if depth == 0 or board.checkmate or board.is_stalemate():
            return self.evaluate_board(board)
        
        if is_maximizing:  # Maximizing player (μαύρα)
            best_score = float('-inf')
            all_moves = self.get_all_moves(board, 'b')
            
            for from_pos, to_pos in all_moves:
                temp_board = deepcopy(board)
                self.make_temp_move(temp_board, from_pos, to_pos)
                score = self.minimax(temp_board, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:  # Minimizing player (λευκά)
            best_score = float('inf')
            all_moves = self.get_all_moves(board, 'w')
            
            for from_pos, to_pos in all_moves:
                temp_board = deepcopy(board)
                self.make_temp_move(temp_board, from_pos, to_pos)
                score = self.minimax(temp_board, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    
    def evaluate_board(self, board):
        """
        Αξιολόγηση θέσης σκακιέρας
        Θετικές τιμές ευνοούν τα μαύρα, αρνητικές τα λευκά
        """
        score = 0
        
        # Έλεγχος για τέλος παιχνιδιού
        if board.checkmate:
            return 10000 if board.turn == 'w' else -10000
        
        if board.is_stalemate():
            return 0  # Ισοπαλία
        
        # Υπολογισμός υλικού και θέσης
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board.board[row][col]
                if piece:
                    # Αξία υλικού
                    value = self.piece_values[piece[1]]
                    
                    # Προσημασμένη τιμή ανάλογα με το χρώμα
                    if piece[0] == 'b':
                        score += value
                        
                        # Επιπλέον μπόνους για την προχωρημένη θέση στρατιωτών
                        if piece[1] == 'p':
                            score += row * 0.5  # Μπόνους για προχωρημένους στρατιώτες
                    else:
                        score -= value
                        
                        # Επιπλέον μπόνους για την προχωρημένη θέση στρατιωτών
                        if piece[1] == 'p':
                            score -= (7 - row) * 0.5
        
        # Μπόνους για τον έλεγχο του κέντρου (τετράγωνα 3,3 έως 4,4)
        for row in range(3, 5):
            for col in range(3, 5):
                piece = board.board[row][col]
                if piece:
                    if piece[0] == 'b':
                        score += 0.5
                    else:
                        score -= 0.5
        
        return score