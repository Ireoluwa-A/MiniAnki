from Utils.Constants import *
import time
import json
import time
import os

class MiniAnkiCore:

    def get_next_card(self):
        """Get the next card due for review"""
        current_time = time.monotonic()
        
        if current_time - self.last_shown < MIN_SHOW_INTERVAL:
            return None
            
        due_cards = [
            card for card in self.cards
            if card.last_review is None or 
            current_time - card.last_review >= card.interval
        ]
        
        if not due_cards:
            print("No cards due for review")
            return None
            
        most_overdue_card = None
        highest_overdue_factor = 0
        
        for card in due_cards:
            overdue_factor = (10.0 if card.last_review is None else 
                             (current_time - card.last_review) / card.interval)
            
            if overdue_factor > highest_overdue_factor:
                highest_overdue_factor = overdue_factor
                most_overdue_card = card
        
        if most_overdue_card:
            print(f"Selected card: {most_overdue_card.hanzi} (Overdue factor: {highest_overdue_factor:.2f})")
        
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
        self.last_shown = time.monotonic()
        
        print(f"Card: {card.hanzi}, Response: {response}, Interval: {old_interval}s → {card.interval}s")
        self.save_cards()
        return card
