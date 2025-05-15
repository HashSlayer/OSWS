"""
Inventory Calibration Tool for OSWS Framework

This module provides a graphical interface for calibrating inventory slot positions.
Key features:
- Visual grid representation of inventory slots (4x7)
- Click-based coordinate calibration
- Configuration saving
- Movable/resizable transparent window

This tool is designed to help set up accurate inventory coordinates for use across all
bots in the framework. It acts as a configuration utility rather than a bot itself.

Questions/Unclear Points:
1. Why is this in the tests directory if it's a calibration tool?
2. How does this interact with the actual bot functionality?
3. What's the significance of the running/bot_thread globals?
4. Are ONOFF/KILL keys used in this file?
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import random as rnd
from pynput.keyboard import Listener, Key
import json

try:
    # Get the absolute path to the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.insert(0, project_root)

    # Import utilities
    from utils.core.timing import sleep  # Used for potential future actions
    from utils.core.welcome import welcome  # Not currently used but available for welcome screen
    from utils.movements import bezierMove  # Available for potential future click movement
    from utils.clicker import click  # Available for potential future click actions
    from utils.item_slots import inv_slot  # Reference for coordinate system

    # Global control variables - available for future integration with hotkey system
    running = False  # Controls bot operation state
    bot_thread = None  # Holds the bot's thread

    # Define control keys for future hotkey implementation
    ONOFF = Key.ctrl_l  # Left Control key for toggle
    KILL = Key.ctrl_r   # Right Control key for kill

    # Configuration file path
    CONFIG_FILE = os.path.join(project_root, 'config', 'inventory_config.json')

    class InventoryCalibrator(tk.Tk):
        """
        GUI application for calibrating inventory slot positions.
        
        Features:
        - Transparent, always-on-top window
        - Draggable and resizable
        - 4x7 grid of clickable slots
        - Coordinate saving functionality
        
        The current implementation uses a single slot selection model for simplicity.
        Future improvements could include multi-slot selection for more accurate calibration
        and coordinate range validation.
        """
        
        def __init__(self):
            try:
                super().__init__()
                print("Initializing InventoryCalibrator...")

                # Window properties
                self.attributes('-alpha', 0.7)  # 30% transparent
                self.attributes('-topmost', True)  # Always on top
                self.overrideredirect(True)  # No window decorations
                self.geometry('300x400+100+100')  # Initial size and position
                
                # Main container
                self.main_frame = ttk.Frame(self)
                self.main_frame.grid(row=0, column=0, sticky='nsew')
                
                # Help text at top
                help_text = "Controls:\n• Right-click + drag to move window\n• Ctrl + Right-click + drag to resize\n• Left-click slots to calibrate\n• Escape to close"
                self.help_label = ttk.Label(
                    self.main_frame,
                    text=help_text,
                    justify=tk.LEFT,
                    background='black',
                    foreground='white'
                )
                self.help_label.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
                
                # Initialize slot grid
                self.buttons = []  # Holds all slot buttons
                self.selected_slot = None  # Currently selected slot number
                
                # Create 4x7 grid of slot buttons
                # Row+1 is used in grid() to account for the help label at row 0
                for row in range(7):
                    for col in range(4):
                        slot_num = row * 4 + col + 1  # Calculate 1-based slot number
                        btn = tk.Button(
                            self.main_frame,
                            text=str(slot_num),
                            bg='gray75',  # Default background
                            width=8,
                            height=3
                        )
                        btn.grid(row=row+1, column=col, padx=1, pady=1)  # +1 to leave space for help text
                        # Lambda with default arg to avoid late binding issues
                        btn.bind('<Button-1>', lambda e, s=slot_num: self.on_slot_click(s))
                        self.buttons.append(btn)
                
                # Control panel at bottom
                self.control_frame = ttk.Frame(self)
                self.control_frame.grid(row=8, column=0, sticky='ew', pady=5)
                
                # Save calibration button
                self.save_btn = ttk.Button(
                    self.control_frame,
                    text="Save Calibration",
                    command=self.save_calibration
                )
                self.save_btn.pack(side='left', padx=5)
                
                # Close application button
                self.close_btn = ttk.Button(
                    self.control_frame,
                    text="Close",
                    command=self.quit
                )
                self.close_btn.pack(side='right', padx=5)
                
                # Status display
                self.status_label = ttk.Label(self.control_frame, text="Ready")
                self.status_label.pack(side='left', padx=5)
                
                # Window movement bindings
                self.bind('<Button-3>', self.start_move)  # Right click
                self.bind('<B3-Motion>', self.on_move)  # Right click drag
                
                # Window resize bindings
                self.bind('<Control-Button-3>', self.start_resize)  # Ctrl + Right click
                self.bind('<Control-B3-Motion>', self.on_resize)  # Ctrl + Right click drag
                
                # Exit binding
                self.bind('<Escape>', lambda e: self.quit())
                
                # Movement/resize tracking variables
                self.start_x = None
                self.start_y = None
                self.start_w = None
                self.start_h = None
                
                print("InventoryCalibrator initialized successfully!")
                
            except Exception as e:
                print(f"Error in initialization: {str(e)}")
                messagebox.showerror("Initialization Error", str(e))
                self.quit()

        def start_move(self, event):
            """Store initial coordinates for window movement."""
            self.start_x = event.x
            self.start_y = event.y

        def on_move(self, event):
            """Handle window movement while dragging."""
            if self.start_x is not None:
                dx = event.x - self.start_x
                dy = event.y - self.start_y
                x = self.winfo_x() + dx
                y = self.winfo_y() + dy
                self.geometry(f"+{x}+{y}")

        def start_resize(self, event):
            """Store initial coordinates and dimensions for window resizing."""
            self.start_x = event.x
            self.start_y = event.y
            self.start_w = self.winfo_width()
            self.start_h = self.winfo_height()

        def on_resize(self, event):
            """Handle window resizing while dragging."""
            if self.start_x is not None:
                dx = event.x - self.start_x
                dy = event.y - self.start_y
                w = max(200, self.start_w + dx)  # Enforce minimum width
                h = max(300, self.start_h + dy)  # Enforce minimum height
                self.geometry(f"{w}x{h}")

        def on_slot_click(self, slot_num):
            """
            Handle slot button clicks.
            
            Calculates absolute screen coordinates for the clicked slot. These coordinates
            represent the exact pixel position that would be used by the bot when clicking
            on the given inventory slot.
            
            The absolute coordinates are used (rather than relative) because they directly
            correspond to the screen positions needed for bot interaction.
            """
            try:
                # Calculate absolute screen coordinates for slot center
                x = self.winfo_x() + self.buttons[slot_num-1].winfo_x() + self.buttons[slot_num-1].winfo_width()//2
                y = self.winfo_y() + self.buttons[slot_num-1].winfo_y() + self.buttons[slot_num-1].winfo_height()//2
                print(f"Slot {slot_num}: x={x}, y={y}")
                
                # Update status display
                self.status_label.config(text=f"Slot {slot_num}: x={x}, y={y}")
                
                # Update button highlighting
                for btn in self.buttons:
                    btn.configure(bg='gray75')  # Reset all buttons
                self.buttons[slot_num-1].configure(bg='light blue')  # Highlight selected
                self.selected_slot = slot_num
            except Exception as e:
                print(f"Error in slot click: {str(e)}")
                self.status_label.config(text=f"Error: {str(e)}")

        def save_calibration(self):
            """
            Save slot calibration data to config file.
            
            This method calculates the base coordinates and spacing between inventory slots
            based on the current GUI layout. It then saves this information to a configuration
            file that can be used by all bots in the framework.
            
            The spacing calculation uses fixed slots (first and second for horizontal,
            first and fifth for vertical) to determine consistent grid measurements.
            
            Future enhancements could include:
            - Multiple slot selection for more accurate average measurements
            - Validation of reasonable coordinate ranges
            - Backup of previous configuration before overwriting
            """
            try:
                if not self.selected_slot:
                    messagebox.showwarning("Warning", "Please click a slot first to calibrate")
                    return
                    
                # Get base coordinates from first slot
                first_btn = self.buttons[0]
                base_x = self.winfo_x() + first_btn.winfo_x() + first_btn.winfo_width()//2
                base_y = self.winfo_y() + first_btn.winfo_y() + first_btn.winfo_height()//2
                
                # Calculate horizontal spacing from first two slots
                second_btn = self.buttons[1]
                x_spacing = second_btn.winfo_x() - first_btn.winfo_x()
                
                # Calculate vertical spacing from first and fifth slots
                fifth_btn = self.buttons[4]
                y_spacing = fifth_btn.winfo_y() - first_btn.winfo_y()
                
                # Prepare configuration data
                config = {
                    'base_x': base_x,
                    'base_y': base_y,
                    'x_spacing': x_spacing,
                    'y_spacing': y_spacing
                }
                
                # Ensure config directory exists
                os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
                
                # Save to file
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=4)
                
                print(f"Calibration saved to {CONFIG_FILE}")
                self.status_label.config(text="Calibration saved!")
                messagebox.showinfo("Success", "Calibration saved successfully!")
                
            except Exception as e:
                print(f"Error saving calibration: {str(e)}")
                self.status_label.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to save calibration: {str(e)}")

    def main():
        """Initialize and run the calibration tool."""
        try:
            print("Starting Inventory Calibrator...")
            app = InventoryCalibrator()
            app.mainloop()
        except Exception as e:
            print(f"Error in main: {str(e)}")
            messagebox.showerror("Error", f"Application error: {str(e)}")

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"Fatal error: {str(e)}")
    try:
        messagebox.showerror("Fatal Error", str(e))
    except:
        pass  # If even the messagebox fails
