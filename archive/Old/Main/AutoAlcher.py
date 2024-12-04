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


global running, ClickCount, maxItems, SleepWeight, bot_thread

ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program

running_lock = threading.Lock()
bot_thread = None
running = False

ClickCount = 1
SleepWeight = .08 
maxItems = 100 #Amount of item 1



welcome()

def doWeW8():
    global ClickCount, SleepWeight

    if (rnd.random() > 0.9929):
        click()
        for _ in range(0, rnd.randint(1, 32)):
            time.sleep(rnd.random() * 0.01 + 0.001)
            if (rnd.random() > 0.8):
                click()
                sleep(.1, .1)
                if (rnd.random() > 0.69):
                    click()

    if (rnd.random() > 0.8889):
        sleep(.1, 1)
        if (rnd.random() > 0.68):
            sleep(.1, 1)
            if (rnd.random() > 0.87):
                for _ in range(0, rnd.randint(1, 7)):
                    sleep(.01, 0.09)
                    click()

    if ((rnd.random() > 0.9889) and (ClickCount > rnd.randint(100, 2000))):
        sleep(1, rnd.randint(5, 10))
        print ("Time for a sleep!")
        SleepWeight += 0.0001

    if ((rnd.random() > 0.9989) and (ClickCount > rnd.randint(1000, 4200))):
        sleep(10, 300, 20)
        print ("Oops, a big sleep!!")

    #After 100 clicks, print the number of clicks
    if ((ClickCount % 100 == 0) and (ClickCount > 0)):
        print ("You have", ClickCount, "clicks")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#=======================================================================================================================

# GUI Class
class AutoClickerGUI:
    # ... existing methods ...
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OSWS Auto Alchemy")
        self.apply_style()
        # Create the background Canvas
        self.create_background_canvas()
        # Create GUI components
        self.create_top_frame()
        self.create_text_box()

    def create_background_canvas(self):
        self.bg_canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)  # Cover the entire window

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
        # Time Label
        self.time_label = tk.Label(top_frame, text="", bg="#FFD30D" , fg='#FF780D', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth= 3) #FF780D is Orange
        self.time_label.pack(side="left", padx=80, pady=10)
        # Kill Button
        self.kill_button = tk.Button(top_frame, text="Kill", command=self.kill_bot, bg='#FF6B6B', fg='#ECF0F1', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=5)
        self.update_time()
        # Start / Stop Button
        self.start_button = tk.Button(top_frame, text="Start / Stop", command=self.toggle_bot, bg=self.button_color, fg='#FF780D', font=self.custom_font, activebackground='#28B065', relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=5)
        # Max Items Entry
        tk.Label(top_frame, text="Max Items:", bg=self.bg_color, fg=self.text_color, font=self.custom_font).pack(side=tk.LEFT, padx=(10, 0))
        self.max_items_entry = tk.Entry(top_frame, width=7, font=self.custom_font)
        self.max_items_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.max_items_entry.insert(0, "100")  # Default value    

    def create_text_box(self):
        self.text_box = tk.Text(self.root, height=10, bg=self.bg_color, fg=self.text_color, font=self.custom_font, relief=tk.RIDGE, borderwidth=3)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def update_time(self):
        now = datetime.now().strftime(" %H:%M:%S ")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def kill_bot(self):
        k2()

    def append_message(self, message):
        self.text_box.insert(tk.END, message + '\n')
        self.text_box.see(tk.END)

    def toggle_bot(self):
        self.append_message("Starting in 3, 2, 1..")
        print ("Starting in 3")
        sleep(1, 0, 0)
        print ("Starting in 2")
        sleep(1, 0, 0)
        print ("Starting in 1")
        sleep(1, 0, 0)
        print ("Turning running to", not running)
        k1()

    def run(self):
        self.root.mainloop()


def walker(gui):
    while True:
        if running:
            global ClickCount, maxItems, SleepWeight

            # Retrieve values from entry widgets
            try:
                maxItems = int(gui.max_items_entry.get())
                # ... [retrieve other values] ...
            except ValueError:
                print("Invalid input value")
                break

            if ClickCount == 1:
               maxItems *= 2
               print ("Let's RIDE; ", maxItems, "clicks.")

            #THE HEART OF THE PROGRAM :)
            if rnd.random() > 0.00199:
                sleep(.74, SleepWeight)
            click()
            ClickCount += 1
            if ClickCount % 10 == 0:
                gui.append_message(f"You have {ClickCount} clicks!")
                gui.start_confetti_animation()
            if ClickCount % 2 ==0:    
                sleep(.34, SleepWeight / 2)
            doWeW8()

            if rnd.random() > 0.9989:
                sleep(.3)
                k4()
                sleep(.3)
                #Append and send the message to the GUI
                gui.append_message("4 was automatically pressed")

            if (ClickCount % (maxItems * 2) == 0): #Kill the program after X Clicks
                print ("Time for a break! A big one!")
                gui.append_message(f"You have reached the goal of {ClickCount} alchs!")
                stop_bot()

def stop_bot():
    global running, bot_thread
    with running_lock:
        running = False
    if bot_thread is not None:
        bot_thread.join()

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
        sys.exit()

# Start the GUI and bot
if __name__ == "__main__":
    gui = AutoClickerGUI()
    listener_thread = threading.Thread(target=lambda: Listener(on_press=lambda key: togglebot(key, gui)).start())
    listener_thread.start()
    gui.run()
    listener_thread.join()

