import json
import time
import random
from MiniAnki.Constants import *
from MiniAnki.Flashcard import Flashcard
from MiniAnki.Hardware import *
from MiniAnki.Display import ConsoleDisplay

class MiniAnki:
    def __init__(self, flashcards_path=FLASHCARDS_PATH):
        self.flashcards_path = flashcards_path
        self.cards = []
        self.last_shown = 0
        self.display = ConsoleDisplay()
        setup_sd_card()
        self.load_cards()

    def load_cards(self):
        try:
            with open(self.flashcards_path, "r") as f:
                data = json.load(f)
                self.cards = [Flashcard(**card) for card in data]
                print(f"Loaded {len(self.cards)} flashcards")
        except Exception as e:
            print(f"Error loading flashcards: {e}")
            self.cards = []


    def save_cards(self):
        with open(self.flashcards_path, "w") as f:
            json.dump([card.to_dict() for card in self.cards], f)

    def reset_cards(self):
        # reset the last review property to null on all cards
        print("Resetting cards...")
        for card in self.cards:
            card.last_review = None
            card.interval = MIN_INTERVAL
            card.review_count = 0
        self.last_shown = 0
    
    def get_next_card(self):
        '''Get the next card due for review based on spaced repetition
        Will choose a random time between MIN_SHOW_INTERVAL AND MAX_SHOW_INTERVAL
        to show the next card, weighted by how overdue they are
        '''
        current_time = time.monotonic()
        print(f"Current time: {current_time}")
        print(f"Last shown: {self.last_shown}")
        if current_time - self.last_shown < MIN_SHOW_INTERVAL:
            print("Not yet time to show card...")
            return None

        due_cards = [
            card for card in self.cards
            if card.last_review is None or 
            current_time - card.last_review >= card.interval
        ]
        
        if not due_cards:
            print("No cards due for review...")
            for card in self.cards:
                print(card.last_review)
                print("")
            return None
        
        # Soft randomness, probability of showing card increases as time goes on
        time_factor = (current_time - self.last_shown - MIN_SHOW_INTERVAL) / (MAX_SHOW_INTERVAL - MIN_SHOW_INTERVAL)
        if random.random() > time_factor:
            print("Skipping card...")
            return None

        # Calculate overdue factors
        overdue_factors = []
        for card in due_cards:
            if card.last_review is None:
                overdue_factors.append(10.0)  # High weight for new cards
            else:
                factor = (current_time - card.last_review) / card.interval
                overdue_factors.append(min(factor, 10.0))  # Cap at 10x
        
        # Use overdue factors as probability weights
        total_weight = sum(overdue_factors)
        r = random.random() * total_weight
        
        cumulative_weight = 0
        for i, weight in enumerate(overdue_factors):
            cumulative_weight += weight
            if r <= cumulative_weight:
                print(f"Showing card {i+1}/{len(due_cards)}...")
                print("last shown is now", self.last_shown)
                return due_cards[i]
            
        print("Error selecting card...")
        return due_cards[-1]  # Fallback to last card if something goes wrong

    def process_response(self, card, quality):
        """Process response quality (1=Easy, 2=Medium, 3=Hard)"""
        multipliers = {
            RESPONSE_EASY: 2.5, 
            RESPONSE_MEDIUM: 1.5, 
            RESPONSE_HARD: 0.8
        }

        # Update card interval based on response quality
        # if we've never seen the card before, set interval to MIN_INTERVAL
        # otherwise, multiply the interval by the quality multiplier
        if card.review_count == 0:
            card.interval = MIN_INTERVAL
        else:
            card.interval = min(
                MAX_INTERVAL,
                int(card.interval * multipliers[quality])
            )
        
        card.last_review = time.monotonic()
        card.review_count += 1
        self.last_shown = time.monotonic()
        
        self.save_cards()
        return card

    def _get_user_response(self):
        """Get user response with timeout using supervisor for CircuitPython"""
        start_time = time.monotonic()
        
        while time.monotonic() - start_time < RESPONSE_TIMEOUT:
            if supervisor.runtime.serial_bytes_available:
                byte = input().strip().lower()
                return byte if byte else None
            time.sleep(0.1)
        
        print("Response timeout")
        return None

    def show_card_and_get_response(self, card):
        """Show card, wait for user to see answer, then get response"""
        # Show question
        self.display.show_card(card, show_answer=False)
        
        # Wait for user to request answer
        print("Press Enter to see answer...")
        response = self._get_user_response()
        if response is None:
            return DEFAULT_RESPONSE
        
        # Show answer
        self.display.show_card(card, show_answer=True)
        
        # Get response
        self.display.show_input_prompt()
        response = self._get_user_response()
        
        # Parse response
        try:
            quality = int(response) if response else DEFAULT_RESPONSE
            if quality not in [RESPONSE_EASY, RESPONSE_MEDIUM, RESPONSE_HARD]:
                quality = DEFAULT_RESPONSE
        except ValueError:
            quality = DEFAULT_RESPONSE
            
        return quality
