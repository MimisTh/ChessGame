import pygame
import sys
from pygame.locals import *
import time
from datetime import datetime

#Αρχικοποίηση pygame
pygame.init()
# Συνάρτηση για αναβάθμιση πιονιού
def handle_pawn_promotion(chess_board, row, col):

    piece = chess_board.board[row][col]
    if piece and piece[1] == 'p':  # If it's a pawn
        # Έλεγχος για λευκό πιόνι στην κορυφή ή μαύρο στη βάση του πίνακα
        if (piece[0] == 'w' and row == 0) or (piece[0] == 'b' and row == 7):
            # Αναβάθμιση σε βασίλισσα μέσω αντικατάστασης
            chess_board.board[row][col] = piece[0] + 'q'
            chess_board.message = f"Ο στρατιώτης αναβαθμίστηκε σε βασίλισσα!"
            return True
    return False
# Σταθερές για το παιχνίδι κατά pygame
BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_PX = BOARD_SIZE * SQUARE_SIZE
WINDOW_WIDTH = BOARD_PX + 300  # Χώρος για μηνύματα/ενημερώσεις παιχνιδιού
WINDOW_HEIGHT = BOARD_PX
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (75, 75, 75)
LIGHT = (238, 238, 238)
HIGHLIGHT = (186, 202, 68)#πράσινη υπογράμμιση για δυνατές κινήσεις
MOVE_HIGHLIGHT = (255, 255, 0, 100)#κίτρινη υπογράμμιση για τελευταία κίνηση
CHECK_HIGHLIGHT = (255, 0, 0, 100)#κόκκινη υπογράμμιση για σαχ

# Χρονόμετρο(σε δευτερόλεπτα)
DEFAULT_MAIN_TIME = 2 * 60 * 60  # 2 ώρες για τις χ πρώτες κινήσεις παρακάτω
DEFAULT_SECONDARY_TIME = 30 * 60  # 30 λεπτά για το υπόλοιπο του παιχνιδιού
MOVES_THRESHOLD = 40  # Αριθμός κινήσεων πριν τη λήξη του αρχικού παιχνιδιού
# Παραμετροποίηση Παραθύρου
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Σκάκι ΠΛΗΠΡΟ')
clock = pygame.time.Clock()

# Κλάση Χρονομέτρου για ρολόγια σκακιού παικτών
class ChessTimer:
    """
ChessTimer - Μια κλάση για τη διαχείριση χρονομέτρων παιχνιδιού σκακιού με σύστημα ελέγχου χρόνου δύο περιόδων.
Το χρονόμετρο υλοποιεί ένα ρολόι σκακιού με κύρια περίοδο χρόνου και δευτερεύουσα περίοδο χρόνου. Οι παίκτες πρέπει 
να πραγματοποιήσουν έναν καθορισμένο αριθμό κινήσεων (MOVES_THRESHOLD) εντός του κύριου χρόνου τους. Αφού φτάσουν
αυτό το όριο, παίζουν με τον δευτερεύοντα χρόνο τους.
Ιδιότητες:
    white_main_time (float): Κύριος χρόνος σε δευτερόλεπτα για τον λευκό παίκτη
    black_main_time (float): Κύριος χρόνος σε δευτερόλεπτα για τον μαύρο παίκτη
    white_secondary_time (float): Δευτερεύων χρόνος σε δευτερόλεπτα για τον λευκό παίκτη
    black_secondary_time (float): Δευτερεύων χρόνος σε δευτερόλεπτα για τον μαύρο παίκτη
    white_moves (int): Αριθμός κινήσεων που έγιναν από τον λευκό παίκτη
    black_moves (int): Αριθμός κινήσεων που έγιναν από τον μαύρο παίκτη
    active_color (str): Τρέχων ενεργός παίκτης ('w' για λευκό, 'b' για μαύρο)
    last_update (float): Χρονική στιγμή της τελευταίας ενημέρωσης του χρονομέτρου
    game_over (bool): Ένδειξη που δηλώνει αν το παιχνίδι έχει τελειώσει λόγω λήξης χρόνου
Μέθοδοι:
    __init__(main_time, secondary_time): 
        Αρχικοποίηση του χρονομέτρου με καθορισμένες περιόδους κύριου και δευτερεύοντος χρόνου.
    update(): 
        Ενημέρωση του υπολειπόμενου χρόνου του ενεργού παίκτη βάσει του χρόνου που έχει περάσει από την τελευταία ενημέρωση.
    switch_turn(): 
        Αλλαγή του ενεργού παίκτη και αύξηση του μετρητή κινήσεων για τον παίκτη που μόλις κινήθηκε.
    format_time(seconds): 
        Μορφοποίηση τιμής χρόνου σε δευτερόλεπτα σε αναγνώσιμη μορφή (ΩΩ:ΛΛ:ΔΔ ή ΛΛ:ΔΔ).
    draw(surface): 
        Απεικόνιση των πληροφοριών χρονομέτρησης στην παρεχόμενη επιφάνεια pygame, συμπεριλαμβανομένων των μετρητών κινήσεων,
        του υπολειπόμενου χρόνου για κάθε παίκτη και της ένδειξης ενεργού παίκτη.
"""
    
    def __init__(self, main_time=DEFAULT_MAIN_TIME, secondary_time=DEFAULT_SECONDARY_TIME):
        #Αρχικοποίηση χρόνων για τους παίκτες
        self.white_main_time = main_time
        self.black_main_time = main_time
        self.white_secondary_time = secondary_time
        self.black_secondary_time = secondary_time
        #Αριθμός κινήσεων για κάθε παίκτη
        self.white_moves = 0
        self.black_moves = 0
        #Αρχικοποίηση του χρώματος του ενεργού παίκτη
        self.active_color = 'w'
        #Αρχικοποίηση του χρόνου τελευταίας ενημέρωσης
        self.last_update = time.time()
        #αντικείμενο τερματισμού παιχνιδιού
        self.game_over = False
    

    def update(self):

        if self.game_over:
            return
            
        current = time.time()

        elapsed = current - self.last_update

        self.last_update = current
        
        # Ενημέρωση του χρόνου για τον ενεργό παίκτη
        if self.active_color == 'w':
            # Έλεγχος αν ο λευκός παίκτης έχει υπερβεί τον κύριο χρόνο
            if self.white_moves < MOVES_THRESHOLD:
                self.white_main_time -= elapsed
                if self.white_main_time <= 0:
                    # Υπολογισμός του δευτερεύοντος χρόνου που υπερβαίνει τον κύριο χρόνο
                    elapsed_overflow = -self.white_main_time
                    self.white_main_time = 0
                    self.white_secondary_time -= elapsed_overflow
            else:
                self.white_secondary_time -= elapsed
            
            # Έλεγχος αν ο χρόνος έχει λήξει
            if self.white_moves < MOVES_THRESHOLD and self.white_main_time <= 0 and self.white_secondary_time <= 0:
                self.white_secondary_time = 0
                self.game_over = True
            elif self.white_moves >= MOVES_THRESHOLD and self.white_secondary_time <= 0:
                self.white_secondary_time = 0
                self.game_over = True
        else:
            # Έλεγχος αν ο μαύρος παίκτης έχει υπερβεί τον κύριο χρόνο
            if self.black_moves < MOVES_THRESHOLD:
                self.black_main_time -= elapsed
                if self.black_main_time <= 0:
                    elapsed_overflow = -self.black_main_time
                    self.black_main_time = 0
                    self.black_secondary_time -= elapsed_overflow
            else:
                self.black_secondary_time -= elapsed
            
            # Έλεγχος αν ο χρόνος έχει λήξει
            if self.black_moves < MOVES_THRESHOLD and self.black_main_time <= 0 and self.black_secondary_time <= 0:
                self.black_secondary_time = 0
                self.game_over = True
            elif self.black_moves >= MOVES_THRESHOLD and self.black_secondary_time <= 0:
                self.black_secondary_time = 0
                self.game_over = True
    
    def switch_turn(self):
        # Αύξηση του μετρητή κινήσεων για τον ενεργό παίκτη
        if self.active_color == 'w':
            self.white_moves += 1
        else:
            self.black_moves += 1
        
        # Αλλαγή του ενεργού παίκτη
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
        # Ενημέρωση του χρόνου στο γραφικό περιβάλλον
        self.update()
        
        #  Δημιουργία γραμματοσειράς για το ρολόι
        font = pygame.font.SysFont('Arial', 22, bold=True)
        small_font = pygame.font.SysFont('Arial', 18)
        
        # Σχεδίαση ρολογιού για τον λευκό παίκτη
        y_pos = 180
        
        # Σχεδίαση μετρητή κινήσεων για τον λευκό παίκτη
        move_text = f"Κινήσεις: {self.white_moves}/{MOVES_THRESHOLD}"
        move_surface = small_font.render(move_text, True, BLACK)
        surface.blit(move_surface, (BOARD_PX + 20, y_pos))
        y_pos += 25
        
        # Σχεδίαση κύριου χρόνου για τον λευκό παίκτη (αν είναι ακόμα κάτω από το όριο κινήσεων)
        if self.white_moves < MOVES_THRESHOLD:
            main_color = (255, 0, 0) if self.white_main_time < 300 else BLACK  # Red if < 5 min
            main_text = f"Κύριος Χρόνος: {self.format_time(self.white_main_time)}"
            main_surface = font.render(main_text, True, main_color)
            surface.blit(main_surface, (BOARD_PX + 20, y_pos))
            y_pos += 25
        
        # Σχεδίαση δευτερεύοντα χρόνου για τον λευκό παίκτη
        second_color = (255, 0, 0) if self.white_secondary_time < 300 else BLACK
        second_text = f"Δευτερεύων Χρόνος: {self.format_time(self.white_secondary_time)}"
        second_surface = font.render(second_text, True, second_color)
        surface.blit(second_surface, (BOARD_PX + 20, y_pos))
        y_pos += 35
        
        # Σχεδίαση ρολογιού για τον μαύρο παίκτη
        # Σχεδίαση μετρητή κινήσεων για τον μαύρο παίκτη
        move_text = f"Κινήσεις: {self.black_moves}/{MOVES_THRESHOLD}"
        move_surface = small_font.render(move_text, True, BLACK)
        surface.blit(move_surface, (BOARD_PX + 20, y_pos))
        y_pos += 25
        
        # Σχεδίαση κύριου χρόνου για τον μαύρο παίκτη (αν είναι ακόμα κάτω από το όριο κινήσεων)
        if self.black_moves < MOVES_THRESHOLD:
            main_color = (255, 0, 0) if self.black_main_time < 300 else BLACK
            main_text = f"Κύριος Χρόνος: {self.format_time(self.black_main_time)}"
            main_surface = font.render(main_text, True, main_color)
            surface.blit(main_surface, (BOARD_PX + 20, y_pos))
            y_pos += 25
        
        # Σχεδίαση δευτερεύοντα χρόνου για τον μαύρο παίκτη
        second_color = (255, 0, 0) if self.black_secondary_time < 300 else BLACK
        second_text = f"Δευτερεύων Χρόνος: {self.format_time(self.black_secondary_time)}"
        second_surface = font.render(second_text, True, second_color)
        surface.blit(second_surface, (BOARD_PX + 20, y_pos))
        
        # Ενημέρωση του ενεργού παίκτη
        active_text = "> ΛΕΥΚΟ" if self.active_color == 'w' else "> ΜΑΥΡΟ"
        active = font.render(active_text, True, BLACK)
        surface.blit(active, (BOARD_PX + 20, 150))
        
        # Εμφάνιση μηνύματος για το τέλος του παιχνιδιού στην περίπτωση που έχει λήξει ο χρόνος
        if self.game_over:
            winner = "ΜΑΥΡΟΣ" if (self.white_moves < MOVES_THRESHOLD and self.white_main_time <= 0 and self.white_secondary_time <= 0) or (self.white_moves >= MOVES_THRESHOLD and self.white_secondary_time <= 0) else "ΛΕΥΚΟΣ"
            timeout_text = font.render(f"Ο {winner} ΝΙΚΗΣΕ ΕΝΤΟΣ ΧΡΟΝΟΥ!", True, (255, 0, 0))
            surface.blit(timeout_text, (BOARD_PX + 20, y_pos + 30))

# Συνάρτηση για την φόρτωση των πιονιών
def load_pieces():
    pieces = {}
    for color in ['w', 'b']:
        for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
            img = pygame.image.load(f'pieces/{color}{piece}.png')
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            pieces[f'{color}{piece}'] = img
    return pieces

# Συνάρτηση για την δημιουργία των πιονιών με σύμβολα (περίπτωση σφάλματος στην φόρτωση των εικόνων)
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
        self.turn = 'w'  # Εκκίνηση με τον λευκό
        self.black_king_pos = (0, 4)
        self.in_check = False
        self.checkmate = False
        self.last_move = None
        self.valid_moves = []
        self.message = "Σειρά του Λευκού να κινηθεί"
        self.game_over = False  # Κατάσταση τέλους παιχνιδιού
    #Επαναφορά του πίνακα
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
    #Σχεδίαση του πίνακα
    def draw_board(self, surface):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
                color = LIGHT if (row + col) % 2 == 0 else DARK
                
                # Σχεδιασμός τετραγώνου
                pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Υπογράμμιση τελευταίας κίνησης
                if self.last_move and ((row, col) == self.last_move[0] or (row, col) == self.last_move[1]):
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((255, 255, 0, 50))  # Semi-transparent yellow
                    surface.blit(highlight, (x, y))
                
                # Υπογράμμιση επιλεγμένου πιονιού
                if self.selected_piece and self.selected_piece[0] == row and self.selected_piece[1] == col:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((100, 100, 255, 100))  # Semi-transparent blue
                    surface.blit(highlight, (x, y))
                
                # Υπογράμμιση δυνατών κινήσεων
                if (row, col) in self.valid_moves:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((0, 255, 0, 70))  # Semi-transparent green
                    surface.blit(highlight, (x, y))
                
                # Υπογράμμιση βασιλιά υπο σαχ
                if self.in_check:
                    king_pos = self.white_king_pos if self.turn == 'w' else self.black_king_pos
                    if (row, col) == king_pos:
                        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill((255, 0, 0, 100))  # Ημιδιάφανο κόκκινο
                        surface.blit(highlight, (x, y))
    # Σχεδίαση πιονιών
    def draw_pieces(self, surface, pieces):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE
                    surface.blit(pieces[piece], (x, y))
    #Σχεδίαση πιονιών που μετακινούνται
    def draw_dragged_piece(self, surface, pieces, piece, pos):
        if piece:
            piece_img = pieces[piece]
            rect = piece_img.get_rect(center=pos)
            surface.blit(piece_img, rect)
    #Σχεδίαση πάνελ μηνυμάτων
    def draw_message_panel(self, surface):
        # Σχεδίαση υποβάθρου πάνελ μηνυμάτων
        pygame.draw.rect(surface, (240, 240, 240), (BOARD_PX, 0, 300, WINDOW_HEIGHT))
        pygame.draw.line(surface, BLACK, (BOARD_PX, 0), (BOARD_PX, WINDOW_HEIGHT), 2)
        
        # Δημιουργία μεταβλητών γραμματοσειρών
        title_font = pygame.font.SysFont('Arial', 28, bold=True)
        msg_font = pygame.font.SysFont('Arial', 22)
        turn_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Δημιουργία τίτλου και στρογγυλεμένου πλαισίου
        title = title_font.render("Σκάκι ΠΛΗΠΡΟ", True, BLACK)
        surface.blit(title, (BOARD_PX + 20, 30))
        
        # Σχεδίαση μηνύματος σειράς ή λήξης
        if not self.game_over:
            turn_text = "Σειρά του Λευκού παίκτη" if self.turn == 'w' else "Σειρά του Μαύρου παίκτη"
            turn_color = BLACK
        else:
            turn_text = "Τέλος παιχνιδιού"
            turn_color = (255, 0, 0)  # Κόκκινο για τέλος παιχνιδιού
            
        turn_label = turn_font.render(turn_text, True, turn_color)
        surface.blit(turn_label, (BOARD_PX + 20, 80))
        
        # Σχεδίαση μηνυμάτων κατάστασης
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
    #Κατασκευαστής κλάσης
    def __init__(self):
        self.reset_board()
        self.selected_piece = None
        self.turn = 'w'
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.in_check = False
        self.checkmate = False
        self.last_move = None
        self.valid_moves = []
        self.message = "White's turn to move"
        self.game_over = False 
        self.moves_history = []  # Ιστορικό κινήσεων

    # Μετατροπή συντεταγμένων σε αλγεβρική σημειογραφία σκακιού (π.χ. e4)
    def coords_to_algebraic(self, row, col):
        cols = 'abcdefgh'
        rows = '87654321'
        return cols[col] + rows[row]
    # Αποθήκευση κινήσεων σε αρχείο κειμένου
    def save_moves_to_file(self, filename=None):
        if not self.moves_history:
            self.message = "Καμία κίνηση προς αποθήκευση!"
            return
        
        # Αν δεν υφίστατι αρχείο, δημιουργία με βάση την τρέχουσα χρονική στιγμή
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chess_game_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                # Εγγραφή κεφαλίδας
                f.write("Κινήσεις Σκακιού\n")
                f.write("===============\n\n")
                
                # Εγγραφή χρόνου και ημερομηνίας
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Το παιχνίδι πραγματοποιήθηκε την: {current_time}\n\n")
                
                # Write the moves in a nice format
                f.write("Κινήσεις:\n")
                for i, move in enumerate(self.moves_history):
                    move_number = i // 2 + 1
                    if i % 2 == 0:  # White's move
                        f.write(f"{move_number}. {move} ")
                    else:  # Black's move
                        f.write(f"{move}\n")
                
                # Add a newline if the last move was white's
                if len(self.moves_history) % 2 == 1:
                    f.write("\n")
                
                # Εμφάνιση αποτελέσματος όπου δύναται
                if self.game_over:
                    f.write("\nΑποτέλεσμα: ")
                    if self.checkmate:
                        winner = "Μαύρος" if self.turn == 'w' else "Λευκός"
                        f.write(f"Ο {winner} παίκτης νίκησε!")
                    else:
                        f.write("Ισοπαλία!")
            
            self.message = f"Το ιστορικό του παιχνιδιού αποθηκεύτηκε με όνομα {filename}"
        except Exception as e:
            self.message = f"Σφάλμα κατά την αποθήκευση: {str(e)}"\
    #Συνάρτηση μετακίνησης πιονιού
    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Εντοπισμός κινούμενου πιονιού
        piece = self.board[from_row][from_col]
        
        # Έλεγχος αν η κίνηση είναι έγκυρη
        if to_pos in self.valid_moves:
            # Καταγραφή κίνησης με αλγεβραική σημειογραφία
            from_algebraic = self.coords_to_algebraic(from_row, from_col)
            to_algebraic = self.coords_to_algebraic(to_row, to_col)
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
            handle_pawn_promotion(self, to_row, to_col)
            
            # αλλαγή γύρου
            self.turn = 'b' if self.turn == 'w' else 'w'
            
            # Έλεγχος για σαχ
            king_pos = self.white_king_pos if self.turn == 'w' else self.black_king_pos
            self.in_check = self.is_square_under_attack(king_pos[0], king_pos[1], self.turn)
            
            if self.in_check:
                # Έλεγχος για checkmate
                self.checkmate = self.is_checkmate()
                if self.checkmate:
                    winner = "Μάυρος" if self.turn == 'w' else "Άσπρος"
                    self.message = f"Ρουά Ματ!Ο {winner} παικτης νίκησε!"
                    self.game_over = True  # Ορισμός κατάστασης τέλους παιχνιδιού
                else:
                    self.message = f"{'Ο άσπρος' if self.turn == 'w' else 'μαύρος'} παίκτης είναι σε σαχ!"
            else:
                # Έλεγχος για πατ
                if self.is_stalemate():
                    self.message = "Πατ!Το παιχνίδι είναι ισοπαλία."
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
        valid_moves = []
        
        # Εύρεση δυνατών κινήσεων ανάλογα με τον τύπο του πιονιού
        potential_moves = []
        
        if piece_type == 'p':  # Στρατιώτης
            direction = -1 if color == 'w' else 1
            
            # Κίνηση μπροστά
            if 0 <= row + direction < BOARD_SIZE and not self.board[row + direction][col]:
                potential_moves.append((row + direction, col))
                
                # Κίνηση δύο τετραγώνων αν είναι η πρώτη κίνηση
                if (color == 'w' and row == 6) or (color == 'b' and row == 1):
                    if not self.board[row + 2*direction][col]:
                        potential_moves.append((row + 2*direction, col))
            
            # Κίνηση διαγώνια για φάγωμα
            for dcol in [-1, 1]:
                if 0 <= row + direction < BOARD_SIZE and 0 <= col + dcol < BOARD_SIZE:
                    target = self.board[row + direction][col + dcol]
                    if target and target[0] != color:
                        potential_moves.append((row + direction, col + dcol))
        
        elif piece_type == 'r':  # Πύργος   
            # Κίνηση κάθετα και οριζόντια
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
        
        elif piece_type == 'n':  # Ίππος
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    target = self.board[r][c]
                    if not target or target[0] != color:
                        potential_moves.append((r, c))
        
        elif piece_type == 'b':  # Αξιωματικός
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
        
        elif piece_type == 'q':  # Βασίλισσα (συνδυασμός Πύργου και Ιππότη)
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
        
        elif piece_type == 'k':  # Βασιλιάς
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    target = self.board[r][c]
                    if not target or target[0] != color:
                        potential_moves.append((r, c))
        
        # Έλεγχος κινήσεων βασιλιά στο ρουά
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
        
        #Έλεγχος αν ο βασιλιάς είναι σε σαχ
        king_pos = self.white_king_pos if piece[0] == 'w' else self.black_king_pos
        is_safe = not self.is_square_under_attack(king_pos[0], king_pos[1], piece[0])
        
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
    
    def is_square_under_attack(self, row, col, color):
        # Έλεγχος αν η συγκεκριμένη θέση είναι υπό επίθεση από τον αντίπαλο παίκτη
        opposite_color = 'b' if color == 'w' else 'w'
        
        # Έλεγχος στρατιωτών
        pawn_dir = 1 if color == 'w' else -1
        for dcol in [-1, 1]:
            r, c = row + pawn_dir, col + dcol
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                piece = self.board[r][c]
                if piece == opposite_color + 'p':
                    return True
        
        # Έλεγχος ίππου
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                piece = self.board[r][c]
                if piece == opposite_color + 'n':
                    return True
        
        # Έλεγχος βασιλιά
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                piece = self.board[r][c]
                if piece == opposite_color + 'k':
                    return True
        
        # Έλεγχος πύργου, αξιωματικού και βασίλισσας
        directions = {
            'straight': [(1, 0), (-1, 0), (0, 1), (0, -1)],
            'diagonal': [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        
        # Έλεγχος ίσιων γραμμών(πύργος και βασίλισσα)
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
        
        # Έλεγχος διαγώνιων γραμμών(αξιωματικός και βασίλισσα)
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

def main():
    # Αρχικοποίηση της σκακιέρας
    board = ChessBoard()
    # Αρχικοποίηση του χρονομέτρου
    timer = ChessTimer()
    
    try:
        # Φόρτωση πραγματικών εικόνων πιονιών
        pieces = load_pieces()
    except:
        # Φόρτωση συμβόλων στην περίπτωση αποτυχίας
        pieces = create_placeholder_pieces()
    
    dragging = False
    drag_piece = None
    drag_pos = (0, 0)
    orig_pos = (0, 0)
    
    # ΚΎΡΙΑ ΔΟΜΗ ΕΠΑΝΑΛΗΨΗΑΣ ΠΑΙΧΝΙΔΙΟΥ
    running = True
    while running:
        # ΔΙΑΧΕΙΡΙΣΗ ΑΜΕΣΩΝ ΧΕΙΡΙΣΜΩΝ ΓΡΑΦΙΚΟΥ ΠΕΡΙΒΑΛΛΟΝΤΟΣ
        for event in pygame.event.get():
            # Έλεγχος για τερματισμό του παιχνιδιού
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Μετατροπή θέσης ποντιού σε συντεταγμένες
                mouseX, mouseY = event.pos
                
                # Έλεγχος για κλικ σε πιόνι στην σκακιέρα (εντός ισχύος παιχνιδιού και εντός ορίων σκακιέρας)
                if mouseX < BOARD_PX and not board.game_over:
                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE
                    # Εύρεση πιονιού στην συγκεκριμένη θέση
                    piece = board.get_piece_at(row, col)
                    # Έλεγχος αν το πιόνι είναι του παίκτη που παίζει και ενεργοποίηση της λειτουργίας drag και μετακίνησης
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
                
                # Έλεγχος για απελευθέρωση πιονιού εντός της σκακιέρας
                if mouseX < BOARD_PX:
                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE
                    to_pos = (row, col)
                    
                    # Επιχείρηση μετακίνησης πιονιού
                    if orig_pos != to_pos:  # Έλεγχος επιλογής διαφορετικής θέσης
                        if board.move_piece(orig_pos, to_pos):
                            # εναλλαγή χρονομέτρου που μειώνεται με την κίνηση
                            if not board.game_over:  # Μόνο αν το παιχνίδι δεν έχει τελειώσει
                                timer.switch_turn()
                            else:
                                # Αν το παιχνίδι έχει τελειώσει λόγω ρουά ματ, διακοπή χρονομέτρου
                                timer.game_over = True
                
                # Απενεργοποίηση λειτουργίας drag
                dragging = False
                drag_piece = None
                board.selected_piece = None
                board.valid_moves = []
        
        # ΕΝΗΜΕΡΩΣΗ ΓΡΑΦΙΚΟΥ ΠΕΡΙΒΑΛΛΟΝΤΟΣ
        window.fill(WHITE)
        board.draw_board(window)
        board.draw_pieces(window, pieces)
        
        # Σχεδίαση πιονιού που μετακινείται στο προσκήνιο
        if dragging and drag_piece:
            board.draw_dragged_piece(window, pieces, drag_piece, drag_pos)
        
        # Σχεδίαση πάνελ μηνυμάτων
        board.draw_message_panel(window)
        
        # Σχεδίαση χρονομέτρου
        timer.draw(window)
        
        # Ενημέρωση οθόνης
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    def show_checkmate_modal(window, winner):
        """Σχηματισμός modal μηνύματος στο προσκήνιο για ρουά ματ."""
        modal_width = 400
        modal_height = 250
        
        # θέση κεντραρίσματος του modal
        modal_x = (WINDOW_WIDTH - modal_width) // 2
        modal_y = (WINDOW_HEIGHT - modal_height) // 2
        
        # Σκίαση υποβάθρου του modal
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Ημιδιάφανο μαύρο
        window.blit(overlay, (0, 0))
        
        # Σχεδίαση modal και υποβάθρου
        pygame.draw.rect(window, (240, 240, 210), (modal_x, modal_y, modal_width, modal_height), 0, 10)
        pygame.draw.rect(window, (218, 165, 32), (modal_x, modal_y, modal_width, modal_height), 3, 10)
        
        # Γραμματοσειρά modal
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        message_font = pygame.font.SysFont('Arial', 28, bold=True)
        instruction_font = pygame.font.SysFont('Arial', 18)
        
        # Σχεδίαση συγχαρητήριου τίτλου
        title = title_font.render("Ρουά Ματ!", True, (180, 0, 0))
        title_rect = title.get_rect(center=(modal_x + modal_width // 2, modal_y + 70))
        window.blit(title, title_rect)
        
        # Σχεδίαση μηνύματος νικητή
        winner_msg = message_font.render(f"Ο {winner} παίκτης νίκησε!", True, (0, 100, 0))
        winner_rect = winner_msg.get_rect(center=(modal_x + modal_width // 2, modal_y + 130))
        window.blit(winner_msg, winner_rect)
        
        # Σχεδίαση οδηγίας συνέχειας
        instruction = instruction_font.render("Πατήστε οπουδήποτε να συνεχίσετε..", True, (100, 100, 100))
        instruction_rect = instruction.get_rect(center=(modal_x + modal_width // 2, modal_y + 200))
        window.blit(instruction, instruction_rect)
        
        # Ενημέρωση οθόνης
        pygame.display.flip()
        
        # Αναμονή για κλικ για συνέχεια
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    waiting_for_click = False

    def main():
        # Αρχικοποίηση σκακιέρας
        board = ChessBoard()
        # Αρχικοποίηση χρονομέτρου
        timer = ChessTimer()
        
        try:
            # Φόρτωση πραγματικών εικόνων πιονιών
            pieces = load_pieces()
        except:
            # Φόρτωση συμβόλων στην περίπτωση αποτυχίας φόρτωσης πραγματικών εικόνων
            pieces = create_placeholder_pieces()
        
        dragging = False
        drag_piece = None
        drag_pos = (0, 0)
        orig_pos = (0, 0)
        
        # Κύρια δομή επανάληψης παιχνιδιού
        running = True
        while running:
            # Διαχείριση αμεσών χειρισμών γραφικού περιβάλλοντος
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Μετατροπή θέσης ποντιού σε συντεταγμένες
                    mouseX, mouseY = event.pos
                    
                    # Έλεγχος για κλικ σε πιόνι στην σκακιέρα (εντός ισχύος παιχνιδιού και εντός ορίων σκακιέρας)
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
                    
                    # Έλεγχος για απελευθέρωση πιονιού εντός της σκακιέρας
                    if mouseX < BOARD_PX:
                        col = mouseX // SQUARE_SIZE
                        row = mouseY // SQUARE_SIZE
                        to_pos = (row, col)
                        
                        #   Επιχείρηση μετακίνησης πιονιού
                        if orig_pos != to_pos:  # Έλεγχος επιλογής διαφορετικής θέσης
                            move_successful = board.move_piece(orig_pos, to_pos)
                            if move_successful:
                                # Εναλλαγή χρονομέτρου που μειώνεται με την κίνηση
                                if not board.game_over:  # Μόνο αν το παιχνίδι δεν έχει τελειώσει
                                    timer.switch_turn()
                                else:
                                    # Αν το παιχνίδι έχει τελειώσει λόγω ρουά ματ, διακοπή χρονομέτρου
                                    timer.game_over = True
                                    
                                    # Εμφάνιση modal για ρουά ματ
                                    if board.checkmate:
                                        winner = "Μαύρος" if board.turn == 'w' else "Λευκός"
                                        show_checkmate_modal(window, winner)
                    
                    # Απενεργοποίηση λειτουργίας drag
                    dragging = False
                    drag_piece = None
                    board.selected_piece = None
                    board.valid_moves = []
                    
                elif event.type == KEYDOWN:
                    # Έλεγχος για αποθήκευση παιχνιδιού(πάτημα πλήκτρου 's')
                    if event.key == K_s:
                        board.save_moves_to_file()
                        print("Game saved to file")
            
            # Ενημέρωση γραφικού περιβάλλοντος
            window.fill(WHITE)
            board.draw_board(window)
            board.draw_pieces(window, pieces)
            
            # Σχεδίαση πιονιού που μετακινείται στο προσκήνιο
            if dragging and drag_piece:
                board.draw_dragged_piece(window, pieces, drag_piece, drag_pos)
            
            # Σχεδίαση πάνελ μηνυμάτων
            board.draw_message_panel(window)
            
            # Σχεδίαση χρονομέτρου
            timer.draw(window)
            
            # Ενημέρωση οθόνης
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

    if __name__ == "__main__":
        main()