"""
Constants used throughout MiniAnki
All time values are in seconds unless otherwise specified
"""

# File paths
SD_CARD_PATH = "/sd"
FLASHCARDS_PATH = f"{SD_CARD_PATH}/flashcards.json"
ANKI_IMPORT_PATH = f"{SD_CARD_PATH}/anki_export.txt"

# SD Card configuration
SD_CS_PIN = 13  # GP13
SPI_SCK_PIN = 10  # GP10
SPI_MOSI_PIN = 11  # GP11
SPI_MISO_PIN = 12  # GP12

# Spaced repetition intervals
# MIN_INTERVAL = 5 * 60  # 5 minutes
# MAX_INTERVAL = 30 * 24 * 60 * 60  # 30 days

MIN_INTERVAL = 1  # 5 minutes
MAX_INTERVAL = 10

# Show intervals - time between showing cards
# MIN_SHOW_INTERVAL = 5 * 60  # 5 minutes
# MAX_SHOW_INTERVAL = 60 * 60  # 1 hour

MIN_SHOW_INTERVAL = 5
MAX_SHOW_INTERVAL = 10  

RESPONSE_TIMEOUT = 5  # Time user has to respond

RESPONSE_EASY = 1
RESPONSE_MEDIUM = 2
RESPONSE_HARD = 3
DEFAULT_RESPONSE = RESPONSE_HARD

EINK_REFRESH_INTERVAL_SEC = 180  # Time between E-Ink refreshes