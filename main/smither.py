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


def walker():
    """Loop that performs clicks at a fixed interval while running is True."""
    global running
    global loops
    while True:
        with running_lock:
            if not running:
                break

        sleep(1, 1)
        print("Starting Smithing Sequence")
        bezier_between(886, 893, 281, 289) #clicking on the bank is slightly off
        sleep(.5, 2)
        click()
        sleep()
        if rnd.random() > 0.843:
            sleep(0,3)

        sleep(4, 3)
        #deposit_all()
        #sleep()
        #click()
        #sleep(0.1, 1) 
        if rnd.random() > 0.913:
            Notbotting()

        #bank_slot(7)
        #sleep()
        #click()
        #if rnd.random() > 0.913:
        #    Notbotting()
        #sleep()
        #if rnd.random() > 0.813:
        #    sleep(0,3)

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
                print("Bigger Sleep")
        if loops > 30 and rnd.random() > 0.9891:
            sleep(10, 60, 120)
            print("Biggest Sleep")

        loops += 1
        print("Completed Sequence", loops, "times")


#zoomed out by 4 pixels 

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
    """Main function to start the keyboard listener."""
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
