# Μονάδα Χρονομέτρου (timer.py)

## Επισκόπηση
Αυτή η μονάδα υλοποιεί ένα σύστημα χρονομέτρου σκακιού δύο περιόδων, το οποίο χρησιμοποιείται για τη διαχείριση και απεικόνιση του χρόνου των παικτών κατά τη διάρκεια ενός παιχνιδιού σκακιού. Παρέχει λειτουργικότητα για την παρακολούθηση του διαθέσιμου χρόνου για κάθε παίκτη, για εναλλαγή μεταξύ των χρονομέτρων των παικτών, και για οπτική απεικόνιση της κατάστασης του χρονομέτρου στο γραφικό περιβάλλον.

## Ανάλυση Γραμμή προς Γραμμή

### Εισαγωγές
```python
import time
from ..config import DEFAULT_MAIN_TIME, DEFAULT_SECONDARY_TIME, MOVES_THRESHOLD, BLACK
```
- Εισάγει το pygame για λειτουργίες γραφικών και απεικόνισης
- Εισάγει τη μονάδα time για λειτουργίες χρονομέτρησης

### Ορισμός Κλάσης
```python
class ChessTimer:
    """
    ChessTimer - Μια κλάση για τη διαχείριση χρονομέτρων παιχνιδιού σκακιού με σύστημα ελέγχου χρόνου δύο περιόδων.
    """
```
- Ορίζει την κλάση ChessTimer για τη διαχείριση χρονομέτρων σκακιού
- Θέτει τις αρχικές παραμέτρους χρονισμού:
  - Αρχικός χρόνος 10 λεπτών (600 δευτερόλεπτα) για κάθε παίκτη
  - Προσαύξηση χρόνου 5 δευτερολέπτων μετά από κάθε κίνηση

### Μέθοδος Αρχικοποίησης
```python
def __init__(self, main_time=DEFAULT_MAIN_TIME, secondary_time=DEFAULT_SECONDARY_TIME):
    # Αρχικοποίηση χρόνων για τους παίκτες
    self.white_main_time = main_time
    self.black_main_time = main_time
    self.white_secondary_time = secondary_time
    self.black_secondary_time = secondary_time
```
- Αρχικοποιεί και τους δύο χρονομετρητές με τον αρχικό χρόνο
- Ορίζει το λευκό παίκτη ως τον τρέχοντα παίκτη (ο λευκός παίζει πάντα πρώτος στο σκάκι)

```python
# Αριθμός κινήσεων για κάθε παίκτη
self.white_moves = 0
self.black_moves = 0
# Αρχικοποίηση του χρώματος του ενεργού παίκτη
self.active_color = 'w'
# Αρχικοποίηση του χρόνου τελευταίας ενημέρωσης
self.last_update = time.time()
# αντικείμενο τερματισμού παιχνιδιού
self.game_over = False
```
- Αρχικοποιεί μεταβλητές παρακολούθησης χρόνου:
  - `last_update`: αποθηκεύει την τελευταία χρονική στιγμή ενημέρωσης του χρονομέτρου
  - `running`: δηλώνει αν το χρονόμετρο τρέχει (αρχικά δεν τρέχει)
  - `game_over`: δηλώνει αν το παιχνίδι έχει τελειώσει

### Μέθοδος Ενημέρωσης Χρονομέτρου
```python
def update(self):
    if self.game_over:
        return
        
    current = time.time()
    elapsed = current - self.last_update
    self.last_update = current
```
- Ενημερώνει το χρονόμετρο του τρέχοντος παίκτη
- Ελέγχει πρώτα αν το χρονόμετρο τρέχει και αν το παιχνίδι συνεχίζεται
- Υπολογίζει τον χρόνο που έχει περάσει από την τελευταία ενημέρωση
- Ενημερώνει το χρονικό σημείο της τελευταίας ενημέρωσης

```python
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
```
- Μειώνει το χρονόμετρο του τρέχοντος παίκτη με βάση τον χρόνο που πέρασε
- Αν το χρονόμετρο φτάσει στο 0, θέτει την κατάσταση παιχνιδιού σε "τέλος παιχνιδιού"
- Αποτρέπει αρνητικούς χρόνους θέτοντας την ελάχιστη τιμή στο 0

```python
# Έλεγχος αν ο χρόνος έχει λήξει
if self.white_moves < MOVES_THRESHOLD and self.white_main_time <= 0 and self.white_secondary_time <= 0:
    self.white_secondary_time = 0
    self.game_over = True
elif self.white_moves >= MOVES_THRESHOLD and self.white_secondary_time <= 0:
    self.white_secondary_time = 0
    self.game_over = True
```
- Ελέγχει αν ο χρόνος του λευκού παίκτη έχει λήξει:
  - Αν βρίσκεται στην κύρια φάση, ελέγχει αν έχουν εξαντληθεί και ο κύριος και ο δευτερεύων χρόνος
  - Αν βρίσκεται στη δευτερεύουσα φάση, ελέγχει αν έχει εξαντληθεί ο δευτερεύων χρόνος
  - Θέτει την κατάσταση παιχνιδιού σε "τέλος παιχνιδιού" αν ο χρόνος έχει λήξει

```python
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
```
- Παρόμοια λογική για τον χρόνο του μαύρου παίκτη όταν είναι ο ενεργός παίκτης

### Μέθοδος Εναλλαγής Σειράς
```python
def switch_turn(self):
    # Αύξηση του μετρητή κινήσεων για τον ενεργό παίκτη
    if self.active_color == 'w':
        self.white_moves += 1
    else:
        self.black_moves += 1
    
    # Αλλαγή του ενεργού παίκτη
    self.active_color = 'b' if self.active_color == 'w' else 'w'
    self.last_update = time.time()
```
- Καλείται όταν ένας παίκτης ολοκληρώνει μια κίνηση
- Αυξάνει τον μετρητή κινήσεων για τον παίκτη που μόλις έπαιξε
- Αλλάζει το ενεργό χρώμα στον άλλο παίκτη
- Επαναφέρει το χρονικό σημείο της τελευταίας ενημέρωσης

### Μέθοδος Μορφοποίησης Χρόνου
```python
def format_time(self, seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"
```
- Μορφοποιεί τον χρόνο σε δευτερόλεπτα σε μια αναγνώσιμη μορφή H:MM:SS ή MM:SS
- Χρησιμοποιεί μηδενικά για τα λεπτά και τα δευτερόλεπτα
- Παραλείπει την εμφάνιση των ωρών όταν απομένει λιγότερο από μία ώρα

### Μέθοδος Απεικόνισης
```python
def draw(self, surface):
    import pygame
    from ..config import BOARD_PX, BLACK
    
    # Ενημέρωση του χρόνου στο γραφικό περιβάλλον
    self.update()
    
    #  Δημιουργία γραμματοσειράς για το ρολόι
    font = pygame.font.SysFont('Arial', 22, bold=True)
    small_font = pygame.font.SysFont('Arial', 18)
```
- Απεικονίζει τα χρονόμετρα στην οθόνη του παιχνιδιού
- Πρώτα ενημερώνει τους χρονομετρητές για να έχουν τις τρέχουσες τιμές
- Ορίζει χρώματα για το φόντο και το κείμενο των χρονομετρητών

```python
# Σχεδίαση ρολογιού για τον λευκό παίκτη
y_pos = 180

# Σχεδίαση μετρητή κινήσεων για τον λευκό παίκτη
move_text = f"Κινήσεις: {self.white_moves}/{MOVES_THRESHOLD}"
move_surface = small_font.render(move_text, True, BLACK)
surface.blit(move_surface, (BOARD_PX + 20, y_pos))
y_pos += 25
```
- Σχεδιάζει τις ετικέτες "Λευκός Παίκτης" και "Μαύρος Παίκτης" πάνω από τα αντίστοιχα χρονόμετρα
- Σχεδιάζει τους χρόνους των παικτών στα κεντρικά σημεία των πλαισίων των χρονομετρητών
- Χρησιμοποιεί τη μεγαλύτερη γραμματοσειρά για τους χρόνους και τη μικρότερη για τις ετικέτες
- Κεντράρει όλα τα κείμενα οριζόντια και κάθετα στις αντίστοιχες θέσεις τους

```python
# Σχεδίαση κύριου χρόνου για τον λευκό παίκτη (αν είναι ακόμα κάτω από το όριο κινήσεων)
if self.white_moves < MOVES_THRESHOLD:
    main_color = (255, 0, 0) if self.white_main_time < 300 else BLACK  # Red if < 5 min
    main_text = f"Κύριος Χρόνος: {self.format_time(self.white_main_time)}"
    main_surface = font.render(main_text, True, main_color)
    surface.blit(main_surface, (BOARD_PX + 20, y_pos))
    y_pos += 25
```
- Εμφανίζει τον κύριο χρόνο για τον λευκό αν βρίσκεται ακόμα στην κύρια φάση
- Εμφανίζει τον χρόνο με κόκκινο χρώμα όταν απομένουν λιγότερα από 5 λεπτά
- Εμφανίζεται μόνο αν ο παίκτης βρίσκεται ακόμα κάτω από το όριο κινήσεων

```python
# Σχεδίαση δευτερεύοντα χρόνου για τον λευκό παίκτη
second_color = (255, 0, 0) if self.white_secondary_time < 300 else BLACK
second_text = f"Δευτερεύων Χρόνος: {self.format_time(self.white_secondary_time)}"
second_surface = font.render(second_text, True, second_color)
surface.blit(second_surface, (BOARD_PX + 20, y_pos))
y_pos += 35
```
- Εμφανίζει τον δευτερεύοντα χρόνο για τον λευκό
- Εμφανίζει τον χρόνο με κόκκινο χρώμα όταν απομένουν λιγότερα από 5 λεπτά
- Εμφανίζεται πάντα, ανεξάρτητα από τη φάση στην οποία βρίσκεται ο παίκτης

```python
# Σχεδίαση ρολογιού για τον μαύρο παίκτη
# [similar code for black player's times]
```
- Παρόμοια λογική για τον χρόνο του μαύρου παίκτη όταν είναι ο ενεργός παίκτης

```python
# Ενημέρωση του ενεργού παίκτη
active_text = "> ΛΕΥΚΟ" if self.active_color == 'w' else "> ΜΑΥΡΟ"
active = font.render(active_text, True, BLACK)
surface.blit(active, (BOARD_PX + 20, 150))
```
- Σχεδιάζει ένα κόκκινο σύμβολο "▶" δίπλα στο χρονόμετρο του ενεργού παίκτη
- Το σύμβολο εμφανίζεται μόνο όταν το χρονόμετρο τρέχει και το παιχνίδι δεν έχει τελειώσει
- Τοποθετεί το σύμβολο στην αριστερή πλευρά του χρονομέτρου του τρέχοντα παίκτη, κεντραρισμένο κάθετα

```python
# Εμφάνιση μηνύματος για το τέλος του παιχνιδιού στην περίπτωση που έχει λήξει ο χρόνος
if self.game_over:
    winner = "ΜΑΥΡΟΣ" αν (self.white_moves < MOVES_THRESHOLD και self.white_main_time <= 0 και self.white_secondary_time <= 0) ή (self.white_moves >= MOVES_THRESHOLD και self.white_secondary_time <= 0) αλλιώς "ΛΕΥΚΟΣ"
    timeout_text = font.render(f"Ο {winner} ΝΙΚΗΣΕ ΕΝΤΟΣ ΧΡΟΝΟΥ!", True, (255, 0, 0))
    surface.blit(timeout_text, (BOARD_PX + 20, y_pos + 30))
```
- Αν το παιχνίδι έχει τελειώσει λόγω λήξης χρόνου, εμφανίζει ένα μήνυμα που ανακοινώνει τον νικητή
- Καθορίζει τον νικητή ελέγχοντας ποιος παίκτης εξάντλησε τον χρόνο του
- Εμφανίζει το μήνυμα με κόκκινο χρώμα για να το τονίσει