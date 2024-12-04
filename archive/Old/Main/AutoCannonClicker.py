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

global running
global clicks

ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program

running = False
clicks = 1


welcome()

#=======================================================================================================================



# GUI Class
class AutoClickerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OSWS Auto Cannon Clicker")

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
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(padx=10, pady=10)

        self.time_label = tk.Label(top_frame, text="", bg="#FFD30D" , fg='#FF780D', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth= 3) #FF780D is Orange
        self.time_label.pack(side="left", padx=80, pady=10)

        self.kill_button = tk.Button(top_frame, text="Kill", command=self.kill_bot, bg='#FF6B6B', fg='#ECF0F1', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=5)

        self.update_time()

        self.start_button = tk.Button(top_frame, text="Start / Stop", command=self.toggle_bot, bg=self.button_color, fg='#FF780D', font=self.custom_font, activebackground='#28B065', relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=5)



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
        global running
        if not running:
            self.append_message("Starting in 3, 2, 1..")
            print ("Starting in 3")
            sleep(1, 0, 0)
            print ("Starting in 2")
            sleep(1, 0, 0)
            print ("Starting in 1")
            sleep(1, 0, 0)
            print ("Turning running to", not running)
            #Append and send the message to the GUI
            self.append_message("Turning running to " + str(not running))
            running = True
            self.start_button.config(text="Stop")
            bot_thread = threading.Thread(target=lambda: walker(self))
            bot_thread.start()
        else:
            running = False
            self.start_button.config(text="Start")

    def run(self):
        self.root.mainloop()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~------------
# Create the GUI

# Modify your existing bot functions to update the GUI
def walker(gui):
    while True:
        if running:
            global clicks
            if clicks == 1:
               print ("Let's RIDE!")

            sleep(8, 8, 10)
            if (rnd.random() > 0.21789):
                sleep(1, 4, .20)
            if (rnd.random() > 0.41789):
                sleep(1, 5, .40)
            if (rnd.random() > 0.61789):
                sleep(1, 6, .60)
            if (rnd.random() > 0.91789):
                sleep(1, 7, .80)

            click()
            gui.append_message(f"You now have {clicks} clicks on the cannon!")
            gui.start_confetti_animation()

            if (rnd.random() > 0.8789):
                sleep(4, 4, 1)
                click()
                sleep(1, 3, 1)
                click()
                print ("Oops, a double click!!")


            if (rnd.random() > 0.98173):
                for _ in range(0, rnd.randint(1, 7)):
                    sleep(.1, 0.09)
                    if rnd.random() > 0.5:
                        click()


            clicks = clicks + 1

            #After 100 clicks, print the number of clicks
            if ((clicks % 100 == 0) and (clicks > 0)):
                print ("You have", clicks, "clicks")


            if (clicks % 1200 == 0):
                #sleep for 12 hours
                #This alchs about 1400 items (4200 clikz)
                print ("Time for a break! A big one!")
                time.sleep(43200)
                sys.exit()

            if rnd.random() > 0.97:
                print ("Random Key Press")
                #Randomly press a key from 1-8 using k1() - k8()
                kplus()
                sleep(1, .1, .1)


def offon_bot():
    global running
    running = not running
    bot_thread = threading.Thread(target=walker)
    bot_thread.start()

def stop_bot():
    global running
    running = False

def togglebot(key, gui):
    if key == ONOFF:
        global running
        print("Program is on:", not running)
        gui.append_message("Program is on: " + str(not running))
        if not running:
            running = True
            bot_thread = threading.Thread(target=lambda: walker(gui))
            bot_thread.start()
        else:
            running = False
    elif key == KEY:
        print("Kill switch activated")
        gui.append_message("You killed it!")
        gui.start_confetti_animation()
        stop_bot()
        sys.exit()

# Start the GUI and bot
if __name__ == "__main__":
    gui = AutoClickerGUI()
    # Start the keyboard listener in a separate thread
    listener_thread = threading.Thread(target=lambda: Listener(on_press=lambda key: togglebot(key, gui)).start())
    listener_thread.start()
    gui.run()
    listener_thread.join()  # Wait for the listener thread to finish
#=======================================================================================================================
    
