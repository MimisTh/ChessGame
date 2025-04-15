from ..config import BOARD_SIZE

def get_pawn_moves(board, row, col, color):
    moves = []
    direction = -1 if color == 'w' else 1
    
    # Κίνηση μπροστά
    if 0 <= row + direction < BOARD_SIZE and not board[row + direction][col]:
        moves.append((row + direction, col))
        
        # Κίνηση δύο τετραγώνων αν είναι η πρώτη κίνηση
        if (color == 'w' and row == 6) or (color == 'b' and row == 1):
            if not board[row + 2*direction][col]:
                moves.append((row + 2*direction, col))
    
    # Κίνηση διαγώνια για φάγωμα
    for dcol in [-1, 1]:
        if 0 <= row + direction < BOARD_SIZE and 0 <= col + dcol < BOARD_SIZE:
            target = board[row + direction][col + dcol]
            if target and target[0] != color:
                moves.append((row + direction, col + dcol))
    
    return moves

def get_rook_moves(board, row, col, color):
    moves = []
    # Κίνηση κάθετα και οριζόντια
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        for dist in range(1, BOARD_SIZE):
            r, c = row + dr * dist, col + dc * dist
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                break
            target = board[r][c]
            if not target:
                moves.append((r, c))
            elif target[0] != color:
                moves.append((r, c))
                break
            else:
                break
    
    return moves

def get_knight_moves(board, row, col, color):
    moves = []
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            target = board[r][c]
            if not target or target[0] != color:
                moves.append((r, c))
    
    return moves

def get_bishop_moves(board, row, col, color):
    moves = []
    # Diagonal moves
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for dist in range(1, BOARD_SIZE):
            r, c = row + dr * dist, col + dc * dist
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                break
            target = board[r][c]
            if not target:
                moves.append((r, c))
            elif target[0] != color:
                moves.append((r, c))
                break
            else:
                break
    
    return moves

def get_queen_moves(board, row, col, color):
    # Συνδυασμός κινήσεων πύργου και αξιωματικού
    moves = get_rook_moves(board, row, col, color)
    moves.extend(get_bishop_moves(board, row, col, color))
    return moves

def get_king_moves(board, row, col, color):
    moves = []
    king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in king_moves:
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            target = board[r][c]
            if not target or target[0] != color:
                moves.append((r, c))
    
    return moves

def is_square_under_attack(board, row, col, color):
    # Έλεγχος αν η συγκεκριμένη θέση είναι υπό επίθεση από τον αντίπαλο παίκτη
    opposite_color = 'b' if color == 'w' else 'w'
    
    # Έλεγχος στρατιωτών
    pawn_dir = 1 if color == 'w' else -1
    for dcol in [-1, 1]:
        r, c = row + pawn_dir, col + dcol
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            piece = board[r][c]
            if piece == opposite_color + 'p':
                return True
    
    # Έλεγχος ίππου
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dr, dc in knight_moves:
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            piece = board[r][c]
            if piece == opposite_color + 'n':
                return True
    
    # Έλεγχος βασιλιά
    king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in king_moves:
        r, c = row + dr, col + dc
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            piece = board[r][c]
            if piece == opposite_color + 'k':
                return True
    
    # Έλεγχος πύργου, αξιωματικού και βασίλισσας
    directions = {
        'straight': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        'diagonal': [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    }
    
    # Έλεγχος ίσιων γραμμών(πύργος και βασίλισσα)
    for dr, dc in directions['straight']:
        for dist in range(1, BOARD_SIZE):
            r, c = row + dr * dist, col + dc * dist
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                break
            piece = board[r][c]
            if piece:
                if piece[0] == opposite_color and (piece[1] == 'r' or piece[1] == 'q'):
                    return True
                break
    
    # Έλεγχος διαγώνιων γραμμών(αξιωματικός και βασίλισσα)
    for dr, dc in directions['diagonal']:
        for dist in range(1, BOARD_SIZE):
            r, c = row + dr * dist, col + dc * dist
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                break
            piece = board[r][c]
            if piece:
                if piece[0] == opposite_color and (piece[1] == 'b' or piece[1] == 'q'):
                    return True
                break
    
    return False