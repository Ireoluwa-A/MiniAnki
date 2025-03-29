class ConsoleDisplay:
    def __init__(self):
        pass

    def show_card(self, card, show_answer=False):
        if show_answer:
            print("\n=== Answer ===")
            print(str(card))
            print(f"Part of Speech: {card.part_of_speech}")
            if card.example:
                print(f"Example: {card.example}")
        else:
            print("\n=== Question ===")
            print(f"Hanzi: {card.hanzi}")

    def show_input_prompt(self):
        print("\nRate your response (1-3):")
        print("1: Easy")
        print("2: Medium")
        print("3: Hard")
