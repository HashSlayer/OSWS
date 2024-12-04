import sys
import os
import threading
import random as rnd
from pynput.keyboard import Listener, Key
import tkinter as tk
from tkinter import font as tkFont
from datetime import datetime
# Get the directory of the current script
current_script_dir = os.path.dirname(__file__)
# Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
from Conffeti import *
from ItemSlots import *
from MainFunctions import *
from MouseMovement import *
from Welcome import *

# Global variables
running = False
running_lock = threading.Lock()
bot_thread = threading.Thread(target=lambda: walker(gui), daemon=True)
wine_laps, max_laps, speed_multiple, interval_variance, = 1, 420, 1, 0.1

# Define your special keys
ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program


running = False
sipped = True
sips = 0
pots = 1
rows = 1
pot_number = 0
skill_pot_number = 25 #25-28
skill_pot_sips = 0

welcome()

# =======================================================================================================================
# Functions

def SipCounter():
    global sips, pots, skill_pot_sips, skill_pot_number
    sips = sips
    if (sips >= 4):
        print("Drank 4 sips, moving to next potion next time.")
        gui.append_message(f"Drank 4 sips, moving to next potion {pot_number} next time.")
        pots += 1
        sleep(1.2, .6, .6)
        if rnd.random() > 0.3 and skill_pot_number < 29:
            sleepif()
            inv_slot(skill_pot_number)
            sleep(1.08, .59, .43)
            click()
            skill_pot_sips +=1
            if (skill_pot_sips % 4 == 0):
                print("Drank 4 sips, moving to next range potion.")
                sleep(.05, .1)
                skill_pot_number += 1
                skill_pot_sips = 0

        sleep(1.3, 1.2, .1)
        sleep()
        sips = 0

def PotCounter():
    global pots, rows
    if (pots % 4 == 0 and sips == 0):
        print("Drank 4 potions, moving to next range potion.")
        gui.append_message("Drank 4 potions, moving to next range potion.")
        sleep(.08, .07, .03)
        rows += 1
        gui.append_message(f"Row: {rows}")
        print ("Rows:", rows)
        if pots >= 24:
            sleep(6000, 3, 3)

def click_near():
    bezier_between(700, 1510, 316, 916, rnd.randint(23, 67)/100)
    sleep(.1, .1, .1)
    click()
# =======================================================================================================================

def SimulatedPause(): #Example of a function
    global wine_laps
    if (rnd.random() > 0.8):
        sleep(.01, 1)
        if (rnd.random() > 0.8):
            sleep(.01, 5)

# [~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GUI Class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]
#GGui
class GGui:

    def __init__(self):
        self.root = tk.Tk()  # Initialize the main window
        self.root.title("5MEkailO's Beautiful Nightmare Zone")  # Set window title
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # GUI setup and styling
        self.setup_gui()  # Setup GUI components like background colors
        self.apply_style()  # Apply styles to GUI elements
        self.root.geometry("1666x710")
        # GUI layout creation
        self.create_top_frame()  # Create and layout the top frame of the GUI
        self.create_text_box()  # Create the main text box
        self.create_additional_text_box()  # Create an additional notepad text box
        # Canvas setup
        self.canvas_width = self.canvas.winfo_width()  # Get initial canvas width
        self.canvas_height = self.canvas.winfo_height()  # Get initial canvas height
        self.canvas.bind("<Configure>", self.on_resize)  # Bind window resize event to on_resize function
        # Click tracking setup
        self.click_tracker = ClickTracker(self.append_message, self.canvas)  # Initialize the click tracker
        self.click_tracker_thread = None  # Initialize the click tracker thread
        self.click_tracking_enabled = False
        self.random_sleep_enabled = False  # Initialize random sleep flag
        self.spam_clicks_enabled = False
        self.double_click_enabled = False
        self.alchemy_interval_cycles = False
        self.double_click_wait = tk.DoubleVar(value=0.9)
        # Load text from file when initializing
        self.load_text()


    def setup_gui(self):
        self.background_color_start = "#7D0000"  # Set the start color for the gradient (Vibrant pink)
        self.background_color_end = "#333333"    # Set the end color for the gradient (Bright blue)
        self.create_gradient_background()  # Call method to create the gradient background


    def apply_style(self):
        # Set colors and font for various GUI elements
        self.bg_color = "#333333"        # Background color (Vibrant pink) 7D0000 Electric blue: #333333
        self.button_color = "#7D0000"    # Button color (Also set to Vibrant pink, consider changing to a different color)
        self.text_color = "#F5F5F5"      # Text color (Fresh green)
        self.hover_color = "#9B111E"     # Button hover color (Fiery orange)
        self.custom_font = tkFont.Font(family="Garamond", size=12, weight="bold")
        self.root.configure(bg=self.bg_color)  # Apply the background color to the root window

    
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


    def create_gradient_background(self):
        self.canvas = tk.Canvas(self.root)  # Initialize a canvas in the main window
        self.canvas.pack(fill="both", expand=True)  # Pack the canvas to fill the entire window
        self.canvas.bind("<Configure>", self.on_resize)  # Bind the resize event to the on_resize method
        self.on_resize(None)  # Make an initial call to set up the gradient background


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


    def start_confetti_animation(self):
        startConfetti(self.canvas)  # Initiate the confetti animation on the canvas


    def create_text_box(self):
        # Initialize a PanedWindow for layout management
        self.pane = tk.PanedWindow(self.canvas, bd=0, sashwidth=3, orient=tk.HORIZONTAL, bg='#333333')
        self.pane.pack(fill=tk.BOTH, expand=True, padx=33, pady=23)  # Set padding and make it expandable

        # Create the main text box for user input
        self.text_box = tk.Text(self.pane, wrap="word", bg="#666666", fg="#7D0000", font=("Garamond", 13), insertbackground="#5BCB77", relief="sunken", borderwidth=5, height=10)
        self.pane.add(self.text_box, stretch="always")  # Add to the pane with stretch option
        self.text_box.insert(tk.END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.text_box.insert(tk.END, "      Welcome to OSWS's Nightmare Zone (In Beta)                                      \n")                         # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Press the [left alt] key to toggle the bot OFF/ON ; or (START/STOP)  \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Press the [right alt] key to Kill the bot                            \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Enjoy your walk!                                                     \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")  # Prepopulate with a welcome message


    def create_additional_text_box(self):
        # Create an additional text box for notes
        self.notepad_text_box = tk.Text(self.pane, wrap="word", bg="#666666", fg="#7D0000", font=("Garamond", 12), relief="sunken", borderwidth=5, height=10)
        self.pane.add(self.notepad_text_box, width= 444)  # Set a fixed width for the notepad
        self.notepad_text_box.insert(tk.END, "Notes: \n")  # Prepopulate with "Notes:"

    def save_text(self):
        """Save the content of the notepad text box to a file."""
        with open("notepad_content.txt", "w") as file:
            file.write(self.notepad_text_box.get("1.0", tk.END))

    def load_text(self):
        """Load the content from the file to the notepad text box."""
        if os.path.exists("notepad_content.txt"):
            with open("notepad_content.txt", "r") as file:
                self.notepad_text_box.delete("1.0", tk.END)
                self.notepad_text_box.insert(tk.END, file.read())


    def on_resize(self, event):
        if event:  # Check if event is None
            width, height = event.width, event.height
        else:
            width, height = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        self.canvas.delete("gradient")
        self.create_gradient(self.canvas, self.background_color_start, self.background_color_end, width, height)


    def kill_bot(self):
        global running, bot_thread
        # Immediate UI feedback to indicate shutdown is in progress
        # Disable click tracking UI update
        self.click_tracking_enabled = False
        running = False
        self.toggle_button.config(text=" Track Clicks: OFF ", bg="#7D0000")
        self.start_button.config(text="    START    ", bg="#2ECC73", fg='#F5F5F5')
        # GUI-specific logic
        self.start_confetti_animation()
        # Ensure this operation is safe and necessary
        # Restore the kill button state after shutdown process
        self.kill_button.config(text="KILLED", state=tk.NORMAL)



    def append_message(self, message):
        self.text_box.insert(tk.END, message + '\n')  # Insert the message at the end of the text box
        self.text_box.see(tk.END)  # Scroll to the end of the text box to make the message visible

    def toggle_walk_button(self):
        global running, bot_thread
        with running_lock:  # Ensure thread-safe access to the 'running' variable
            if running: # Stop the bot
                running = False
                print("Bot Paused")  # Log to the console
                gui.append_message("Bot Paused")  # Update GUI with the bot's status
                gui.start_button.config(text="     START     ", bg="#09C159", fg='#F5F5F5')  # Update button appearance while not running
            else: # Start the bot
                running = True
                print("Bot started")  # Log to the console
                gui.append_message("Bot Started")  # Update GUI with the bot's status
                gui.start_button.config(text="       STOP       ", bg="#7D0000", fg='#F5F5F5')  # Update button appearance while running
                if bot_thread is None or not bot_thread.is_alive():
                    # Start a new thread for the bot if not already running
                    bot_thread = threading.Thread(target=lambda: walker(gui), daemon=True)
                    bot_thread.start()


    def track_clicks(self):
        self.click_tracking_enabled = not self.click_tracking_enabled  # Toggle the state

        if self.click_tracking_enabled:
            if not self.click_tracker.tracking and (self.click_tracker_thread is None or not self.click_tracker_thread.is_alive()):
                # Start a new thread if it's not already tracking
                self.click_tracker_thread = threading.Thread(target=self.click_tracker.run)
                self.click_tracker_thread.daemon = True
                self.click_tracker_thread.start()
            else:
                # Enable click processing
                self.click_tracker.process_clicks = True
            self.toggle_button.config(text=" Track Clicks: ON ", bg="#2ECC73")
        else:
            # Disable click processing
            self.click_tracker.process_clicks = False
            # Optionally, implement a mechanism to gracefully stop the thread if required
            self.toggle_button.config(text=" Track Clicks: OFF ", bg="#7D0000")



    def toggle_sleeps(self):
        self.random_sleep_enabled = not self.random_sleep_enabled
        if self.random_sleep_enabled:
            self.toggle_sleep_button.config(text="Random Breaks: ON", bg="#2ECC71")
        else:
            self.toggle_sleep_button.config(text="Random Breaks: OFF", bg="#7D0000")

    def toggle_double_click(self):
        self.double_click_enabled = not self.double_click_enabled
        if self.double_click_enabled:
            self.double_click_toggle_button.config(text="Double Click: ON", bg="#2ECC71")
        else:
            self.double_click_toggle_button.config(text="Double Click: OFF", bg="#7D0000")

    def toggle_spam_clicks_enabled(self):
        self.spam_clicks_enabled = not self.spam_clicks_enabled
        if self.spam_clicks_enabled:
            self.spam_clicks_toggle_button.config(text="Random Clicks: ON", bg="#2ECC71")
        else:
            self.spam_clicks_toggle_button.config(text="Random Clicks: OFF", bg="#7D0000")
        
    def alchemy_cycles_enabled(self):
        self.alchemy_interval_cycles = not self.alchemy_interval_cycles
        if self.alchemy_interval_cycles:
            self.alchemy_interval_cycles_button.config(text="Multiple Cycles: ON", bg="#2ECC71")
        else:
            self.alchemy_interval_cycles_button.config(text="Multiple Cycles: OFF", bg="#7D0000")

                
    def on_close(self):
        global running
        running = False  # Signal all threads to stop
        
        # Safely join bot_thread with a timeout
        if bot_thread and bot_thread.is_alive():
            try:
                bot_thread.join(timeout=1.0)
            except Exception as e:
                print(f"Exception while stopping bot_thread: {e}")
        
        # Safely join click_tracker_thread with a timeout
        if self.click_tracker_thread and self.click_tracker_thread.is_alive():
            try:
                self.click_tracker_thread.join(timeout=1.0)
            except Exception as e:
                print(f"Exception while stopping click_tracker_thread: {e}")
        
        # Save any state if necessary
        self.save_text()
        print("Exiting... Text File save <3" )
        # Close the GUI
        self.root.destroy()

                
    def create_top_frame(self):
        # Initialize the top frame of the GUI
        top_frame = tk.Frame(self.canvas, bg='#7D0000')
        top_frame.pack(padx=15, pady=15)  # Pack the frame with padding

        # Create and pack the date label
        self.date_label = tk.Label(top_frame, text="", bg="#7D0000", fg='#F5F5F5', font=("Garamond", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.date_label.pack(side="left", padx=(80, 2))  # Position it on the left with padding
        # Create and pack the time label
        self.time_label = tk.Label(top_frame, text="", bg="#7D0000", fg='#F5F5F5', font=("Garamond", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.time_label.pack(side="left", padx=2)  # Position next to the date label

        # Define the style for labels and entries
        label_style = {"bg": "#7D0000", "fg": "#F5F5F5", "font": self.custom_font, "relief": tk.FLAT, "borderwidth": 1}
        entry_style = {"bg": "#FFFFE4", "fg": "#7D0000", "font": self.custom_font, "relief": tk.SUNKEN, "borderwidth": 1}

        # Create the 'Click Interval' label and entry box
        tk.Label(top_frame, text="Speed Multiplier:", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.speed_multiple = tk.Entry(top_frame, width=5, **entry_style)
        self.speed_multiple.pack(side=tk.LEFT, padx=(3, 10))
        self.speed_multiple.insert(0, "0.5")  # Set the default value
        # Create the 'Random Multiplier' label and entry box
        tk.Label(top_frame, text="(+/-):", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.click_variance = tk.Entry(top_frame, width=5, **entry_style)
        self.click_variance.pack(side=tk.LEFT, padx=(3, 10))
        self.click_variance.insert(0, "0.5")  # Set the default value
        # Create the 'Max Clicks' label and entry box
        tk.Label(top_frame, text="Max Wine Laps:", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.max_clicks_entry = tk.Entry(top_frame, width=7, **entry_style)
        self.max_clicks_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.max_clicks_entry.insert(0, "420")  # Set the default value
        # Create and pack the 'Kill' button
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot, bg=self.button_color, fg='#F5F5F5', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=9)
        # Create and pack the 'Start / Stop' button
        self.start_button = tk.Button(top_frame, text="  Start / Stop  ", command=self.toggle_walk_button, bg=self.button_color, fg='#F5F5F5', font=self.custom_font, activebackground='#C8F6AD', relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=9)

        # Create and pack the 'Track Clicks' toggle button
        self.toggle_button = tk.Button(top_frame, text="   Track Clicks?   ", command=self.track_clicks, bg=self.button_color, fg='#F5F5F5', font=self.custom_font, activebackground='#C8F6AD', relief=tk.RAISED, borderwidth=3)
        self.toggle_button.pack(side=tk.LEFT, padx=9)

        # Frame for toggle switches
        toggle_frame = tk.Frame(self.root, bg=self.background_color_end)
        toggle_frame.pack(padx=10, pady=(0, 10))

        # Alchemy Interval Cycles Toggle Switch
        self.alchemy_interval_cycles_button = tk.Button(toggle_frame, text="Alchemy Interval Cycles: OFF", command=self.alchemy_cycles_enabled, bg="#7D0000", fg='#F5F5F5', font=self.custom_font)
        self.alchemy_interval_cycles_button.pack(side=tk.LEFT, padx=(10, 2))

        # Random Breaks Toggle Switch
        self.toggle_sleep_button = tk.Button(toggle_frame, text="Random Breaks: OFF", command=self.toggle_sleeps, bg="#7D0000", fg='#F5F5F5', font=self.custom_font)
        self.toggle_sleep_button.pack(side=tk.LEFT, padx=(10, 2))

        # spam_clicks_enabled Toggle Switch
        self.spam_clicks_toggle_button = tk.Button(toggle_frame, text="Spam Clicks: OFF", command=self.toggle_spam_clicks_enabled, bg="#7D0000", fg='#F5F5F5', font=self.custom_font)
        self.spam_clicks_toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # Double-Click Toggle Switch
        self.double_click_toggle_button = tk.Button(toggle_frame, text="Double Click Every: OFF", command=self.toggle_double_click, bg="#7D0000", fg='#F5F5F5', font=self.custom_font)
        self.double_click_toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # Double-Click Wait Entry (placed right next to the double-click toggle button)
        self.double_click_wait_entry = tk.Entry(toggle_frame, textvariable=self.double_click_wait, width=5, font=self.custom_font, relief=tk.SUNKEN, borderwidth=1, bg="#FFFFE4", fg="#7D0000")
        self.double_click_wait_entry.pack(side=tk.LEFT, padx=(10, 2))
        self.double_click_wait_entry.insert(0, "0.8")  # Set the default value


        # Call the method to update the time display
        self.update_time()

    def double_click_wait(self):
        pass

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the close event
        self.root.mainloop() #Start main loop


#  =========================================== | End of GUI Class | ===========================================
        
#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW        
def walker(gui):
    while True:
        if running:
            global wine_laps, max_laps, speed_multiple, interval_variance
            # Retrieve values from entry widgets
            try:
                max_laps = int(gui.max_clicks_entry.get())
                speed_multiple = (float(gui.speed_multiple.get())) #Subtract .2 to account for the average time it takes to click
                speed_multiple = max(0, speed_multiple)  # Ensure non-negative
                interval_variance = float(gui.click_variance.get())
                interval_variance = max(0, interval_variance)  # Ensure non-negative
            except ValueError:
                print("Invalid values entered")
                break
            # Calculate the interval between clicks

            global sips, pots, rows, sipped

            sleep(57, 7, 6) # SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP HERE
            if rnd.random() > 0.889:
                click_near()
                Notbotting()
                Notbotting()
            sleep(15, 12, 6) # SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP HERE
            if rnd.random() > 0.289:
                    Notbotting()
                    if rnd.random() > 0.889:
                        twokey()
                        sleep(.1, 1)
                        onekey()

            print("Starting loop!")
            gui.append_message("Starting loop!")

            if ((rnd.random() > 0.71388)):
                inv_slot(pots)
                click()
                sips += 1
                print ("sips is now:", sips)
                time.sleep(rnd.random() * 0.06 + 0.198)
                SipCounter()
                PotCounter()
            else:
                print("No single sip this lap. Time for one more.")
                gui.append_message("No single sip this lap. Time for one more.")
                
                sleep(65, 8, 8) # SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP SLEEP HERE
                click_near()
                if rnd.random() > 0.489:
                    Notbotting()
                    Notbotting()
                #sleep(24, 3, 2)
                if rnd.random() > 0.289:
                    Notbotting()
                    if rnd.random() > 0.889:
                        Notbotting()
                sleep(.1, .5, .2)
                inv_slot(pots)
                sleep(.3, .3, .25)
                click()
                sleep(.3, .3, .25)
                sips += 1
                print ("sips:", sips)
                sleep(1.9, 1, 2)
                SipCounter()
                PotCounter()

                inv_slot(pots)
                click()
                sips += 1
                SipCounter()
                PotCounter()
                print ("sips:", sips)
                sipped = True

            if (rows >= 7):
                print("Sleeping for ever hours, FAIL SAFE ACTIVATED.")
                gui.append_message("Sleeping for ever hours, FAIL SAFE ACTIVATED.")
                sys.exit()
            print (" Time for another loop!")
            gui.append_message(" Time for another loop!")

            if pots >= 23:
                sleep(6000, 3, 3)
        #Not Running
    #Not True
#End of NMZ()
            '''
            gui.append_message(f"~ ❤️ Lap #{wine_laps -1}/{max_laps} At: {datetime.now().strftime('%H:%M:%S.%f')[:-3]} ❤️ ~") 
            bank_near_inv(x1=1377, x2=1560, y1=600, y2=777, time= rnd.randint(23, 48)/100, wait=.3)
            bezierMoveRelative(rnd.randint(-151, -53), rnd.randint(-11, 84), rnd.random() * 0.03 + 0.05) #random movement
            sleep(.15,rnd.randint(40, 70)/100)

            if gui.random_sleep_enabled:
                if rnd.random() > 0.85:
                    Notbotting()
            deposit_all(x=1020, y=770, size=9, time = rnd.randint(30, 45)/100, pause_upto=.5)
            bezierMoveRelative(rnd.randint(-121, 52), rnd.randint(-11, 82), rnd.random() * 0.03 + 0.05) #random movement
            sleep(.1,.2)
            if rnd.random() > 0.77:
                Notbotting()


            bezierMoveRelative(rnd.randint(-30, 50), rnd.randint(-20, 10), rnd.random() * 0.03 + 0.03) #move mouse down to quantity of all

            if gui.spam_clicks_enabled:
                for i in range(rnd.randint(2, 4)):
                    kspace()
                    if rnd.random() > 0.5:
                        sleep()

            Notbotting()


            #End of wine run; time to sleep and repeat     
            if gui.random_sleep_enabled:
                if rnd.random() > 0.95: #3% chance of random sleep after each click
                    SimulatedPause()
                    gui.append_message("Random Sleep Activated")

            if wine_laps > max_laps == 0:  # Check if the goal has been reached
                gui.start_confetti_animation() # Start the confetti animation
                gui.append_message(f"You have reached the goal of {wine_laps} clicks!")
                print("Goal Reached!")
                if running: # Ensure the bot is even running
                    gui.toggle_bot() # Toggle bot off when goal is reached
                break
                '''

#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW            

def toggle_walker_key(key, gui):
    global running, bot_thread
    if key == ONOFF:
        with running_lock:  # Ensure thread-safe access to the 'running' variable
            if running: # Stop the bot
                running = False
                print("Bot Paused")  # Log to the console
                gui.append_message("Bot Paused")  # Update GUI with the bot's status
                gui.start_button.config(text="       STOP       ", bg="#7D0000", fg='#F5F5F5')  # Update button appearance while running
            else: # Start the bot
                running = True
                print("Bot started")  # Log to the console
                gui.append_message("Bot Started")  # Update GUI with the bot's status
                gui.start_button.config(text="     START     ", bg="#09C159", fg='#F5F5F5')  # Update button appearance while not running
                if bot_thread is None or not bot_thread.is_alive():
                    # Start a new thread for the bot if not already running
                    bot_thread = threading.Thread(target=lambda: walker(gui), daemon=True)
                    bot_thread.start()
    elif key == KEY:
        # Handle the kill switch
        print("Kill switch activated")  # Log to the console
        gui.append_message("You killed it!")  # Update GUI with the termination message
        gui.start_confetti_animation()  # Trigger confetti animation as a visual feedback
        running = False  # Stop the bot's operation
        sys.exit()  # Exit the application

if __name__ == "__main__":
    gui = GGui()
    listener_thread = threading.Thread(target=lambda: Listener(on_press=lambda key: toggle_walker_key(key, gui)).start())
    listener_thread.start()
    gui.run()
    listener_thread.join()
#><#~ End of Script ~#><#