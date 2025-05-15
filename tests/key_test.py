import os
import sys
import time
import threading
import statistics
from datetime import datetime
from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import defaultdict
import random

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils.clicker import *

class KeyPressAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Key Press Pattern Analysis")
        self.root.geometry("1400x800")
        
        # Controllers
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        
        # Tracking state
        self.is_recording = False
        self.bot_running = False
        self.bot_thread = None
        self.press_times = {}
        self.last_action_time = None
        self.intervals = []
        self.stats = defaultdict(list)
        
        # Separate tracking for human and bot data
        self.human_data = defaultdict(list)  # {key: [(timestamp, duration), ...]}
        self.bot_data = defaultdict(list)
        self.start_time = None
        
        self.setup_gui()
        self.setup_listeners()

    def setup_gui(self):
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left control panel
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        
        # Controls
        controls = ttk.LabelFrame(left_panel, text="Controls")
        controls.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(controls, text="Left Ctrl: Start/Stop Recording").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(controls, text="Right Ctrl: Quit").pack(anchor=tk.W, padx=5, pady=2)
        
        # Clear data button
        ttk.Button(controls, text="Clear All Data", command=self.clear_data).pack(fill=tk.X, padx=5, pady=5)
        
        # Bot controls
        bot_frame = ttk.LabelFrame(left_panel, text="Bot Settings")
        bot_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Bot speed
        speed_frame = ttk.Frame(bot_frame)
        speed_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(speed_frame, text="Delay (ms):").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="500")
        speed_entry = ttk.Entry(speed_frame, textvariable=self.speed_var, width=8)
        speed_entry.pack(side=tk.LEFT, padx=5)
        
        # Action selection
        action_frame = ttk.Frame(bot_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(action_frame, text="Actions:").pack(anchor=tk.W)
        
        self.action_vars = {}
        actions = [
            ("Keys 1-5", "keys"),
            ("Space", "space"),
            ("Left Click", "left_click"),
            ("Right Click", "right_click")
        ]
        for text, val in actions:
            var = tk.BooleanVar(value=True)
            self.action_vars[val] = var
            ttk.Checkbutton(action_frame, text=text, variable=var).pack(anchor=tk.W, padx=20)
        
        # Start/Stop button
        self.bot_button = ttk.Button(bot_frame, text="Start Bot", command=self.toggle_bot)
        self.bot_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Right panel for plots and log
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=3)
        
        # Plots
        self.setup_plots(right_panel)
        
        # Statistics/Analysis section
        stats_frame = ttk.LabelFrame(right_panel, text="Key Press Statistics (seconds)")
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=10, font=("Consolas", 10))
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
        self.stats_text.config(state=tk.DISABLED)
        
        # Log section
        log_frame = ttk.LabelFrame(right_panel, text="Action Log")
        log_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6)
        self.log_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - Press Left Ctrl to start recording")
        ttk.Label(self.root, textvariable=self.status_var).pack(pady=5)

    def setup_plots(self, parent):
        plot_frame = ttk.LabelFrame(parent, text="Key Pattern Analysis")
        plot_frame.pack(fill=tk.BOTH, expand=True)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.ax1.set_title('Human Key Press Durations')
        self.ax2.set_title('Bot Key Press Durations')
        
        # Set up common y-axis labels for both plots
        key_labels = ['1', '2', '3', '4', '5', 'space', 'left_click', 'right_click']
        self.ax1.set_yticks(range(len(key_labels)))
        self.ax1.set_yticklabels(key_labels)
        self.ax2.set_yticks(range(len(key_labels)))
        self.ax2.set_yticklabels(key_labels)
        
        plt.tight_layout()

    def setup_listeners(self):
        def on_press(key):
            if not self.is_recording:
                if key == Key.ctrl_l:
                    self.toggle_recording()
                elif key == Key.ctrl_r:
                    self.quit_application()
                return True

            try:
                # Convert the key to a string representation
                if hasattr(key, 'char'):
                    key_char = key.char
                elif key == Key.space:
                    key_char = 'space'
                else:
                    return True  # Ignore other special keys
                
                # Only track number keys 1-5 and space
                if key_char not in ['1', '2', '3', '4', '5', 'space']:
                    return True
                    
                self.press_times[key_char] = time.time()
                
                if self.last_action_time is not None:
                    interval = time.time() - self.last_action_time
                    self.intervals.append(interval)
                
            except AttributeError:
                pass
            return True

        def on_release(key):
            if not self.is_recording:
                return True
                
            try:
                # Convert the key to a string representation
                if hasattr(key, 'char'):
                    key_char = key.char
                elif key == Key.space:
                    key_char = 'space'
                else:
                    return True  # Ignore other special keys
                
                # Only track number keys 1-5 and space
                if key_char not in ['1', '2', '3', '4', '5', 'space']:
                    return True
                    
                if key_char in self.press_times:
                    duration = time.time() - self.press_times[key_char]
                    self.log_action(key_char, duration)
                    self.stats[key_char].append(duration)
                    self.last_action_time = time.time()
                    del self.press_times[key_char]
                    
            except AttributeError:
                pass
            return True

        def on_click(x, y, button, pressed):
            if not self.is_recording:
                return True
                
            button_name = "left_click" if button == Button.left else "right_click"
            
            if pressed:
                self.press_times[button_name] = time.time()
                if self.last_action_time is not None:
                    interval = time.time() - self.last_action_time
                    self.intervals.append(interval)
            else:
                if button_name in self.press_times:
                    duration = time.time() - self.press_times[button_name]
                    self.log_action(button_name, duration)
                    self.stats[button_name].append(duration)
                    self.last_action_time = time.time()
                    del self.press_times[button_name]
            
            return True

        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        status = "Recording..." if self.is_recording else "Recording stopped"
        self.status_var.set(status)
        
        # Initialize/reset timing variables when starting recording
        if self.is_recording:
            if self.start_time is None:  # Only reset start time if not already recording
                self.start_time = time.time()
            self.last_action_time = None
            self.intervals = []
        
        self.update_plots()
        self.update_statistics()

    def toggle_bot(self):
        if not self.bot_running:
            try:
                delay = max(100, int(self.speed_var.get()))  # Minimum 100ms delay
                self.speed_var.set(str(delay))
                
                self.bot_running = True
                self.bot_button.config(text="Stop Bot")
                self.bot_thread = threading.Thread(target=self.run_bot, args=(delay/1000,))
                self.bot_thread.daemon = True
                self.bot_thread.start()
                
            except ValueError:
                self.status_var.set("Invalid delay value")
        else:
            self.bot_running = False
            self.bot_button.config(text="Start Bot")
            if self.bot_thread:
                self.bot_thread.join(timeout=1.0)

    def get_human_like_duration(self, key_name):
        key_params = {
            '1': (0.12, 0.035),
            '2': (0.13, 0.037),
            '3': (0.11, 0.032),
            '4': (0.14, 0.040),
            '5': (0.10, 0.030),
            'space': (0.15, 0.045),
            'left_click': (0.09, 0.030),
            'right_click': (0.09, 0.030),
        }
        mean, stddev = key_params.get(key_name, (0.12, 0.035))
        duration = random.gauss(mean, stddev)
        # Outlier fast presses (6%)
        if random.random() < 0.06:
            duration = random.gauss(mean * 0.45, stddev * 0.5)
        # Outlier slow presses (6%)
        elif random.random() > 0.94:
            duration = random.gauss(mean * 2.2, stddev * 1.3)
        # Add a small right-skew for imperfection
        duration += abs(random.gauss(0, 0.005))
        return max(0.01, duration)

    def run_bot(self, delay):
        import os
        import sys
        import tempfile
        null_file = open(os.devnull, 'w')
        old_stdout = sys.stdout
        
        key_funcs = []
        if self.action_vars["keys"].get():
            key_funcs.extend([
                ('1', onekey), ('2', twokey), ('3', threekey),
                ('4', fourkey), ('5', fivekey)
            ])
        if self.action_vars["space"].get():
            key_funcs.append(('space', spacekey))
        if self.action_vars["left_click"].get():
            key_funcs.append(('left_click', lambda: click(0.01, True)))
        if self.action_vars["right_click"].get():
            key_funcs.append(('right_click', lambda: right_click(0.03, True)))
        
        try:
            while self.bot_running:
                for key_name, func in key_funcs:
                    if not self.bot_running:
                        break
                    sys.stdout = null_file
                    # Use human-like duration for this key
                    duration = self.get_human_like_duration(key_name)
                    start_time = time.time()
                    func()
                    # Sleep for the simulated key hold duration
                    time.sleep(duration)
                    sys.stdout = old_stdout
                    self.log_action(key_name, duration, is_bot=True)
                    time.sleep(delay)
        finally:
            sys.stdout = old_stdout
            null_file.close()

    def log_action(self, action, duration, is_bot=False):
        try:
            # Initialize start time if not set
            if self.start_time is None:
                self.start_time = time.time()
            
            # Store data
            current_time = time.time()
            if is_bot:
                self.bot_data[action].append((current_time, duration))
            else:
                self.human_data[action].append((current_time, duration))
            
            # Log entry
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            mode = "Bot" if is_bot else "Human"
            log_entry = f"[{mode}] {timestamp} - Action: {action}, Duration: {duration:.3f}s"
            
            # Use after to schedule the GUI update to avoid Tcl errors
            self.root.after(1, lambda: self.log_text.insert(tk.END, log_entry + '\n'))
            self.root.after(1, lambda: self.log_text.see(tk.END))
            
            # Update visualization and statistics
            self.root.after(1, self.update_plots)
            self.root.after(1, self.update_statistics)
            
        except Exception as e:
            print(f"Log action error: {e}")
            import traceback
            traceback.print_exc()

    def update_statistics(self):
        import statistics
        from collections import Counter
        key_labels = ['1', '2', '3', '4', '5', 'space', 'left_click', 'right_click']
        def get_stats(data):
            if not data:
                return {'mean': '-', 'median': '-', 'mode': '-', 'min': '-', 'max': '-', 'std': '-', 'n': 0}
            try:
                mean = statistics.mean(data)
                median = statistics.median(data)
                # Mode: use the most common bin (rounded to nearest 0.01)
                rounded = [round(x, 2) for x in data]
                mode = Counter(rounded).most_common(1)[0][0]
                minv = min(data)
                maxv = max(data)
                std = statistics.stdev(data) if len(data) > 1 else 0
                return {'mean': mean, 'median': median, 'mode': mode, 'min': minv, 'max': maxv, 'std': std, 'n': len(data)}
            except Exception:
                return {'mean': '-', 'median': '-', 'mode': '-', 'min': '-', 'max': '-', 'std': '-', 'n': len(data)}
        
        lines = []
        header = f"{'Key':<10}{'Source':<8}{'Mean':>8}{'Median':>8}{'Mode':>8}{'Min':>8}{'Max':>8}{'Std':>8}{'n':>6}"
        lines.append(header)
        lines.append('-'*len(header))
        for key in key_labels:
            # Human stats
            human_durations = [d for _, d in self.human_data.get(key, [])]
            h = get_stats(human_durations)
            lines.append(f"{key:<10}{'Human':<8}{h['mean']:>8.3f}{h['median']:>8.3f}{h['mode']:>8.3f}{h['min']:>8.3f}{h['max']:>8.3f}{h['std']:>8.3f}{h['n']:>6}" if h['n'] else f"{key:<10}{'Human':<8}{'-':>8}{'-':>8}{'-':>8}{'-':>8}{'-':>8}{'-':>8}{'0':>6}")
            # Bot stats
            bot_durations = [d for _, d in self.bot_data.get(key, [])]
            b = get_stats(bot_durations)
            lines.append(f"{key:<10}{'Bot':<8}{b['mean']:>8.3f}{b['median']:>8.3f}{b['mode']:>8.3f}{b['min']:>8.3f}{b['max']:>8.3f}{b['std']:>8.3f}{b['n']:>6}" if b['n'] else f"{key:<10}{'Bot':<8}{'-':>8}{'-':>8}{'-':>8}{'-':>8}{'-':>8}{'-':>8}{'0':>6}")
        
        # Update the stats text box
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, '\n'.join(lines))
        self.stats_text.config(state=tk.DISABLED)

    def update_plots(self):
        try:
            self.ax1.clear()
            self.ax2.clear()
            
            # Common setup
            key_labels = ['1', '2', '3', '4', '5', 'space', 'left_click', 'right_click']
            
            # Plot human data
            self.ax1.set_title('Human Key Press Durations')
            has_human_data = False
            for i, key in enumerate(key_labels):
                if key in self.human_data and self.human_data[key]:
                    has_human_data = True
                    data_points = self.human_data[key]
                    durations = [duration for _, duration in data_points]
                    # Create jittered y-positions for better visualization
                    y_positions = [i + np.random.normal(0, 0.1) for _ in durations]
                    self.ax1.scatter(durations, y_positions, alpha=0.6, 
                                   label=f'{key} (n={len(durations)})')
            
            if has_human_data:
                self.ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Plot bot data
            self.ax2.set_title('Bot Key Press Durations')
            has_bot_data = False
            for i, key in enumerate(key_labels):
                if key in self.bot_data and self.bot_data[key]:
                    has_bot_data = True
                    data_points = self.bot_data[key]
                    durations = [duration for _, duration in data_points]
                    # Create jittered y-positions for better visualization
                    y_positions = [i + np.random.normal(0, 0.1) for _ in durations]
                    self.ax2.scatter(durations, y_positions, alpha=0.6,
                                   label=f'{key} (n={len(durations)})')
            
            if has_bot_data:
                self.ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Common formatting
            for ax in [self.ax1, self.ax2]:
                ax.set_yticks(range(len(key_labels)))
                ax.set_yticklabels(key_labels)
                ax.set_xlabel('Duration (seconds)')
                ax.grid(True, alpha=0.3)
                ax.set_xlim(0, 1.0)  # Show durations up to 1 second
            
            # Adjust layout to prevent legend cutoff
            if has_human_data or has_bot_data:
                self.fig.subplots_adjust(right=0.85)
            else:
                self.fig.subplots_adjust(right=0.98)
                
            self.canvas.draw()
            
        except Exception as e:
            print(f"Plot update error: {e}")
            import traceback
            traceback.print_exc()

    def clear_data(self):
        self.human_data.clear()
        self.bot_data.clear()
        self.start_time = None
        self.log_text.delete(1.0, tk.END)
        self.update_plots()
        self.update_statistics()
        self.status_var.set("Data cleared")

    def quit_application(self):
        self.bot_running = False
        if self.bot_thread:
            self.bot_thread.join(timeout=1.0)
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KeyPressAnalyzer()
    app.run() 