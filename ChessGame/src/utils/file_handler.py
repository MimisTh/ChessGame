from datetime import datetime

def coords_to_algebraic(row, col):
    """Μετατροπή συντεταγμένων σε αλγεβρική σημειογραφία σκακιού (π.χ. e4)"""
    cols = 'abcdefgh'
    rows = '87654321'
    return cols[col] + rows[row]

def save_moves_to_file(moves_history, game_over=False, checkmate=False, turn=None, filename=None):
    """Αποθήκευση κινήσεων σε αρχείο κειμένου"""
    if not moves_history:
        return "Καμία κίνηση προς αποθήκευση!", False
    
    # Αν δεν υφίστατι αρχείο, δημιουργία με βάση την τρέχουσα χρονική στιγμή
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"./game_history/chess_game_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            # Εγγραφή κεφαλίδας
            f.write("Κινήσεις Σκακιού\n")
            f.write("===============\n\n")
            
            # Εγγραφή χρόνου και ημερομηνίας
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Το παιχνίδι πραγματοποιήθηκε την: {current_time}\n\n")
            
            # Εγγραφή κινήσεων
            f.write("Κινήσεις:\n")
            for i, move in enumerate(moves_history):
                move_number = i // 2 + 1
                if i % 2 == 0:  # Λευκός παίκτης
                    f.write(f"{move_number}. {move} ")
                else:  # Μαύρος παίκτης
                    f.write(f"{move}\n")
            
            # Προσθήκη κενής γραμμής αν ο τελευταίος παίκτης ήταν ο λευκός
            if len(moves_history) % 2 == 1:
                f.write("\n")
            
            # Εμφάνιση αποτελέσματος όπου δύναται
            if game_over:
                f.write("\nΑποτέλεσμα: ")
                if checkmate:
                    winner = "Μαύρος" if turn == 'w' else "Λευκός"
                    f.write(f"Ο {winner} παίκτης νίκησε!")
                else:
                    f.write("Ισοπαλία!")
        
        return f"Το ιστορικό του παιχνιδιού αποθηκεύτηκε με όνομα {filename}", True
    except Exception as e:
        return f"Σφάλμα κατά την αποθήκευση: {str(e)}", False