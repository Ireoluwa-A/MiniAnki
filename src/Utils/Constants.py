"""
Constants used throughout MiniAnki
All time values are in seconds unless otherwise specified
"""
import board

# File paths
SD_CARD_PATH = "/sd"
MANDARIN_FONT_PATH = f"{SD_CARD_PATH}/ChineseFont.bdf"
# FLASHCARDS_PATH = f"/sd/flashcards2.json"
FLASHCARDS_PATH = f"flashcardsbackup.json"
ANKI_IMPORT_PATH = f"{SD_CARD_PATH}/anki_export.txt"

# SD Card configuration
SD_SCK_PIN = board.GP2
SD_MOSI_PIN = board.GP3
SD_MISO_PIN = board.GP4
SD_CS_PIN = board.GP5

# Button configuration
BUTTON_EASY_PIN = board.GP21
BUTTON_MEDIUM_PIN = board.GP20
BUTTON_HARD_PIN = board.GP19

# E-Ink display configuration
EINK_SCK_PIN = board.GP10
EINK_MOSI_PIN = board.GP11
EINK_CS_PIN = board.GP9
EINK_DC_PIN = board.GP8
EINK_RESET_PIN = board.GP12
EINK_BUSY_PIN = board.GP13

EINK_BAUDRATE = 1000000  # Baudrate for SPI communication
EINK_WIDTH = 250
EINK_HEIGHT = 122
EINK_ROTATION = 270  # Rotation for the display
EINK_COLOR = 0xFF0000  # Highlight color for display

# Time intervals for flashcard display
# Minimum and maximum intervals for displaying any cards
MIN_SHOW_INTERVAL_SEC = 5 
MAX_SHOW_INTERVAL_SEC = 10 

# Spaced repetition intervals (in seconds)
# Minimum and maximum intervals assigned to cards
# after a review. These intervals are used to determine how long to wait
# before showing particular card again
MIN_INTERVAL = 60 * 5 # minutes
MAX_INTERVAL = 60 * 60 * 24 * 30 # days

# Spaced Repition settings
RESPONSE_EASY = 1
RESPONSE_MEDIUM = 2
RESPONSE_HARD = 3
DEFAULT_RESPONSE = RESPONSE_HARD
# Weights that affect how long to wait before showing the card again
# These are multipliers for the intervals based on user response
RESPONSE_EASY_MULTIPLIER = 2.0
RESPONSE_MEDIUM_MULTIPLIER = 1.3
RESPONSE_HARD_MULTIPLIER = 0.5

RESPONSE_TIMEOUT_SEC = 5  # Time to wait for user response