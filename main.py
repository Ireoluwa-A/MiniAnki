"""
Main module for MiniAnki flashcard application
"""

import time
from MiniAnki.MiniAnki import MiniAnki

def main():
    anki = MiniAnki()
    anki.reset_cards()
    try:
        while True:
            card = anki.get_next_card()
            if card:
                print("Showing card...")
                quality = anki.show_card_and_get_response(card)
                if quality is not None:
                    card = anki.process_response(card, quality)
            time.sleep(0.1)

    except Exception as e:
        print(f"Exception: {str(e)}")
        print("\nSaving and exiting...")
        anki.save_cards()

if __name__ == "__main__":
    main()