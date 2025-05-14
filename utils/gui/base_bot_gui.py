import tkinter as tk
from tkinter import font as tkFont
from pynput.keyboard import Listener, Key
import threading
from datetime import datetime
import os
import random

class BaseBotGUI:
    def __init__(self, bot_name="Bot", bot_function=None):
        """
        Initialize base GUI for bots
        :param bot_name: Name to display in the title
        :param bot_function: The main bot function to run (e.g., walker)
        """
        self.bot_function = bot_function
        self.running = False
        self.running_lock = threading.Lock()
        self.bot_thread = None
        self.walk_count = 0
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(f"{bot_name} Status")
        self.root.geometry("1530x710")
        self.setup_gui()
        
        # Initialize keyboard listener
        self.listener = Listener(on_press=self._on_key_press)
        self.listener.start()
        
    def generate_random_color(self):
        """Generate a random vibrant color"""
        # Generate random RGB values but ensure they're vibrant
        r = random.randint(100, 255)  # Ensure some red component
        g = random.randint(100, 255)  # Ensure some green component
        b = random.randint(100, 255)  # Ensure some blue component
        return f'#{r:02x}{g:02x}{b:02x}'
        
    def setup_gui(self):
        """Setup the GUI components"""
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
        
        # Start time updates
        self.update_time()
        
        # Start gradient color updates
        self.update_gradient_color()
        
    def create_gradient_background(self):
        """Create gradient background canvas"""
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.background_color_start = "#FF6B6B"  # Fixed top color
        self.background_color_end = self.generate_random_color()  # Random bottom color
        self.on_resize(None)
        
    def update_gradient_color(self):
        """Update the bottom gradient color periodically"""
        self.background_color_end = self.generate_random_color()
        self.on_resize(None)
        # Update every 5 seconds
        self.root.after(5000, self.update_gradient_color)
        
    def create_top_frame(self):
        """Create the top frame with controls"""
        top_frame = tk.Frame(self.canvas, bg='#FF6B6B')
        top_frame.pack(padx=15, pady=15)
        
        # Date and Time
        self.date_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg=self.text_color, 
                                 font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.date_label.pack(side="left", padx=(80, 2))
        
        self.time_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg=self.text_color,
                                 font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.time_label.pack(side="left", padx=2)
        
        # Max Walks Entry
        tk.Label(top_frame, text="Max Walks:", bg="#FF6B6B", fg=self.text_color,
                font=self.custom_font).pack(side=tk.LEFT, padx=(10, 0))
        self.max_walks_entry = tk.Entry(top_frame, width=7, bg="#FFFAE4", fg="#217BFF",
                                      font=self.custom_font, relief=tk.SUNKEN, borderwidth=1)
        self.max_walks_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.max_walks_entry.insert(0, "420")
        
        # Control Buttons
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot,
                                   bg=self.button_color, fg=self.text_color, font=self.custom_font)
        self.kill_button.pack(side=tk.RIGHT, padx=9)
        
        self.start_button = tk.Button(top_frame, text="START", command=self.toggle_bot,
                                    bg=self.button_color, fg=self.text_color, font=self.custom_font)
        self.start_button.pack(side=tk.RIGHT, padx=9)
        
        # Track Clicks Button
        self.track_clicks_button = tk.Button(top_frame, text="Track Clicks: OFF",
                                           command=self.toggle_click_tracking,
                                           bg=self.button_color, fg=self.text_color,
                                           font=self.custom_font)
        self.track_clicks_button.pack(side=tk.LEFT, padx=9)
        
    def create_text_boxes(self):
        """Create the main text box and notepad"""
        self.pane = tk.PanedWindow(self.canvas, bd=0, sashwidth=3, orient=tk.HORIZONTAL, bg='#4D96FF')
        self.pane.pack(fill=tk.BOTH, expand=True, padx=33, pady=23)
        
        # Main text box
        self.text_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF",
                               font=("Consolas", 13), relief="sunken", borderwidth=5)
        self.pane.add(self.text_box, stretch="always")
        self.write_welcome_message()
        
        # Notepad
        self.notepad = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF",
                              font=("Consolas", 12), relief="sunken", borderwidth=5)
        self.pane.add(self.notepad, width=444)
        self.load_notepad()
        
    def write_welcome_message(self):
        """Write the welcome message to the text box"""
        welcome_text = [
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
            "      Welcome to the Bot",
            "    ❤️ Press the [left CTRL] key to toggle the bot OFF/ON",
            "    ❤️ Press the [right CTRL] key to Kill the bot",
            "    ❤️ Enjoy your walk!",
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        ]
        for line in welcome_text:
            self.append_message(line)
            
    def update_time(self):
        """Update the date and time display"""
        now = datetime.now()
        self.date_label.config(text=now.strftime(" %B %d, %Y "))
        self.time_label.config(text=now.strftime(" %H:%M:%S") + ".{:03d} ".format(now.microsecond // 1000))
        self.root.after(50, self.update_time)
        
    def on_resize(self, event):
        """Handle window resize events"""
        width = event.width if event else self.root.winfo_reqwidth()
        height = event.height if event else self.root.winfo_reqheight()
        self.canvas.delete("gradient")
        self.create_gradient(width, height)
        
    def create_gradient(self, width, height):
        """Create the gradient background"""
        for i in range(height):
            # Calculate color components
            ratio = i / height
            r = int((1-ratio) * int(self.background_color_start[1:3], 16) + 
                   ratio * int(self.background_color_end[1:3], 16))
            g = int((1-ratio) * int(self.background_color_start[3:5], 16) + 
                   ratio * int(self.background_color_end[3:5], 16))
            b = int((1-ratio) * int(self.background_color_start[5:7], 16) + 
                   ratio * int(self.background_color_end[5:7], 16))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)
            
    def toggle_click_tracking(self):
        """Toggle click tracking"""
        self.click_tracking = not getattr(self, 'click_tracking', False)
        self.track_clicks_button.config(
            text=f"Track Clicks: {'ON' if self.click_tracking else 'OFF'}",
            bg="#2ECC73" if self.click_tracking else self.button_color
        )
        
    def toggle_bot(self):
        """Toggle the bot on/off"""
        with self.running_lock:
            self.running = not self.running
            if self.running:
                if self.bot_function:
                    self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
                    self.bot_thread.start()
                self.start_button.config(text="STOP", bg="#FF6B6B")
                self.append_message("Bot Started")
            else:
                self.start_button.config(text="START", bg="#2ECC73")
                self.append_message("Bot Stopped")
                
    def _run_bot(self):
        """Wrapper for the bot function that handles the running state"""
        while self.running:
            if self.bot_function:
                try:
                    max_walks = int(self.max_walks_entry.get())
                    if self.walk_count >= max_walks:
                        self.running = False
                        self.append_message(f"Reached maximum walks ({max_walks}). Stopping bot.")
                        self.root.after(0, lambda: self.start_button.config(text="START", bg="#2ECC73"))
                        break
                except ValueError:
                    self.append_message("Invalid max walks value. Using default.")
                self.bot_function(self)
                
    def kill_bot(self):
        """Kill the bot and close the GUI"""
        with self.running_lock:
            self.running = False
        self.save_notepad()
        self.append_message("Bot killed! Cleaning up...")
        self.root.after(500, self.root.destroy)
        
    def append_message(self, message):
        """Append a message to the text box"""
        self.text_box.insert(tk.END, f"{message}\n")
        self.text_box.see(tk.END)
        
    def save_notepad(self):
        """Save notepad contents"""
        with open("notepad_content.txt", "w") as file:
            file.write(self.notepad.get("1.0", tk.END))
            
    def load_notepad(self):
        """Load notepad contents"""
        self.notepad.insert(tk.END, "Notes:\n")
        if os.path.exists("notepad_content.txt"):
            with open("notepad_content.txt", "r") as file:
                self.notepad.delete("1.0", tk.END)
                self.notepad.insert(tk.END, file.read())
                
    def _on_key_press(self, key):
        """Handle keyboard controls"""
        if key == Key.ctrl_l:  # Toggle
            self.toggle_bot()
        elif key == Key.ctrl_r:  # Kill
            self.kill_bot()
            return False
            
    def run(self):
        """Start the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.kill_bot)
        self.root.mainloop() 