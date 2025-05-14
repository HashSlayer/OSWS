import os
import sys
import threading
import tkinter as tk
from tkinter import ttk
import random as rnd
from pynput.keyboard import Listener, Key

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.core.timing import sleep, long_sleep
from utils.core.welcome import welcome
from utils.movements import bezierMove
from utils.clicker import click
from utils.item_slots import inv_slot

# Global control variables
running = False
bot_thread = None

# Define control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r   # Right Control key for kill

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OSWS Test Bot")
        
        # Configure style
        style = ttk.Style()
        style.configure("Status.TLabel", font=("Helvetica", 12))
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status label
        self.status_var = tk.StringVar(value="Status: Waiting to start")
        self.status_label = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            style="Status.TLabel"
        )
        self.status_label.grid(row=0, column=0, pady=5)
        
        # Iteration counter
        self.iteration_var = tk.StringVar(value="Iterations: 0")
        self.iteration_label = ttk.Label(
            self.main_frame,
            textvariable=self.iteration_var,
            style="Status.TLabel"
        )
        self.iteration_label.grid(row=1, column=0, pady=5)
        
        # Current slot counter
        self.slot_var = tk.StringVar(value="Current Slot: -")
        self.slot_label = ttk.Label(
            self.main_frame,
            textvariable=self.slot_var,
            style="Status.TLabel"
        )
        self.slot_label.grid(row=2, column=0, pady=5)
        
        # Instructions
        instructions = """
        Left CTRL: Start/Stop Bot
        Right CTRL: Exit Program
        """
        self.instructions_label = ttk.Label(
            self.main_frame,
            text=instructions,
            justify=tk.LEFT,
            style="Status.TLabel"
        )
        self.instructions_label.grid(row=3, column=0, pady=20)

    def update_status(self, status):
        self.status_var.set(f"Status: {status}")
        self.root.update()

    def update_iteration(self, count):
        self.iteration_var.set(f"Iterations: {count}")
        self.root.update()

    def update_slot(self, slot):
        self.slot_var.set(f"Current Slot: {slot}")
        self.root.update()

def on_press(key, gui):
    global running, bot_thread
    
    if key == ONOFF:  # Left Control
        running = not running
        if running and (bot_thread is None or not bot_thread.is_alive()):
            gui.update_status("Starting...")
            bot_thread = threading.Thread(target=bot_loop, args=(gui,), daemon=True)
            bot_thread.start()
        elif not running:
            gui.update_status("Stopping...")
    
    elif key == KILL:  # Right Control
        running = False
        gui.update_status("Exiting...")
        gui.root.after(1000, gui.root.destroy)
        return False

def bot_loop(gui):
    global running
    iteration_count = 0
    
    while running:
        iteration_count += 1
        gui.update_iteration(iteration_count)
        gui.update_status("Running")
        
        # Click through inventory slots
        for slot in range(1, 29):
            if not running:
                break
                
            gui.update_slot(slot)
            inv_slot(slot)  # Move to slot
            sleep()  # Random pause before click
            click()  # Click the slot
            sleep()  # Random pause after click
            
        # Rest between iterations
        if running:
            gui.update_status("Resting")
            sleep(3)

def main():
    # Show welcome message
    welcome()
    
    # Create GUI
    root = tk.Tk()
    gui = BotGUI(root)
    
    # Setup keyboard listener
    listener = Listener(on_press=lambda key: on_press(key, gui))
    listener.start()
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
