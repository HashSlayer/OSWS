#!/usr/bin/env python
"""
Screenshot Calibration Test

This script tests the calibrated inventory slot coordinates from the screenshot
calibration tool by displaying a visual overlay of all 28 inventory slots.

Usage:
  python tests/calibration/test-screenshot-calibration.py

Features:
- Loads calibration data from config file
- Displays transparent overlay showing all detected slot positions
- Highlights each slot with its number and coordinates
- Allows you to test clicking on specific slots
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import threading
import random as rnd

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.movements import bezierMove
from utils.clicker import click
from utils.item_slots import load_inventory_config

# Configuration file path
CONFIG_FILE = os.path.join(project_root, 'config', 'inventory_config.json')

class ScreenshotCalibrationTest(tk.Tk):
    """GUI for testing screenshot-based inventory slot calibration."""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Screenshot Calibration Test")
        self.geometry("400x600")
        self.attributes('-topmost', True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Success.TLabel", font=("Arial", 10), foreground="green")
        self.style.configure("Warning.TLabel", font=("Arial", 10), foreground="red")
        
        # Main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_label = ttk.Label(
            self.main_frame, 
            text="Screenshot Calibration Test",
            style="Header.TLabel"
        )
        self.header_label.pack(pady=(0, 20))
        
        # Configuration info
        self.config_frame = ttk.LabelFrame(
            self.main_frame,
            text="Current Configuration",
            padding=10
        )
        self.config_frame.pack(fill=tk.X, pady=10)
        
        # Load configuration
        self.config = load_inventory_config()
        
        # Display configuration
        self.base_label = ttk.Label(
            self.config_frame,
            text=f"Base coordinates: ({self.config['base_x']}, {self.config['base_y']})"
        )
        self.base_label.pack(anchor=tk.W)
        
        self.spacing_label = ttk.Label(
            self.config_frame,
            text=f"Spacing: {self.config['x_spacing']}px horizontal, {self.config['y_spacing']}px vertical"
        )
        self.spacing_label.pack(anchor=tk.W)
        
        # Test options frame
        self.options_frame = ttk.LabelFrame(
            self.main_frame,
            text="Test Options",
            padding=10
        )
        self.options_frame.pack(fill=tk.X, pady=10)
        
        # Button frame for main actions
        self.button_frame = ttk.Frame(self.options_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # Show overlay button
        self.show_overlay_btn = ttk.Button(
            self.button_frame,
            text="Show Slot Overlay",
            command=self.show_slot_overlay
        )
        self.show_overlay_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Test click button
        self.test_click_btn = ttk.Button(
            self.button_frame,
            text="Test Click Slot",
            command=self.test_click_slot
        )
        self.test_click_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Slot selection
        self.slot_frame = ttk.Frame(self.options_frame)
        self.slot_frame.pack(fill=tk.X, pady=5)
        
        self.slot_label = ttk.Label(
            self.slot_frame,
            text="Select slot (1-28):"
        )
        self.slot_label.pack(side=tk.LEFT, padx=5)
        
        self.slot_var = tk.StringVar(value="1")
        self.slot_spinbox = ttk.Spinbox(
            self.slot_frame,
            from_=1,
            to=28,
            width=5,
            textvariable=self.slot_var
        )
        self.slot_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready to test inventory slots"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Result display
        self.result_frame = ttk.LabelFrame(
            self.main_frame,
            text="Test Results",
            padding=10
        )
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(
            self.result_frame,
            height=10,
            width=50,
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        self.close_btn = ttk.Button(
            self.main_frame,
            text="Close",
            command=self.quit
        )
        self.close_btn.pack(pady=10)
        
        # Overlay window
        self.overlay = None
        
        # Check if config file exists
        if not os.path.exists(CONFIG_FILE):
            self.status_label.configure(
                text="No configuration found! Please run screenshot-calibrate.py first.", 
                style="Warning.TLabel"
            )
            messagebox.showwarning(
                "Configuration Missing", 
                "No inventory configuration found.\nPlease run screenshot-calibrate.py first."
            )
    
    def show_slot_overlay(self):
        """Show transparent overlay with inventory slot positions."""
        # Close existing overlay if open
        if self.overlay:
            self.overlay.destroy()
        
        # Create new overlay window
        self.overlay = tk.Toplevel(self)
        self.overlay.title("Inventory Slots Overlay")
        self.overlay.attributes('-alpha', 0.8)  # 20% transparent
        self.overlay.attributes('-topmost', True)
        
        # Create canvas for drawing slots
        canvas = tk.Canvas(
            self.overlay,
            width=400,
            height=500,
            bg="lightgray"
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw each inventory slot
        base_x = self.config['base_x']
        base_y = self.config['base_y']
        x_spacing = self.config['x_spacing']
        y_spacing = self.config['y_spacing']
        
        # Calculate offsets for overlay window positioning
        min_x = base_x
        min_y = base_y
        max_x = base_x + (3 * x_spacing)
        max_y = base_y + (6 * y_spacing)
        
        # Position overlay near the inventory
        overlay_x = min_x - 50
        overlay_y = min_y - 50
        overlay_width = (max_x - min_x) + 100
        overlay_height = (max_y - min_y) + 100
        
        # Set overlay size and position
        self.overlay.geometry(f"{overlay_width}x{overlay_height}+{overlay_x}+{overlay_y}")
        
        # Draw slots
        for slot in range(1, 29):
            # Convert to 0-based index
            idx = slot - 1
            row = idx // 4
            col = idx % 4
            
            # Calculate slot position
            x = base_x + (col * x_spacing) - overlay_x
            y = base_y + (row * y_spacing) - overlay_y
            
            # Draw slot rectangle
            rect_size = 30  # Size of the rectangle
            rect_x = x - rect_size // 2
            rect_y = y - rect_size // 2
            
            canvas.create_rectangle(
                rect_x, rect_y,
                rect_x + rect_size, rect_y + rect_size,
                fill="orange",
                outline="black",
                width=2
            )
            
            # Draw slot number
            canvas.create_text(
                x, y,
                text=str(slot),
                fill="black",
                font=("Arial", 10, "bold")
            )
            
            # Draw coordinates below
            canvas.create_text(
                x, y + rect_size // 2 + 10,
                text=f"({base_x + col * x_spacing}, {base_y + row * y_spacing})",
                fill="black",
                font=("Arial", 8)
            )
        
        # Add close button to overlay
        close_btn = ttk.Button(
            self.overlay,
            text="Close Overlay",
            command=self.overlay.destroy
        )
        close_btn.pack(side=tk.BOTTOM, pady=10)
        
        self.status_label.configure(text="Overlay displayed")
        self.result_text.insert(tk.END, "Displaying overlay of all 28 inventory slots\n")
        self.result_text.see(tk.END)
    
    def test_click_slot(self):
        """Test clicking on a specific inventory slot."""
        try:
            # Get selected slot
            slot = int(self.slot_var.get())
            
            if not 1 <= slot <= 28:
                messagebox.showerror("Error", "Slot must be between 1 and 28")
                return
            
            # Update status
            self.status_label.configure(text=f"Testing click on slot {slot}...")
            
            # Calculate slot position
            base_x = self.config['base_x']
            base_y = self.config['base_y']
            x_spacing = self.config['x_spacing']
            y_spacing = self.config['y_spacing']
            
            # Convert to 0-based index
            idx = slot - 1
            row = idx // 4
            col = idx % 4
            
            # Calculate slot coordinates
            x = base_x + (col * x_spacing)
            y = base_y + (row * y_spacing)
            
            # Add small random variance
            z = 8
            x += rnd.randint(-z, z)
            y += rnd.randint(-z, z)
            
            # Log info
            self.result_text.insert(tk.END, f"Clicking slot {slot} at ({x}, {y})\n")
            self.result_text.see(tk.END)
            
            # Move mouse and click in a new thread to avoid freezing GUI
            thread = threading.Thread(target=self.perform_click, args=(x, y))
            thread.daemon = True
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid slot number")
    
    def perform_click(self, x, y):
        """Perform the actual mouse movement and click."""
        try:
            # Move to slot
            bezierMove(x, y)
            
            # Wait briefly
            time.sleep(0.2)
            
            # Click
            click()
            
            # Update status
            self.status_label.configure(text=f"Click completed at ({x}, {y})")
            self.result_text.insert(tk.END, f"Click successful at ({x}, {y})\n")
            self.result_text.see(tk.END)
            
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            self.result_text.insert(tk.END, f"Error: {str(e)}\n")
            self.result_text.see(tk.END)

def main():
    """Run the screenshot calibration test GUI."""
    app = ScreenshotCalibrationTest()
    app.mainloop()

if __name__ == "__main__":
    main() 