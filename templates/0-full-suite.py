#Use this file template to set the path to the project root directory

import os
import sys
import threading
from datetime import datetime
from pynput.keyboard import Key

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
# Walker Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def walker(gui):
    """Loop that performs clicks at a fixed interval while running is True."""
    try:
        while gui.running:
            sleep(5)
            print("Starting Sequence")
            gui.walk_count += 1
            print("Completed Sequence", gui.walk_count, "times")
            gui.append_message(f"Completed Sequence {gui.walk_count} times")

            # Check if we've reached max walks
            try:
                max_walks = int(gui.max_walks_entry.get())
                if gui.walk_count >= max_walks:
                    gui.running = False
                    gui.append_message(f"Reached maximum walks ({max_walks}). Stopping bot.")
                    break
            except ValueError:
                gui.append_message("Invalid max walks value. Using default.")

    except Exception as e:
        gui.append_message(f"Error in walker: {e}")
        gui.running = False

# Warning holding left CTRL turning the progran on and off can crash the program
# Warning holding right CTRL will exit the program
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    """Main function to start the bot with GUI."""
    # Create GUI instance with bot name and walker function
    gui = BaseGUI(bot_name="HashSlayer's Template Bot", bot_function=walker)
    # Start the GUI
    gui.run()

if __name__ == "__main__":
    main()
