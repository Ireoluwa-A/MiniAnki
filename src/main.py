"""
Main module for MiniAnki flashcard application
Handles main application loop and integrates all components
"""

from MiniAnki.MiniAnki import MiniAnki
from Utils.Constants import *

def main():
    """Main application loop"""
    print("\n----- MiniAnki Starting -----\n")
    
    mini_anki = MiniAnki()
    
    print("\n----- System Ready -----\n")

    try:
        # Main loop
        while True:

            print("System active - checking for due cards")
            
            card = mini_anki.get_next_card()
            
            # If its time to show a card, show it
            if card:
                # Show card to user
                # Will block until display is ready
                print(f"Showing card: {card.hanzi}")
                mini_anki.show_card(card)

                print(f"Revealing Card: {card.pinyin}")
                mini_anki.reveal_card(card)
                
                print(f"Waiting for Response...")
                response = mini_anki.wait_for_response()

                # Process response
                print(f"Processing response: {response}")
                mini_anki.process_response(card, response)


    except KeyboardInterrupt:
        print("\n\nUser interrupted - exiting")
    except Exception as e:
        print(f"\n\nError in main loop: {str(e)}")
    finally:
        # Cleanup and exit
        print("\nCleaning up before exit...")
        mini_anki.cleanup()
        print("\n----- MiniAnki Shutdown Complete -----")

if __name__ == "__main__":
    main()