import time
from ..config import DEFAULT_MAIN_TIME, DEFAULT_SECONDARY_TIME, MOVES_THRESHOLD, BLACK

class ChessTimer:
    """
    ChessTimer - Μια κλάση για τη διαχείριση χρονομέτρων παιχνιδιού σκακιού με σύστημα ελέγχου χρόνου δύο περιόδων.
    """
    
    def __init__(self, main_time=DEFAULT_MAIN_TIME, secondary_time=DEFAULT_SECONDARY_TIME):
        # Αρχικοποίηση χρόνων για τους παίκτες
        self.white_main_time = main_time
        self.black_main_time = main_time
        self.white_secondary_time = secondary_time
        self.black_secondary_time = secondary_time
        # Αριθμός κινήσεων για κάθε παίκτη
        self.white_moves = 0
        self.black_moves = 0
        # Αρχικοποίηση του χρώματος του ενεργού παίκτη
        self.active_color = 'w'
        # Αρχικοποίηση του χρόνου τελευταίας ενημέρωσης
        self.last_update = time.time()
        # αντικείμενο τερματισμού παιχνιδιού
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
        import pygame
        from ..config import BOARD_PX, BLACK
        
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