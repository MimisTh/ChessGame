# Μονάδα Ανάλυσης PGN (pgn_parser.py)

## Επισκόπηση
Αυτή η μονάδα υλοποιεί έναν αναλυτή για αρχεία PGN (Portable Game Notation) σκακιού. Επικεντρώνεται στην εξαγωγή και ανάλυση κινήσεων, ιδιαίτερα από την οπτική του μαύρου παίκτη, για να διευκολύνει την ικανότητα της μηχανής κλώνου να μιμείται το στυλ παιχνιδιού ενός συγκεκριμένου παίκτη.

## Ανάλυση Γραμμή προς Γραμμή

### Εισαγωγές
```python
import re
import os
from tkinter import Tk, filedialog
from ..config import BOARD_SIZE
```
- Εισάγει απαραίτητες βιβλιοθήκες:
  - `re`: Μονάδα κανονικών εκφράσεων για αντιστοίχιση προτύπων σε κείμενο PGN
  - `os`: Συναρτήσεις λειτουργικού συστήματος για εργασίες με διαδρομές αρχείων
  - `Tk, filedialog` από tkinter: Στοιχεία GUI για επιλογή αρχείων
  - `BOARD_SIZE`: Σταθερά διαμόρφωσης από τη μονάδα config

### Ορισμός Κλάσης
```python
class PGNParser:
    """
    Class for parsing PGN (Portable Game Notation) chess files.
    Extracts moves, especially focusing on the black player's moves.
    """
```
- Ορίζει την κλάση PGNParser με μια περιγραφή του σκοπού της

### Μέθοδος Αρχικοποίησης
```python
def __init__(self):
    self.black_player_name = ""
    self.games = []
    self.black_moves = {}  # Dictionary to store position -> move mappings
    self.position_frequency = {}  # Track frequency of positions
```
- Αρχικοποιεί μεταβλητές στιγμιότυπου:
  - `black_player_name`: Αποθηκεύει το όνομα του μαύρου παίκτη του οποίου το στυλ αναλύεται
  - `games`: Λίστα για αποθήκευση δεδομένων αναλυμένων παιχνιδιών
  - `black_moves`: Λεξικό που αντιστοιχίζει θέσεις σκακιέρας σε κινήσεις (για ανάλυση στυλ)
  - `position_frequency`: Λεξικό που παρακολουθεί πόσο συχνά εμφανίζονται οι θέσεις

### Μέθοδος Επιλογής Αρχείου
```python
def select_pgn_file(self):
    """Opens a file dialog to select a PGN file"""
    root = Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title="Select PGN File",
        filetypes=[("PGN files", "*.pgn"), ("All files", "*.*")],
        initialdir=os.path.expanduser("~\\Documents")
    )
    
    root.destroy()
    return file_path
```
- Δημιουργεί ένα διάλογο επιλογής αρχείου για την επιλογή ενός αρχείου PGN:
  - Δημιουργεί ένα κρυφό παράθυρο ρίζας Tkinter
  - Ανοίγει ένα διάλογο αρχείων με κατάλληλα φίλτρα για αρχεία PGN
  - Ορίζει τον αρχικό κατάλογο στον φάκελο Έγγραφα του χρήστη
  - Επιστρέφει τη διαδρομή του επιλεγμένου αρχείου ή κενή συμβολοσειρά αν ακυρωθεί

### Μέθοδος Ανάλυσης Αρχείου PGN
```python
def parse_pgn_file(self, file_path):
    """Parses a PGN file and extracts games"""
    if not file_path or not os.path.exists(file_path):
        return False
```
- Κύρια μέθοδος για την ανάλυση ενός αρχείου PGN:
  - Δέχεται μια διαδρομή αρχείου ως είσοδο
  - Επιστρέφει νωρίς με False αν η διαδρομή είναι άκυρη ή δεν υπάρχει

```python
try:
    with open(file_path, 'r', encoding='utf-8') as pgn_file:
        content = pgn_file.read()
```
- Ανοίγει το αρχείο PGN με κωδικοποίηση UTF-8 και διαβάζει όλο το περιεχόμενό του
- Χρησιμοποιεί ένα μπλοκ try-except για να χειριστεί πιθανά σφάλματα αρχείου

```python
# Split file into individual games
game_texts = re.split(r'\n\s*\n\[Event', content)

# Handle the first game (which doesn't have [Event at the beginning after split)
if game_texts and not game_texts[0].strip().startswith('[Event'):
    game_texts[0] = '[Event' + game_texts[0]
```
- Χωρίζει το αρχείο σε μεμονωμένα παιχνίδια χρησιμοποιώντας κανονικές εκφράσεις
  - Τα παιχνίδια σε PGN συνήθως διαχωρίζονται με κενές γραμμές
  - Κάθε παιχνίδι ξεκινά με ζεύγη ετικετών όπως `[Event "..."]`
- Διορθώνει το κείμενο του πρώτου παιχνιδιού προσθέτοντας πίσω το πρόθεμα `[Event` αν αφαιρέθηκε κατά τον διαχωρισμό

```python
# Process each game
num_games_parsed = 0
for game_text in game_texts:
    if not game_text.strip():
        continue
```
- Επαναλαμβάνεται σε κάθε κείμενο παιχνιδιού, παραλείποντας κενές καταχωρήσεις
- Παρακολουθεί πόσα παιχνίδια έχουν αναλυθεί επιτυχώς

```python
game_data = self.parse_single_game('[Event' + game_text if not game_text.startswith('[Event') else game_text)
if game_data and 'moves' in game_data:
    self.games.append(game_data)
    num_games_parsed += 1
    
    # Extract information about black's playing style
    if game_data['black_player']:
        self.black_player_name = game_data['black_player']
        
    self.analyze_black_moves(game_data['moves'])
```
- Αναλύει κάθε κείμενο παιχνιδιού σε δομημένα δεδομένα παιχνιδιού
- Αν το παιχνίδι αναλύθηκε επιτυχώς και περιέχει κινήσεις:
  - Το προσθέτει στην εσωτερική λίστα παιχνιδιών
  - Ενημερώνει το όνομα του μαύρου παίκτη εάν είναι διαθέσιμο
  - Αναλύει τις κινήσεις του μαύρου παίκτη για την εξαγωγή προτύπων στυλ

```python
# Limit to 50 games as requested
if num_games_parsed >= 50:
    break
```
- Περιορίζει την επεξεργασία στα πρώτα 50 παιχνίδια για λόγους απόδοσης

```python
return num_games_parsed > 0

except Exception as e:
    print(f"Error parsing PGN file: {str(e)}")
    return False
```
- Επιστρέφει True αν αναλύθηκε επιτυχώς τουλάχιστον ένα παιχνίδι, αλλιώς False
- Συλλαμβάνει και εκτυπώνει τυχόν εξαιρέσεις κατά τη διαδικασία ανάλυσης

### Μέθοδος Ανάλυσης Μεμονωμένου Παιχνιδιού
```python
def parse_single_game(self, game_text):
    """Parses a single game from PGN notation"""
    game_data = {
        'event': '',
        'date': '',
        'white_player': '',
        'black_player': '',
        'result': '',
        'moves': []
    }
```
- Δημιουργεί ένα λεξικό για την αποθήκευση δομημένων δεδομένων σχετικά με ένα μεμονωμένο παιχνίδι σκακιού
- Αρχικοποιεί πεδία για λεπτομέρειες εκδήλωσης, ονόματα παικτών, αποτέλεσμα και κινήσεις

```python
# Extract header information
headers = re.findall(r'\[(\w+)\s+"([^"]+)"\]', game_text)
for key, value in headers:
    if key == 'Event':
        game_data['event'] = value
    elif key == 'Date':
        game_data['date'] = value
    elif key == 'White':
        game_data['white_player'] = value
    elif key == 'Black':
        game_data['black_player'] = value
    elif key == 'Result':
        game_data['result'] = value
```
- Χρησιμοποιεί κανονικές εκφράσεις για να εξαγάγει πληροφορίες επικεφαλίδας από ζεύγη ετικετών PGN
- Αντιστοιχίζει τυπικές ετικέτες PGN σε πεδία στο λεξικό game_data

```python
# Extract moves - find the movetext section (after the last header)
movetext_match = re.search(r'\]\s*(1\..*?(?:1-0|0-1|1\/2-1\/2|\*))', game_text, re.DOTALL)
if movetext_match:
    movetext = movetext_match.group(1)
```
- Εξάγει την ενότητα movetext που περιέχει τις πραγματικές κινήσεις σκακιού
- Αναζητά περιεχόμενο που ξεκινά με "1." (πρώτη κίνηση) και τελειώνει με αποτέλεσμα παιχνιδιού

```python
# Clean up annotations, comments, and variations
movetext = re.sub(r'\{[^}]*\}', '', movetext)  # Remove comments
movetext = re.sub(r'\([^)]*\)', '', movetext)  # Remove variations
```
- Αφαιρεί στοιχεία που δεν είναι απαραίτητα για την ανάλυση κίνησης:
  - Σχόλια που περικλείονται σε αγκύλες `{ ... }`
  - Εναλλακτικές παραλλαγές που περικλείονται σε παρενθέσεις `( ... )`

```python
# Extract the moves
moves = re.findall(r'(\d+)\.+\s*([^\s.]+)(?:\s+([^\s.]+))?', movetext)
for move_num, white_move, black_move in moves:
    if white_move:
        game_data['moves'].append(('w', white_move))
    if black_move:
        game_data['moves'].append(('b', black_move))
```
- Χρησιμοποιεί κανονικές εκφράσεις για να εξαγάγει ζεύγη κινήσεων με τη μορφή "1. e4 e5"
- Αναλύει τον αριθμό κίνησης, την κίνηση του λευκού και την κίνηση του μαύρου
- Προσθέτει κάθε κίνηση στη λίστα κινήσεων με αναγνωριστικό χρώματος ('w' ή 'b')

```python
return game_data
```
- Επιστρέφει το λεξικό αναλυμένων δεδομένων παιχνιδιού

### Μέθοδος Ανάλυσης Κινήσεων Μαύρου
```python
def analyze_black_moves(self, moves):
    """Analyzes black player's moves to extract patterns"""
    # In a real implementation, we would maintain a board state
    # and analyze the positions and responses
    # For simplicity, we'll just count occurrence of moves
    
    for i, (color, move) in enumerate(moves):
        if color == 'b':
            # Get the current position representation - in a real implementation
            # this would be a FEN or simplified board state
            # For now we use the previous moves as a simplified representation
            position_key = str(moves[max(0, i-2):i])
```
- Αναλύει μια λίστα κινήσεων για να εξαγάγει μοτίβα στο στυλ του μαύρου παίκτη
- Για κάθε κίνηση του μαύρου, δημιουργεί ένα "κλειδί θέσης" με βάση τις προηγούμενες 2 κινήσεις
- Η απλοποιημένη προσέγγιση χρησιμοποιεί προηγούμενες κινήσεις ως αναγνωριστικό θέσης αντί για πλήρη κατάσταση σκακιέρας

```python
if position_key not in self.black_moves:
    self.black_moves[position_key] = []
    self.position_frequency[position_key] = 0
    
self.black_moves[position_key].append(move)
self.position_frequency[position_key] += 1
```
- Για κάθε θέση:
  - Αρχικοποιεί την παρακολούθηση αν αυτή είναι η πρώτη φορά που βλέπει αυτή τη θέση
  - Καταγράφει την επιλεγμένη κίνηση του μαύρου παίκτη σε αυτή τη θέση
  - Αυξάνει τον μετρητή συχνότητας για αυτή τη θέση

### Μέθοδος Πρόβλεψης Κίνησης
```python
def get_most_likely_move(self, position_key):
    """Returns the most likely move for a given position based on the black player's style"""
    if position_key in self.black_moves and self.black_moves[position_key]:
        # Count occurrences of each move
        move_counts = {}
        for move in self.black_moves[position_key]:
            if move not in move_counts:
                move_counts[move] = 0
            move_counts[move] += 1
```
- Δεδομένου ενός κλειδιού θέσης, καθορίζει την πιο πιθανή κίνηση με βάση το ιστορικό του παίκτη
- Μετρά πόσες φορές παίχτηκε κάθε πιθανή κίνηση σε αυτή τη θέση

```python
# Return the most frequent move
return max(move_counts.items(), key=lambda x: x[1])[0]
```
- Επιστρέφει την κίνηση με την υψηλότερη συχνότητα (την πιο συνηθισμένη επιλογή του παίκτη)
- Χρησιμοποιεί τη συνάρτηση `max()` με μια προσαρμοσμένη συνάρτηση κλειδιού για να βρει την κίνηση με τη μεγαλύτερη καταμέτρηση

```python
return None
```
- Επιστρέφει None αν η θέση δεν έχει εμφανιστεί ποτέ στο παρελθόν

### Βοηθητικές Μέθοδοι
```python
def get_player_name(self):
    """Returns the name of the black player whose style we're analyzing"""
    return self.black_player_name if self.black_player_name else "Unknown Player"
```
- Επιστρέφει το όνομα του μαύρου παίκτη του οποίου το στυλ αναλύεται
- Χρησιμοποιείται προεπιλογή "Unknown Player" αν δεν βρέθηκε όνομα στα αναλυμένα παιχνίδια

```python
def get_style_summary(self):
    """Returns a summary of the black player's playing style"""
    if not self.black_moves:
        return "No games analyzed."
        
    num_games = len(self.games)
    num_positions = len(self.black_moves)
    
    return f"Analyzed {num_games} games with {num_positions} unique positions from player {self.get_player_name()}"
```
- Δημιουργεί μια σύνοψη των αποτελεσμάτων ανάλυσης στυλ παίκτη:
  - Επιστρέφει μήνυμα σφάλματος αν δεν αναλύθηκαν παιχνίδια
  - Διαφορετικά, αναφέρει τον αριθμό των παιχνιδιών, τις μοναδικές θέσεις και το όνομα του παίκτη
  - Αυτή η σύνοψη εμφανίζεται στον χρήστη μετά τη φόρτωση ενός αρχείου PGN