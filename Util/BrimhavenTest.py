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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Walker Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def walker():
    """Loop that performs clicks at a fixed interval while running is True."""
    global running
    while True:
        with running_lock:
            if not running:
                break

        bezier_between(500, 590, 533, 633, .5)
        sleep(.8, 1)
        print("Clicking Left")
        click()
        if rnd.random() < 0.69:
            click()
            if rnd.random() < 0.539:
                click()
                if rnd.random() < 0.75:
                    click()
                    if rnd.random() < 0.92:
                        click()
        sleep(.8, 1)

        bezier_between(1280, 1387, 570, 654, .5)
        sleep(.8, 1)
        print("Clicking Right")
        click()
        if rnd.random() < 0.69:
            click()
            if rnd.random() < 0.539:
                click()
                if rnd.random() < 0.75:
                    click()
                    if rnd.random() < 0.92:
                        click()
        sleep(.8, 1)

        if rnd.random() > 0.991:
            sleep(.1, 5)
            print("Small Sleep")    
            if rnd.random() > 0.991:
                sleep(1, 30)
                print("Big Sleep")

        if rnd.random() > 0.999:
            sleep(1, 300)


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
