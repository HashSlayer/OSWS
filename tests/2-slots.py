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
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)

    # Import utilities
    from utils.core.timing import sleep
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

    CONFIG_FILE = os.path.join(project_root, 'config', 'inventory_config.json')

    class InventoryCalibrator(tk.Tk):
        def __init__(self):
            try:
                super().__init__()
                print("Initializing InventoryCalibrator...")

                # Make window transparent and always on top
                self.attributes('-alpha', 0.7)
                self.attributes('-topmost', True)
                
                # Remove window decorations
                self.overrideredirect(True)
                
                # Window size and position
                self.geometry('300x400+100+100')  # Default size, will be adjustable
                
                # Create main frame
                self.main_frame = ttk.Frame(self)
                self.main_frame.grid(row=0, column=0, sticky='nsew')
                
                # Help label at top
                help_text = "Controls:\n• Right-click + drag to move window\n• Ctrl + Right-click + drag to resize\n• Left-click slots to calibrate\n• Escape to close"
                self.help_label = ttk.Label(
                    self.main_frame,
                    text=help_text,
                    justify=tk.LEFT,
                    background='black',
                    foreground='white'
                )
                self.help_label.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
                
                # Grid of inventory slots (4x7)
                self.buttons = []
                self.selected_slot = None
                
                for row in range(7):
                    for col in range(4):
                        slot_num = row * 4 + col + 1
                        btn = tk.Button(
                            self.main_frame,
                            text=str(slot_num),
                            bg='gray75',
                            width=8,
                            height=3
                        )
                        btn.grid(row=row+1, column=col, padx=1, pady=1)  # Shifted down by 1 row for help text
                        btn.bind('<Button-1>', lambda e, s=slot_num: self.on_slot_click(s))
                        self.buttons.append(btn)
                
                # Control frame at bottom
                self.control_frame = ttk.Frame(self)
                self.control_frame.grid(row=8, column=0, sticky='ew', pady=5)  # Shifted down by 1 row
                
                # Save button
                self.save_btn = ttk.Button(
                    self.control_frame,
                    text="Save Calibration",
                    command=self.save_calibration
                )
                self.save_btn.pack(side='left', padx=5)
                
                # Close button
                self.close_btn = ttk.Button(
                    self.control_frame,
                    text="Close",
                    command=self.quit
                )
                self.close_btn.pack(side='right', padx=5)
                
                # Status label
                self.status_label = ttk.Label(self.control_frame, text="Ready")
                self.status_label.pack(side='left', padx=5)
                
                # Bind window dragging
                self.bind('<Button-3>', self.start_move)
                self.bind('<B3-Motion>', self.on_move)
                
                # Bind window resizing
                self.bind('<Control-Button-3>', self.start_resize)
                self.bind('<Control-B3-Motion>', self.on_resize)
                
                # Bind escape key to close
                self.bind('<Escape>', lambda e: self.quit())
                
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
            self.start_x = event.x
            self.start_y = event.y

        def on_move(self, event):
            if self.start_x is not None:
                dx = event.x - self.start_x
                dy = event.y - self.start_y
                x = self.winfo_x() + dx
                y = self.winfo_y() + dy
                self.geometry(f"+{x}+{y}")

        def start_resize(self, event):
            self.start_x = event.x
            self.start_y = event.y
            self.start_w = self.winfo_width()
            self.start_h = self.winfo_height()

        def on_resize(self, event):
            if self.start_x is not None:
                dx = event.x - self.start_x
                dy = event.y - self.start_y
                w = max(200, self.start_w + dx)  # Minimum width
                h = max(300, self.start_h + dy)  # Minimum height
                self.geometry(f"{w}x{h}")

        def on_slot_click(self, slot_num):
            try:
                x = self.winfo_x() + self.buttons[slot_num-1].winfo_x() + self.buttons[slot_num-1].winfo_width()//2
                y = self.winfo_y() + self.buttons[slot_num-1].winfo_y() + self.buttons[slot_num-1].winfo_height()//2
                print(f"Slot {slot_num}: x={x}, y={y}")
                
                # Update status label
                self.status_label.config(text=f"Slot {slot_num}: x={x}, y={y}")
                
                # Highlight the clicked button
                for btn in self.buttons:
                    btn.configure(bg='gray75')
                self.buttons[slot_num-1].configure(bg='light blue')
                self.selected_slot = slot_num
            except Exception as e:
                print(f"Error in slot click: {str(e)}")
                self.status_label.config(text=f"Error: {str(e)}")

        def save_calibration(self):
            try:
                if not self.selected_slot:
                    messagebox.showwarning("Warning", "Please click a slot first to calibrate")
                    return
                    
                # Calculate base coordinates from first slot
                first_btn = self.buttons[0]
                base_x = self.winfo_x() + first_btn.winfo_x() + first_btn.winfo_width()//2
                base_y = self.winfo_y() + first_btn.winfo_y() + first_btn.winfo_height()//2
                
                # Calculate slot spacing
                second_btn = self.buttons[1]
                x_spacing = second_btn.winfo_x() - first_btn.winfo_x()
                
                fifth_btn = self.buttons[4]
                y_spacing = fifth_btn.winfo_y() - first_btn.winfo_y()
                
                config = {
                    'base_x': base_x,
                    'base_y': base_y,
                    'x_spacing': x_spacing,
                    'y_spacing': y_spacing
                }
                
                # Ensure config directory exists
                os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
                
                # Save configuration
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
