#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from pynput.keyboard import Listener, Key
from datetime import datetime
import tkinter as tk
from tkinter import ttk
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

# Define control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r   # Right Control key for kill

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
    if key == ONOFF:
        toggle_program()
    elif key == KILL:
        exit_program()

class NMZGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NMZ Helper")
        self.root.geometry("400x300")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status indicator
        self.status_var = tk.StringVar(value="Status: Stopped")
        self.status_label = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            font=("Arial", 12, "bold")
        )
        self.status_label.grid(row=0, column=0, pady=10)
        
        # Configuration frame
        self.config_frame = ttk.LabelFrame(self.main_frame, text="Configuration", padding="5")
        self.config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Rock cake slot
        ttk.Label(self.config_frame, text="Rock Cake Slot:").grid(row=0, column=0, padx=5)
        self.rock_slot_var = tk.StringVar(value="1")
        self.rock_slot_entry = ttk.Entry(
            self.config_frame, 
            textvariable=self.rock_slot_var,
            width=5
        )
        self.rock_slot_entry.grid(row=0, column=1, padx=5)
        
        # Control buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, pady=20)
        
        self.start_button = ttk.Button(
            self.button_frame,
            text="Start (Left Ctrl)",
            command=self.toggle_program
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(
            self.button_frame,
            text="Exit (Right Ctrl)",
            command=self.exit_program
        )
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Stats frame
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Statistics", padding="5")
        self.stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Runtime
        self.runtime_var = tk.StringVar(value="Runtime: 0:00:00")
        self.runtime_label = ttk.Label(
            self.stats_frame,
            textvariable=self.runtime_var
        )
        self.runtime_label.grid(row=0, column=0, padx=5)
        
        # Current slots
        self.slots_var = tk.StringVar(value="Current Slots - Overload: 1, Absorption: 9")
        self.slots_label = ttk.Label(
            self.stats_frame,
            textvariable=self.slots_var
        )
        self.slots_label.grid(row=1, column=0, padx=5)
        
        # Start time for runtime calculation
        self.start_time = None
        
        # Update GUI periodically
        self.update_gui()
    
    def toggle_program(self):
        global running
        toggle_program()
        if running:
            self.status_var.set("Status: Running")
            self.start_button.configure(text="Stop (Left Ctrl)")
            if not self.start_time:
                self.start_time = datetime.now()
        else:
            self.status_var.set("Status: Stopped")
            self.start_button.configure(text="Start (Left Ctrl)")
            self.start_time = None
    
    def exit_program(self):
        self.root.quit()
        exit_program()
    
    def update_gui(self):
        if running and self.start_time:
            runtime = datetime.now() - self.start_time
            hours = runtime.seconds // 3600
            minutes = (runtime.seconds % 3600) // 60
            seconds = runtime.seconds % 60
            self.runtime_var.set(f"Runtime: {hours}:{minutes:02d}:{seconds:02d}")
            
            # Update current slots
            self.slots_var.set(
                f"Current Slots - Overload: {current_overload_slot}, "
                f"Absorption: {current_absorption_slot}"
            )
        
        self.root.after(1000, self.update_gui)

def main():
    """Main function to start the GUI and keyboard listener."""
    root = tk.Tk()
    app = NMZGUI(root)
    
    # Start keyboard listener in a separate thread
    listener = Listener(on_press=on_press)
    listener.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
