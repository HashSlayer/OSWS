#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from pynput.keyboard import Listener, Key
from datetime import datetime

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.core.timing import *
from utils.core.welcome import welcome
from utils.movements import *
from utils.clicker import *

# Display welcome message
welcome()

# Global variables to control the bot state
running = False
running_lock = threading.Lock()
bot_thread = None

# Define control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r   # Right Control key for kill

loops = 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Bot Program - This is where you write your automation logic!
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def bot_function():
    """Your main bot logic goes here."""
    global loops
    
    while True:
        if not running:
            break
            
        try:
            # Example: Move to a position and click
            print("Starting sequence...")
            
            # Move the mouse (using bezier curves for smooth movement)
            bezierMove(500, 500)  # Move to center of screen
            sleep(2, 0.2)  # Random sleep between 0.3-0.5 seconds
            bezierMove(800, 400)  # Move to center of screen
            # Perform a click
            sleep(0.5, 0.2)  # Another random sleep
            
            # Count the loop
            loops += 1
            print(f"Completed sequence {loops} times")
            
            # Add some randomness (5% chance of a longer break)
            if rnd.random() > 0.95:
                print("Taking a short break...")
                sleep(1, 3)
                
        except Exception as e:
            print(f"Error: {e}")
            sleep(1)  # Wait before retrying

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Program - Don't change this unless you know what you're doing!
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def toggle_program():
    """Toggle the running state and start/stop the program."""
    global running, bot_thread
    with running_lock:
        running = not running
        if running:
            if bot_thread is None or not bot_thread.is_alive():
                bot_thread = threading.Thread(target=bot_function, daemon=True)
                bot_thread.start()
            print("Bot started")
        else:
            print("Bot stopped")

def exit_program():
    """Exit the program cleanly."""
    global running
    with running_lock:
        running = False
    print("Exiting program")
    exit(0)

def on_press(key):
    """Handle key press events to toggle the bot or exit."""
    if key == ONOFF:
        toggle_program()
    elif key == KILL:
        exit_program()

def main():
    """Main function to start the program."""
    print("❤️ Press LEFT CTRL to toggle the bot ON/OFF")
    print("❤️ Press RIGHT CTRL to exit")
    
    # Start listening for keyboard events
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main() 