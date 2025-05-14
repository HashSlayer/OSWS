"""
NMZ Melee Bot - A GUI application for automating NMZ melee training
Features:
- Inventory slot rotation system
- Click tracking
- Random breaks
- Clean shutdown handling
"""

import os
import sys
import threading
import random
from pynput.keyboard import Listener, Key
import tkinter as tk
from tkinter import font as tkFont
from datetime import datetime
import time

# Set up project paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import utility modules
from utils.core.timing import sleep
from utils.core.welcome import welcome
from utils.movements import right_ctrl
from utils.clicker import ClickTracker
from utils.item_slots import inv_slot
from utils.gui.confetti import startConfetti

# Global state management
running = False
running_lock = threading.Lock()
bot_thread = None

# Control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r    # Right Control key for kill

# Display welcome message
welcome()

class GGui:
    """Main GUI class handling the application interface and controls"""
    
    def __init__(self):
        self.root = tk.Tk()  # Initialize the main window
        self.root.title("5MEkailO's Beautiful Bot")  # Set window title
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # GUI setup and styling
        self.setup_gui()  # Setup GUI components like background colors
        self.apply_style()  # Apply styles to GUI elements
        self.root.geometry("1530x710")
        # GUI layout creation
        self.create_top_frame()  # Create and layout the top frame of the GUI
        self.create_text_box()  # Create the main text box
        self.create_additional_text_box()  # Create an additional notepad text box
        # Canvas setup
        self.canvas_width = self.canvas.winfo_width()  # Get initial canvas width
        self.canvas_height = self.canvas.winfo_height()  # Get initial canvas height
        self.canvas.bind("<Configure>", self.on_resize)  # Bind window resize event to on_resize function
        # Click tracking setup
        self.click_tracker = ClickTracker(self.append_message, self.canvas)  # Initialize the click tracker
        self.click_tracker_thread = None  # Initialize the click tracker thread
        self.random_sleep_enabled = False  # Initialize random sleep flag
        self.load_text()
        self.bot_active = False  # Add this flag to track bot state

    def setup_gui(self):
        self.background_color_start = "#FF6B6B"  # Set the start color for the gradient (Vibrant pink)
        self.background_color_end = "#4D96FF"    # Set the end color for the gradient (Bright blue)
        self.create_gradient_background()  # Call method to create the gradient background

    def apply_style(self):
        # Set colors and font for various GUI elements
        self.bg_color = "#4D96FF"        # Background color (Vibrant pink) FF6B6B Electric blue: #4D96FF
        self.button_color = "#FF6B6B"    # Button color (Also set to Vibrant pink, consider changing to a different color)
        self.text_color = "#99E1A2"      # Text color (Fresh green)
        self.hover_color = "#F55C47"     # Button hover color (Fiery orange)
        self.custom_font = tkFont.Font(family="Consolas", size=13, weight="bold")  # Custom font for GUI elements
        self.root.configure(bg=self.bg_color)  # Apply the background color to the root window

    def create_gradient(self, canvas, color1, color2, width, height):
        for i in range(height):
            # Calculate color components based on the gradient
            r1, g1, b1 = canvas.winfo_rgb(color1)  # Get RGB components of the start color
            r2, g2, b2 = canvas.winfo_rgb(color2)  # Get RGB components of the end color
            # Interpolate the RGB components based on the current position
            r = (r1 + int((r2 - r1) * i / height)) & 0xff00 
            g = (g1 + int((g2 - g1) * i / height)) & 0xff00 
            b = (b1 + int((b2 - b1) * i / height)) & 0xff00 
            color = f'#{r:04x}{g:04x}{b:04x}'
            canvas.create_line(0, i, width, i, fill=color)  # Draw a line with the interpolated color

    def create_gradient_background(self):
        self.canvas = tk.Canvas(self.root)  # Initialize a canvas in the main window
        self.canvas.pack(fill="both", expand=True)  # Pack the canvas to fill the entire window
        self.canvas.bind("<Configure>", self.on_resize)  # Bind the resize event to the on_resize method
        self.on_resize(None)  # Make an initial call to set up the gradient background

    def update_time(self):
        """Update time display with reduced frequency"""
        now = datetime.now()
        
        # Update date only if it has changed
        new_date = now.strftime(" %B %d, %Y ")
        if not hasattr(self, '_last_date') or new_date != self._last_date:
            self.date_label.config(text=new_date)
            self._last_date = new_date
        
        # Update time with reduced precision
        time_str = now.strftime(" %H:%M:%S ")
        self.time_label.config(text=time_str)
        
        # Reduce update frequency to 500ms
        self.root.after(500, self.update_time)

    def start_confetti_animation(self):
        startConfetti(self.canvas)  # Initiate the confetti animation on the canvas

    def create_text_box(self):
        # Initialize a PanedWindow for layout management
        self.pane = tk.PanedWindow(self.canvas, bd=0, sashwidth=3, orient=tk.HORIZONTAL, bg='#4D96FF')
        self.pane.pack(fill=tk.BOTH, expand=True, padx=33, pady=23)  # Set padding and make it expandable

        # Create the main text box for user input
        self.text_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF", font=("Consolas", 13), insertbackground="#5BCB77", relief="sunken", borderwidth=5, height=10)
        self.pane.add(self.text_box, stretch="always")  # Add to the pane with stretch option
        self.text_box.insert(tk.END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.text_box.insert(tk.END, "      Welcome                                       \n")                         # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Press the [left CTRL] key to toggle the bot OFF/ON ; or (START/STOP)  \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Press the [right CTRL] key to Kill the bot                            \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Enjoy your walk!                                                     \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")  # Prepopulate with a welcome message

    def create_additional_text_box(self):
        # Create an additional text box for notes
        self.notepad_text_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF", font=("Consolas", 12), relief="sunken", borderwidth=5, height=10)
        self.pane.add(self.notepad_text_box, width= 444)  # Set a fixed width for the notepad
        self.notepad_text_box.insert(tk.END, "Notes: \n")  # Prepopulate with "Notes:"

    def save_text(self):
        """Save the content of the notepad text box to a file."""
        with open("notepad_content.txt", "w") as file:
            file.write(self.notepad_text_box.get("1.0", tk.END))

    def load_text(self):
        """Load the content from the file to the notepad text box."""
        if os.path.exists("notepad_content.txt"):
            with open("notepad_content.txt", "r") as file:
                self.notepad_text_box.delete("1.0", tk.END)
                self.notepad_text_box.insert(tk.END, file.read())

    def on_resize(self, event):
        """Handle window resize events"""
        if event:
            width, height = event.width, event.height
        else:
            width, height = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        
        # This is computationally expensive and runs frequently
        self.canvas.delete("gradient")
        self.create_gradient(self.canvas, self.background_color_start, self.background_color_end, width, height)

    def kill_bot(self):
        global running, bot_thread
        # Immediate UI feedback to indicate shutdown is in progress
        # Disable click tracking UI update
        self.click_tracking_enabled = False
        running = False
        self.toggle_button.config(text=" Track Clicks: OFF ", bg="#FF6B6B")
        self.start_button.config(text="    START    ", bg="#2ECC73", fg='#97E469')
        # GUI-specific logic
        self.start_confetti_animation()
        # Ensure this operation is safe and necessary
        right_ctrl()
        # Restore the kill button state after shutdown process
        self.kill_button.config(text="KILLED", state=tk.NORMAL)

    def append_message(self, message):
        self.text_box.insert(tk.END, message + '\n')  # Insert the message at the end of the text box
        self.text_box.see(tk.END)  # Scroll to the end of the text box to make the message visible

    def toggle_walk_button(self):
        """Toggle the bot's walking state"""
        global running, bot_thread
        with running_lock:
            if running:
                self.stop_bot()
            else:
                self.start_bot()

    def start_bot(self):
        """Start the bot operation"""
        global running, bot_thread
        running = True
        self.bot_active = True
        self.append_message("Bot Started")
        self.start_button.config(text="       STOP       ", bg="#FF6B6B", fg='#97E469')
        
        # Only create a new thread if one isn't already running
        if bot_thread is None or not bot_thread.is_alive():
            bot_thread = threading.Thread(target=lambda: walker(self), daemon=True)
            bot_thread.start()

    def stop_bot(self):
        """Stop the bot operation"""
        global running
        running = False
        self.bot_active = False
        self.append_message("Bot Paused")
        self.start_button.config(text="     START     ", bg="#09C159", fg='#97E469')

    def track_clicks(self):
        if not self.click_tracking_enabled:
            self.track_clicks()  # Start click tracking if it's not already enabled
        else:
            self.track_clicks()  # Stop click tracking if it's already enabled

    def track_clicks(self):
        self.click_tracking_enabled = not self.click_tracking_enabled  # Toggle the state

        if self.click_tracking_enabled:
            if not self.click_tracker.tracking and (self.click_tracker_thread is None or not self.click_tracker_thread.is_alive()):
                # Start a new thread if it's not already tracking
                self.click_tracker_thread = threading.Thread(target=self.click_tracker.run)
                self.click_tracker_thread.daemon = True
                self.click_tracker_thread.start()
            else:
                # Enable click processing
                self.click_tracker.process_clicks = True
            self.toggle_button.config(text=" Track Clicks: ON ", bg="#2ECC73")
        else:
            # Disable click processing
            self.click_tracker.process_clicks = False
            # Optionally, implement a mechanism to gracefully stop the thread if required
            self.toggle_button.config(text=" Track Clicks: OFF ", bg="#FF6B6B")

    def toggle_sleeps(self):
        self.random_sleep_enabled = not self.random_sleep_enabled
        if self.random_sleep_enabled:
            self.toggle_sleep_button.config(text="Random Breaks: ON", bg="#2ECC71")
        else:
            self.toggle_sleep_button.config(text="Random Breaks: OFF", bg="#FF6B6B")

    def on_close(self):
        """Handle cleanup when the application is closed"""
        global running
        
        # Stop the bot if it's running
        if self.bot_active:
            self.stop_bot()
        
        # Signal all threads to stop
        running = False
        
        # Stop click tracking if active
        if self.click_tracking_enabled:
            self.click_tracker.process_clicks = False
            if self.click_tracker_thread and self.click_tracker_thread.is_alive():
                try:
                    self.click_tracker_thread.join(timeout=1.0)
                except Exception as e:
                    print(f"Error stopping click tracker: {e}")
        
        # Stop bot thread if active
        if bot_thread and bot_thread.is_alive():
            try:
                bot_thread.join(timeout=1.0)
            except Exception as e:
                print(f"Error stopping bot thread: {e}")
        
        # Save notepad content
        self.save_text()
        print("Exiting... Text File saved <3")
        
        # Directly destroy the window without waiting for confetti
        self.root.destroy()

    def create_top_frame(self):
        """Set up the top frame of the GUI with controls"""
        # Initialize the top frame of the GUI
        top_frame = tk.Frame(self.canvas, bg='#FF6B6B')
        top_frame.pack(padx=15, pady=15)

        # Create and pack the date label
        self.date_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg='#97E469', 
                                  font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.date_label.pack(side="left", padx=(80, 2))
        
        # Create and pack the time label
        self.time_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg='#97E469', 
                                  font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.time_label.pack(side="left", padx=2)

        # Define the style for labels and entries
        label_style = {"bg": "#FF6B6B", "fg": "#97E469", "font": self.custom_font, 
                      "relief": tk.FLAT, "borderwidth": 0}
        entry_style = {"bg": "#FFFAE4", "fg": "#217BFF", "font": self.custom_font, 
                      "relief": tk.SUNKEN, "borderwidth": 1}

        # Create and pack the 'Kill' button
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot, bg=self.button_color, fg='#97E469', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=9)
        # Create and pack the 'Start / Stop' button
        self.start_button = tk.Button(top_frame, text="  Start / Stop  ", 
                                     command=self.toggle_walk_button, 
                                     bg=self.button_color, fg='#97E469', 
                                     font=self.custom_font, 
                                     activebackground='#C8F6AD', 
                                     relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=9)

        # Create and pack the 'Track Clicks' toggle button
        self.click_tracking_enabled = False
        self.toggle_button = tk.Button(top_frame, text=" Track Clicks ", 
                                     command=self.track_clicks, 
                                     bg=self.button_color, fg='#97E469', 
                                     font=self.custom_font, 
                                     activebackground='#C8F6AD', 
                                     relief=tk.RAISED, borderwidth=3)
        self.toggle_button.pack(side=tk.LEFT, padx=9)

        # Frame for toggle switches
        toggle_frame = tk.Frame(self.root, bg=self.background_color_end)
        toggle_frame.pack(padx=10, pady=(0, 10))

        # Random Breaks Toggle Switch
        self.toggle_sleep_button = tk.Button(toggle_frame, 
                                           text="Random Breaks: OFF", 
                                           command=self.toggle_sleeps, 
                                           bg="#FF6B6B", fg='#97E469', 
                                           font=self.custom_font)
        self.toggle_sleep_button.pack(side=tk.LEFT, padx=(10, 2))

        # Call the method to update the time display
        self.update_time()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the close event
        self.root.mainloop() #Start main loop

def walker(gui):
    """Main bot logic for inventory slot rotation"""
    slot_rotation = [1, 2, 3, 4]  # Slots to rotate through
    current_slot_index = 0
    last_slot28_time = time.time()
    last_rotation_time = time.time()
    rotation_interval = 300  # 5 minutes

    gui.append_message("Bot walker initialized")  # Confirm walker has started

    while True:
        if not running:
            time.sleep(0.1)  # Reduced CPU usage while paused
            continue

        try:
            current_time = time.time()
            
            # Handle slot 28 clicking (every 1-1.1 minutes)
            if current_time - last_slot28_time >= (60 + (random.random() * 6)):
                inv_slot(28)
                gui.append_message(f"Clicked inventory slot 28")
                last_slot28_time = current_time
            
            # Handle rotation slot clicking (every 5 minutes)
            if current_time - last_rotation_time >= rotation_interval:
                current_slot = slot_rotation[current_slot_index]
                inv_slot(current_slot)
                gui.append_message(f"Clicked rotation slot {current_slot}")
                current_slot_index = (current_slot_index + 1) % len(slot_rotation)
                last_rotation_time = current_time
            
            time.sleep(0.1)  # Prevent excessive CPU usage

        except Exception as e:
            gui.append_message(f"Error in walker: {str(e)}")
            time.sleep(1)  # Pause briefly on error

def toggle_walker_key(key, gui):
    """Handle keyboard control inputs"""
    if key == ONOFF:  # Left CTRL
        if gui.bot_active:
            gui.stop_bot()
        else:
            gui.start_bot()
    elif key == KILL:  # Right CTRL
        gui.on_close()

if __name__ == "__main__":
    try:
        # Initialize and start the application
        gui = GGui()
        listener_thread = threading.Thread(
            target=lambda: Listener(
                on_press=lambda key: toggle_walker_key(key, gui)
            ).start(),
            daemon=True  # Ensure thread closes with main program
        )
        listener_thread.start()
        gui.run()
    except Exception as e:
        print(f"Application error: {str(e)}")
    finally:
        # Ensure clean shutdown
        running = False
        if bot_thread and bot_thread.is_alive():
            bot_thread.join(timeout=1.0)
