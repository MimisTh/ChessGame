# Μονάδα Σκακιέρας (chess_board.py)

## Επισκόπηση
Αυτή η μονάδα υλοποιεί την κλάση `ChessBoard`, η οποία αναπαριστά μια σκακιέρα και όλους τους κανόνες της. Περιλαμβάνει λειτουργίες για την προετοιμασία της σκακιέρας, τη μετακίνηση κομματιών, την ανίχνευση σαχ, και τον έλεγχο για ρουά-ματ ή πατ. Η κλάση `ChessBoard` λειτουργεί ως το κεντρικό στοιχείο της λογικής του παιχνιδιού, ενσωματώνοντας όλους τους κανόνες του σκακιού και επιβάλλοντάς τους κατά τη διάρκεια του παιχνιδιού.

## Ανάλυση Κώδικα Γραμμή προς Γραμμή

### Εισαγωγές
```python
from ..config import BOARD_SIZE
from ..pieces.piece_movement import (get_pawn_moves, get_rook_moves, get_knight_moves, 
                                    get_bishop_moves, get_queen_moves, get_king_moves, 
                                    is_square_under_attack)
from ..utils.file_handler import coords_to_algebraic, save_moves_to_file
```
- Εισάγει την σταθερά BOARD_SIZE από τη μονάδα config, που ορίζει το μέγεθος της σκακιέρας (8×8)
- Εισάγει όλες τις συναρτήσεις κίνησης κομματιών από τη μονάδα piece_movement που υλοποιούν τους κανόνες κίνησης για κάθε τύπο κομματιού

### Αρχικοποίηση
```python
class ChessBoard:
    def __init__(self):
        """
        Αρχικοποιεί μια νέα σκακιέρα με όλα τα κομμάτια στις αρχικές τους θέσεις.
        """
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
```
- Δημιουργεί μια άδεια σκακιέρα 8×8
- Καλεί τη μέθοδο setup_pieces για να τοποθετήσει τα κομμάτια στις αρχικές τους θέσεις
- Αρχικοποιεί τις μεταβλητές κατάστασης του παιχνιδιού:
  - turn: προσδιορίζει ποιος παίκτης παίζει ('w' για λευκά, 'b' για μαύρα)
  - last_move: αποθηκεύει την τελευταία κίνηση που έγινε
  - white_king_pos και black_king_pos: αποθηκεύουν τις θέσεις των βασιλιάδων
  - Μεταβλητές για δυνατότητα ροκέ
  - en_passant_target: αποθηκεύει τον στόχο για το "εν διελεύσει" αν είναι διαθέσιμο

### Αρχική Τοποθέτηση Κομματιών
```python
def reset_board(self):
    # Αρχικοποίηση του πίνακα
    self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # Τοποθέτηση στρατιωτών
    for col in range(BOARD_SIZE):
        self.board[1][col] = 'bp'  # Black pawns
        self.board[6][col] = 'wp'  # White pawns
```
- Τοποθετεί όλα τα κομμάτια στις αρχικές τους θέσεις στη σκακιέρα
- Κάθε κομμάτι αναπαριστάται από έναν συμβολοσειρά δύο χαρακτήρων:
  - Ο πρώτος χαρακτήρας υποδεικνύει το χρώμα ('w' για λευκό, 'b' για μαύρο)
  - Ο δεύτερος χαρακτήρας υποδεικνύει τον τύπο του κομματιού:
    - 'p' για πιόνι, 'r' για πύργο, 'n' για ίππο, 'b' για αξιωματικό, 'q' για βασίλισσα, 'k' για βασιλιά
- Τα κομμάτια τοποθετούνται σύμφωνα με την παραδοσιακή αρχική διάταξη σκακιέρας

```python
# Τοποθέτηση υπόλοιπων πιονιών
back_row = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
for col in range(BOARD_SIZE):
    self.board[0][col] = 'b' + back_row[col]  # μαύρα πιόνια
    self.board[7][col] = 'w' + back_row[col]  # λευκά πιόνια
```
- Τοποθετεί όλα τα κομμάτια στις αρχικές τους θέσεις στη σκακιέρα
- Κάθε κομμάτι αναπαριστάται από έναν συμβολοσειρά δύο χαρακτήρων:
  - Ο πρώτος χαρακτήρας υποδεικνύει το χρώμα ('w' για λευκό, 'b' για μαύρο)
  - Ο δεύτερος χαρακτήρας υποδεικνύει τον τύπο του κομματιού:
    - 'p' για πιόνι, 'r' για πύργο, 'n' για ίππο, 'b' για αξιωματικό, 'q' για βασίλισσα, 'k' για βασιλιά
- Τα κομμάτια τοποθετούνται σύμφωνα με την παραδοσιακή αρχική διάταξη σκακιέρας

### Απόκτηση Έγκυρων Κινήσεων
```python
def get_valid_moves(self, row, col):
    """
    Επιστρέφει μια λίστα όλων των έγκυρων κινήσεων για το κομμάτι στη συγκεκριμένη θέση.
    Περιλαμβάνει φιλτράρισμα κινήσεων που θα άφηναν τον βασιλιά εκτεθειμένο σε σαχ.
    """
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
```
- Επιστρέφει όλες τις έγκυρες κινήσεις για το κομμάτι στη συγκεκριμένη θέση
- Ελέγχει αν η θέση περιέχει κομμάτι και αν αυτό ανήκει στον τρέχοντα παίκτη
- Καλεί την κατάλληλη συνάρτηση κίνησης για τον συγκεκριμένο τύπο κομματιού
- Για τα πιόνια, ελέγχει αν υπάρχει δυνατότητα "en passant" (αιχμαλώτιση εν διελεύσει)
- Για τους βασιλιάδες, προσθέτει τις κινήσεις ροκέ όταν είναι διαθέσιμες, ελέγχοντας όλες τις προϋποθέσεις:
  - Ο βασιλιάς και ο πύργος δεν έχουν κινηθεί ακόμη
  - Δεν παρεμβάλλονται κομμάτια
  - Ο βασιλιάς δεν είναι σε σαχ
  - Τα τετράγωνα από τα οποία περνά ο βασιλιάς δεν απειλούνται
- Φιλτράρει τις κινήσεις που θα άφηναν τον βασιλιά εκτεθειμένο σε σαχ

```python
# Έλεγχος κινήσεων που αφήνουν τον βασιλιά σε σαχ
valid_moves = []
for move in potential_moves:
    if self.is_move_safe(row, col, move[0], move[1]):
        valid_moves.append(move)

return valid_moves
```
- Επιστρέφει όλες τις έγκυρες κινήσεις για το κομμάτι στη συγκεκριμένη θέση
- Ελέγχει αν η θέση περιέχει κομμάτι και αν αυτό ανήκει στον τρέχοντα παίκτη
- Καλεί την κατάλληλη συνάρτηση κίνησης για τον συγκεκριμένο τύπο κομματιού
- Για τα πιόνια, ελέγχει αν υπάρχει δυνατότητα "en passant" (αιχμαλώτιση εν διελεύσει)
- Για τους βασιλιάδες, προσθέτει τις κινήσεις ροκέ όταν είναι διαθέσιμες, ελέγχοντας όλες τις προϋποθέσεις:
  - Ο βασιλιάς και ο πύργος δεν έχουν κινηθεί ακόμη
  - Δεν παρεμβάλλονται κομμάτια
  - Ο βασιλιάς δεν είναι σε σαχ
  - Τα τετράγωνα από τα οποία περνά ο βασιλιάς δεν απειλούνται
- Φιλτράρει τις κινήσεις που θα άφηναν τον βασιλιά εκτεθειμένο σε σαχ

### Έλεγχος για Σαχ
```python
def is_king_in_check(self, color):
    """
    Ελέγχει αν ο βασιλιάς του δεδομένου χρώματος είναι σε σαχ.
    """
    if color == 'w':
        king_row, king_col = self.white_king_pos
    else:
        king_row, king_col = self.black_king_pos
    
    return self.is_square_attacked(king_row, king_col, color)

def is_square_attacked(self, row, col, color):
    """
    Ελέγχει αν το συγκεκριμένο τετράγωνο απειλείται από οποιοδήποτε κομμάτι του αντιπάλου.
    """
    return is_square_under_attack(self.board, row, col, color)
```
- is_king_in_check: Επιστρέφει αν ο βασιλιάς του δεδομένου χρώματος είναι σε σαχ
- is_square_attacked: Ελέγχει αν ένα συγκεκριμένο τετράγωνο απειλείται από αντίπαλα κομμάτια
- Χρησιμοποιεί τη συνάρτηση is_square_under_attack από τη μονάδα piece_movement που υλοποιεί τον πλήρη αλγόριθμο ανίχνευσης επιθέσεων

### Έλεγχος Κινήσεων που Προκαλούν Σαχ
```python
def is_move_safe(self, from_row, from_col, to_row, to_col):
    # Προσωρινή εκτέλεση κίνησης
    piece = self.board[from_row][from_col]
    captured = self.board[to_row][to_col]
    
    # Προσωρινή ενημέρωση της σκακιέρας
    self.board[to_row][to_col] = piece
    self.board[from_row][from_col] = ''
```
- Ελέγχει αν μια κίνηση θα άφηνε τον βασιλιά του παίκτη σε σαχ
- Δημιουργεί ένα προσωρινό αντίγραφο της κατάστασης της σκακιέρας
- Εκτελεί δοκιμαστικά την κίνηση
- Ελέγχει αν ο βασιλιάς είναι σε σαχ μετά την κίνηση
- Χειρίζεται ειδικές περιπτώσεις όπως το en-passant
- Επαναφέρει την αρχική κατάσταση της σκακιέρας ανεξάρτητα από το αποτέλεσμα

```python
# Ενημέρωση θέσης βασιλιά στην περίπτωση που κινείται
original_king_pos = None
if piece[1] == 'k':
    if piece[0] == 'w':
        original_king_pos = self.white_king_pos
        self.white_king_pos = (to_row, to_col)
    else:
        original_king_pos = self.black_king_pos
        self.black_king_pos = (to_row, to_col)
```
- Ενημερώνει τη θέση του βασιλιά αν κινείται βασιλιάς

```python
# Έλεγχος αν ο βασιλιάς είναι σε σαχ
king_pos = self.white_king_pos if piece[0] == 'w' else self.black_king_pos
is_safe = not is_square_under_attack(self.board, king_pos[0], king_pos[1], piece[0])
```
- Ελέγχει αν ο βασιλιάς του παίκτη είναι σε σαχ μετά την κίνηση
- Αν ο βασιλιάς είναι σε σαχ, η κίνηση δεν είναι ασφαλής

```python
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
```
- Επαναφέρει την αρχική κατάσταση της σκακιέρας
- Επαναφέρει τη θέση του βασιλιά αν κινήθηκε βασιλιάς
- Επιστρέφει αν η κίνηση είναι ασφαλής (δεν αφήνει τον βασιλιά σε σαχ)

### Εκτέλεση Κίνησης
```python
def move_piece(self, from_pos, to_pos):
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    # Εντοπισμός κινούμενου πιονιού
    piece = self.board[from_row][from_col]
    
    # Έλεγχος αν η κίνηση είναι έγκυρη
    if to_pos in self.valid_moves:
```
- Εκτελεί μια κίνηση στη σκακιέρα και ενημερώνει την κατάσταση του παιχνιδιού
- Χειρίζεται όλους τους ειδικούς κανόνες:
  - Ροκέ (μικρό και μεγάλο): μετακινεί τόσο τον βασιλιά όσο και τον πύργο
  - Αιχμαλώτιση en-passant: αφαιρεί το αιχμαλωτισμένο πιόνι
  - Προαγωγή πιονιού: αυτόματα προάγει τα πιόνια που φτάνουν στην τελευταία γραμμή σε βασίλισσες
- Ενημερώνει σημαίες για τη δυνατότητα ροκέ όταν κινούνται βασιλιάδες ή πύργοι
- Θέτει τον στόχο en-passant όταν ένα πιόνι κινείται δύο τετράγωνα
- Αποθηκεύει την τελευταία κίνηση για αναφορά
- Εναλλάσσει τη σειρά παίκτη
- Επιστρέφει ένα μήνυμα που περιγράφει την κίνηση

```python
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
```
- Καταγράφει την κίνηση σε αλγεβρική σημειογραφία σκακιού:
  - Μετατρέπει τις συντεταγμένες σε αλγεβρική σημειογραφία (π.χ., "e4")
  - Παίρνει το σύμβολο του κομματιού (κεφαλαίο για μη-πιόνια)
  - Χρησιμοποιεί 'x' για αιχμαλωτίσεις
  - Προσθέτει την κίνηση στο ιστορικό κινήσεων του παιχνιδιού

```python
# Ενημέρωση θέσης βασιλιά
if piece[1] == 'k':
    if piece[0] == 'w':
        self.white_king_pos = to_pos
    else:
        self.black_king_pos = to_pos
```
- Ενημερώνει τη θέση του βασιλιά αν κινείται βασιλιάς

```python
# Εκτέλεση κίνησης
self.board[to_row][to_col] = piece
self.board[from_row][from_col] = ''
self.last_move = (from_pos, to_pos)

# Έλεγχος για αναβάθμιση στρατιώτη
self.handle_pawn_promotion(to_row, to_col)
```
- Εκτελεί την κίνηση στη σκακιέρα:
  - Τοποθετεί το κομμάτι στη νέα του θέση
  - Αφαιρεί το κομμάτι από την αρχική του θέση
  - Καταγράφει την κίνηση ως την τελευταία κίνηση (για επισήμανση στο UI)
  - Ελέγχει για προαγωγή πιονιού αν είναι απαραίτητο

```python
# αλλαγή γύρου
self.turn = 'b' if self.turn == 'w' else 'w'
```
- Εναλλάσσει τη σειρά παίκτη

```python
# Έλεγχος για σαχ
king_pos = self.white_king_pos if self.turn == 'w' else self.black_king_pos
self.in_check = is_square_under_attack(self.board, king_pos[0], king_pos[1], self.turn)
```
- Ελέγχει αν ο βασιλιάς του τρέχοντος παίκτη είναι σε σαχ μετά την κίνηση
- Χρησιμοποιεί τη συνάρτηση is_square_under_attack από τη μονάδα piece_movement

```python
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
```
- Ενημερώνει την κατάσταση του παιχνιδιού και τα μηνύματα με βάση το αποτέλεσμα της κίνησης:
  - Αν ο τρέχων παίκτης είναι σε σαχ:
    - Ελέγχει αν είναι ρουά ματ (τέλος παιχνιδιού, ο τρέχων παίκτης χάνει)
    - Αν δεν είναι ρουά ματ, θέτει μήνυμα για σαχ
  - Αν δεν είναι σε σαχ:
    - Ελέγχει για πατ (ισοπαλία)
    - Διαφορετικά θέτει ένα τυπικό μήνυμα σειράς παίκτη

```python
return True
else:
    self.message = "Άκυρη κίνηση! Προσπάθησε ξανά."
    return False
```
- Επιστρέφει true αν η κίνηση εκτελέστηκε επιτυχώς
- Διαφορετικά θέτει μήνυμα για άκυρη κίνηση και επιστρέφει false

### Έλεγχος για Ματ ή Πατ
```python
def is_checkmate(self):
    """
    Ελέγχει αν η τρέχουσα κατάσταση του παιχνιδιού είναι ματ.
    """
    # Έλεγχος αν ο παίκτης που έχει σειρά είναι σε σαχ
    if not self.is_king_in_check(self.turn):
        return False
    
    # Έλεγχος αν υπάρχουν οποιεσδήποτε έγκυρες κινήσεις
    return self.has_no_valid_moves()

def is_stalemate(self):
    """
    Ελέγχει αν η τρέχουσα κατάσταση του παιχνιδιού είναι πατ (ισοπαλία).
    """
    # Έλεγχος αν ο παίκτης που έχει σειρά ΔΕΝ είναι σε σαχ
    if self.is_king_in_check(self.turn):
        return False
    
    # Έλεγχος αν δεν υπάρχουν έγκυρες κινήσεις
    return self.has_no_valid_moves()

def has_no_valid_moves(self):
    """
    Ελέγχει αν ο τρέχων παίκτης δεν έχει καμία έγκυρη κίνηση.
    """
    # Έλεγχος κάθε κομματιού του παίκτη
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = self.board[row][col]
            if piece and piece[0] == self.turn:
                # Αν βρεθεί έστω και μία έγκυρη κίνηση, επιστρέφει False
                if self.get_valid_moves(row, col):
                    return False
    
    # Αν ελεγχθούν όλα τα κομμάτια και δεν βρεθεί καμία έγκυρη κίνηση, επιστρέφει True
    return True
```
- is_checkmate: Ελέγχει αν η τρέχουσα κατάσταση είναι ματ (ο βασιλιάς είναι σε σαχ και δεν υπάρχουν έγκυρες κινήσεις)
- is_stalemate: Ελέγχει αν η τρέχουσα κατάσταση είναι πατ (ο βασιλιάς δεν είναι σε σαχ και δεν υπάρχουν έγκυρες κινήσεις)
- has_no_valid_moves: Ελέγχει αν ο τρέχων παίκτης έχει οποιαδήποτε έγκυρη κίνηση
  - Διατρέχει όλα τα κομμάτια του παίκτη
  - Ελέγχει αν υπάρχει τουλάχιστον μία έγκυρη κίνηση για οποιοδήποτε κομμάτι
  - Επιστρέφει True αν δεν βρεθεί καμία έγκυρη κίνηση

### Μετατροπή Συντεταγμένων
```python
def coords_to_algebraic(self, row, col):
    """
    Μετατρέπει συντεταγμένες πλέγματος (row, col) σε αλγεβρική σημειογραφία σκακιού (π.χ., 'e4').
    """
    file = chr(97 + col)  # 'a' έως 'h'
    rank = 8 - row        # 1 έως 8
    return file + str(rank)

def algebraic_to_coords(self, algebraic):
    """
    Μετατρέπει αλγεβρική σημειογραφία σκακιού (π.χ., 'e4') σε συντεταγμένες πλέγματος (row, col).
    """
    if len(algebraic) != 2:
        return None
    
    file = algebraic[0].lower()
    rank = algebraic[1]
    
    if not ('a' <= file <= 'h') or not ('1' <= rank <= '8'):
        return None
    
    col = ord(file) - ord('a')  # 0 έως 7
    row = 8 - int(rank)          # 0 έως 7
    
    return (row, col)
```
- coords_to_algebraic: Μετατρέπει συντεταγμένες πίνακα (row, col) σε τυπική αλγεβρική σημειογραφία σκακιού (π.χ., 'e4')
- algebraic_to_coords: Αντίστροφη μετατροπή, από αλγεβρική σημειογραφία σε συντεταγμένες πίνακα
- Αυτές οι μέθοδοι είναι χρήσιμες για την ανάγνωση και καταγραφή παιχνιδιών σκακιού και για επικοινωνία με τον χρήστη με τη χρήση τυπικών συντεταγμένων σκακιού