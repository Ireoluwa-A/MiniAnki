"""
Constants used throughout MiniAnki
All time values are in seconds unless otherwise specified
"""
import board

# File paths
SD_CARD_PATH = "/sd"
MANDARIN_FONT_PATH = f"{SD_CARD_PATH}/ChineseFont.bdf"
FLASHCARDS_PATH = f"{SD_CARD_PATH}/flashcards.json"
ANKI_IMPORT_PATH = f"{SD_CARD_PATH}/anki_export.txt"

# SD Card configuration
SD_SCK_PIN = board.GP10
SD_MOSI_PIN = board.GP11
SD_MISO_PIN = board.GP12
SD_CS_PIN = board.GP13

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
# Minimum and maximum intervals for showing cards
MIN_SHOW_INTERVAL_SEC = 5 
MAX_SHOW_INTERVAL_SEC = 10 


MIN_INTERVAL = 1  # 5 minutes
MAX_INTERVAL = 10

RESPONSE_TIMEOUT = 5  # Time user has to respond

RESPONSE_EASY = 1
RESPONSE_MEDIUM = 2
RESPONSE_HARD = 3
DEFAULT_RESPONSE = RESPONSE_HARD

