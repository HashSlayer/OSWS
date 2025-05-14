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
from utils.core.welcome import *
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.confetti import *

welcome()
#Fireburner is a script that burns logs at the G.E. 
#First stand in front of the most south eastern banker and light a campfire below your player for this to work.


# Global variables to control the bot state
running = False
running_lock = threading.Lock()
bot_thread = None  # Track the bot thread globally

# Define control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r   # Right Control key for kill

loops = 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Walker Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def walker():
    """Loop that performs clicks at a fixed interval while running is True."""
    global running, loops
    while True:
        with running_lock:
            if not running:
                break

        sleep(1, 1)
        print("Starting Smithing Sequence")
        bezier_between(1166, 1252, 498, 572) #clicking on the bank is slightly off
        sleep(.5, 2)
        click()
        sleep()
        if rnd.random() > 0.813:
            sleep(0,3)

        bank_slot(8)
        sleep()
        get_x_items()
        sleep()
        click()
        sleep(1,1)
        if rnd.random() > 0.813:
            sleep(0,3)

        bezier_between(935, 955, 808, 869)
        sleep(0.5, 1)
        click()
        sleep(2, 2)
        spacekey()
        if rnd.random() > 0.7:
            sleep(0,1)
            spacekey()
            if rnd.random() > 0.3:
                sleep()
                spacekey()

        sleep(60 , 9)

        sleep()
        if rnd.random() > 0.9:
            sleep(0,10)


        loops += 1
        print("Completed Sequence", loops, "times")


#zoomed out by 4 pixels 

# Warning holding left CTRL turning the progran on and off can crash the program
# Warning holding right CTRL will exit the program
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def kill_bot():
    """Properly cleanup and exit the bot."""
    global running, bot_thread
    running = False
    
    # Clean up threads
    if bot_thread and bot_thread.is_alive():
        try:
            bot_thread.join(timeout=1.0)
        except Exception as e:
            print(f"Exception while stopping bot_thread: {e}")
    
    print("Bot killed! Cleaning up...")
    sys.exit(0)

def on_press(key):
    """Handle keyboard events."""
    if key == ONOFF:
        toggle_program()
    elif key == KILL:
        kill_bot()
        return False  # Stop listener

def toggle_program():
    """Toggle the running state and start/stop the program."""
    global running, bot_thread
    with running_lock:
        running = not running
        if running:
            if bot_thread is None or not bot_thread.is_alive():
                bot_thread = threading.Thread(target=walker, daemon=True)
                bot_thread.start()
            print("Bot started")
        else:
            print("Bot stopped")

def main():
    """Main function to start the keyboard listener."""
    # Start listener in daemon mode for clean exit
    listener = Listener(on_press=on_press, daemon=True)
    listener.start()
    try:
        listener.join()
    except KeyboardInterrupt:
        kill_bot()

if __name__ == "__main__":
    main()
