"""
Main module for MiniAnki flashcard application
Handles main application loop and integrates all components
"""

from MiniAnki.MiniAnki import MiniAnki
from Utils.Constants import *
import time

def main():
    """Main application loop"""
    print("\n----- MiniAnki Starting -----\n")
    
    mini_anki = MiniAnki()
    
    print("\n----- System Ready -----\n")
    
    try:
        # Main loop
        while True:
            # Get the next card to show
            print("\nChecking for due cards...")
            card = mini_anki.get_next_card()

            if card:
                # Wait before showing the card and preload card
                mini_anki.wait_for_random_interval(card)

                print(f"Showing card: {card.hanzi}")
                # mini_anki.show_card(card)

                # print(f"Waiting for button press to reveal answer...")
                # mini_anki.wait_for_any_button()

                print(f"Revealing Card: {card.pinyin}")
                mini_anki.reveal_card(card)
                
                print(f"Waiting for Response...")
                response = mini_anki.wait_for_response()

                print(f"Processing response: {response}")
                mini_anki.process_response(card, response)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nUser interrupted - exiting")
    except Exception as e:
        print(f"\n\nError in main loop: {str(e)}")
    finally:
        # Cleanup and exit
        print("\nCleaning up before exit...")
        mini_anki.cleanup()
        print("\n----- MiniAnki Shutdown Complete -----")
        
main()