#Use this file template to set the path to the project root directory

import os
import sys
import threading
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
from utils.gui.confetti import *
from utils.gui.base_bot_gui import BaseBotGUI

welcome()

# Global variables to control the clicker state
running = False
running_lock = threading.Lock()

# Define control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r   # Right Control key for kill

loops = 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Walker Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def walker(gui):
    """Loop that performs clicks at a fixed interval while running is True."""
    loops = 0
    while gui.running:
        sleep(5)
        print("Starting Sequence")
        loops += 1
        print("Completed Sequence", loops, "times")
        gui.update_iterations(loops)  # Update iteration count in GUI

# Warning holding left CTRL turning the progran on and off can crash the program
# Warning holding right CTRL will exit the program
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def toggle_program():
    """Toggle the running state and start/stop the program."""
    global running
    with running_lock:
        running = not running
        if running:
            threading.Thread(target=walker, daemon=True).start()
        print("Program running" if running else "Program stopped")

def exit_program():
    """Exit the program by setting running to False and printing a message."""
    global running
    with running_lock:
        running = False
    print("Exiting program")
    exit(0)

def on_press(key):
    """Handle key press events to toggle the clicker or exit the program."""
    if key == ONOFF:
        toggle_program()
    elif key == KILL:
        exit_program()

def main():
    """Main function to start the bot with GUI."""
    # Create GUI instance with bot name and walker function
    gui = BaseBotGUI(bot_name="HashSlayer's Template Bot", bot_function=walker)
    # Start the GUI
    gui.run()

if __name__ == "__main__":
    main()
