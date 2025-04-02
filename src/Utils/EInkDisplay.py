"""
E-Ink display handler for MiniAnki
Manages display initialization, refresh timing, and content rendering
"""

import time
import board
import displayio
import busio
import adafruit_ssd1680
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from Utils.Constants import *

class EInkDisplay:
    def __init__(self):
        """Initialize the e-ink display and required hardware"""
        self.display = None
        self.font = None
        self.group = None
        
        # Initialize the display
        self._initialize_display()
        self._load_font()
    
    def _initialize_display(self):
        """Initialize the e-ink display hardware"""
        try:
            displayio.release_displays()
            
            spi_epd = busio.SPI(clock=EINK_SCK_PIN, MOSI=EINK_MOSI_PIN)  
            
            # Create display bus
            display_bus = displayio.FourWire(
                spi_epd, 
                command=EINK_DC_PIN, 
                chip_select=EINK_CS_PIN, 
                reset=EINK_RESET_PIN, 
                baudrate=EINK_BAUDRATE
            )
            
            # Initialize the display
            self.display = adafruit_ssd1680.SSD1680(
                display_bus,
                width=EINK_WIDTH,
                height=EINK_HEIGHT,
                busy_pin=EINK_BUSY_PIN,
                highlight_color=EINK_COLOR,
                rotation=EINK_ROTATION
            )
            
            # Initialize display group
            self.group = displayio.Group()
            self.display.root_group = self.group
            
            print("E-ink display initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing e-ink display: {e}")
            return False
    
    def _load_font(self):
        """Load Chinese font from SD card"""
        try:
            # Assuming SD card is already mounted
            print("Loading font...")
            self.font = bitmap_font.load_font(MANDARIN_FONT_PATH)
            print("Font loaded")
            
        except Exception as e:
            print(f"Error loading font: {e}")
           
            try:
                self.font = bitmap_font.load_font("/fonts/Arial-12.bdf")
                print("Fallback font loaded")
            except:
                print("No font available")
        
    def _clear_display(self):
        """Clear all items from display group"""
        while len(self.group) > 0:
            self.group.pop()
            print("Cleared display group")
    
    def refresh(self):
        """
        Refresh the display using built-in timing with periodic progress updates
        """
        if not self.display:
            return False
        
        total_refresh_time = self.display.time_to_refresh
        print(f"Total refresh time: {total_refresh_time} seconds")
        
        elapsed_time = 0
        while elapsed_time < total_refresh_time:
            time.sleep(1)  # Sleep for 1 second
            elapsed_time += 1
            
            remaining_time = total_refresh_time - elapsed_time
            print(f"Refresh in progress: {elapsed_time} seconds elapsed, {remaining_time} seconds remaining")
        
        # Perform the actual display refresh
        print("Refreshing display...")
        self.display.refresh()
        print("Display refresh complete")
        return True
    
    def create_labels(self, card):
        """Create labels for the flashcard"""
        # Create labels for the card
        question_label = label.Label(
            self.font, 
            text=card.hanzi, 
            color=0xFFFFFF, 
            x=10, 
            y=30, 
            scale=2
        )
        print("question_label created")
        pinyin_label = label.Label(
            self.font, 
            text=card.pinyin, 
            color=0xFFFFFF, 
            x=10, 
            y=60, 
            scale=1
        )
        print("pinyin_label created")
        english_label = label.Label(
            self.font, 
            text=card.english, 
            color=0xFFFFFF, 
            x=10, 
            y=90, 
            scale=1
        )
        print("english_label created")
        return question_label, pinyin_label, english_label
    
    def show_card(self, card, show_answer=False):
        """Show a flashcard on the display"""
        print("E ink show card", card)
        if not self.display or not self.font:
            return False

        # Clear the display
        self._clear_display()
        
        # Create labels for the card
        if not card.question_label or not card.pinyin_label or not card.answer_label:
            question_label, pinyin_label, english_label = self.create_labels(card)
            card.question_label = question_label
            card.pinyin_label = pinyin_label
            card.answer_label = english_label
        else:
            question_label = card.question_label
            pinyin_label = card.pinyin_label
            english_label = card.answer_label
            print("Labels already created")

        if show_answer:
            self.group.append(question_label)
            self.group.append(pinyin_label)
            self.group.append(english_label)
            print("show_answer is True")
        else:
            self.group.append(question_label)
        
        return self.refresh()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self._clear_display()
            if self.display:
                self.display.refresh()
        except:
            pass

    def _show_startup_screen(self):
        """Show initial startup screen"""
        if not self.display or not self.font:
            return False
            
        self._clear_display()
            
        title = label.Label(
            self.font, 
            text="MiniAnki", 
            color=0xFFFFFF, 
            x=80, 
            y=40, 
            scale=2
        )
        
        subtitle = label.Label(
            self.font, 
            text="Ready for learning", 
            color=0xFFFFFF, 
            x=60, 
            y=80, 
            scale=1
        )
        
        self.group.append(title)
        self.group.append(subtitle)
        
        self.refresh()