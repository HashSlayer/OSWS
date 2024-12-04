import time
import sys
import os
import threading
import random as rnd
from pynput.keyboard import Listener, KeyCode, Key
# Get the directory of the current script
current_script_dir = os.path.dirname(__file__)
# Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
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
ClickCount, maxClicks, Ct, Xt, shift_pressed = 1, 420, 1, 0.1, False

# Define your special keys
ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program

welcome()

def SimulatedPause():
    global ClickCount, SleepWeight
    if (rnd.random() > 0.8889):
        sleep(.1, 1)
        if (rnd.random() > 0.68):
            sleep(.1, 1)

    if ((rnd.random() > 0.9889) and (ClickCount > rnd.randint(100, 2000))):
        sleep(1, rnd.randint(5, 10))
        print ("Time for a sleep!")

def create_gradient(canvas, color1, color2, width, height):
    for i in range(height):
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)
        r = (r1 + int((r2 - r1) * i / height)) & 0xff00
        g = (g1 + int((g2 - g1) * i / height)) & 0xff00
        b = (b1 + int((b2 - b1) * i / height)) & 0xff00
        color = f'#{r:04x}{g:04x}{b:04x}'
        canvas.create_line(0, i, width, i, fill=color)
#=======================================================================================================================

# GUI Class
class AutoClickerGUI:
    # ... existing methods ...
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("@5MEkailO's Snowball Bot")
        self.apply_style()
        self.random_sleep_enabled = False
        self.double_click_enabled = False
        self.double_click_wait = tk.DoubleVar(value=0.5)
        self.create_background_canvas()
        self.create_top_frame()
        self.create_text_box()

    def create_background_canvas(self):
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)
        self.apply_gradient(self.bg_canvas, "#A7C7E7", "#0077FF", self.root.winfo_screenwidth(), self.root.winfo_screenheight())

    def apply_gradient(self, canvas, color1, color2, width, height):
        for i in range(height):
            r1, g1, b1 = canvas.winfo_rgb(color1)
            r2, g2, b2 = canvas.winfo_rgb(color2)
            r = (r1 + int((r2 - r1) * i / height)) & 0xff00
            g = (g1 + int((g2 - g1) * i / height)) & 0xff00
            b = (b1 + int((b2 - b1) * i / height)) & 0xff00
            color = f'#{r:04x}{g:04x}{b:04x}'
            canvas.create_line(0, i, width, i, fill=color)

    def start_confetti_animation(self):
        startConfetti(self.bg_canvas)

    def apply_style(self):
        # Enhanced color palette
        self.bg_color = "#A7C7E7"  # Pastel blue
        self.button_color = "#C6A9E9"  # Soft green, like muted Christmas tree foliage
        self.text_color = "#F4F4F4"  # Very light gray, for a soft contrast
        self.hover_color = "#FF6B6B"  # Pastel red,
        # Stylish font
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        # Set root window background color
        self.root.configure(bg=self.bg_color)

    def create_top_frame(self):
        # Create the top frame
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(padx=10, pady=10)

        # Date Label
        self.date_label = tk.Label(top_frame, text="", bg="#FFDA35", fg='#97E469', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=2)
        self.date_label.pack(side="left", padx=(80, 2))  # Small separation between date and time

        # Time Label
        self.time_label = tk.Label(top_frame, text="", bg="#FFDA35", fg='#97E469', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=2)
        self.time_label.pack(side="left", padx=2)

        # Label style with border
        label_style = {"bg": "#FFDA35", "fg": "#97E469", "font": self.custom_font, "relief": tk.FLAT, "borderwidth": 3}

        # Click Every (Ct) Label and Entry
        tk.Label(top_frame, text="Click Every (Ct): ", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.ct_entry = tk.Entry(top_frame, width=5, font=self.custom_font)
        self.ct_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.ct_entry.insert(0, "25")  # Default value

        # Random Multiplier (Xt) Label and Entry
        tk.Label(top_frame, text="(+/-) (CXt): ", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.xt_entry = tk.Entry(top_frame, width=5, font=self.custom_font)
        self.xt_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.xt_entry.insert(0, "330")  # Default value

        # Max Clicks Label and Entry
        tk.Label(top_frame, text="Max Clicks: ", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.max_clicks_entry = tk.Entry(top_frame, width=7, font=self.custom_font)
        self.max_clicks_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.max_clicks_entry.insert(0, "420")  # Default value

        # Kill Button
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot, bg='#FF6B6B', fg='#97E469', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=5)

        # Start / Stop Button
        self.start_button = tk.Button(top_frame, text="  Start / Stop  ", command=self.toggle_bot, bg=self.button_color, fg='#97E469', font=self.custom_font, activebackground='#C8F6AD', relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=5)

        # Frame for toggle switches
        toggle_frame = tk.Frame(self.root, bg=self.bg_color)
        toggle_frame.pack(padx=10, pady=(0, 10))

        # Random Breaks Toggle Switch
        self.toggle_button = tk.Button(toggle_frame, text="Random Breaks: OFF", command=self.toggle_sleeps, bg="#FF6B6B", fg='#97E469', font=self.custom_font)
        self.toggle_button.pack(side=tk.LEFT)

        # Double-Click Toggle Switch
        self.double_click_toggle_button = tk.Button(toggle_frame, text="Double Click: OFF", command=self.toggle_double_click, bg="#FF6B6B", fg='#97E469', font=self.custom_font)
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


    def create_text_box(self):
        self.text_box = tk.Text(self.root, height=10, bg=self.bg_color, fg=self.text_color, font=self.custom_font, relief=tk.RIDGE, borderwidth=3)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def update_time(self):
        # Get current date and time with milliseconds
        now = datetime.now()
        date_str = now.strftime(" %B %d, %Y ")
        time_str = now.strftime(" %H:%M:%S") + ".{:03d} ".format(now.microsecond // 1000)

        self.date_label.config(text=date_str)
        self.time_label.config(text=time_str)
        self.root.after(50, self.update_time)  # Update the time more frequently

    def kill_bot(self):
        kAltright()

    def append_message(self, message):
        self.text_box.insert(tk.END, message + '\n')
        self.text_box.see(tk.END)

    def toggle_bot(self):
        global running, bot_thread
        with running_lock:
            if not running:
                self.append_message("Starting in 3, 2, 1..")
                print("Starting in 3")
                sleep(1, 0, 0)
                print("Starting in 2")
                sleep(1, 0, 0)
                print("Starting in 1")
                sleep(1, 0, 0)
                print("Turning running to", not running)
                running = True
                self.start_button.config(text="       STOP       ", bg="#FF6B6B", fg='#97E469')  # Red background, white font
                if bot_thread is None or not bot_thread.is_alive():
                    bot_thread = threading.Thread(target=lambda: walker(self))
                    bot_thread.start()
            else:
                running = False
                self.start_button.config(text="     START     ", bg="#2ECC71", fg='#97E469')  # Green background, white font
                self.append_message("Bot Paused")

    def run(self):
        self.root.mainloop()


def walker(gui):
    while True:
        if running:
            global ClickCount, maxClicks, Ct, Xt

            # Retrieve values from entry widgets
            try:
                maxClicks = int(gui.max_clicks_entry.get())
                Ct = (float(gui.ct_entry.get() ) - 0.28)
                if Ct < 0:
                    Ct = 0.01 #Expect a minimum delay of .23 ~, as thats how long it takes to click minimum average
                Xt = float(gui.xt_entry.get())
            except ValueError:
                print("Invalid Ct or Xt value")
                break

            if not running:
                break

            if ClickCount == 1:
               print ("Let's Click; ", maxClicks, "times.")

            #THE HEART OF THE PROGRAM :)
            sleep(Ct, Xt/2, Xt/2) #Sleeps for up to 1 min 30 seconds naturally
            if (rnd.random() > 0.61789):
                sleep(10, 50, 10) #sleeps up to 1 minute totaling 2.5 minutes
                if (rnd.random() > 0.51789):
                    sleep(10, 50, 10) #sleeps up to 1 minute totaling 3.5 minutes

            if (rnd.random() > 0.31789):
                sleep(5, 60, 20) #sleeps up to 1 minute totaling 4.5 minutes
            if (rnd.random() > 0.61789):
                sleep(5, 60, 20) #sleeps up to 1 minute totaling 5.5 minutes
            if (rnd.random() > 0.81789):
                sleep(5, 60, 20) #sleeps up to 1 minute totaling 6.5 minutes
            if (rnd.random() > 0.91789):
                sleep(5, 60, 20) #sleeps up to 1 minute totaling 7.5 minutes
            if (rnd.random() > 0.91789):
                sleep(30, 60, 20) #sleeps up to 1 minute totaling 8.5 minutes
                if (rnd.random() > 0.91789):
                    sleep(60, 60, 20) #sleeps up to 2 minutes totaling 11.5 minutes

            if (rnd.random() > 0.8789):
                click()
                if rnd.random() > 0.6:
                    click()
                    print ("double click")
            else:  
                quick_click()
                if rnd.random() > 0.621:
                    click()
                    print ("double click")

            if (rnd.random() > 0.9789):
                sleep(.1, 4, 1)
                click()
                sleep(.21, 4, 1)
                click()
                print ("Oops, a double click!!")

            if (rnd.random() > 0.98173):
                time.sleep(rnd.random() * 0.1 + 0.01)
                click()
                time.sleep(rnd.random() * 0.01 + 0.01)
                click()
                print ("Oops, a triple click!!!")
            time.sleep(rnd.random() * 3/27 + 0.43)
            if (rnd.random() > 0.9789):
                sleep(6, 1, 1)
                click()
                print ("Oops, a double click!!")

            if not running:
                break
            gui.append_message(f"Click #{ClickCount} at {datetime.now().strftime('%H:%M:%S')}")
            click()
            ClickCount += 1
            #gui.append_message describing the position of the click

            if ((ClickCount - 1) % 10) == 0:
                gui.append_message(f"❤️============================================❤️")
                gui.start_confetti_animation()

            if gui.random_sleep_enabled:
                if rnd.random() > 0.98: #2% chance of random sleep after each click
                    if Ct < 1:
                        sleep(Ct/3, Ct * 3, Xt)
                    elif Ct > 1 and Ct <10:
                        sleep(Ct/10, Ct, Xt)
                    elif Ct > 10:
                        sleep(Ct/10, Ct / 5, Xt)
                    gui.append_message("Random Sleep Activated")

            if gui.double_click_enabled:
                doubleClickWait = float(gui.double_click_wait.get())
                if ClickCount % 2 == 0:
                    sleep(doubleClickWait, doubleClickWait / 10, doubleClickWait / 50)

            if (ClickCount % maxClicks == 0):
                gui.start_confetti_animation()
                gui.append_message(f"You have reached the goal of {ClickCount} clicks!")
                print ("Time to end script!")
                stop_bot()
                

def stop_bot():
    global running
    running = False


def togglebot(key, gui):
    global running, bot_thread
    if key == ONOFF:
        with running_lock:
            if running:
                running = False
                print("Bot Paused")  # Console message
                gui.append_message("Bot Paused")  # GUI message
            else:
                running = True
                print("Bot started")  # Console message
                gui.append_message("Bot Started")  # GUI message
                if bot_thread is None or not bot_thread.is_alive():
                    bot_thread = threading.Thread(target=lambda: walker(gui))
                    bot_thread.start()
    elif key == KEY:
        print("Kill switch activated")
        gui.append_message("You killed it!")
        gui.start_confetti_animation()
        stop_bot()
        running = False
        sys.exit()

# Start the GUI and bot
if __name__ == "__main__":
    gui = AutoClickerGUI()
    listener_thread = threading.Thread(target=lambda: Listener(on_press=lambda key: togglebot(key, gui)).start())
    listener_thread.start()
    gui.run()
    listener_thread.join()

# ~#~ End Script ~#~