# Μονάδα Τεχνητής Νοημοσύνης Μηχανής Κλώνου (clone_engine.py)

## Επισκόπηση
Αυτή η μονάδα υλοποιεί μια μηχανή τεχνητής νοημοσύνης σκακιού που προσπαθεί να μιμηθεί το στυλ παιχνιδιού ενός συγκεκριμένου παίκτη αναλύοντας προηγούμενα παιχνίδια του από αρχεία PGN (Portable Game Notation). Αν δεν έχουν φορτωθεί δεδομένα παίκτη ή δεν βρεθούν αντίστοιχες κινήσεις, επιστρέφει σε μια τυπική μηχανή σκακιού.

## Ανάλυση Γραμμή προς Γραμμή

### Εισαγωγές
```python
import random
from copy import deepcopy
import time
from ..utils.pgn_parser import PGNParser
from ..config import BOARD_SIZE
```
- Εισάγει απαραίτητες βιβλιοθήκες:
  - `random`: Χρησιμοποιείται για τυχαιοποίηση όταν χρειάζεται
  - `deepcopy`: Χρησιμοποιείται για τη δημιουργία βαθιών αντιγράφων της κατάστασης της σκακιέρας
  - `time`: Χρησιμοποιείται για την προσθήκη καθυστερήσεων για προσομοίωση σκέψης
  - `PGNParser`: Προσαρμοσμένη κλάση για την ανάλυση αρχείων PGN
  - `BOARD_SIZE`: Σταθερά διαμόρφωσης που ορίζει το μέγεθος της σκακιέρας

### Ορισμός Κλάσης
```python
class CloneEngine:
    """
    A chess engine that attempts to mimic the play style of a specific player
    by analyzing their previous games from PGN files.
    """
```
- Ορίζει την κλάση CloneEngine με την περιγραφή της.

### Μέθοδος Αρχικοποίησης
```python
def __init__(self):
    self.pgn_parser = PGNParser()
    self.loaded = False
    self.player_name = "Unknown Player"
    self.fallback_difficulty = 2  #Επίπεδο δυσκολίας για την εναλλακτική μηχανή σκακιού
    self.move_history = []  # Διατήρηση ιστορικού κινήσεων
```
- Δημιουργεί ένα νέο στιγμιότυπο του PGNParser για την ανάλυση σημειογραφιών παιχνιδιών σκακιού
- Ορίζει αρχική κατάσταση: μη φορτωμένο, άγνωστος παίκτης, μέτρια δυσκολία (2) για εφεδρική λειτουργία
- Αρχικοποιεί μια κενή λίστα ιστορικού κινήσεων για την παρακολούθηση των κινήσεων του παιχνιδιού

```python
# Μετατροπή αλγεβρικής σημειογραφίας σε συντεταγμένες πίνακα
self.file_to_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
self.rank_to_row = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
```
- Δημιουργεί λεξικά για αντιστοίχιση μεταξύ αλγεβρικής σημειογραφίας σκακιού και συντεταγμένων πίνακα
- Αντιστοιχίζει στήλες σκακιού (a-h) σε δείκτες στηλών (0-7)
- Αντιστοιχίζει σειρές σκακιού (1-8) σε δείκτες γραμμών (7-0) - σημειώστε την αντιστροφή καθώς η σειρά 1 της σκακιέρας είναι στο κάτω μέρος

### Μέθοδος Φόρτωσης Δεδομένων Παίκτη
```python
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
```
- Ανοίγει ένα διάλογο επιλογής αρχείου για να επιλέξει ένα αρχείο PGN
- Αν επιλεγεί ένα αρχείο, προσπαθεί να το αναλύσει χρησιμοποιώντας τον αναλυτή PGN
- Σε επιτυχή ανάλυση:
  - Θέτει τη σημαία φόρτωσης σε αληθή
  - Λαμβάνει και αποθηκεύει το όνομα του παίκτη
  - Επιστρέφει μια περίληψη του στυλ του παίκτη
- Επιστρέφει κατάλληλα μηνύματα σφάλματος εάν η επιλογή αρχείου ή η ανάλυση αποτύχει

### Μέθοδος Επιλογής Καλύτερης Κίνησης
```python
def get_best_move(self, board):
    """
    Get the best move based on the player's style.
    If no matching position is found, fall back to a standard algorithm.
    """
    # Add a small delay to simulate thinking
    time.sleep(0.5)
```
- Δέχεται την κατάσταση της σκακιέρας ως είσοδο και επιστρέφει την καλύτερη κίνηση σύμφωνα με την τεχνητή νοημοσύνη
- Προσθέτει καθυστέρηση μισού δευτερολέπτου για να προσομοιώσει τη "σκέψη" της τεχνητής νοημοσύνης

```python
if not self.loaded:
    # If no player data is loaded, use standard algorithm
    from .chess_engine import ChessEngine
    fallback_engine = ChessEngine(difficulty=self.fallback_difficulty)
    return fallback_engine.get_best_move(board)
```
- Αν δεν έχουν φορτωθεί δεδομένα παίκτη, δημιουργεί μια τυπική μηχανή σκακιού με τη διαμορφωμένη δυσκολία
- Επιστρέφει την κίνηση που προτείνεται από την εφεδρική μηχανή

```python
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
```
- Αν είναι η σειρά του μαύρου (η τεχνητή νοημοσύνη) και υπάρχει μια τελευταία κίνηση, μετατρέπει την τελευταία κίνηση (του λευκού) σε μορφή PGN
- Εξάγει τις θέσεις προέλευσης/προορισμού της τελευταίας κίνησης
- Μετατρέπει τις συντεταγμένες σε αλγεβρική σημειογραφία
- Προσδιορίζει τον τύπο του κομματιού που μετακινήθηκε (εμφανίζει κεφαλαία για μη πιόνια)
- Δημιουργεί σημειογραφία κίνησης στυλ PGN
- Αν η τελευταία καταγεγραμμένη κίνηση ήταν από τον μαύρο, προσθέτει αυτή τη λευκή κίνηση στο ιστορικό

```python
# Create a simplified position key from recent moves
position_key = str(self.move_history[-6:]) if len(self.move_history) >= 6 else str(self.move_history)

# Try to get a move from the player's style
pgn_move = self.pgn_parser.get_most_likely_move(position_key)
```
- Δημιουργεί ένα κλειδί που αναπαριστά την πρόσφατη κατάσταση του παιχνιδιού με βάση τις τελευταίες 6 κινήσεις (ή όλες τις κινήσεις αν είναι λιγότερες)
- Ερωτά τον αναλυτή PGN για την πιο πιθανή κίνηση σε αυτή τη θέση με βάση το στυλ του φορτωμένου παίκτη

```python
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
```
- Αν βρεθεί μια κίνηση από τα δεδομένα στυλ του παίκτη:
  - Προσπαθεί να μετατρέψει την κίνηση από τη σημειογραφία PGN σε συντεταγμένες σκακιέρας
  - Επαληθεύει αν είναι έγκυρη κίνηση στην τρέχουσα θέση
  - Αν είναι έγκυρη, προσθέτει την κίνηση στο ιστορικό και την επιστρέφει
  - Χειρίζεται τις εξαιρέσεις με κομψότητα, προχωρώντας στην εφεδρική λειτουργία αν προκύψουν προβλήματα

```python
# Fallback to standard algorithm if no matching style move is found
from .chess_engine import ChessEngine
fallback_engine = ChessEngine(difficulty=self.fallback_difficulty)
best_move = fallback_engine.get_best_move(board)
```
- Αν δεν βρεθεί έγκυρη κίνηση από τα δεδομένα στυλ ή αποτύχει η μετατροπή, δημιουργεί μια τυπική μηχανή σκακιού
- Λαμβάνει την κίνηση από την εφεδρική μηχανή

```python
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
```
- Αν βρεθεί μια κίνηση από την εφεδρική μηχανή:
  - Μετατρέπει την κίνηση σε μορφή PGN
  - Χρησιμοποιεί σημειογραφία 'x' για αιχμαλωτίσεις
  - Προσθέτει την κίνηση στο ιστορικό
  
```python
return best_move
```
- Επιστρέφει την καλύτερη κίνηση που βρέθηκε, είτε από το στυλ του παίκτη είτε από την εφεδρική μηχανή

### Βοηθητικές Μέθοδοι

```python
def _coords_to_algebraic(self, coords):
    """Convert board coordinates to algebraic notation"""
    row, col = coords
    files = "abcdefgh"
    ranks = "87654321"
    return files[col] + ranks[row]
```
- Βοηθητική μέθοδος για τη μετατροπή εσωτερικών συντεταγμένων σκακιέρας (γραμμή, στήλη) σε αλγεβρική σημειογραφία (π.χ., "e4")
- Αντιστοιχίζει τον δείκτη στήλης σε γράμμα στήλης και τον δείκτη γραμμής σε αριθμό σειράς

```python
def _algebraic_to_coords(self, algebraic):
    """Convert algebraic notation to board coordinates"""
    if len(algebraic) < 2:
        return None
    col = self.file_to_col.get(algebraic[0].lower())
    row = self.rank_to_row.get(algebraic[1])
    if col is not None and row is not None:
        return row, col
    return None
```
- Βοηθητική μέθοδος για τη μετατροπή αλγεβρικής σημειογραφίας (π.χ., "e4") σε εσωτερικές συντεταγμένες σκακιέρας (γραμμή, στήλη)
- Επιστρέφει None αν η αλγεβρική σημειογραφία είναι άκυρη ή πολύ σύντομη

```python
def _pgn_move_to_coords(self, board, pgn_move):
    """
    Convert a PGN move to board coordinates.
    This is a simplified implementation and doesn't handle all PGN formats.
    """
    # Remove check/mate symbols
    pgn_move = pgn_move.replace('+', '').replace('#', '')
```
- Αναλύει τη σημειογραφία κίνησης PGN σε συντεταγμένες σκακιέρας
- Πρώτα αφαιρεί τα σύμβολα σαχ (+) και ματ (#) που δεν επηρεάζουν την ίδια την κίνηση

```python
# Handle castling
if pgn_move == "O-O" or pgn_move == "0-0":  # Kingside castling
    return (0, 4), (0, 6) if board.turn == 'b' else (7, 4), (7, 6)
elif pgn_move == "O-O-O" or pgn_move == "0-0-0":  # Queenside castling
    return (0, 4), (0, 2) if board.turn == 'b' else (7, 4), (7, 2)
```
- Ειδικός χειρισμός για κινήσεις ροκέ, αναγνωρίζοντας τόσο τη σημειογραφία με γράμμα "O" όσο και με αριθμό "0" 
- Επιστρέφει τις συντεταγμένες κίνησης του βασιλιά με βάση τη σειρά του παίκτη (μαύρα ή λευκά)

```python
# Handle standard moves (this is a simplified version)
# For simplicity, we'll just look for a piece of the right type that can move to the target square

# Extract piece type, if any
piece_type = 'p'  # Default to pawn
if pgn_move[0].upper() in "RNBQK":
    piece_type = pgn_move[0].lower()
    pgn_move = pgn_move[1:]
```
- Για τυπικές κινήσεις, εξάγει τον τύπο του κομματιού από τη σημειογραφία
- Προεπιλέγει σε πιόνι ('p') αν δεν καθορίζεται τύπος κομματιού
- Αφαιρεί τον τύπο του κομματιού από τη συμβολοσειρά κίνησης για περαιτέρω επεξεργασία

```python
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
```
- Εντοπίζει και χειρίζεται τη σημειογραφία αιχμαλώτισης ('x')
- Διαχωρίζει την κίνηση σε τμήματα 'από' και 'προς'
- Για μη αιχμαλωτίσεις, υποθέτει ότι οι δύο τελευταίοι χαρακτήρες είναι ο προορισμός και οποιοιδήποτε προηγούμενοι χαρακτήρες είναι για διαφοροποίηση

```python
# Get destination coordinates
to_coords = self._algebraic_to_coords(to_part)
if not to_coords:
    return None
```
- Μετατρέπει το τετράγωνο προορισμού από αλγεβρική σημειογραφία σε συντεταγμένες
- Επιστρέφει None αν ο προορισμός είναι άκυρος

```python
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
```
- Αναζητά στη σκακιέρα κομμάτια του σωστού τύπου και χρώματος που μπορούν να μετακινηθούν στον προορισμό
- Για κάθε αντίστοιχο κομμάτι, ελέγχει αν η κίνηση είναι έγκυρη
- Αν παρέχονται πληροφορίες διαφοροποίησης (from_part), διασφαλίζει ότι ταιριάζουν
- Επιστρέφει τις συντεταγμένες κίνησης όταν βρεθεί έγκυρο αντιστοίχιση

```python
return None
```
- Επιστρέφει None αν δεν μπορεί να βρεθεί καμία έγκυρη κίνηση που να ταιριάζει με τη σημειογραφία PGN