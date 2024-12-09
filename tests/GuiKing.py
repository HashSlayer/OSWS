import sys
import os
import threading
import random as rnd
from pynput.keyboard import Listener, Key
import tkinter as tk
from tkinter import font as tkFont
from datetime import datetime
from Utilities.MainFunctions import *
from Utilities.Movement import *
from Utilities.Conffeti import *
from Utilities.Banking import *

# Global variables
running = False
running_lock = threading.Lock()
bot_thread = threading.Thread(target=lambda: winer(gui), daemon=True)
click_count, max_clicks, click_interval, interval_variance, = 1, 420, 1, 0.1

# Define your special keys
ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program

welcome()

# =======================================================================================================================
# Functions
# =======================================================================================================================

def SimulatedPause(): #Example of a function
    global click_count
    if (rnd.random() > 0.8):
        sleep(.01, 1)
        if (rnd.random() > 0.8):
            sleep(.01, 5)

# [~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GUI Class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]
#GGui
class GGui:

    def __init__(self):
        self.root = tk.Tk()  # Initialize the main window
        self.root.title("5MEkailO's Beautiful Bot")  # Set window title
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # GUI setup and styling
        self.setup_gui()  # Setup GUI components like background colors
        self.apply_style()  # Apply styles to GUI elements
        self.root.geometry("1530x710")
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
        self.random_sleep_enabled = False  # Initialize random sleep flag
        self.spam_clicks_enabled = False
        self.double_click_enabled = False
        self.alchemy_interval_cycles = False
        self.double_click_wait = tk.DoubleVar(value=0.9)
        # Load text from file when initializing
        self.load_text()


    def setup_gui(self):
        self.background_color_start = "#FF6B6B"  # Set the start color for the gradient (Vibrant pink)
        self.background_color_end = "#4D96FF"    # Set the end color for the gradient (Bright blue)
        self.create_gradient_background()  # Call method to create the gradient background


    def apply_style(self):
        # Set colors and font for various GUI elements
        self.bg_color = "#4D96FF"        # Background color (Vibrant pink) FF6B6B Electric blue: #4D96FF
        self.button_color = "#FF6B6B"    # Button color (Also set to Vibrant pink, consider changing to a different color)
        self.text_color = "#99E1A2"      # Text color (Fresh green)
        self.hover_color = "#F55C47"     # Button hover color (Fiery orange)
        self.custom_font = tkFont.Font(family="Consolas", size=13, weight="bold")  # Custom font for GUI elements
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
        self.pane = tk.PanedWindow(self.canvas, bd=0, sashwidth=3, orient=tk.HORIZONTAL, bg='#4D96FF')
        self.pane.pack(fill=tk.BOTH, expand=True, padx=33, pady=23)  # Set padding and make it expandable

        # Create the main text box for user input
        self.text_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF", font=("Consolas", 13), insertbackground="#5BCB77", relief="sunken", borderwidth=5, height=10)
        self.pane.add(self.text_box, stretch="always")  # Add to the pane with stretch option
        self.text_box.insert(tk.END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.text_box.insert(tk.END, "      Welcome                                       \n")                         # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Press the [left alt] key to toggle the bot OFF/ON ; or (START/STOP)  \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Press the [right alt] key to Kill the bot                            \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, "    ❤️ Enjoy your walk!                                                     \n")  # Prepopulate with a welcome message
        self.text_box.insert(tk.END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")  # Prepopulate with a welcome message


    def create_additional_text_box(self):
        # Create an additional text box for notes
        self.notepad_text_box = tk.Text(self.pane, wrap="word", bg="#FFFF76", fg="#217BFF", font=("Consolas", 12), relief="sunken", borderwidth=5, height=10)
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
        self.toggle_button.config(text=" Track Clicks: OFF ", bg="#FF6B6B")
        self.start_button.config(text="    START    ", bg="#2ECC73", fg='#97E469')
        # GUI-specific logic
        self.start_confetti_animation()
        # Ensure this operation is safe and necessary
        kAltright()
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
                gui.start_button.config(text="     START     ", bg="#09C159", fg='#97E469')  # Update button appearance while not running
            else: # Start the bot
                running = True
                print("Bot started")  # Log to the console
                gui.append_message("Bot Started")  # Update GUI with the bot's status
                gui.start_button.config(text="       STOP       ", bg="#FF6B6B", fg='#97E469')  # Update button appearance while running
                if bot_thread is None or not bot_thread.is_alive():
                    # Start a new thread for the bot if not already running
                    bot_thread = threading.Thread(target=lambda: winer(gui), daemon=True)
                    bot_thread.start()

    def track_clicks(self):
        if not self.click_tracking_enabled:
            self.track_clicks()  # Start click tracking if it's not already enabled
        else:
            self.track_clicks()  # Stop click tracking if it's already enabled

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
            self.toggle_button.config(text=" Track Clicks: OFF ", bg="#FF6B6B")



    def toggle_sleeps(self):
        self.random_sleep_enabled = not self.random_sleep_enabled
        if self.random_sleep_enabled:
            self.toggle_sleep_button.config(text="Random Breaks: ON", bg="#2ECC71")
        else:
            self.toggle_sleep_button.config(text="Random Breaks: OFF", bg="#FF6B6B")

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
        
    def alchemy_cycles_enabled(self):
        self.alchemy_interval_cycles = not self.alchemy_interval_cycles
        if self.alchemy_interval_cycles:
            self.alchemy_interval_cycles_button.config(text="Alchemy Interval Cycles: ON", bg="#2ECC71")
        else:
            self.alchemy_interval_cycles_button.config(text="Alchemy Interval Cycles: OFF", bg="#FF6B6B")

                
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
        top_frame = tk.Frame(self.canvas, bg='#FF6B6B')
        top_frame.pack(padx=15, pady=15)  # Pack the frame with padding

        # Create and pack the date label
        self.date_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg='#97E469', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.date_label.pack(side="left", padx=(80, 2))  # Position it on the left with padding
        # Create and pack the time label
        self.time_label = tk.Label(top_frame, text="", bg="#FF6B6B", fg='#97E469', font=("Consolas", 13, "bold"), relief=tk.RAISED, borderwidth=1)
        self.time_label.pack(side="left", padx=2)  # Position next to the date label

        # Define the style for labels and entries
        label_style = {"bg": "#FF6B6B", "fg": "#97E469", "font": self.custom_font, "relief": tk.FLAT, "borderwidth": 0}
        entry_style = {"bg": "#FFFAE4", "fg": "#217BFF", "font": self.custom_font, "relief": tk.SUNKEN, "borderwidth": 1}

        # Create the 'Click Interval' label and entry box
        tk.Label(top_frame, text="Click Interval:", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.click_interval = tk.Entry(top_frame, width=5, **entry_style)
        self.click_interval.pack(side=tk.LEFT, padx=(3, 10))
        self.click_interval.insert(0, "1.0")  # Set the default value
        # Create the 'Random Multiplier' label and entry box
        tk.Label(top_frame, text="(+/-):", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.click_variance = tk.Entry(top_frame, width=5, **entry_style)
        self.click_variance.pack(side=tk.LEFT, padx=(3, 10))
        self.click_variance.insert(0, "0.5")  # Set the default value
        # Create the 'Max Clicks' label and entry box
        tk.Label(top_frame, text="Max Clicks:", **label_style).pack(side=tk.LEFT, padx=(10, 0))
        self.max_clicks_entry = tk.Entry(top_frame, width=7, **entry_style)
        self.max_clicks_entry.pack(side=tk.LEFT, padx=(3, 10))
        self.max_clicks_entry.insert(0, "420")  # Set the default value
        # Create and pack the 'Kill' button
        self.kill_button = tk.Button(top_frame, text="KILL", command=self.kill_bot, bg=self.button_color, fg='#97E469', font=self.custom_font, activebackground=self.hover_color, relief=tk.RAISED, borderwidth=3)
        self.kill_button.pack(side=tk.RIGHT, padx=9)
        # Create and pack the 'Start / Stop' button
        self.start_button = tk.Button(top_frame, text="  Start / Stop  ", command=self.toggle_walk_button, bg=self.button_color, fg='#97E469', font=self.custom_font, activebackground='#C8F6AD', relief=tk.RAISED, borderwidth=3)
        self.start_button.pack(side=tk.RIGHT, padx=9)

        # Create and pack the 'Track Clicks' toggle button
        self.click_tracking_enabled = False  # Initialize the click tracking flag as False
        self.toggle_button = tk.Button(top_frame, text=" Track Clicks ", command=self.track_clicks, bg=self.button_color, fg='#97E469', font=self.custom_font, activebackground='#C8F6AD', relief=tk.RAISED, borderwidth=3)
        self.toggle_button.pack(side=tk.LEFT, padx=9)

        # Frame for toggle switches
        toggle_frame = tk.Frame(self.root, bg=self.background_color_end)
        toggle_frame.pack(padx=10, pady=(0, 10))

        # Alchemy Interval Cycles Toggle Switch
        self.alchemy_interval_cycles_button = tk.Button(toggle_frame, text="Alchemy Interval Cycles: OFF", command=self.alchemy_cycles_enabled, bg="#FF6B6B", fg='#97E469', font=self.custom_font)
        self.alchemy_interval_cycles_button.pack(side=tk.LEFT, padx=(10, 2))

        # Random Breaks Toggle Switch
        self.toggle_sleep_button = tk.Button(toggle_frame, text="Random Breaks: OFF", command=self.toggle_sleeps, bg="#FF6B6B", fg='#97E469', font=self.custom_font)
        self.toggle_sleep_button.pack(side=tk.LEFT, padx=(10, 2))

        # spam_clicks_enabled Toggle Switch
        self.spam_clicks_toggle_button = tk.Button(toggle_frame, text="Spam Clicks: OFF", command=self.toggle_spam_clicks_enabled, bg="#FF6B6B", fg='#97E469', font=self.custom_font)
        self.spam_clicks_toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # Double-Click Toggle Switch
        self.double_click_toggle_button = tk.Button(toggle_frame, text="Double Click Every: OFF", command=self.toggle_double_click, bg="#FF6B6B", fg='#97E469', font=self.custom_font)
        self.double_click_toggle_button.pack(side=tk.LEFT, padx=(10, 2))

        # Double-Click Wait Entry (placed right next to the double-click toggle button)
        self.double_click_wait_entry = tk.Entry(toggle_frame, textvariable=self.double_click_wait, width=5, font=self.custom_font, relief=tk.SUNKEN, borderwidth=1, bg="#FFFAE4", fg="#217BFF")
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
def winer(gui):
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
                print("Invalid values entered")
                break

            if not running:
                break

            if click_count == 1:
                print("Let's Click;", max_clicks, "times.")

            # Sleep logic
            sleep(click_interval, interval_variance, 0) #Sleep for a random amount of time between click_interval +/- wait_upto
            if not running:
                break

            # Click action
            click()
            click_count += 1
            gui.append_message(f"Click #{click_count}/{max_clicks} At: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

            if gui.random_sleep_enabled:
                if rnd.random() > 0.95: #3% chance of random sleep after each click
                    SimulatedPause()
                    gui.append_message("Random Sleep Activated")

            if gui.double_click_enabled:
                doubleClickWait = float(gui.double_click_wait.get())
                if click_count % 2 == 0:
                    sleep(interval_variance, doubleClickWait / 10, doubleClickWait / 100)
                    click()
                    click_count += 1
                    gui.append_message(f"Click #{click_count}/{max_clicks} At: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

            if gui.alchemy_interval_cycles:
                if rnd.random() > 0.95:
                    # Define the parameters for each cycle
                    cycles = [
                        (1.5, 0.25 + rnd.random() * 0.1, 0.8, "Alchemy Interval Cycle 1 Activated"),
                        (1.3, 0.25 + rnd.random() * 0.05, 0.9, "Alchemy Interval Cycle 2 Activated"),
                        (1.8, 0.3 + rnd.random() * 0.1, 0.4, "Alchemy Interval Cycle 3 Activated"),
                        (1.4 + rnd.random() * 0.5, 0.2 + rnd.random() * 0.2, 0.45 + rnd.random() * 0.3, "Alchemy Interval Cycle 4 Activated")
                    ]

                    if rnd.random() > 0.95:
                        gui.append_message("Alchemy Interval Cycles Activated")
                        selected_cycle = rnd.choice(cycles)
                        click_interval, interval_variance, doubleClickWait, message = selected_cycle
                        gui.append_message(message)
                        return click_interval, interval_variance, doubleClickWait

                    GGui.double_click_wait_entry.delete(0, tk.END)
                    GGui.double_click_wait_entry.insert(0, doubleClickWait)
                    GGui.click_interval.delete(0, tk.END)
                    GGui.click_interval.insert(0, click_interval)
                    GGui.click_variance.delete(0, tk.END)
                    GGui.click_variance.insert(0, interval_variance)
                    return None, None, None  # Default return if no cycle is activated

            if gui.spam_clicks_enabled:
                if rnd.random() > 0.97: 
                    if rnd.random() > 0.7:
                        for i in range(0, rnd.randint(2, 16)):
                            if rnd.random() > 0.1:
                                click()
                                sleep(0.001, 0.1)
                                gui.append_message(f"You have encountered a spam click! hit {i} times!")
                    else:
                        for i in range(0, rnd.randint(2, 9)):
                            if rnd.random() > 0.1:
                                click()
                                sleep(0.001, 0.1)
                                gui.append_message(f"You have encountered a spam click! hit {i} times!")


            # Confetti animation and message every "100 clicks"
            if (click_count - 1) % 100 == 0: # Subtract 1 from click_count to account for the initial click
                gui.append_message(f"❤️ =================={click_count}======================== ❤️")
                gui.start_confetti_animation()

            if click_count % max_clicks == 0:  # Check if the goal has been reached
                gui.start_confetti_animation() # Start the confetti animation
                gui.append_message(f"You have reached the goal of {click_count} clicks!")
                print("Goal Reached!")
                if running: # Ensure the bot is even running
                    gui.toggle_bot() # Toggle bot off when goal is reached
                break

#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW            

def toggle_winer_key(key, gui):
    global running, bot_thread
    if key == ONOFF:
        with running_lock:  # Ensure thread-safe access to the 'running' variable
            if running: # Stop the bot
                running = False
                print("Bot Paused")  # Log to the console
                gui.append_message("Bot Paused")  # Update GUI with the bot's status
                gui.start_button.config(text="       STOP       ", bg="#FF6B6B", fg='#97E469')  # Update button appearance while running
            else: # Start the bot
                running = True
                print("Bot started")  # Log to the console
                gui.append_message("Bot Started")  # Update GUI with the bot's status
                gui.start_button.config(text="     START     ", bg="#09C159", fg='#97E469')  # Update button appearance while not running
                if bot_thread is None or not bot_thread.is_alive():
                    # Start a new thread for the bot if not already running
                    bot_thread = threading.Thread(target=lambda: winer(gui), daemon=True)
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
    listener_thread = threading.Thread(target=lambda: Listener(on_press=lambda key: toggle_winer_key(key, gui)).start())
    listener_thread.start()
    gui.run()
    listener_thread.join()
#><#~ End of Script ~#><#