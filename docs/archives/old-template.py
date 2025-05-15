import os
import sys
import threading
from datetime import datetime
from pynput.keyboard import Key, Listener
import tkinter as tk
from tkinter import font as tkFont

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import utilities
from utils.core.timing import *
from utils.core.welcome import welcome
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.utils.click_tracker import ClickTracker

welcome()

# Global variables to control the bot state
running = False
running_lock = threading.Lock()

# Define control keys
ONOFF = Key.ctrl_l  # Left Control key for toggle
KILL = Key.ctrl_r   # Right Control key for kill

class TemplateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Template Bot")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("1530x710")
        
        # GUI setup
        self.setup_gui()
        self.apply_style()
        
        # Create layout
        self.create_top_frame()
        self.create_text_boxes()
        
        # Initialize click tracker
        self.click_tracker = ClickTracker(self.append_message, self.canvas)
        self.click_tracker_thread = None
        self.click_tracking_enabled = False
        
        # Initialize bot state
        self.running = False
        self.bot_thread = None
        self.iterations = 0
        
        # Start time display updates
        self.update_time()

    def setup_gui(self):
        self.background_color_start = "#FF6B6B"
        self.background_color_end = "#4D96FF"
        self.create_gradient_background()

    def apply_style(self):
        self.bg_color = "#4D96FF"
        self.button_color = "#FF6B6B"
        self.text_color = "#99E1A2"
        self.hover_color = "#F55C47"
        self.custom_font = tkFont.Font(family="Consolas", size=13, weight="bold")
        self.root.configure(bg=self.bg_color)

    def create_gradient(self, canvas, color1, color2, width, height):
        for i in range(height):
            r1, g1, b1 = canvas.winfo_rgb(color1)
            r2, g2, b2 = canvas.winfo_rgb(color2)
            r = (r1 + int((r2 - r1) * i / height)) & 0xff00
            g = (g1 + int((g2 - g1) * i / height)) & 0xff00
            b = (b1 + int((b2 - b1) * i / height)) & 0xff00
            color = f'#{r:04x}{g:04x}{b:04x}'
            canvas.create_line(0, i, width, i, fill=color)

    def create_gradient_background(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.on_resize(None)

    def update_time(self):
        now = datetime.now()
        date_str = now.strftime(" %B %d, %Y ")
        time_str = now.strftime(" %H:%M:%S") + ".{:03d} ".format(now.microsecond // 1000)
        self.date_label.config(text=date_str)
        self.time_label.config(text=time_str)
        self.root.after(50, self.update_time)

    def create_text_boxes(self):
        # Main text area with logs and notes
        self.pane = tk.PanedWindow(self.canvas, bd=0, sashwidth=3, orient=tk.HORIZONTAL, bg='#4D96FF')
        self.pane.pack(fill=tk.BOTH, expand=True, padx=33, pady=23)

        # Log text box
        self.text_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF",
                               font=("Consolas", 13), insertbackground="#5BCB77",
                               relief="sunken", borderwidth=5, height=10)
        self.pane.add(self.text_box, stretch="always")
        
        # Welcome message
        welcome_text = """
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      Welcome to Template Bot
    ❤️ Press the [left CTRL] key to toggle bot ON/OFF
    ❤️ Press the [right CTRL] key to exit
    ❤️ Happy botting!
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
        self.text_box.insert(tk.END, welcome_text)

        # Notes text box
        self.notes_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF",
                                font=("Consolas", 12), relief="sunken",
                                borderwidth=5, height=10)
        self.pane.add(self.notes_box, width=444)
        self.notes_box.insert(tk.END, "Notes:\n")

    def on_resize(self, event):
        width = event.width if event else self.root.winfo_reqwidth()
        height = event.height if event else self.root.winfo_reqheight()
        self.canvas.delete("gradient")
        self.create_gradient(self.canvas, self.background_color_start,
                           self.background_color_end, width, height)

    def create_top_frame(self):
        # Top frame with controls
        top_frame = tk.Frame(self.canvas, bg='#FF6B6B')
        top_frame.pack(padx=15, pady=15)

        # Date and time display
        self.date_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg='#97E469',
                                 font=("Consolas", 13, "bold"),
                                 relief=tk.RAISED, borderwidth=1)
        self.date_label.pack(side="left", padx=(80, 2))
        
        self.time_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg='#97E469',
                                 font=("Consolas", 13, "bold"),
                                 relief=tk.RAISED, borderwidth=1)
        self.time_label.pack(side="left", padx=2)

        # Styles for inputs
        label_style = {"bg": "#FF6B6B", "fg": "#97E469",
                      "font": self.custom_font,
                      "relief": tk.FLAT, "borderwidth": 0}
        entry_style = {"bg": "#FFFAE4", "fg": "#217BFF",
                      "font": self.custom_font,
                      "relief": tk.SUNKEN, "borderwidth": 1}

        # Iterations display
        tk.Label(top_frame, text="Iterations:", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.iterations_label = tk.Label(top_frame, text="0", **label_style)
        self.iterations_label.pack(side=tk.LEFT, padx=(3, 10))

        # Control buttons
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot,
                                   bg=self.button_color, fg='#97E469',
                                   font=self.custom_font,
                                   activebackground=self.hover_color,
                                   relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=9)

        self.start_button = tk.Button(top_frame, text="Start / Stop",
                                    command=self.toggle_bot,
                                    bg=self.button_color, fg='#97E469',
                                    font=self.custom_font,
                                    activebackground='#C8F6AD',
                                    relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=9)

        # Click tracking button
        self.track_clicks_button = tk.Button(top_frame, text="Track Clicks: OFF",
                                           command=self.toggle_click_tracking,
                                           bg=self.button_color, fg='#97E469',
                                           font=self.custom_font)
        self.track_clicks_button.pack(side=tk.LEFT, padx=9)

    def append_message(self, message):
        self.text_box.insert(tk.END, f"{message}\n")
        self.text_box.see(tk.END)

    def toggle_click_tracking(self):
        self.click_tracking_enabled = not self.click_tracking_enabled
        
        if self.click_tracking_enabled:
            if not self.click_tracker.tracking:
                self.click_tracker_thread = threading.Thread(target=self.click_tracker.run)
                self.click_tracker_thread.daemon = True
                self.click_tracker_thread.start()
            self.click_tracker.process_clicks = True
            self.track_clicks_button.config(text="Track Clicks: ON", bg="#2ECC73")
        else:
            self.click_tracker.process_clicks = False
            self.track_clicks_button.config(text="Track Clicks: OFF", bg=self.button_color)

    def toggle_bot(self):
        self.running = not self.running
        if self.running:
            self.append_message("Bot started")
            self.start_button.config(text="Stop", bg="#FF6B6B")
            if self.bot_thread is None or not self.bot_thread.is_alive():
                self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
                self.bot_thread.start()
        else:
            self.append_message("Bot stopped")
            self.start_button.config(text="Start", bg="#09C159")

    def bot_loop(self):
        """Main bot loop - override this in your bot implementation"""
        while self.running:
            try:
                # Example bot action
                sleep(1)
                self.iterations += 1
                self.iterations_label.config(text=str(self.iterations))
                self.append_message(f"Iteration {self.iterations}")
                
            except Exception as e:
                self.append_message(f"Error: {str(e)}")
                self.running = False
                break

    def kill_bot(self):
        self.running = False
        
        # Stop click tracking
        if self.click_tracker:
            self.click_tracker.stop()
        
        if self.click_tracker_thread and self.click_tracker_thread.is_alive():
            try:
                self.click_tracker_thread.join(timeout=1.0)
            except Exception as e:
                print(f"Error stopping click tracker: {e}")
        
        # Update UI
        self.start_button.config(text="Start", bg="#09C159")
        self.kill_button.config(text="KILLED")
        self.append_message("Bot terminated")
        
        # Clean up bot thread
        if self.bot_thread and self.bot_thread.is_alive():
            try:
                self.bot_thread.join(timeout=1.0)
            except Exception as e:
                print(f"Error stopping bot thread: {e}")
        
        # Close GUI
        self.root.after(500, self.root.destroy)

    def on_close(self):
        self.kill_bot()

    def run(self):
        # Start keyboard listener
        self.listener = Listener(on_press=lambda key: self.on_key_press(key))
        self.listener.daemon = True
        self.listener.start()
        
        # Start GUI
        self.root.mainloop()

    def on_key_press(self, key):
        if key == ONOFF:
            self.toggle_bot()
        elif key == KILL:
            self.kill_bot()
            return False

def main():
    gui = TemplateGUI()
    try:
        gui.run()
    except KeyboardInterrupt:
        gui.kill_bot()

if __name__ == "__main__":
    main() 