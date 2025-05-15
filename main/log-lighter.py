#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from datetime import datetime

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.core.timing import *
from utils.core.welcome import welcome
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.base_gui import BaseGUI

welcome()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Fire Burner Bot
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class FireBurnerGUI(BaseGUI):
    """Custom GUI for Fire Burner with unique theme"""
    def __init__(self, bot_name="Fire Burner", bot_function=None):
        # Initialize parent class
        super().__init__(bot_name=bot_name, bot_function=bot_function)
        
        # Override colors for a fire-themed look
        self.text_box_bg = "#FFEBCD"  # Blanched Almond
        self.text_box_fg = "#8B4513"  # Saddle Brown
        
        # Update text box colors
        self.text_box.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                              insertbackground=self.text_box_fg)
        self.notepad.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                             insertbackground=self.text_box_fg)
        self.max_walks_entry.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                                     insertbackground=self.text_box_fg)

def burn_logs(gui):
    """Main fire burning loop with human-like behavior"""
    try:
        while gui.running:
            sleep(1, 1)
            gui.append_message("Starting Fire Burning Sequence")
            
            # Click bank
            bezier_between(1166, 1252, 498, 572)
            sleep(.5, 2)
            click()
            sleep()
            if rnd.random() > 0.813:
                sleep(0, 3)

            # Get logs
            bank_slot(8)
            sleep()
            get_x_items()
            sleep()
            click()
            sleep(1, 1)
            if rnd.random() > 0.813:
                sleep(0, 3)

            # Light fire
            bezier_between(935, 955, 808, 869)
            sleep(0.5, 1)
            click()
            sleep(2, 2)
            spacekey()
            if rnd.random() > 0.7:
                sleep(0, 1)
                spacekey()
                if rnd.random() > 0.3:
                    sleep()
                    spacekey()

            # Wait for fire to burn out
            sleep(60, 9)

            sleep()
            if rnd.random() > 0.9:
                sleep(0, 10)

            # Update progress
            gui.walk_count += 1
            gui.append_message(f"Completed Sequence {gui.walk_count} times")

            # Check if we've reached max walks
            try:
                max_walks = int(gui.max_walks_entry.get())
                if gui.walk_count >= max_walks:
                    gui.running = False
                    gui.append_message(f"Reached maximum fires ({max_walks}). Stopping bot.")
                    break
            except ValueError:
                gui.append_message("Invalid max fires value. Using default.")

    except Exception as e:
        gui.append_message(f"Error in fire burning loop: {e}")
        gui.running = False

def main():
    """Main function to start the bot with GUI."""
    # Create GUI instance with bot name and walker function
    gui = FireBurnerGUI(bot_name="HashSlayer's Fire Burner", bot_function=burn_logs)
    # Start the GUI
    gui.run()

if __name__ == "__main__":
    main()
