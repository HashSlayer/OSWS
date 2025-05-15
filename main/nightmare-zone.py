#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from datetime import datetime
import time

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils.core.timing import *
from utils.core.welcome import welcome
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.base_gui import BaseGUI

welcome()

class NMZGUI(BaseGUI):
    """Custom GUI for NMZ bot with dark theme"""
    def __init__(self):
        super().__init__(bot_name="NMZ Bot", bot_function=walker)
        
        # Override colors after parent initialization
        self.text_box_bg = "#4A4A4A"  # Lighter gray
        self.text_box_fg = "#D3D3A4"  # Gray with a khaki hue
        
        # Update text box colors
        self.text_box.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                              insertbackground=self.text_box_fg)
        self.notepad.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                             insertbackground=self.text_box_fg)
        self.max_walks_entry.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                                     insertbackground=self.text_box_fg)

def walker(gui):
    """Walker implementation for NMZ (Nightmare Zone) automation.
    Handles overload and absorption potion sipping with rock cake usage."""
    try:
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
        
        while gui.running:
            current_time = time.time()
            
            # Handle potion sips (every 5 minutes)
            if current_time - last_potion_time >= 300:
                gui.append_message(f"Taking overload sip from slot {current_overload_slot}")
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
                gui.append_message(f"Taking first absorption sip from slot {current_absorption_slot}")
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

                gui.append_message(f"Taking second absorption sip from slot {current_absorption_slot}")
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
            if current_time - last_rock_time >= 60:
                gui.append_message(f"Using rock cake from slot {rock_slot}")
                sleep(1.5, 2)
                inv_slot(rock_slot)
                click()
                last_rock_time = current_time
                sleep(0.5, 1)
                if rnd.random() < 0.8:  # 80% chance of second click
                    sleep(0.5, 1)
                    click()
                
                sleep(0.5, 1)
            
            sleep(0.1)  # Small sleep to prevent excessive CPU usage
            
            # Update progress
            gui.walk_count += 1
            if gui.walk_count % 10 == 0:  # Log every 10 cycles
                gui.append_message(f"Completed {gui.walk_count} cycles")

            # Check max walks limit
            try:
                max_walks = int(gui.max_walks_entry.get())
                if gui.walk_count >= max_walks:
                    gui.running = False
                    gui.append_message(f"Reached maximum cycles ({max_walks}). Stopping bot.")
                    break
            except ValueError:
                pass  # Invalid max walks value, continue running

    except Exception as e:
        gui.append_message(f"Error in NMZ loop: {e}")
        gui.running = False

def main():
    """Initialize and run the NMZ bot with GUI."""
    gui = NMZGUI()
    gui.run()

if __name__ == "__main__":
    main()
