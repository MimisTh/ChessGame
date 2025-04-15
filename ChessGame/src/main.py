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

def main():
    # Εμφάνιση μενού επιλογής τρόπου παιχνιδιού
    game_mode, ai_difficulty = show_game_mode_selection(window)
    
    # Αρχικοποίηση του AI αν επιλέχθηκε
    chess_engine = None
    clone_engine = None
    
    if game_mode == "PVE" and ai_difficulty is not None:
        chess_engine = ChessEngine(difficulty=ai_difficulty)
    elif game_mode == "CLONE":
        # Δημιουργία και ρύθμιση του clone engine
        clone_engine = CloneEngine()
        # Αναδυόμενο παράθυρο για επιλογή αρχείου PGN
        result_message = clone_engine.load_player_data()
        
        # Εμφάνιση μηνύματος αποτελέσματος της φόρτωσης
        font = pygame.font.SysFont('Arial', 24)
        window.fill((240, 240, 240))
        message_lines = [line for line in result_message.split("\n")]
        
        # Τίτλος
        title_font = pygame.font.SysFont('Arial', 32, bold=True)
        title = title_font.render("Φόρτωση Δεδομένων Παίκτη", True, (0, 0, 0))
        window.blit(title, (BOARD_PX // 2 - 150, 200))
        
        # Μηνύματα
        for i, line in enumerate(message_lines):
            line_surface = font.render(line, True, (0, 0, 0))
            window.blit(line_surface, (BOARD_PX // 2 - 200, 250 + i * 30))
        
        # Μήνυμα συνέχειας
        continue_font = pygame.font.SysFont('Arial', 20, italic=True)
        continue_text = continue_font.render("Πατήστε οποιοδήποτε πλήκτρο για συνέχεια...", True, (100, 100, 100))
        window.blit(continue_text, (BOARD_PX // 2 - 150, 350))
        
        pygame.display.flip()
        
        # Αναμονή για κλικ ή πάτημα πλήκτρου
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                    waiting = False
    
    # Αρχικοποίηση σκακιέρας και χρονομέτρου
    board = ChessBoard()
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
    
    # Μήνυμα έναρξης παιχνιδιού
    if game_mode == "PVE":
        difficulty_text = "Εύκολο" if ai_difficulty == 1 else "Μεσαίο" if ai_difficulty == 2 else "Δύσκολο"
        board.message = f"Ξεκινά παιχνίδι εναντίον AI ({difficulty_text})"
    elif game_mode == "CLONE":
        player_name = clone_engine.player_name if clone_engine.loaded else "Unknown Player"
        board.message = f"Ξεκινά παιχνίδι εναντίον Clone AI που μιμείται τον παίκτη {player_name}"
    else:
        board.message = "Ξεκινά παιχνίδι μεταξύ δύο παικτών"
    
    # Κύρια δομή επανάληψης παιχνιδιού
    running = True
    while running:
        # Έλεγχος αν είναι η σειρά του AI να παίξει
        if (game_mode == "PVE" or game_mode == "CLONE") and board.turn == 'b' and not board.game_over:
            # Εύρεση καλύτερης κίνησης ανάλογα με το είδος του AI
            ai_move = None
            if game_mode == "PVE" and chess_engine:
                ai_move = chess_engine.get_best_move(board)
            elif game_mode == "CLONE" and clone_engine:
                ai_move = clone_engine.get_best_move(board)
            
            if ai_move:
                from_pos, to_pos = ai_move
                # Επιλογή του πιονιού για την κίνηση
                board.select_piece(from_pos[0], from_pos[1])
                # Εκτέλεση της κίνησης
                move_successful = board.move_piece(from_pos, to_pos)
                
                if move_successful:
                    if not board.game_over:
                        timer.switch_turn()
                    else:
                        timer.game_over = True
                        if board.checkmate:
                            winner = "Μαύρος" if board.turn == 'w' else "Λευκός"
                            show_checkmate_modal(window, winner)
            # Καθαρισμός επιλογής και έγκυρων κινήσεων μετά την κίνηση του AI
            board.selected_piece = None
            board.valid_moves = []
        
        # Διαχείριση αμεσών χειρισμών γραφικού περιβάλλοντος
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # Επιτρέπουμε κινήσεις του χρήστη μόνο αν είναι η σειρά του λευκού ή
            # αν παίζουν δύο άνθρωποι (PVP mode) και δεν έχει τελειώσει το παιχνίδι
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and 
                 (board.turn == 'w' or game_mode == "PVP") and not board.game_over):
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
            
            elif event.type == MOUSEMOTION and dragging:
                drag_pos = event.pos
            
            elif (event.type == MOUSEBUTTONUP and event.button == 1 and dragging and
                 (board.turn == 'w' or game_mode == "PVP")):
                mouseX, mouseY = event.pos
                
                if mouseX < BOARD_PX:
                    col = mouseX // SQUARE_SIZE
                    row = mouseY // SQUARE_SIZE
                    to_pos = (row, col)
                    
                    if orig_pos != to_pos:  # Έλεγχος επιλογής διαφορετικής θέσης
                        move_successful = board.move_piece(orig_pos, to_pos)
                        if move_successful:
                            if not board.game_over:
                                timer.switch_turn()
                            else:
                                timer.game_over = True
                                if board.checkmate:
                                    winner = "Μαύρος" if board.turn == 'w' else "Λευκός"
                                    show_checkmate_modal(window, winner)
                
                dragging = False
                drag_piece = None
                board.selected_piece = None
                board.valid_moves = []
                
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    board.save_moves_to_file()
                    print("Επιτυχής αποθήκευση αρχείου!")
                elif event.key == K_n:
                    # Επανεκκίνηση παιχνιδιού
                    return main()
                elif event.key == K_q:
                    running = False
        
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
        
        # Σχεδίαση πιονιών
        draw_pieces(window, board.board, pieces)
        
        # Σχεδίαση πιονιού που έχει επιλεγεί για μετακίνηση
        if dragging and drag_piece:
            draw_dragged_piece(window, pieces, drag_piece, drag_pos)
        
        # Σχεδίαση πάνελ μηνυμάτων
        draw_message_panel(window, board.message, board.turn, board.game_over)
        
        # Σχεδίαση χρονομέτρου
        timer.draw(window)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()