# Μονάδα Απεικόνισης (rendering.py)

## Επισκόπηση
Αυτή η μονάδα χειρίζεται την οπτική παρουσίαση του παιχνιδιού σκακιού. Περιλαμβάνει συναρτήσεις για την απεικόνιση της σκακιέρας, των κομματιών, του πίνακα μηνυμάτων, των οθονών επιλογής τρόπου παιχνιδιού και διαφόρων οπτικών εφέ. Η μονάδα απεικόνισης λειτουργεί ως το επίπεδο παρουσίασης του παιχνιδιού, μετατρέποντας τη λογική κατάσταση του παιχνιδιού σε γραφικά στοιχεία που βλέπει ο χρήστης.

## Ανάλυση Κώδικα Γραμμή προς Γραμμή

### Εισαγωγές
```python
import pygame
import sys
from pygame.locals import *
from ..config import SQUARE_SIZE, BOARD_PX, WINDOW_WIDTH, WINDOW_HEIGHT, LIGHT, DARK, BLACK, WHITE
```
- Εισάγει το pygame για την απεικόνιση γραφικών και τη διαχείριση συμβάντων
- Εισάγει βοηθητικά συστήματα για τον έλεγχο του προγράμματος
- Εισάγει σταθερές συμβάντων του pygame
- Εισάγει σταθερές διαμόρφωσης για διαστάσεις και χρώματα

### Εμφάνιση Μενού Επιλογής Τρόπου Παιχνιδιού
```python
def show_game_mode_selection(window):
    """Εμφάνιση μενού επιλογής τρόπου παιχνιδιού"""
    # Καθαρισμός παραθύρου
    window.fill((240, 240, 240))
```
- Εμφανίζει την αρχική οθόνη επιλογής τρόπου παιχνιδιού
- Γεμίζει το παράθυρο με ανοιχτό γκρι φόντο

```python
# Δημιουργία τίτλου
title_font = pygame.font.SysFont('Arial', 48, bold=True)
title = title_font.render("Σκάκι ΠΛΗΠΡΟ", True, (0, 0, 0))
title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
window.blit(title, title_rect)
```
- Δημιουργεί και εμφανίζει τον κύριο τίτλο "Σκάκι ΠΛΗΠΡΟ"
- Κεντράρει τον τίτλο στην κορυφή του παραθύρου

```python
# Επιλογές παιχνιδιού
button_font = pygame.font.SysFont('Arial', 24)
button_width, button_height = 300, 60
```
- Ορίζει τη γραμματοσειρά και τις διαστάσεις για τα κουμπιά επιλογής τρόπου παιχνιδιού

```python
# Κουμπί για παιχνίδι με άλλον παίκτη
pvp_button = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 280, button_width, button_height)
pygame.draw.rect(window, (200, 200, 200), pvp_button)
pygame.draw.rect(window, (0, 0, 0), pvp_button, 2)
pvp_text = button_font.render("Παίκτης εναντίον Παίκτη", True, (0, 0, 0))
pvp_rect = pvp_text.get_rect(center=pvp_button.center)
window.blit(pvp_text, pvp_rect)
```
- Δημιουργεί και εμφανίζει ένα κουμπί για τον τρόπο παιχνιδιού Παίκτης εναντίον Παίκτη
- Σχεδιάζει ένα γκρι κουμπί με μαύρο περίγραμμα και κεντραρισμένο κείμενο

```python
# [Παρόμοιοι κώδικες για τα άλλα κουμπιά τρόπου παιχνιδιού]
```
- Παρόμοια δημιουργία κουμπιών για τα τρία επίπεδα δυσκολίας της τεχνητής νοημοσύνης (Εύκολο, Μεσαίο, Δύσκολο)
- Κάθε κουμπί τοποθετείται κάτω από το προηγούμενο

```python
# Κουμπί για παιχνίδι με AI που μιμείται το στυλ ενός παίκτη
clone_button = pygame.Rect((WINDOW_WIDTH - button_width) // 2, 560, button_width, button_height)
pygame.draw.rect(window, (180, 220, 180), clone_button)  # Διαφορετικό χρώμα για έμφαση
pygame.draw.rect(window, (0, 100, 0), clone_button, 2)
clone_text = button_font.render("Παίκτης εναντίον Clone AI", True, (0, 80, 0))
clone_rect = clone_text.get_rect(center=clone_button.center)
window.blit(clone_text, clone_rect)
```
- Δημιουργεί ένα ειδικό κουμπί για τον τρόπο παιχνιδιού Clone AI
- Χρησιμοποιεί διαφορετικό χρωματικό σχήμα (πράσινο) για να τονίσει αυτή τη δυνατότητα
- Περιλαμβάνει επιπλέον επεξηγηματικό κείμενο κάτω από το κουμπί

```python
pygame.display.flip()
```
- Ενημερώνει την οθόνη για να εμφανίσει όλα τα απεικονισμένα στοιχεία

```python
# Περιμένουμε την επιλογή του χρήστη
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if pvp_button.collidepoint(mouse_pos):
                return "PVP", None
            elif pve_easy_button.collidepoint(mouse_pos):
                return "PVE", 1
            elif pve_medium_button.collidepoint(mouse_pos):
                return "PVE", 2
            elif pve_hard_button.collidepoint(mouse_pos):
                return "PVE", 3
            elif clone_button.collidepoint(mouse_pos):
                return "CLONE", None
```
- Εισέρχεται σε βρόχο αναμονής για την επιλογή του χρήστη
- Διαχειρίζεται την έξοδο από το παιχνίδι όταν κλείνει το παράθυρο
- Ανιχνεύει ποιο κουμπί πατήθηκε χρησιμοποιώντας ανίχνευση σύγκρουσης
- Επιστρέφει την κατάλληλη επιλογή τρόπου παιχνιδιού και επίπεδο δυσκολίας

### Φόρτωση Γραφικών Κομματιών
```python
def load_pieces():
    """Συνάρτηση για την φόρτωση των πιονιών"""
    pieces = {}
    for color in ['w', 'b']:
        for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
            img = pygame.image.load(f'assets/pieces/{color}{piece}.png')
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            pieces[f'{color}{piece}'] = img
    return pieces
```
- Φορτώνει τις εικόνες των κομματιών σκακιού από τον φάκελο assets
- Δημιουργεί ένα λεξικό που αντιστοιχεί κωδικούς κομματιών (π.χ., 'wp' για λευκό πιόνι) στις εικόνες τους
- Προσαρμόζει τις εικόνες στο μέγεθος τετραγώνου της σκακιέρας
- Επιστρέφει το πλήρες λεξικό των εικόνων κομματιών

### Εναλλακτικά Γραφικά Κομματιών
```python
def create_placeholder_pieces():
    """Συνάρτηση για την δημιουργία των πιονιών με σύμβολα (περίπτωση σφάλματος στην φόρτωση των εικόνων)"""
    pieces = {}
    symbols = {
        'wp': '♙', 'wr': '♖', 'wn': '♘', 'wb': '♗', 'wq': '♕', 'wk': '♔',
        'bp': '♟', 'br': '♜', 'bn': '♞', 'bb': '♝', 'bq': '♛', 'bk': '♚'
    }
```
- Δημιουργεί εναλλακτικά γραφικά κομματιών χρησιμοποιώντας σύμβολα Unicode σκακιού
- Χρησιμοποιείται όταν αποτυγχάνει η φόρτωση εικόνων ή για περιβάλλοντα χαμηλών πόρων
- Αντιστοιχεί κάθε κωδικό κομματιού στο αντίστοιχο σύμβολο Unicode

```python
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
```
- Για κάθε τύπο κομματιού:
  - Δημιουργεί κατάλληλο χρωματικό σχήμα με βάση το χρώμα του κομματιού
  - Δημιουργεί μια διαφανή επιφάνεια
  - Σχεδιάζει κυκλικό φόντο
  - Απεικονίζει το σύμβολο Unicode στο κατάλληλο χρώμα
  - Κεντράρει το κείμενο στον κύκλο
  - Αποθηκεύει την επιφάνεια στο λεξικό των κομματιών

### Μήνυμα Ρουά Ματ
```python
def show_checkmate_modal(window, winner):
    """Σχηματισμός modal μηνύματος στο προσκήνιο για ρουά ματ."""
    modal_width = 400
    modal_height = 250
```
- Εμφανίζει ένα αναδυόμενο παράθυρο που ανακοινώνει τον νικητή μετά από ρουά ματ
- Ορίζει τις διαστάσεις του αναδυόμενου παραθύρου

```python
# θέση κεντραρίσματος του modal
modal_x = (WINDOW_WIDTH - modal_width) // 2
modal_y = (WINDOW_HEIGHT - modal_height) // 2

# Σκίαση υποβάθρου του modal
overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 180))  # Ημιδιάφανο μαύρο
window.blit(overlay, (0, 0))
```
- Κεντράρει το αναδυόμενο παράθυρο στην οθόνη
- Δημιουργεί ημιδιαφανές φόντο για να σκιάσει το υπόβαθρο

```python
# Σχεδίαση modal και υποβάθρου
pygame.draw.rect(window, (240, 240, 210), (modal_x, modal_y, modal_width, modal_height), 0, 10)
pygame.draw.rect(window, (218, 165, 32), (modal_x, modal_y, modal_width, modal_height), 3, 10)
```
- Σχεδιάζει το αναδυόμενο παράθυρο με:
  - Ανοιχτό φόντο με στρογγυλεμένες γωνίες
  - Χρυσό περίγραμμα για να τονίσει τη σημασία του μηνύματος

```python
# [Κώδικας δημιουργίας γραμματοσειράς και απεικόνισης κειμένου]
```
- Δημιουργεί γραμματοσειρές για τον τίτλο, το μήνυμα και τις οδηγίες του αναδυόμενου παραθύρου
- Απεικονίζει και τοποθετεί τον τίτλο "Ρουά Ματ!" με κόκκινο χρώμα
- Απεικονίζει το μήνυμα του νικητή με πράσινο χρώμα
- Προσθέτει οδηγίες για τη συνέχεια στο κάτω μέρος

```python
# Αναμονή για κλικ για συνέχεια
waiting_for_click = True
while waiting_for_click:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            waiting_for_click = False
```
- Περιμένει μέχρι ο χρήστης να κάνει κλικ για να κλείσει το αναδυόμενο παράθυρο
- Διαχειρίζεται επίσης την έξοδο από το πρόγραμμα αν κλείσει το παράθυρο

### Σχεδίαση Σκακιέρας
```python
def draw_board(surface, board_state, last_move, selected_piece, valid_moves, white_king_pos, black_king_pos, in_check, turn):
    """Σχεδίαση σκακιέρας και κατάστασης παιχνιδιού"""
    for row in range(8):
        for col in range(8):
            x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
            color = LIGHT if (row + col) % 2 == 0 else DARK
            
            # Σχεδιασμός τετραγώνου
            pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
```
- Σχεδιάζει τη σκακιέρα με εναλλασσόμενα ανοιχτά και σκούρα τετράγωνα
- Υπολογίζει τη θέση κάθε τετραγώνου με βάση τη γραμμή και τη στήλη του

```python
# Υπογράμμιση τελευταίας κίνησης
if last_move and ((row, col) == last_move[0] or (row, col) == last_move[1]):
    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    highlight.fill((255, 255, 0, 50))  # Ημιδιάφανο κίτρινο
    surface.blit(highlight, (x, y))
```
- Υπογραμμίζει τα τετράγωνα προέλευσης και προορισμού της τελευταίας κίνησης
- Χρησιμοποιεί ημιδιάφανο κίτρινο για να διατηρήσει την ορατότητα της σκακιέρας και των κομματιών

```python
# Υπογράμμιση επιλεγμένου πιονιού
if selected_piece and selected_piece[0] == row and selected_piece[1] == col:
    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    highlight.fill((100, 100, 255, 100))  # Ημιδιάφανο μπλε
    surface.blit(highlight, (x, y))
```
- Υπογραμμίζει το επιλεγμένο κομμάτι
- Χρησιμοποιεί ημιδιάφανο μπλε για να υποδείξει την επιλογή

```python
# Υπογράμμιση δυνατών κινήσεων
if (row, col) in valid_moves:
    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    highlight.fill((0, 255, 0, 70))  # Ημιδιάφανο πράσινο
    surface.blit(highlight, (x, y))
```
- Υπογραμμίζει τα τετράγωνα όπου μπορεί να κινηθεί το επιλεγμένο κομμάτι
- Χρησιμοποιεί ημιδιάφανο πράσινο για να δείξει τους έγκυρους προορισμούς κινήσεων

```python
# Υπογράμμιση βασιλιά υπο σαχ
if in_check:
    king_pos = white_king_pos if turn == 'w' else black_king_pos
    if (row, col) == king_pos:
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill((255, 0, 0, 100))  # Ημιδιάφανο κόκκινο
        surface.blit(highlight, (x, y))
```
- Υπογραμμίζει τον βασιλιά όταν είναι σε σαχ
- Χρησιμοποιεί ημιδιάφανο κόκκινο για να υποδείξει τον κίνδυνο

### Σχεδίαση Κομματιών
```python
def draw_pieces(surface, board_state, pieces):
    """Σχεδίαση πιονιών στη σκακιέρα"""
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if (piece):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                surface.blit(pieces[piece], (x, y))
```
- Σχεδιάζει όλα τα κομμάτια στη σκακιέρα
- Διατρέχει την κατάσταση της σκακιέρας και τοποθετεί κάθε κομμάτι στη θέση του

```python
def draw_dragged_piece(surface, pieces, piece, pos):
    """Σχεδίαση πιονιού που μετακινείται"""
    if piece:
        piece_img = pieces[piece]
        rect = piece_img.get_rect(center=pos)
        surface.blit(piece_img, rect)
```
- Σχεδιάζει ένα κομμάτι που σύρεται από τον παίκτη
- Κεντράρει το κομμάτι στη θέση του δείκτη του ποντικιού
- Χρησιμοποιείται για τη διεπαφή μεταφοράς και απόθεσης

### Σχεδίαση Πάνελ Μηνυμάτων
```python
def draw_message_panel(surface, message, turn, game_over):
    """Σχεδίαση πάνελ μηνυμάτων"""
    # Σχεδίαση υποβάθρου πάνελ μηνυμάτων
    pygame.draw.rect(surface, (240, 240, 240), (BOARD_PX, 0, 450, WINDOW_HEIGHT))
    pygame.draw.line(surface, BLACK, (BOARD_PX, 0), (BOARD_PX, WINDOW_HEIGHT), 2)
```
- Σχεδιάζει το πλευρικό πάνελ για μηνύματα και πληροφορίες παιχνιδιού
- Δημιουργεί ανοιχτό γκρι φόντο με μαύρη γραμμή περιγράμματος

```python
# Κεφαλίδα παιχνιδιού - σταθερή θέση στην κορυφή
title = title_font.render("Σκάκι ΠΛΗΠΡΟ", True, BLACK)
surface.blit(title, (BOARD_PX + 20, 30))
```
- Σχεδιάζει τον τίτλο του παιχνιδιού στην κορυφή του πάνελ

```python
# Σχεδίαση μηνύματος σειράς ή λήξης
if not game_over:
    turn_text = "Σειρά του Λευκού παίκτη" if turn == 'w' else "Σειρά του Μαύρου παίκτη"
    turn_color = BLACK
else:
    turn_text = "Τέλος παιχνιδιού"
    turn_color = (255, 0, 0)  # Κόκκινο για τέλος παιχνιδιού
    
turn_label = turn_font.render(turn_text, True, turn_color)
surface.blit(turn_label, (BOARD_PX + 20, 80))
```
- Εμφανίζει ποιανού σειρά είναι ή αν το παιχνίδι έχει τελειώσει
- Χρησιμοποιεί κόκκινο κείμενο για να τονίσει την κατάσταση λήξης παιχνιδιού

```python
# [Κώδικας ρύθμισης περιοχής μηνυμάτων]
```
- Δημιουργεί μια ενότητα στο κάτω μέρος του πάνελ για μηνύματα παιχνιδιού
- Προσθέτει μια οριζόντια γραμμή διαχωρισμού
- Ορίζει έναν τίτλο ενότητας "Μηνύματα Παιχνιδιού"

```python
# Σχεδίαση μηνυμάτων κατάστασης με αναδίπλωση κειμένου
y_pos = bottom_section_y + 30  # Αρχή των μηνυμάτων κάτω από την κεφαλίδα
words = message.split()
lines = []
current_line = []
```
- Υλοποιεί αναδίπλωση κειμένου για μηνύματα που είναι πολύ μεγάλα
- Διαχωρίζει το μήνυμα σε λέξεις

```python
for word in words:
    test_line = ' '.join(current_line + [word])
    if msg_font.size(test_line)[0] < 380:  # Αυξημένο πλάτος για καλύτερη αξιοποίηση χώρου
        current_line.append(word)
    else:
        lines.append(' '.join(current_line))
        current_line = [word]
```
- Προσθέτει λέξεις σε μια γραμμή μέχρι να φτάσει το όριο πλάτους
- Ξεκινά νέα γραμμή όταν η τρέχουσα γραμμή γεμίσει
- Ελέγχει το πλάτος της γραμμής χρησιμοποιώντας τη μέθοδο size της γραμματοσειράς

```python
# Δημιουργία πλαισίου για μηνύματα
message_height = len(lines) * 25 + 10
pygame.draw.rect(surface, (250, 250, 250), 
                (BOARD_PX + 15, y_pos - 5, 420, message_height),
                0, 5)  # Στρογγυλεμένο πλαίσιο για μηνύματα
```
- Δημιουργεί ένα στρογγυλεμένο ορθογώνιο φόντο για το κείμενο του μηνύματος
- Υπολογίζει το ύψος με βάση τον αριθμό των γραμμών

```python
for line in lines:
    text = msg_font.render(line, True, BLACK)
    surface.blit(text, (BOARD_PX + 25, y_pos))
    y_pos += 25
```
- Απεικονίζει κάθε γραμμή κειμένου στη σωστή θέση
- Αυξάνει τη θέση κατακόρυφα για κάθε γραμμή