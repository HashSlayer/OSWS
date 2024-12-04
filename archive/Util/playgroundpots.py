import threading
import time
import pyautogui as pag
import random as rnd
from pynput import keyboard

from ItemSlots import *
from MainFunctions import *
from MouseMovement import *
from Welcome import *

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
        print("Starting Blowpipe Sequence")
        bank_near_inv()
        sleep()
        click()
        sleep(1, 2)

        deposit_all()
        if rnd.random() > 0.713:
            sleep(0,1)
        sleep()
        click()
        if rnd.random() > 0.678114:
            click()
            if rnd.random() > 0.83:
                click()
        if rnd.random() > 0.7:
            sleep(0,1)
        sleep()

        bank_slot(7)
        if rnd.random() > 0.727:
            sleep(0,1)
        click()
        sleep()

        bank_slot(8)
        get_x_items()
        sleep()
        click()
        if rnd.random() > 0.97:
            sleep()
        sleep()

        exit_bank()
        sleep(.7, .5)
        click()
        sleep(.5, 1)

        if rnd.random() > 0.9:
            sleep(0,3)

        inv_slot(1)
        sleep()
        click()
        sleep()

        if rnd.random() > 0.867:
            inv_slot(2)
            sleep()
            click()
            sleep()
        else:
            inv_slot(5)
            sleep()
            click()
            sleep()

        sleep(0.7, 1)
        spacekey()
        if rnd.random() > 0.7:
            spacekey()
        sleep(44, 7, 3)
        print("Ending Blowpipe Sequence")
        if rnd.random() > 0.2:
            sleep(0, 2)
            if rnd.random() > 0.9:
                sleep(.1, 8)
                print("Lets wait a bit")

        loops += 1
        print("Loop:", loops)

        if rnd.random() > 0.991:
            sleep(4, 13)
            print("Small Sleep")    
            if rnd.random() > 0.991:
                sleep(10, 120)
                print("Big Sleep")

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
