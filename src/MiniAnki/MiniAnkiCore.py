from Utils.Constants import *
import time
import random

class MiniAnkiCore:

    def get_next_card(self):
        """Get the next card due for review"""
        current_time = time.monotonic()
        
        # Find cards that are due for review
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
            overdue_factor = (10.0 if card.last_review is None else 
                             (current_time - card.last_review) / card.interval)
            
            if overdue_factor > highest_overdue_factor:
                highest_overdue_factor = overdue_factor
                most_overdue_card = card
        
        return most_overdue_card

    def show_card(self, card):
        """Show the card on the display"""
        self.eink.show_card(card, show_answer=False)
        
    def reveal_card(self, card):
        """Reveal the answer on the display"""
        self.eink.show_card(card, show_answer=True)

    def wait_for_response(self):
        """Wait for user response using buttons"""
        return self.button_manager.wait_for_response()

    def process_response(self, card, response):
        """Process response quality (1=Easy, 2=Medium, 3=Hard)"""
        multipliers = {
            RESPONSE_EASY: 2.0,
            RESPONSE_MEDIUM: 1.3,
            RESPONSE_HARD: 0.5
        }

        old_interval = card.interval

        if card.review_count == 0:
            card.interval = MIN_INTERVAL
        else:
            card.interval = min(MAX_INTERVAL, int(card.interval * multipliers[response]))
        
        card.last_review = time.monotonic()
        card.review_count += 1
        self.last_shown_card_time = time.monotonic()
        
        print(f"Card: {card.hanzi}, Response: {response}, Interval: {old_interval}s → {card.interval}s")
        self.save_cards()
        return card

    def wait_for_next_card(self):
        """
        Wait a random time between MIN_SHOW_INTERVAL_SEC and MAX_SHOW_INTERVAL_SEC
        before showing the next card. Returns immediately if any button is pressed.
        
        Returns:
            bool: True if wait completed normally, False if interrupted by button press
        """
        # Calculate a random wait interval
        wait_interval = random.randint(MIN_SHOW_INTERVAL_SEC, MAX_SHOW_INTERVAL_SEC)
        print(f"Waiting {wait_interval} seconds before next card")
        
        # Wait for the interval, but check for button presses to skip wait
        wait_start = time.monotonic()
        while time.monotonic() - wait_start < wait_interval:
            # Check if any button is pressed to skip waiting
            if self.button_manager.is_any_button_pressed():
                print("Button pressed - skipping wait")
                return False  # Wait was interrupted
            time.sleep(0.5)  # Short sleep to prevent CPU overuse
        
        return True  # Wait completed normally