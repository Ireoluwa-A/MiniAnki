"""
Main module for MiniAnki flashcard application
"""

import time
from MiniAnki.MiniAnki import MiniAnki
from MiniAnki.MotionManager import MotionManager

def main():
    motion = MotionManager()
    anki = MiniAnki()
    anki.reset_cards()
    print("Ready! Waiting for motion...")
    try:
        while True:
            if motion.update():
                card = anki.get_next_card()
                if card:
                    print("Showing card...")
                    quality = anki.show_card_and_get_response(card)
                    if quality is not None:
                        card = anki.process_response(card, quality)
            else: 
                anki.last_shown_card_time = time.monotonic()
            time.sleep(0.1)

    except Exception as e:
        print(f"Exception: {str(e)}")
        print("\nSaving and exiting...")
        anki.save_cards()
        motion.cleanup()

if __name__ == "__main__":
    main()