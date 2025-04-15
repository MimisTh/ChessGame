import pygame
import sys
from pygame.locals import *

from .config import window, clock, BOARD_PX, SQUARE_SIZE
from .board.chess_board import ChessBoard
from .utils.timer import ChessTimer
from .ui.rendering import (load_pieces, create_placeholder_pieces, show_checkmate_modal, 
                         draw_board, draw_pieces, draw_dragged_piece, draw_message_panel)

def main():
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
    
    # Κύρια δομή επανάληψης παιχνιδιού
    running = True
    while running:
        # Διαχείριση αμεσών χειρισμών γραφικού περιβάλλοντος
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                
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