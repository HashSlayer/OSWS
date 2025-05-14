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
walker_thread = None

loops = 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Walker Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def walker():
    global running  # Declare running as global at the start of the function
    
    rock_slot = 1  # Easy to adjust which slot is clicked every minute
    last_rock_time = 0  # Track last time rock slot was clicked
    last_potion_time = 0  # Track last time potions were sipped
    
    # Overload tracking
    current_overload_slot = 2  # Track which overload slot we're using (1-6)
    overload_sip_count = 0  # Track how many sips from current slot
    true_overload_sip_count = 0
    
    # Absorption tracking
    current_absorption_slot = 9  # Track which absorption slot we're using (9-28)
    absorption_sip_count = 0  # Track how many sips from current slot
    
    while True:
        if not running:
            break
            
        current_time = time.time()
    
            
        # Handle potion sips (every 5 minutes)
        if current_time - last_potion_time >= 300:
            # Take overload sip
            print(f"Taking overload sip from slot {current_overload_slot}")
            sleep(true_overload_sip_count * 2, rnd.random() * 1)
            inv_slot(current_overload_slot)
            click()  # Perform a click after moving to the overload slot
            sleep(4, 2)  # Small delay between potions

                        # Update overload slot counter
            overload_sip_count += 1
            true_overload_sip_count += 1
            if overload_sip_count >= 4:
                current_overload_slot += 1
                overload_sip_count = 0
                if current_overload_slot > 6:
                    current_overload_slot = 1
            
            # Take absorption sip (twice with a 2-second rest in between)
            print(f"Taking first absorption sip from slot {current_absorption_slot}")
            inv_slot(current_absorption_slot)
            sleep(.5, 1)
            click()  # Perform a click after moving to the absorption slot
            sleep(.5, 2)  # Rest at least 2 seconds before the second sip
            
            # Update absorption slot counter
            absorption_sip_count += 1
            if absorption_sip_count >= 4:
                current_absorption_slot += 1
                absorption_sip_count = 0
                if current_absorption_slot > 28:
                    current_absorption_slot = 9

            print(f"Taking second absorption sip from slot {current_absorption_slot}")
            inv_slot(current_absorption_slot)
            sleep(.5, 1)
            click()  # Perform a click after moving to the absorption slot
            
            last_potion_time = current_time
            
            # Update absorption slot counter
            absorption_sip_count += 1
            if absorption_sip_count >= 4:
                current_absorption_slot += 1
                absorption_sip_count = 0
                if current_absorption_slot > 28:
                    current_absorption_slot = 9

                    # Handle rock slot (every minute)
        if current_time - last_rock_time >= 60:  # Changed from 60 to 30 seconds for more frequent rock cake usage
            print(f"Pressing inventory slot {rock_slot}")
            sleep(1.5, 2)  # Reduced random delay for more consistent timing
            inv_slot(rock_slot)
            click()  # Perform a click after moving to the rock slot
            last_rock_time = current_time
            sleep(0.5, 1)  # Reduced delay for better responsiveness
            if rnd.random() < 0.8:  # Increased probability of second click
                sleep(0.5, 1)
                click()
            
            sleep(0.5, 1)  # Reduced delay after rock cake usage
            
        sleep(0.1)  # Small sleep to prevent excessive CPU usage

# Warning holding left CTRL turning the progran on and off can crash the program
# Warning holding right CTRL will exit the program
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def toggle_program():
    """Toggle the running state and start/stop the program."""
    global running, walker_thread
    with running_lock:
        running = not running
        if running:
            if walker_thread is None or not walker_thread.is_alive():
                walker_thread = threading.Thread(target=walker, daemon=True)
                walker_thread.start()
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
    if key == Key.ctrl_l:
        toggle_program()
    elif key == Key.ctrl_r:
        exit_program()

def main():
    """Main function to start the keyboard listener."""
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
