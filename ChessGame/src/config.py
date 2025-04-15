import pygame

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_PX = BOARD_SIZE * SQUARE_SIZE
WINDOW_WIDTH = BOARD_PX + 450  # Χώρος για μηνύματα/ενημερώσεις παιχνιδιού
WINDOW_HEIGHT = BOARD_PX

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (75, 75, 75)
LIGHT = (238, 238, 238)
HIGHLIGHT = (186, 202, 68)  # πράσινη υπογράμμιση για δυνατές κινήσεις
MOVE_HIGHLIGHT = (255, 255, 0, 100)  # κίτρινη υπογράμμιση για τελευταία κίνηση
CHECK_HIGHLIGHT = (255, 0, 0, 100)  # κόκκινη υπογράμμιση για σαχ

# Timer settings
DEFAULT_MAIN_TIME = 2 * 60 * 60  # 2 ώρες για τις χ πρώτες κινήσεις παρακάτω
DEFAULT_SECONDARY_TIME = 30 * 60  # 30 λεπτά για το υπόλοιπο του παιχνιδιού
MOVES_THRESHOLD = 40  # Αριθμός κινήσεων πριν τη λήξη του αρχικού παιχνιδιού

# Initialize pygame and setup window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Σκάκι ΠΛΗΠΡΟ')
clock = pygame.time.Clock()