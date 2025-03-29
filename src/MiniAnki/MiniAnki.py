"""
Core MiniAnki class to manage flashcards and spaced repetition
"""

from Utils.Constants import *


from Utils.EInkDisplay import EInkDisplay
from Utils.ButtonManager import ButtonManager


from MiniAnki.MiniAnkiSetup import MiniAnkiSetup
from MiniAnki.MiniAnkiCore import MiniAnkiCore

class MiniAnki(MiniAnkiSetup, MiniAnkiCore):
    def __init__(self):
        """Initialize MiniAnki system"""            
        self.eink = EInkDisplay()
        self.button_manager = ButtonManager()

        self.cards = self.load_cards()
        self.last_shown = 0

        self.setup_sd_card()

        print("MiniAnki initialized")

