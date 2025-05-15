#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from pynput.keyboard import Listener, Key
from datetime import datetime
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root to the Python path
sys.path.insert(0, project_root)
#import other relevant modules here:
#from Utilities.timmy import *
from utils.core.timing import *
from utils.core.welcome import welcome
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.base_gui import BaseGUI

welcome()

# Global variables to control the bot state
running = False
running_lock = threading.Lock()
bot_thread = None  # Track the bot thread globally
loops = 0  # Keep track of loops in the bot logic

class SmitherGUI(BaseGUI):
    def __init__(self):
        super().__init__(bot_name="Smither Bot", bot_function=self.walker)
        
    def walker(self, gui):
        """Loop that performs clicks at a fixed interval while running is True."""
        global loops
        while True:
            if not self.running:
                break

            sleep(1, 1)
            gui.append_message("Starting Smithing Sequence")
            bezier_between(886, 893, 281, 289) #clicking on the bank is slightly off
            sleep(.5, 2)
            click()
            sleep()
            if rnd.random() > 0.843:
                sleep(0,3)

            sleep(4, 3)
            if rnd.random() > 0.913:
                Notbotting()

            bank_slot(8)
            sleep()
            get_x_items()
            sleep()
            click()
            sleep(.1,1)
            if rnd.random() > 0.97:
                sleep(0,30)
            if rnd.random() > 0.813:
                sleep(0,3)

            bezier_between(1065, 1075, 894, 910)
            sleep(0.2, 1)
            click()
            sleep(3.9, 2.5)
            if rnd.random() > 0.9813:
                Notbotting()

            spacekey()
            sleep(.413, 0.5)
            spacekey()

            if rnd.random() > 0.7:
                sleep(0,1)
                spacekey()
                if rnd.random() > 0.93:
                    sleep()
                    spacekey()

            Notbotting()
            sleep(65, 9, 7)
            if rnd.random() > 0.813:
                sleep(0,18)

            if rnd.random() > 0.93:
                sleep(0,30)
                if rnd.random() > 0.911:
                    sleep(10, 130, 180)
                    gui.append_message("Taking a bigger sleep...")

            if loops > 30 and rnd.random() > 0.9891:
                sleep(10, 60, 120)
                gui.append_message("Taking the biggest sleep...")

            loops += 1
            # Update both the bot's loop count and the GUI's walk count
            self.walk_count = loops  # Keep GUI in sync with bot state
            gui.append_message(f"Completed Sequence {loops} times")

            # Check if we've reached max walks
            try:
                max_walks = int(self.max_walks_entry.get())
                if loops >= max_walks:
                    gui.append_message(f"Reached maximum walks ({max_walks}). Stopping bot.")
                    self.running = False
                    break
            except ValueError:
                pass  # Invalid max walks value, continue running

def main():
    """Main function to start the GUI."""
    gui = SmitherGUI()
    gui.run()

if __name__ == "__main__":
    main()
