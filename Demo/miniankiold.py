
import json
import time
import os
from MiniAnki.Constants import *
from MiniAnki.Flashcard import Flashcard
from MiniAnki.Hardware import setup_sd_card
from MiniAnki.Display import ConsoleDisplay
from MiniAnki.EInkDisplay import EInkDisplay
from MiniAnki.ButtonManager import ButtonManager

class MiniAnki:
    def __init__(self, flashcards_path=FLASHCARDS_PATH, use_eink=True, use_buttons=True):
        """Initialize MiniAnki system"""
        FLASHCARDS_PATH = flashcards_path
        self.cards = []
        self.last_shown_card_time = 0
        self.use_eink = use_eink
        self.use_buttons = use_buttons
        
        # Setup hardware
        self._setup_hardware()
        
        # Load flashcards
        self.load_cards()
        
        print("MiniAnki initialized")
    
    def _setup_hardware(self):
        """Setup all hardware components"""
        # Mount SD card for file access
        setup_sd_card()
        
        # Initialize display (e-ink or console)
        if self.use_eink:
            print("Setting up e-ink display...")
            self.display = EInkDisplay()
            
            # Fall back to console if display init failed
            if not hasattr(self.display, 'display') or self.display.display is None:
                print("Falling back to console display")
                self.display = ConsoleDisplay()
                self.use_eink = False
        else:
            self.display = ConsoleDisplay()
        
        # Setup buttons if needed
        if self.use_buttons:
            print("Setting up buttons...")
            self.button_manager = ButtonManager()
        else:
            self.button_manager = None

    def load_cards(self):
        """Load flashcards from JSON file"""
        try:
            if not os.path.exists(FLASHCARDS_PATH):
                print(f"Warning: Flashcards file not found at {FLASHCARDS_PATH}")
                self.cards = []
                return
                
            with open(FLASHCARDS_PATH, "r") as f:
                data = json.load(f)
                self.cards = [Flashcard(**card) for card in data]
                print(f"Loaded {len(self.cards)} flashcards")
                
        except Exception as e:
            print(f"Error loading flashcards: {e}")
            self.cards = []

    def save_cards(self):
        """Save flashcards to JSON file"""
        try:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(FLASHCARDS_PATH), exist_ok=True)
            
            with open(FLASHCARDS_PATH, "w") as f:
                json.dump([card.to_dict() for card in self.cards], f, indent=2)
            print(f"Saved {len(self.cards)} flashcards")
            
        except Exception as e:
            print(f"Error saving flashcards: {e}")

    def reset_cards(self):
        """Reset all cards to initial state"""
        print("Resetting all flashcards...")
        for card in self.cards:
            card.last_review = None
            card.interval = MIN_INTERVAL
            card.review_count = 0
        
        self.last_shown_card_time = 0
        self.save_cards()
        print("All cards have been reset")
    
    def get_next_card(self):
        """Get the next card due for review based on simplified spaced repetition"""
        current_time = time.monotonic()
        
        # Check if minimum time has passed since last card was shown
        if current_time - self.last_shown_card_time < MIN_SHOW_INTERVAL:
            return None
            
        # Get cards that are due for review
        due_cards = [
            card for card in self.cards
            if card.last_review is None or 
            current_time - card.last_review >= card.interval
        ]
        
        if not due_cards:
            print("No cards due for review")
            return None
            
        # Find the most overdue card
        most_overdue_card = None
        highest_overdue_factor = 0
        
        for card in due_cards:
            if card.last_review is None:
                # New cards have highest priority
                overdue_factor = 10.0
            else:
                # Calculate how overdue the card is as a ratio
                overdue_factor = (current_time - card.last_review) / card.interval
                
            if overdue_factor > highest_overdue_factor:
                highest_overdue_factor = overdue_factor
                most_overdue_card = card
        
        if most_overdue_card:
            print(f"Selected card: {most_overdue_card.hanzi} (Overdue factor: {highest_overdue_factor:.2f})")
        
        return most_overdue_card

    def process_response(self, card, quality):
        """Process response quality (1=Easy, 2=Medium, 3=Hard)"""
        # Simplified multipliers
        multipliers = {
            RESPONSE_EASY: 2.0,    # Double interval for easy
            RESPONSE_MEDIUM: 1.3,  # Slightly increase for medium
            RESPONSE_HARD: 0.5     # Halve interval for hard
        }

        # Calculate old interval for logging
        old_interval = card.interval

        # Update interval based on response quality
        if card.review_count == 0:
            # First review, set base interval
            card.interval = MIN_INTERVAL
        else:
            # Adjust interval based on response quality
            card.interval = min(
                MAX_INTERVAL,
                int(card.interval * multipliers[quality])
            )
        
        # Update card stats
        card.last_review = time.monotonic()
        card.review_count += 1
        self.last_shown_card_time = time.monotonic()
        
        # Log the change
        print(f"Card: {card.hanzi}, Response: {quality}, Interval: {old_interval}s → {card.interval}s")
        
        # Save changes
        self.save_cards()
        return card

    def show_card_and_get_response(self, card):
        """Show card and get response using buttons or console input"""
        # Show question
        if self.use_eink:
            # Try to show card, if it fails (due to cooldown) return None
            if not self.display.show_card(card, show_answer=False):
                return None
        else:
            self.display.show_card(card, show_answer=False)
        
        # Wait for user to request answer
        if self.use_buttons and self.button_manager:
            # Wait for any button press to show answer
            print("Press any button to see answer...")
            self.button_manager.wait_for_any_button()
        else:
            # Console mode - wait for Enter key
            print("Press Enter to see answer...")
            input()
            
        # Show answer
        if self.use_eink:
            # Try to show answer, if it fails (due to cooldown) return None
            if not self.display.show_card(card, show_answer=True):
                return None
        else:
            self.display.show_card(card, show_answer=True)
        
        # Get response based on available input methods
        if self.use_buttons and self.button_manager:
            # Use buttons for response
            print("Rate your response:")
            print("1: Easy (Left button)")
            print("2: Medium (Middle button)")
            print("3: Hard (Right button)")
            return self.button_manager.wait_for_response()
        else:
            # Console mode - prompt for response
            if hasattr(self.display, 'show_input_prompt'):
                self.display.show_input_prompt()
                
            try:
                response = input("Rate your response (1-3): ").strip()
                quality = int(response) if response else DEFAULT_RESPONSE
                if quality not in [RESPONSE_EASY, RESPONSE_MEDIUM, RESPONSE_HARD]:
                    quality = DEFAULT_RESPONSE
                return quality
            except ValueError:
                return DEFAULT_RESPONSE
    
    def cleanup(self):
        """Clean up resources before exit"""
        print("Cleaning up...")
        
        # Save card data
        self.save_cards()
        
        # Clean up display
        if hasattr(self.display, 'cleanup'):
            self.display.cleanup()
            
        # Clean up buttons
        if self.button_manager and hasattr(self.button_manager, 'cleanup'):
            self.button_manager.cleanup()