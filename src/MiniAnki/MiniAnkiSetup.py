import board
import busio as io
import digitalio
import storage
import adafruit_sdcard
import json
import os
from Utils.Constants import *
from Utils.Flashcard import Flashcard

class MiniAnkiSetup:
    def setup_sd_card():
        """
        Initialize the SD card
        
        Returns:
            bool: True if SD card was successfully mounted, False otherwise
        """
        try:
            # Create the SPI bus
            spi = io.SPI(board.GP10,    # SCK
                        board.GP11,      # MOSI
                        board.GP12)      # MISO

            # Create the CS (Chip Select) pin
            cs = digitalio.DigitalInOut(board.GP13)
            
            # Initialize SD card
            sdcard = adafruit_sdcard.SDCard(spi, cs)
            
            # Create the filesystem
            vfs = storage.VfsFat(sdcard)
            
            # Mount the filesystem
            try:
                storage.mount(vfs, "/sd")
                print("SD card mounted successfully at /sd")
            except RuntimeError as e:
                # If already mounted, unmount and try again
                storage.umount("/sd")
                storage.mount(vfs, "/sd")
                print("SD card remounted successfully at /sd")
                
            return True
            
        except Exception as e:
            print(f"Failed to mount SD card: {str(e)}")
            return False

    def load_cards(self):
        """Load flashcards from JSON file"""
        try:
            if not os.path.exists(self.flashcards_path):
                print(f"Warning: Flashcards file not found at {self.flashcards_path}")
                return []
                
            with open(self.flashcards_path, "r") as f:
                data = json.load(f)
                cards = [Flashcard(**card) for card in data]
                print(f"Loaded {len(self.cards)} flashcards")
                return cards
                
        except Exception as e:
            print(f"Error loading flashcards: {e}")
            return []

    def cleanup(self):
        """Clean up resources before exit"""
        print("Cleaning up...")
        
        self.save_cards()
        
        self.eink.cleanup()
        self.button_manager.cleanup()
        # cleanup sd card etc

    def save_cards(self):
        """Save flashcards to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.flashcards_path), exist_ok=True)
            
            with open(self.flashcards_path, "w") as f:
                json.dump([card.to_dict() for card in self.cards], f, indent=2)
            print(f"Saved {len(self.cards)} flashcards")
            
        except Exception as e:
            print(f"Error saving flashcards: {e}")
