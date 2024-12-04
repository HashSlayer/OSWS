import sys
import threading
import random as rnd
from pynput.keyboard import Listener, Key
from Utilities.MainFunctions import *
from Utilities.Movement import *
import tkinter as tk
from tkinter import font as tkFont
from datetime import datetime
from Utilities.Conffeti import *


# Global variables
running = False
running_lock = threading.Lock()
bot_thread = None
click_count, max_clicks, click_interval, interval_variance = 1, 420, 1, 0.1

ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program

welcome()

def SimulatedPause():
    global click_count
    sleep(0,0.9)
    if (rnd.random() > 0.05):
        sleep(.05, 2)
    gui.append_message("You have encountered Random sleep #1!")
    if (rnd.random() > 0.50):
        sleep(.1, 5)
    if (rnd.random() > 0.85):
        sleep(.2, 5)
    gui.append_message("You have encountered Random sleep #2!")
    if (rnd.random() > 0.93):
            sleep(.5, 9)
    gui.append_message("You have encountered Random sleep #3!")
    if (rnd.random() > 0.97):
        sleep(3, 80)
        gui.append_message("You have encountered Random sleep #4!")
    if ((rnd.random() > 0.9889) and (click_count > rnd.randint(1000, 2000))):
        sleep(1, rnd.randint(5, 60))
        print ("Time for a longer sleep!")

#=======================================================================================================================

# GUI Class
class AutoClickerGUI:
    # ... existing methods ...
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("@5MEkailO's Auto Clicker")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.apply_style()
        self.random_sleep_enabled = True
        self.double_click_enabled = False
        self.double_click_wait = tk.DoubleVar(value=0.9)
        self.spam_clicks_enabled = False
        self.alchemy_interval_cycles = False
        self.create_background_canvas()
        self.create_top_frame()
        self.create_text_box() #<3

    def create_background_canvas(self):
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)
        self.create_gradient(self.bg_canvas, "#9174BB", "#DCC6E0", self.root.winfo_screenwidth(), self.root.winfo_screenheight())

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

    def start_confetti_animation(self):
        startConfetti(self.bg_canvas)

    def apply_style(self):
        # Enhanced color palette
        self.bg_color = "#9174BB"  # Dark blue-gray
        self.button_color = "#2ECC71"  # Emerald green
        self.text_color = "#ECF0F1"  # Off-white
        self.hover_color = "#E74C3C"  # Soft red
        # Stylish font
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        # Set root window background color
        self.root.configure(bg=self.bg_color)

    def create_top_frame(self):
        # Create the top frame
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(padx=10, pady=10)

        # Date Label
        self.date_label = tk.Label(top_frame, text="", bg="#FFD30D", fg='#FF780D', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=2)
        self.date_label.pack(side="left", padx=(80, 2))  # Small separation between date and time

        # Time Label
        self.time_label = tk.Label(top_frame, text="", bg="#FFD30D", fg='#FF780D', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=2)
        self.time_label.pack(side="left", padx=2)

        # Label style with border
        label_style = {"bg": "#FFD30D", "fg": "#FF780D", "font": self.custom_font, "relief": tk.FLAT, "borderwidth": 3}

        # Click Every (Ct) Label and Entry
        tk.Label(top_frame, text="Click Interval: ", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.click_interval = tk.Entry(top_frame, width=5, font=self.custom_font)
        self.click_interval.pack(side=tk.LEFT, padx=(3, 10))
        self.click_interval.insert(0, "1.3")  # Default value

        # Random Multiplier (Xt) Label and Entry
        tk.Label(top_frame, text="(+/-): ", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.click_variance = tk.Entry(top_frame, width=5, font=self.custom_font)
        self.click_variance.pack(side=tk.LEFT, padx=(3, 10))
        self.click_variance.insert(0, "0.35")  # Default value

        # Max Clicks Label and Entry
        tk.Label(top_frame, text="Max Clicks: ", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.max_clicks_entry = tk.Entry(top_frame, width=7, font=self.custom_font)
        self.max_clicks_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.max_clicks_entry.insert(0, "2880")  # Default value

        # Kill Button
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot, bg='#FF6B6B', fg='#ECF0F1', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=5)

        # Start / Stop Button
        self.start_button = tk.Button(top_frame, text="  Start / Stop  ", command=self.toggle_bot, bg=self.button_color, fg='#FF780D', font=self.custom_font, activebackground='#28B065', relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=5)

        # Frame for toggle switches
        toggle_frame = tk.Frame(self.root, bg=self.bg_color)
        toggle_frame.pack(padx=10, pady=(0, 10))

        # Alchemy Interval Cycles Toggle Switch
        self.alchemy_interval_cycles_button = tk.Button(toggle_frame, text="Alchemy Interval Cycles: OFF", command=self.alchemy_interval_cycles, bg="#FF6B6B", fg='#ECF0F1', font=self.custom_font)
        self.alchemy_interval_cycles_button.pack(side=tk.LEFT, padx=(10, 2))

        # Random Breaks Toggle Switch
        self.toggle_button = tk.Button(toggle_frame, text="Random Breaks: OFF", command=self.toggle_sleeps, bg="#FF6B6B", fg='#ECF0F1', font=self.custom_font)
        self.toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # spam_clicks_enabled Toggle Switch
        self.spam_clicks_toggle_button = tk.Button(toggle_frame, text="Spam Clicks: OFF", command=self.toggle_spam_clicks_enabled, bg="#FF6B6B", fg='#ECF0F1', font=self.custom_font)
        self.spam_clicks_toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # Double-Click Toggle Switch
        self.double_click_toggle_button = tk.Button(toggle_frame, text="Double Click: OFF", command=self.toggle_double_click, bg="#FF6B6B", fg='#ECF0F1', font=self.custom_font)
        self.double_click_toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # Double-Click Wait Entry (placed right next to the double-click toggle button)
        self.double_click_wait_entry = tk.Entry(toggle_frame, textvariable=self.double_click_wait, width=5, font=self.custom_font)
        self.double_click_wait_entry.pack(side=tk.LEFT)


        self.update_time()

    def toggle_sleeps(self):
        self.random_sleep_enabled = not self.random_sleep_enabled
        if self.random_sleep_enabled:
            self.toggle_button.config(text="Random Breaks: ON", bg="#2ECC71")
        else:
            self.toggle_button.config(text="Random Breaks: OFF", bg="#FF6B6B")

    def toggle_double_click(self):
        self.double_click_enabled = not self.double_click_enabled
        if self.double_click_enabled:
            self.double_click_toggle_button.config(text="Double Click: ON", bg="#2ECC71")
        else:
            self.double_click_toggle_button.config(text="Double Click: OFF", bg="#FF6B6B")

    def toggle_spam_clicks_enabled(self):
        self.spam_clicks_enabled = not self.spam_clicks_enabled
        if self.spam_clicks_enabled:
            self.spam_clicks_toggle_button.config(text="Spam Clicks: ON", bg="#2ECC71")
        else:
            self.spam_clicks_toggle_button.config(text="Spam Clicks: OFF", bg="#FF6B6B")
        
    def alchemy_interval_cycles(self):
        alchemy_interval_cycles = not alchemy_interval_cycles
        if alchemy_interval_cycles:
            self.alchemy_interval_cycles_button.config(text="Alchemy Interval Cycles: ON", bg="#2ECC71")
        else:
            self.alchemy_interval_cycles_button.config(text="Alchemy Interval Cycles: OFF", bg="#FF6B6B")



    def create_text_box(self):
        self.text_box = tk.Text(self.root, height=10, bg=self.bg_color, fg=self.text_color, font=self.custom_font, relief=tk.RIDGE, borderwidth=3)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def update_time(self):
        # Retrieve the current date and time, including milliseconds
        now = datetime.now()
        date_str = now.strftime(" %B %d, %Y ")  # Format the date string
        time_str = now.strftime(" %H:%M:%S") + ".{:03d} ".format(now.microsecond // 1000)  # Format the time string with milliseconds
        # Update the labels with the current date and time
        self.date_label.config(text=date_str)
        self.time_label.config(text=time_str)
        # Schedule the next update after 50 milliseconds
        self.root.after(50, self.update_time)

    def kill_bot(self):
        self.kill_button.config(text="KILLED", bg="#FF6B6B", fg='#97E469') #Expression of death
        self.start_confetti_animation()  # Start the confetti animation
        kAltright()  # Preform the kill operation by automatically pressing the right alt key (Function in Movement.py)
        self.click_tracking_enabled = False  # Disable click tracking

    def append_message(self, message):
        self.text_box.insert(tk.END, message + '\n')
        self.text_box.see(tk.END)

    def toggle_bot(self):
        global running, bot_thread
        with running_lock:
            if not running:
                self.append_message("Starting in 3, 2, 1..")
                print("Starting in 2")
                sleep(1, 0, 0)
                print("Starting in 1")
                sleep(1, 0, 0)
                print("Turning running to", not running)
                running = True
                self.start_button.config(text="       STOP       ", bg="#FF6B6B", fg='#ECF0F1')  # Red background, white font
                if bot_thread is None or not bot_thread.is_alive():
                    bot_thread = threading.Thread(target=lambda: walker(self))
                    bot_thread.start()
            else:
                running = False
                self.start_button.config(text="     START     ", bg="#2ECC71", fg='#ECF0F1')  # Green background, white font
                self.append_message("Bot Paused")

    def on_close(self):
        global running
        running = False  # Stop the bot if it's running
        if bot_thread and bot_thread.is_alive():
            bot_thread.join()  # Wait for the bot thread to finish
        if listener_thread and listener_thread.is_alive():
            listener_thread.join()
        self.root.destroy()  # Destroy the root window

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the close event
        self.root.mainloop() #Start main loop


def walker(gui):
    while True:
        if running:
            global click_count, max_clicks, click_interval, interval_variance

            # Retrieve values from entry widgets
            try:
                max_clicks = int(gui.max_clicks_entry.get())
                click_interval = (float(gui.click_interval.get()) -.2) #Subtract .2 to account for the average time it takes to click
                click_interval = max(0, click_interval)  # Ensure non-negative
                interval_variance = float(gui.click_variance.get())
                interval_variance = max(0, interval_variance)  # Ensure non-negative
            except ValueError:
                print("Invalid Ct or Xt value")
                break

            if not running:
                break

            if click_count == 1:
               print ("Let's Click; ", max_clicks, "times.")

            #THE HEART OF THE PROGRAM :)
            sleep(click_interval, interval_variance)
            if not running:
                break
            gui.append_message(f"Click #{click_count}/{max_clicks} At: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
            click()
            click_count += 1
            #gui.append_message describing the position of the click

            if ((click_count - 1) % 10) == 0:
                gui.append_message(f"❤️============================================❤️")
                gui.start_confetti_animation()

            if gui.random_sleep_enabled:
                if rnd.random() > 0.95: #3% chance of random sleep after each click
                    SimulatedPause()
                    gui.append_message("Random Sleep Activated")

            if gui.double_click_enabled:
                doubleClickWait = float(gui.double_click_wait.get())
                if click_count % 2 == 0:
                    sleep(interval_variance, doubleClickWait / 10, doubleClickWait / 100)
                    gui.append_message(f"Click #{click_count}/{max_clicks} At: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
                    click()
                    click_count += 1

            if gui.alchemy_interval_cycles:
                sleep()


            if gui.spam_clicks_enabled:
                if rnd.random() > 0.97: 
                    for i in range(0, rnd.randint(2, 16)):
                        if rnd.random() > 0.15:
                            click()
                            sleep(0.01, 0.2)
                            gui.append_message(f"You have encountered a spam click! hit {i} times!")

            if (click_count >= max_clicks):
                gui.start_confetti_animation()
                gui.append_message(f"You have reached the goal of {click_count} clicks!")
                print ("Time to end script!")
                stop_bot()
                

def stop_bot():
    global running
    running = False


def togglebot(key, gui):
    global running, bot_thread
    if key == ONOFF:
        with running_lock:  # Ensure thread-safe access to the 'running' variable
            if running: # Stop the bot
                running = False
                print("Bot Paused")  # Log to the console
                gui.append_message("Bot Paused")  # Update GUI with the bot's status
                gui.start_button.config(text="     START     ", bg="#09C159", fg='#FFFFFF')  # Update button appearance while not running
            else: # Start the bot
                running = True
                print("Bot started")  # Log to the console
                gui.append_message("Bot Started")  # Update GUI with the bot's status
                gui.start_button.config(text="       STOP       ", bg="#FF6B6B", fg='#FFFFFF')  # Update button appearance while running
                if bot_thread is None or not bot_thread.is_alive():
                    # Start a new thread for the bot if not already running
                    bot_thread = threading.Thread(target=lambda: walker(gui))
                    bot_thread.start()
    elif key == KEY:
        # Handle the kill switch
        print("Kill switch activated")  # Log to the console
        gui.append_message("You killed it!")  # Update GUI with the termination message
        gui.start_confetti_animation()  # Trigger confetti animation as a visual feedback
        running = False  # Stop the bot's operation
        sys.exit()  # Exit the application

# Start the GUI and bot
if __name__ == "__main__":
    gui = AutoClickerGUI()
    listener_thread = threading.Thread(target=lambda: Listener(on_press=lambda key: togglebot(key, gui)).start())
    listener_thread.daemon = True
    listener_thread.start()
    gui.run()
    listener_thread.join()

# ~#~ End Script ~#~