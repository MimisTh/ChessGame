# Μονάδα Παιχνιδιού Σκακιού (chess_game.py και main.py)

## Επισκόπηση
Αυτές οι μονάδες λειτουργούν ως το σημείο εισόδου για την εφαρμογή Παιχνιδιού Σκακιού. Το `chess_game.py` είναι ένα ελάχιστο σενάριο εκκίνησης που εισάγει και εκτελεί την κύρια συνάρτηση, ενώ το `main.py` περιέχει τον βασικό βρόχο του παιχνιδιού και συντονίζει όλα τα συστατικά του παιχνιδιού σκακιού. Αυτή η κύρια μονάδα ενσωματώνει τη λογική της σκακιέρας, τις μηχανές τεχνητής νοημοσύνης, την απεικόνιση διεπαφής χρήστη, τους τρόπους παιχνιδιού και τις αλληλεπιδράσεις χρήστη.

## Ανάλυση chess_game.py

```python
from src.main import main

if __name__ == "__main__":
    main()
```
- Απλό σενάριο σημείου εισόδου που λειτουργεί ως εκκινητής της εφαρμογής
- Εισάγει και καλεί την κύρια συνάρτηση από τη μονάδα src.main
- Ο έλεγχος `if __name__ == "__main__"` διασφαλίζει ότι η κύρια συνάρτηση καλείται μόνο όταν το σενάριο εκτελείται απευθείας

## Ανάλυση main.py Γραμμή προς Γραμμή

### Εισαγωγές
```python
import pygame
import sys
from pygame.locals import *

from .config import window, clock, BOARD_PX, SQUARE_SIZE
from .board.chess_board import ChessBoard
from .utils.timer import ChessTimer
from .ai.chess_engine import ChessEngine
from .ai.clone_engine import CloneEngine
from .ui.rendering import (load_pieces, create_placeholder_pieces, show_checkmate_modal, 
                         draw_board, draw_pieces, draw_dragged_piece, draw_message_panel,
                         show_game_mode_selection)
```
- Εισάγει το pygame για το πλαίσιο του παιχνιδιού και το sys για λειτουργίες συστήματος
- Εισάγει αντικείμενα διαμόρφωσης και σταθερές από τη μονάδα config
- Εισάγει την υλοποίηση της σκακιέρας από τη μονάδα board
- Εισάγει την υλοποίηση του χρονομέτρου σκακιού από τη μονάδα utils
- Εισάγει και τις δύο μηχανές τεχνητής νοημοσύνης: τυπική μηχανή σκακιού και μηχανή κλώνος
- Εισάγει όλες τις συναρτήσεις απεικόνισης από τη μονάδα UI

### Κύρια Συνάρτηση
```python
def main():
    # Εμφάνιση μενού επιλογής τρόπου παιχνιδιού
    game_mode, ai_difficulty = show_game_mode_selection(window)
```
- Ορισμός της κύριας συνάρτησης που οδηγεί το παιχνίδι
- Εμφανίζει το μενού επιλογής τρόπου παιχνιδιού και λαμβάνει την επιλογή του χρήστη
- Επιστρέφει τον επιλεγμένο τρόπο παιχνιδιού και το επίπεδο δυσκολίας της τεχνητής νοημοσύνης (εάν ισχύει)

### Αρχικοποίηση Τεχνητής Νοημοσύνης
```python
# Αρχικοποίηση του AI αν επιλέχθηκε
chess_engine = None
clone_engine = None

if game_mode == "PVE" and ai_difficulty is not None:
    chess_engine = ChessEngine(difficulty=ai_difficulty)
```
- Αρχικοποιεί την κατάλληλη μηχανή τεχνητής νοημοσύνης με βάση την επιλογή τρόπου παιχνιδιού
- Για τη λειτουργία Παίκτης εναντίον Μηχανής (PVE), αρχικοποιεί την τυπική μηχανή σκακιού με την επιλεγμένη δυσκολία

```python
elif game_mode == "CLONE":
    # Δημιουργία και ρύθμιση του clone engine
    clone_engine = CloneEngine()
    # Αναδυόμενο παράθυρο για επιλογή αρχείου PGN
    result_message = clone_engine.load_player_data()
```
- Για τη λειτουργία Κλώνος, αρχικοποιεί το CloneEngine
- Φορτώνει δεδομένα παίκτη από ένα αρχείο PGN μέσω ενός διαλόγου επιλογής αρχείου
- Λαμβάνει ένα μήνυμα αποτελέσματος σχετικά με την επιτυχία της φόρτωσης δεδομένων

```python
# [Κώδικας UI για την εμφάνιση του μηνύματος αποτελέσματος]
```
- Δημιουργεί μια προσωρινή οθόνη UI για να εμφανίσει τα αποτελέσματα της φόρτωσης των δεδομένων του παίκτη
- Δείχνει έναν τίτλο, γραμμές μηνυμάτων και οδηγίες για συνέχεια
- Περιμένει είσοδο από τον χρήστη πριν προχωρήσει με το παιχνίδι

### Αρχικοποίηση Συστατικών Παιχνιδιού
```python
# Αρχικοποίηση σκακιέρας και χρονομέτρου
board = ChessBoard()
timer = ChessTimer()
```
- Δημιουργεί τη σκακιέρα με τις αρχικές θέσεις των κομματιών
- Δημιουργεί το χρονόμετρο σκακιού για την παρακολούθηση του χρόνου των παικτών

```python
try:
    # Φόρτωση πραγματικών εικόνων πιονιών
    pieces = load_pieces()
except:
    # Φόρτωση συμβόλων στην περίπτωση αποτυχίας φόρτωσης πραγματικών εικόνων
    pieces = create_placeholder_pieces()
```
- Προσπαθεί να φορτώσει τις εικόνες των κομματιών σκακιού
- Χρησιμοποιεί εναλλακτικά κομμάτια (σύμβολα Unicode) αν η φόρτωση εικόνων αποτύχει

```python
dragging = False
drag_piece = None
drag_pos = (0, 0)
orig_pos = (0, 0)
```
- Αρχικοποιεί μεταβλητές για τη διεπαφή μετακίνησης κομματιών με σύρσιμο και απόθεση

```python
# Μήνυμα έναρξης παιχνιδιού
if game_mode == "PVE":
    difficulty_text = "Εύκολο" if ai_difficulty == 1 else "Μεσαίο" if ai_difficulty == 2 else "Δύσκολο"
    board.message = f"Ξεκινά παιχνίδι εναντίον AI ({difficulty_text})"
elif game_mode == "CLONE":
    player_name = clone_engine.player_name if clone_engine.loaded else "Unknown Player"
    board.message = f"Ξεκινά παιχνίδι εναντίον Clone AI που μιμείται τον παίκτη {player_name}"
else:
    board.message = "Ξεκινά παιχνίδι μεταξύ δύο παικτών"
```
- Ορίζει το αρχικό μήνυμα του παιχνιδιού με βάση τον επιλεγμένο τρόπο παιχνιδιού
- Για τη λειτουργία PVE, περιλαμβάνει το επίπεδο δυσκολίας
- Για τη λειτουργία Κλώνος, περιλαμβάνει το όνομα του παίκτη που μιμείται

### Βρόχος Παιχνιδιού
```python
# Κύρια δομή επανάληψης παιχνιδιού
running = True
while running:
```
- Ξεκινά τον κύριο βρόχο του παιχνιδιού που εκτελείται μέχρι να τελειώσει το παιχνίδι

```python
# Έλεγχος αν είναι η σειρά του AI να παίξει
if (game_mode == "PVE" or game_mode == "CLONE") and board.turn == 'b' and not board.game_over:
```
- Ελέγχει αν είναι η σειρά της τεχνητής νοημοσύνης να κάνει κίνηση (το μαύρο παίζει πάντα ως τεχνητή νοημοσύνη)
- Εφαρμόζεται μόνο στις λειτουργίες PVE ή Clone και όταν το παιχνίδι δεν έχει τελειώσει

```python
# Εύρεση καλύτερης κίνησης ανάλογα με το είδος του AI
ai_move = None
if game_mode == "PVE" and chess_engine:
    ai_move = chess_engine.get_best_move(board)
elif game_mode == "CLONE" and clone_engine:
    ai_move = clone_engine.get_best_move(board)
```
- Λαμβάνει την καλύτερη κίνηση από την κατάλληλη μηχανή τεχνητής νοημοσύνης
- Η τυπική μηχανή σκακιού χρησιμοποιεί αλγόριθμους αξιολόγησης και αναζήτησης
- Η μηχανή κλώνος χρησιμοποιεί αντιστοίχιση προτύπων με βάση τα δεδομένα του παίκτη

```python
if ai_move:
    from_pos, to_pos = ai_move
    # Επιλογή του πιονιού για την κίνηση
    board.select_piece(from_pos[0], from_pos[1])
    # Εκτέλεση της κίνησης
    move_successful = board.move_piece(from_pos, to_pos)
```
- Αν η τεχνητή νοημοσύνη βρήκε κίνηση, επιλέγει το κατάλληλο κομμάτι και εκτελεί την κίνηση

```python
if move_successful:
    if not board.game_over:
        timer.switch_turn()
    else:
        timer.game_over = True
        if board.checkmate:
            winner = "Μαύρος" if board.turn == 'w' else "Λευκός"
            show_checkmate_modal(window, winner)
```
- Αν η κίνηση ήταν επιτυχής, αλλάζει το χρονόμετρο στον επόμενο παίκτη
- Αν η κίνηση τερμάτισε το παιχνίδι, εμφανίζει το παράθυρο ρουά-ματ αν ισχύει

```python
# Καθαρισμός επιλογής και έγκυρων κινήσεων μετά την κίνηση του AI
board.selected_piece = None
board.valid_moves = []
```
- Επαναφέρει την επιλογή και τις έγκυρες κινήσεις μετά την κίνηση της τεχνητής νοημοσύνης

### Χειρισμός Συμβάντων
```python
# Διαχείριση αμεσών χειρισμών γραφικού περιβάλλοντος
for event in pygame.event.get():
    if event.type == QUIT:
        running = False
```
- Επεξεργάζεται συμβάντα pygame
- Τερματίζει τον βρόχο του παιχνιδιού όταν κλείνει το παράθυρο

```python
# Επιτρέπουμε κινήσεις του χρήστη μόνο αν είναι η σειρά του λευκού ή
# αν παίζουν δύο άνθρωποι (PVP mode) και δεν έχει τελειώσει το παιχνίδι
elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and 
     (board.turn == 'w' or game_mode == "PVP") and not board.game_over):
```
- Χειρίζεται τα κλικ του ποντικιού για την επιλογή κομματιών
- Επιτρέπει κινήσεις μόνο όταν είναι η σειρά ενός ανθρώπινου παίκτη
- Στις λειτουργίες PVE/Clone, ο άνθρωπος ελέγχει μόνο το λευκό· στο PVP, και τα δύο χρώματα

```python
mouseX, mouseY = event.pos

if mouseX < BOARD_PX:
    col = mouseX // SQUARE_SIZE
    row = mouseY // SQUARE_SIZE
    piece = board.get_piece_at(row, col)
    
    if piece and piece[0] == board.turn:
        dragging = True
        drag_piece = piece
        orig_pos = (row, col)
        drag_pos = event.pos
        board.select_piece(row, col)
```
- Αν το κλικ είναι εντός της περιοχής της σκακιέρας:
  - Υπολογίζει τη θέση στη σκακιέρα από τις συντεταγμένες του ποντικιού
  - Επαληθεύει ότι το επιλεγμένο κομμάτι ανήκει στον τρέχοντα παίκτη
  - Ξεκινά τη λειτουργία σύρσιμου και απόθεσης
  - Επιλέγει το κομμάτι για να πάρει τις έγκυρες κινήσεις του

```python
elif event.type == MOUSEMOTION and dragging:
    drag_pos = event.pos
```
- Ενημερώνει τη θέση σύρσιμου όταν το ποντίκι κινείται ενώ σύρεται ένα κομμάτι

```python
elif (event.type == MOUSEBUTTONUP and event.button == 1 and dragging and
     (board.turn == 'w' or game_mode == "PVP")):
    mouseX, mouseY = event.pos
    
    if mouseX < BOARD_PX:
        col = mouseX // SQUARE_SIZE
        row = mouseY // SQUARE_SIZE
        to_pos = (row, col)
        
        if orig_pos != to_pos:  # Έλεγχος επιλογής διαφορετικής θέσης
            move_successful = board.move_piece(orig_pos, to_pos)
```
- Όταν το κουμπί του ποντικιού απελευθερώνεται μετά το σύρσιμο:
  - Υπολογίζει τη θέση προορισμού
  - Προσπαθεί να μετακινήσει το κομμάτι αν ο προορισμός είναι διαφορετικός από την αρχή
  - Χειρίζεται το αποτέλεσμα της απόπειρας κίνησης

```python
if move_successful:
    if not board.game_over:
        timer.switch_turn()
    else:
        timer.game_over = True
        if board.checkmate:
            winner = "Μαύρος" if board.turn == 'w' else "Λευκός"
            show_checkmate_modal(window, winner)
```
- Αν η κίνηση ήταν επιτυχής:
  - Αλλάζει το χρονόμετρο στον επόμενο παίκτη
  - Αν το παιχνίδι τελείωσε, εμφανίζει το παράθυρο ρουά-ματ αν ισχύει

```python
dragging = False
drag_piece = None
board.selected_piece = None
board.valid_moves = []
```
- Επαναφέρει όλες τις καταστάσεις σύρσιμου και επιλογής αφού τοποθετηθεί το κομμάτι

```python
elif event.type == KEYDOWN:
    if event.key == K_s:
        board.save_moves_to_file()
        print("Επιτυχής αποθήκευση αρχείου!")
    elif event.key == K_n:
        # Επανεκκίνηση παιχνιδιού
        return main()
    elif event.key == K_q:
        running = False
```
- Χειρίζεται συντομεύσεις πληκτρολογίου:
  - Πλήκτρο 'S': Αποθηκεύει τις κινήσεις του παιχνιδιού σε αρχείο
  - Πλήκτρο 'N': Επανεκκινεί το παιχνίδι καλώντας αναδρομικά την main()
  - Πλήκτρο 'Q': Τερματίζει το παιχνίδι

### Απεικόνιση
```python
window.fill((255, 255, 255))

# Σχεδίαση σκακιέρας
draw_board(
    window, 
    board.board, 
    board.last_move, 
    board.selected_piece, 
    board.valid_moves, 
    board.white_king_pos, 
    board.black_king_pos, 
    board.in_check, 
    board.turn
)
```
- Καθαρίζει το παράθυρο με λευκό φόντο
- Σχεδιάζει τη σκακιέρα με όλες τις οπτικές ενδείξεις (τελευταία κίνηση, επιλογή, έγκυρες κινήσεις, σαχ)

```python
# Σχεδίαση πιονιών
draw_pieces(window, board.board, pieces)

# Σχεδίαση πιονιού που έχει επιλεγεί για μετακίνηση
if dragging and drag_piece:
    draw_dragged_piece(window, pieces, drag_piece, drag_pos)
```
- Σχεδιάζει όλα τα κομμάτια σκακιού στις τρέχουσες θέσεις τους
- Αν ένα κομμάτι σύρεται, το σχεδιάζει στη θέση του κέρσορα

```python
# Σχεδίαση πάνελ μηνυμάτων
draw_message_panel(window, board.message, board.turn, board.game_over)

# Σχεδίαση χρονομέτρου
timer.draw(window)
```
- Σχεδιάζει το πάνελ μηνυμάτων με πληροφορίες κατάστασης παιχνιδιού
- Σχεδιάζει την οθόνη του χρονομέτρου σκακιού για τους δύο παίκτες

```python
pygame.display.flip()
clock.tick(60)
```
- Ενημερώνει την οθόνη με όλα τα σχεδιασμένα στοιχεία
- Περιορίζει τον ρυθμό καρέ στα 60 FPS

### Καθαρισμός
```python
pygame.quit()
sys.exit()
```
- Τερματίζει καθαρά το pygame και τερματίζει το πρόγραμμα όταν ο βρόχος του παιχνιδιού τελειώνει

### Σημείο Εισόδου Μονάδας
```python
if __name__ == "__main__":
    main()
```
- Καλεί τη συνάρτηση main() αν το σενάριο εκτελείται απευθείας
- Αυτό διπλασιάζει το σημείο εισόδου στο chess_game.py για ευκολία κατά την ανάπτυξη