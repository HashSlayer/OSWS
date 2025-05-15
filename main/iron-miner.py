#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from datetime import datetime
import tkinter as tk
import tkinter.font as tkFont

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.core.timing import *
from utils.core.welcome import welcome
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.base_gui import BaseGUI

welcome()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Iron Miner Bot GUI
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class IronMinerGUI(BaseGUI):
    """Custom GUI for Iron Miner with dark theme"""
    def __init__(self):
        super().__init__(bot_name="Iron Miner Bot", bot_function=walker)
        
        # Override colors after parent initialization
        self.text_box_bg = "#4A4A4A"  # Lighter gray
        self.text_box_fg = "#FFFFFF"  # White text
        
        # Set static gradient colors
        self.background_color_start = "#FF6B6B"  # Fixed top color
        self.background_color_end = self.generate_random_color()  # Random bottom color (set once)
        
        # Update text box colors
        self.text_box.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                              insertbackground=self.text_box_fg)
        self.notepad.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                             insertbackground=self.text_box_fg)
        self.max_walks_entry.configure(bg=self.text_box_bg, fg=self.text_box_fg,
                                     insertbackground=self.text_box_fg)
        
        # Force initial gradient update
        self.on_resize(None)

    def setup_gui(self):
        """Override setup_gui to prevent gradient color updates"""
        # Set colors and styles
        self.bg_color = "#4D96FF"  # Electric blue
        self.button_color = "#FF6B6B"  # Vibrant pink
        self.text_color = "#97E469"  # Fresh green
        self.custom_font = tkFont.Font(family="Consolas", size=13, weight="bold")
        
        # Create gradient background
        self.create_gradient_background()
        
        # Create main components
        self.create_top_frame()
        self.create_text_boxes()
        
        # Start time updates only
        self.update_time()
        
        # Note: We don't start gradient color updates

    def update_gradient_color(self):
        """Override to prevent gradient updates"""
        pass  # Do nothing, keeping the initial gradient colors

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Iron Miner Bot Logic
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Timebot():  
    """Add random delays to simulate human behavior"""
    if (rnd.random() > 0.947):
        time.sleep(rnd.random() * 0.4 + 0.03)
        if (rnd.random() > 0.917):
            Notbotting()

def walker(gui):
    """Walker implementation for iron mining with human-like behavior.
    Walks between three iron ore spots, mining and dropping inventory when full."""
    try:
        dug = 0  # Track ores mined for inventory management
        
        while gui.running:
            if rnd.random() > 0.02:  # 95% chance to execute the ore mining
                # Ore 1 (Top ore)
                bezierMove(rnd.randint(933,983), rnd.randint(361, 421), rnd.random() * 0.281 + 0.88913)
                if (rnd.random() > 0.388):
                    bezierMove(rnd.randint(936,983), rnd.randint(381, 425), rnd.random() * 0.081 + 0.418913)
                sleep(.3,.1,.1)
                if rnd.random() > 0.5:
                    sleep(.1,.1,.2)
                click()
                if (rnd.random() > 0.976):
                    click()
                    gui.append_message("Nice double click!")
                    if rnd.random() > 0.97:
                        click()
                time.sleep(rnd.random() *0.28 + 0.661)
                sleep(.3,.2,.2)
                if rnd.random() > 0.97:
                    sleep(.3, 4, 2)
                    if rnd.random() > 0.97:
                        sleep(.3, 14, 2)
                dug += 1
                gui.walk_count += 1
                gui.append_message(f"Mined ore {dug}/26 (Total: {gui.walk_count})")
                
                if dug == 26:
                    if rnd.random() > 0.412:
                        drop_inventory(rnd.randint(23, 27))
                    else:
                        drop_inventory(26)
                    dug = 0
                    gui.append_message("Inventory full - dropping ores")
            else:  # 5% chance to skip and sleep
                sleep(1, 3, 3)
                if rnd.random() > 0.98:
                    sleep(1, 20)
                    Notbotting()

            if not gui.running:
                break

            if rnd.random() > 0.02:  # 95% chance to execute the ore mining
                # Ore 2 (middle ore)
                bezierMove(rnd.randint(685, 765), rnd.randint(595, 645), rnd.random() * 0.2832 + 0.881)
                if (rnd.random() > 0.381):
                    bezierMove(rnd.randint(695, 775), rnd.randint(595, 645), rnd.random() * 0.081 + 0.418913)
                time.sleep(rnd.random() *0.381 + 0.683)
                if rnd.random() > 0.5:
                    sleep(.2,.1,.2)
                click()
                if (rnd.random() > 0.93):
                    click()
                    gui.append_message("Nice double click!")
                Timebot()
                time.sleep(rnd.random() *0.36 + 0.651)
                if rnd.random() > 0.97:
                    sleep(.3, 4, 2)
                dug += 1
                gui.walk_count += 1
                gui.append_message(f"Mined ore {dug}/26 (Total: {gui.walk_count})")
                
                if dug == 26:
                    if rnd.random() > 0.112:
                        drop_inventory(25)
                    else:
                        drop_inventory(26)
                    dug = 0
                    gui.append_message("Inventory full - dropping ores")
            else:  # 5% chance to skip and sleep
                sleep(1, 3, 3)
                if rnd.random() > 0.91:
                    sleep(1, 8)
                    Notbotting()

            if not gui.running:
                break

            if rnd.random() > 0.02:  # 95% chance to execute the ore mining
                # Ore 3 (Bottom ore)
                bezierMove(rnd.randint(909, 960), rnd.randint(765, 835), rnd.random() * 0.281 + 0.889111)
                if (rnd.random() > 0.381):
                    bezierMove(rnd.randint(897, 963), rnd.randint(765, 835), rnd.random() * 0.081 + 0.4118913)
                time.sleep(rnd.random() *0.51 + 0.513)
                click()
                if rnd.random() > 0.5:
                    sleep(.3,.3,.2)
                if (rnd.random() > 0.939):
                    click()
                    gui.append_message("Nice double click!")
                time.sleep(rnd.random() *0.61 + 0.631)
                if rnd.random() > 0.97:
                    sleep(.3, 4, 2)
                Timebot()
                dug += 1
                gui.walk_count += 1
                gui.append_message(f"Mined ore {dug}/26 (Total: {gui.walk_count})")
            else:  # 5% chance to skip and sleep
                sleep(2, 3, 3)
                if rnd.random() > 0.91:
                    sleep(1, 7)
                    Notbotting()

            if dug == 26:
                if rnd.random() > 0.112:
                    drop_inventory(25)
                else:
                    drop_inventory(26)
                dug = 0
                gui.append_message("Inventory full - dropping ores")

            # Check if we've reached max walks
            try:
                max_walks = int(gui.max_walks_entry.get())
                if gui.walk_count >= max_walks:
                    gui.running = False
                    gui.append_message(f"Reached maximum walks ({max_walks}). Stopping bot.")
                    break
            except ValueError:
                gui.append_message("Invalid max walks value. Using default.")

    except Exception as e:
        gui.append_message(f"Error in mining loop: {e}")
        gui.running = False

def main():
    """Main function to start the bot with GUI."""
    # Create GUI instance with bot name and walker function
    gui = IronMinerGUI()
    # Start the GUI
    gui.run()

if __name__ == "__main__":
    main() 