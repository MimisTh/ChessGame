import pygame
import sys
from pygame.locals import *
from ..config import SQUARE_SIZE, BOARD_PX, WINDOW_WIDTH, WINDOW_HEIGHT, LIGHT, DARK, BLACK, WHITE

def load_pieces():
    """Συνάρτηση για την φόρτωση των πιονιών"""
    pieces = {}
    for color in ['w', 'b']:
        for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
            img = pygame.image.load(f'assets/pieces/{color}{piece}.png')
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            pieces[f'{color}{piece}'] = img
    return pieces

def create_placeholder_pieces():
    """Συνάρτηση για την δημιουργία των πιονιών με σύμβολα (περίπτωση σφάλματος στην φόρτωση των εικόνων)"""
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

def draw_board(surface, board_state, last_move, selected_piece, valid_moves, white_king_pos, black_king_pos, in_check, turn):
    """Σχεδίαση σκακιέρας και κατάστασης παιχνιδιού"""
    for row in range(8):
        for col in range(8):
            x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
            color = LIGHT if (row + col) % 2 == 0 else DARK
            
            # Σχεδιασμός τετραγώνου
            pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Υπογράμμιση τελευταίας κίνησης
            if last_move and ((row, col) == last_move[0] or (row, col) == last_move[1]):
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill((255, 255, 0, 50))  # Semi-transparent yellow
                surface.blit(highlight, (x, y))
            
            # Υπογράμμιση επιλεγμένου πιονιού
            if selected_piece and selected_piece[0] == row and selected_piece[1] == col:
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill((100, 100, 255, 100))  # Semi-transparent blue
                surface.blit(highlight, (x, y))
            
            # Υπογράμμιση δυνατών κινήσεων
            if (row, col) in valid_moves:
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill((0, 255, 0, 70))  # Semi-transparent green
                surface.blit(highlight, (x, y))
            
            # Υπογράμμιση βασιλιά υπο σαχ
            if in_check:
                king_pos = white_king_pos if turn == 'w' else black_king_pos
                if (row, col) == king_pos:
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill((255, 0, 0, 100))  # Ημιδιάφανο κόκκινο
                    surface.blit(highlight, (x, y))

def draw_pieces(surface, board_state, pieces):
    """Σχεδίαση πιονιών στη σκακιέρα"""
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece:
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                surface.blit(pieces[piece], (x, y))

def draw_dragged_piece(surface, pieces, piece, pos):
    """Σχεδίαση πιονιού που μετακινείται"""
    if piece:
        piece_img = pieces[piece]
        rect = piece_img.get_rect(center=pos)
        surface.blit(piece_img, rect)

def draw_message_panel(surface, message, turn, game_over):
    """Σχεδίαση πάνελ μηνυμάτων"""
    # Σχεδίαση υποβάθρου πάνελ μηνυμάτων
    pygame.draw.rect(surface, (240, 240, 240), (BOARD_PX, 0, 450, WINDOW_HEIGHT))
    pygame.draw.line(surface, BLACK, (BOARD_PX, 0), (BOARD_PX, WINDOW_HEIGHT), 2)
    
    # Δημιουργία μεταβλητών γραμματοσειρών
    title_font = pygame.font.SysFont('Arial', 28, bold=True)
    msg_font = pygame.font.SysFont('Arial', 22)
    turn_font = pygame.font.SysFont('Arial', 24, bold=True)
    
    # Δημιουργία τίτλου και στρογγυλεμένου πλαισίου
    title = title_font.render("Σκάκι ΠΛΗΠΡΟ", True, BLACK)
    surface.blit(title, (BOARD_PX + 20, 30))
    
    # Σχεδίαση μηνύματος σειράς ή λήξης
    if not game_over:
        turn_text = "Σειρά του Λευκού παίκτη" if turn == 'w' else "Σειρά του Μαύρου παίκτη"
        turn_color = BLACK
    else:
        turn_text = "Τέλος παιχνιδιού"
        turn_color = (255, 0, 0)  # Κόκκινο για τέλος παιχνιδιού
        
    turn_label = turn_font.render(turn_text, True, turn_color)
    surface.blit(turn_label, (BOARD_PX + 20, 80))
    
    # Σχεδίαση μηνυμάτων κατάστασης
    y_pos = 320  # Τοποθέτηση κάτω από το χρονόμετρο
    words = message.split()
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
    
    for line in lines:
        text = msg_font.render(line, True, BLACK)
        surface.blit(text, (BOARD_PX + 20, y_pos))
        y_pos += 25