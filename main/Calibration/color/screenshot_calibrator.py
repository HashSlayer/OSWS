"""
Screenshot-based Inventory Calibration GUI

This module provides a graphical interface for calibrating inventory slots 
using screenshots with highlighted borders. It detects the orange highlights 
and calculates the grid parameters automatically.

Uses the utilities from utils.calibration.vision for detection and configuration.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
from pynput.keyboard import Key, Listener

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.calibration.vision import take_screenshot, detect_inventory_slots, save_debug_image
from utils.calibration.config import (
    load_inventory_config, 
    save_inventory_config, 
    reset_inventory_config,
    DEFAULT_INVENTORY_CONFIG
)

class ScreenshotCalibratorGUI(tk.Tk):
    """
    GUI for the screenshot-based calibration tool.
    
    Provides a simple interface for triggering screenshot calibration
    and displays the results.
    """
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Inventory Screenshot Calibrator")
        self.geometry("500x500")  # Increased height for new buttons
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"), background="#f0f0f0")
        self.style.configure("Result.TLabel", font=("Consolas", 10), background="#f0f0f0")
        self.style.configure("Warning.TLabel", font=("Arial", 10), foreground="red", background="#f0f0f0")
        self.style.configure("Success.TLabel", font=("Arial", 10), foreground="green", background="#f0f0f0")
        
        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_label = ttk.Label(
            self.main_frame, 
            text="Inventory Screenshot Calibrator",
            style="Header.TLabel"
        )
        self.header_label.pack(pady=(0, 20))
        
        # Instructions
        instructions = [
            "This tool will detect inventory slots using a screenshot.",
            "",
            "Instructions:",
            "1. Make sure your inventory is open and visible",
            "2. Ensure inventory slots are highlighted (click on an item)",
            "3. Press LEFT CTRL key to capture a screenshot",
            "4. Review the detected coordinates before saving",
            "",
            "Note: The highlighted border should be orange (#FFFF6A00)"
        ]
        
        for instruction in instructions:
            label = ttk.Label(self.main_frame, text=instruction, justify=tk.LEFT)
            label.pack(anchor=tk.W)
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=20)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Ready - Press LEFT CTRL to capture screenshot",
            font=("Arial", 10, "italic")
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Detection Results",
            padding=10
        )
        self.results_frame.pack(fill=tk.X, pady=10)
        
        # Results labels
        self.base_coord_label = ttk.Label(
            self.results_frame, 
            text="Base coordinates: Not detected",
            style="Result.TLabel"
        )
        self.base_coord_label.pack(anchor=tk.W)
        
        self.spacing_label = ttk.Label(
            self.results_frame, 
            text="Spacing: Not detected", 
            style="Result.TLabel"
        )
        self.spacing_label.pack(anchor=tk.W)
        
        self.detected_slots_label = ttk.Label(
            self.results_frame, 
            text="Detected slots: N/A", 
            style="Result.TLabel"
        )
        self.detected_slots_label.pack(anchor=tk.W)
        
        # Current config frame
        self.current_config_frame = ttk.LabelFrame(
            self.main_frame,
            text="Current Configuration",
            padding=10
        )
        self.current_config_frame.pack(fill=tk.X, pady=10)
        
        # Load and display current config
        self.current_config = load_inventory_config()
        
        self.current_base_label = ttk.Label(
            self.current_config_frame,
            text=f"Base coordinates: ({self.current_config['base_x']}, {self.current_config['base_y']})",
            style="Result.TLabel"
        )
        self.current_base_label.pack(anchor=tk.W)
        
        self.current_spacing_label = ttk.Label(
            self.current_config_frame,
            text=f"Spacing: {self.current_config['x_spacing']}px horizontal, {self.current_config['y_spacing']}px vertical",
            style="Result.TLabel"
        )
        self.current_spacing_label.pack(anchor=tk.W)
        
        # Save status label
        self.save_status_label = ttk.Label(
            self.main_frame,
            text="",
            style="Warning.TLabel"
        )
        self.save_status_label.pack(pady=5)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        # Save button - Initially disabled
        self.save_btn = ttk.Button(
            self.button_frame,
            text="Save New Configuration",
            command=self.save_configuration,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Revert to defaults button
        self.revert_btn = ttk.Button(
            self.button_frame,
            text="Revert to Defaults",
            command=self.revert_to_defaults
        )
        self.revert_btn.pack(side=tk.LEFT, padx=5)
        
        # View debug button - Initially disabled
        self.debug_btn = ttk.Button(
            self.button_frame,
            text="View Debug Images",
            command=self.view_debug_images,
            state=tk.DISABLED
        )
        self.debug_btn.pack(side=tk.LEFT, padx=5)
        
        # Bottom button frame
        self.bottom_button_frame = ttk.Frame(self.main_frame)
        self.bottom_button_frame.pack(pady=5)
        
        # Close button
        self.close_btn = ttk.Button(
            self.bottom_button_frame,
            text="Close",
            command=self.quit
        )
        self.close_btn.pack()
        
        # Calibration thread and results
        self.calibration_thread = None
        self.calibration_results = None
        self.screenshot = None
        
        # Set up keyboard listener for LEFT CTRL
        self.keyboard_listener = Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        # Flag to prevent multiple screenshots while processing
        self.processing = False
    
    def on_key_press(self, key):
        """Handle key press events, looking for LEFT CTRL to trigger screenshot."""
        if key == Key.ctrl_l and not self.processing:
            self.start_calibration()
    
    def start_calibration(self):
        """Start the calibration process in a separate thread."""
        if self.processing:
            return
            
        self.processing = True
        self.save_btn.configure(state=tk.DISABLED)
        self.revert_btn.configure(state=tk.DISABLED)
        self.debug_btn.configure(state=tk.DISABLED)
        self.close_btn.configure(state=tk.DISABLED)
        
        self.status_label.configure(text="Taking screenshot now...")
        self.update_progress(10)
        self.save_status_label.configure(text="")
        
        # Start calibration in a separate thread
        self.calibration_thread = threading.Thread(target=self.perform_calibration)
        self.calibration_thread.daemon = True
        self.calibration_thread.start()
        
        # Check thread status periodically
        self.after(100, self.check_calibration)
    
    def perform_calibration(self):
        """Perform the actual calibration."""
        try:
            # Take screenshot and save for debugging
            self.update_progress_threadsafe(20)
            self.screenshot = take_screenshot()
            
            if self.screenshot is None:
                self.update_status_threadsafe("Error: Failed to take screenshot")
                return
                
            self.update_progress_threadsafe(40)
            save_debug_image(self.screenshot, "screenshot.png")
            
            # Detect inventory slots
            self.update_status_threadsafe("Detecting inventory slots...")
            self.calibration_results = detect_inventory_slots(self.screenshot)
            
            self.update_progress_threadsafe(100)
            
            if self.calibration_results:
                self.update_status_threadsafe("Detection successful! Review results before saving.")
            else:
                self.update_status_threadsafe("Detection failed. Check debug images for details.")
                
        except Exception as e:
            self.update_status_threadsafe(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def check_calibration(self):
        """Check if the calibration thread has finished."""
        if self.calibration_thread and not self.calibration_thread.is_alive():
            self.calibration_thread = None
            self.close_btn.configure(state=tk.NORMAL)
            self.revert_btn.configure(state=tk.NORMAL)
            self.processing = False
            
            if self.calibration_results:
                self.save_btn.configure(state=tk.NORMAL)
                self.debug_btn.configure(state=tk.NORMAL)
                self.update_results()
            
        else:
            self.after(100, self.check_calibration)
    
    def update_results(self):
        """Update the results display with calibration data."""
        if not self.calibration_results:
            return
            
        self.base_coord_label.configure(
            text=f"Base coordinates: ({self.calibration_results['base_x']}, {self.calibration_results['base_y']})"
        )
        
        self.spacing_label.configure(
            text=f"Spacing: {self.calibration_results['x_spacing']}px horizontal, {self.calibration_results['y_spacing']}px vertical"
        )
        
        self.detected_slots_label.configure(
            text=f"Detected slots: {self.calibration_results['num_detected_slots']} (expected: 28)"
        )
    
    def save_configuration(self):
        """Save the detected configuration to the config file."""
        if not self.calibration_results:
            return
        
        try:
            # Save only the necessary keys
            config_to_save = {
                'base_x': self.calibration_results['base_x'],
                'base_y': self.calibration_results['base_y'],
                'x_spacing': self.calibration_results['x_spacing'],
                'y_spacing': self.calibration_results['y_spacing']
            }
            
            # Save to file using utility
            if save_inventory_config(config_to_save):
                self.save_status_label.configure(
                    text="Configuration saved successfully!",
                    style="Success.TLabel"
                )
                
                # Update current config display
                self.current_config = config_to_save
                self.current_base_label.configure(
                    text=f"Base coordinates: ({self.current_config['base_x']}, {self.current_config['base_y']})"
                )
                self.current_spacing_label.configure(
                    text=f"Spacing: {self.current_config['x_spacing']}px horizontal, {self.current_config['y_spacing']}px vertical"
                )
            else:
                self.save_status_label.configure(
                    text="Failed to save configuration!",
                    style="Warning.TLabel"
                )
                
        except Exception as e:
            self.save_status_label.configure(
                text=f"Error saving configuration: {str(e)}",
                style="Warning.TLabel"
            )
    
    def revert_to_defaults(self):
        """Revert to default inventory configuration."""
        try:
            # Save default configuration using utility
            if reset_inventory_config():
                self.save_status_label.configure(
                    text="Reverted to default configuration!",
                    style="Success.TLabel"
                )
                
                # Update current config display
                self.current_config = DEFAULT_INVENTORY_CONFIG.copy()
                self.current_base_label.configure(
                    text=f"Base coordinates: ({self.current_config['base_x']}, {self.current_config['base_y']})"
                )
                self.current_spacing_label.configure(
                    text=f"Spacing: {self.current_config['x_spacing']}px horizontal, {self.current_config['y_spacing']}px vertical"
                )
            else:
                self.save_status_label.configure(
                    text="Failed to revert to defaults!",
                    style="Warning.TLabel"
                )
                
        except Exception as e:
            self.save_status_label.configure(
                text=f"Error reverting to defaults: {str(e)}",
                style="Warning.TLabel"
            )
    
    def update_progress(self, value):
        """Update the progress bar."""
        self.progress["value"] = value
        self.update_idletasks()
    
    def update_status_threadsafe(self, text):
        """Update the status label from a non-main thread."""
        self.after(0, lambda: self.status_label.configure(text=text))
        
    def update_progress_threadsafe(self, value):
        """Update the progress bar from a non-main thread."""
        self.after(0, lambda: self.update_progress(value))
    
    def view_debug_images(self):
        """Open debug images in the default image viewer."""
        try:
            debug_dir = os.path.join(project_root, 'debug')
            
            # Just open the directory in explorer for now
            if sys.platform == 'win32':
                os.startfile(debug_dir)
            elif sys.platform == 'darwin':
                import subprocess
                subprocess.Popen(['open', debug_dir])
            else:
                import subprocess
                subprocess.Popen(['xdg-open', debug_dir])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open debug images: {str(e)}")
    
    def quit(self):
        """Clean up and exit."""
        try:
            # Stop the keyboard listener
            if hasattr(self, 'keyboard_listener'):
                self.keyboard_listener.stop()
        finally:
            super().quit()

def main():
    """Run the screenshot calibrator GUI."""
    app = ScreenshotCalibratorGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
