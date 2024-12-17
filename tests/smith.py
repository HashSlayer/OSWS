#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from pynput import keyboard
from datetime import datetime
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root to the Python path
sys.path.insert(0, project_root)
#import other relevant modules here:
#from Utilities.timmy import *
from utilities.timmy import *
from utilities.welcome import *
from utilities.movements import *
from utilities.clicker import *
from utilities.item_slots import *
from utilities.gui.confetti import *

welcome()

# Global variables to control the clicker state
running = False
running_lock = threading.Lock()

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
        if rnd.random() > 0.813:
            sleep(0,3)

        sleep(4, 3)
        deposit_all()
        sleep()
        click()
        sleep(0.1, 1) 
        if rnd.random() > 0.813:
            Notbotting()

        bank_slot(7)
        sleep()
        click()
        if rnd.random() > 0.913:
            Notbotting()
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

        bezier_between(1065, 1075, 894, 910)
        sleep(0.5, 1)
        click()
        Notbotting()
        sleep(4, 2)
        if rnd.random() > 0.813:
            Notbotting()

        spacekey()
        if rnd.random() > 0.7:
            sleep(0,1)
            spacekey()
            if rnd.random() > 0.3:
                sleep()
                spacekey()

        Notbotting()
        sleep(62 , 8)

        sleep()
        if rnd.random() > 0.9:
            sleep(0,10)
        if loops > 100 and rnd.random() > 0.9:
            sleep(0,30, 30)
            print("Bigger Sleep")

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
    if key == keyboard.Key.ctrl_l:
        toggle_program()
    elif key == keyboard.Key.ctrl_r:
        exit_program()

def main():
    """Main function to start the keyboard listener."""
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
