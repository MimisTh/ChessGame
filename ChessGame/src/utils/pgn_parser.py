import re
import os
from tkinter import Tk, filedialog
from ..config import BOARD_SIZE

class PGNParser:
    """
    Class for parsing PGN (Portable Game Notation) chess files.
    Extracts moves, especially focusing on the black player's moves.
    """
    
    def __init__(self):
        self.black_player_name = ""
        self.games = []
        self.black_moves = {}  # Dictionary to store position -> move mappings
        self.position_frequency = {}  # Track frequency of positions
        
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
        
    def parse_pgn_file(self, file_path):
        """Parses a PGN file and extracts games"""
        if not file_path or not os.path.exists(file_path):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as pgn_file:
                content = pgn_file.read()
                
            # Split file into individual games
            game_texts = re.split(r'\n\s*\n\[Event', content)
            
            # Handle the first game (which doesn't have [Event at the beginning after split)
            if game_texts and not game_texts[0].strip().startswith('[Event'):
                game_texts[0] = '[Event' + game_texts[0]
                
            # Process each game
            num_games_parsed = 0
            for game_text in game_texts:
                if not game_text.strip():
                    continue
                    
                game_data = self.parse_single_game('[Event' + game_text if not game_text.startswith('[Event') else game_text)
                if game_data and 'moves' in game_data:
                    self.games.append(game_data)
                    num_games_parsed += 1
                    
                    # Extract information about black's playing style
                    if game_data['black_player']:
                        self.black_player_name = game_data['black_player']
                        
                    self.analyze_black_moves(game_data['moves'])
                    
                # Limit to 50 games as requested
                if num_games_parsed >= 50:
                    break
                    
            return num_games_parsed > 0
            
        except Exception as e:
            print(f"Error parsing PGN file: {str(e)}")
            return False
    
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
                
        # Extract moves - find the movetext section (after the last header)
        movetext_match = re.search(r'\]\s*(1\..*?(?:1-0|0-1|1\/2-1\/2|\*))', game_text, re.DOTALL)
        if movetext_match:
            movetext = movetext_match.group(1)
            
            # Clean up annotations, comments, and variations
            movetext = re.sub(r'\{[^}]*\}', '', movetext)  # Remove comments
            movetext = re.sub(r'\([^)]*\)', '', movetext)  # Remove variations
            
            # Extract the moves
            moves = re.findall(r'(\d+)\.+\s*([^\s.]+)(?:\s+([^\s.]+))?', movetext)
            for move_num, white_move, black_move in moves:
                if white_move:
                    game_data['moves'].append(('w', white_move))
                if black_move:
                    game_data['moves'].append(('b', black_move))
        
        return game_data
    
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
                
                if position_key not in self.black_moves:
                    self.black_moves[position_key] = []
                    self.position_frequency[position_key] = 0
                    
                self.black_moves[position_key].append(move)
                self.position_frequency[position_key] += 1
    
    def get_most_likely_move(self, position_key):
        """Returns the most likely move for a given position based on the black player's style"""
        if position_key in self.black_moves and self.black_moves[position_key]:
            # Count occurrences of each move
            move_counts = {}
            for move in self.black_moves[position_key]:
                if move not in move_counts:
                    move_counts[move] = 0
                move_counts[move] += 1
                
            # Return the most frequent move
            return max(move_counts.items(), key=lambda x: x[1])[0]
            
        return None
    
    def get_player_name(self):
        """Returns the name of the black player whose style we're analyzing"""
        return self.black_player_name if self.black_player_name else "Unknown Player"
        
    def get_style_summary(self):
        """Returns a summary of the black player's playing style"""
        if not self.black_moves:
            return "No games analyzed."
            
        num_games = len(self.games)
        num_positions = len(self.black_moves)
        
        return f"Analyzed {num_games} games with {num_positions} unique positions from player {self.get_player_name()}"