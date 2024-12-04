import tkinter as tk
from tkinter import font as tkFont
from pynput import mouse
import datetime
import random
import threading
import time
from Utilities.Movement import *
from Utilities.MainFunctions import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_confetti(canvas):
    confetti = []
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for _ in range(random.randint(69,420)):  # Create 50 pieces of confetti
        x, y = random.randint(0, canvas_width), random.randint(0, canvas_height)
        confetti.append(canvas.create_oval(x, y, x+5, y+5, fill=random.choice(['red', 'blue', 'green', 'yellow', 'pink', 'purple', 'orange'])))
    return confetti

def update_confetti(canvas, confetti, start_time, duration=2):
    current_time = time.time()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    if current_time - start_time < duration:  # Run the animation for 2 seconds
        for item in confetti:
            x_move = random.randint(-5, 5)
            y_move = random.randint(-5, 5)
            canvas.move(item, x_move, y_move)
            # Ensure confetti stays within canvas bounds
            coords = canvas.coords(item)
            if coords[2] > canvas_width or coords[0] < 0:
                canvas.move(item, -x_move, 0)
            if coords[3] > canvas_height or coords[1] < 0:
                canvas.move(item, 0, -y_move)
        canvas.after(50, update_confetti, canvas, confetti, start_time)
    else:
        for item in confetti:
            canvas.delete(item)  # Remove confetti after animation

def startConfetti (on = True):
    if on:  # Start animation every 10 clicks
        confetti = create_confetti(canvas)
        start_time = time.time()
        update_confetti(canvas, confetti, start_time)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClickTracker:
    def __init__(self, output_function):
        self.output_function = output_function
        self.listener = mouse.Listener(on_click=self.on_click)
        self.tracking = False
        self.click_count = 0  # Initialize click count

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if pressed:
                self.start_time = time.time()
            else:
                self.end_time = time.time()
                duration = self.end_time - self.start_time
                self.click_count += 1  # Increment click count
                message = f"Click {self.click_count}: Duration: {duration:.3f} seconds.. Position: ({x}, {y})\n"
                if self.click_count % 10 == 0:
                    message += f"❤️ -+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+-  ❤️\n"
                    startConfetti()
                print("bezierMove(rnd.randint(",(x - 5),",",(x + 5),"), rnd.randint(",y-5,",",y+5,"), sleep(.3))")
                self.output_function(message)
    def run(self):
        self.tracking = True
        with self.listener:
            self.listener.join()
        self.tracking = False
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OSWSGUI:
    def __init__(self, title="OSWS"):
        self.root = tk.Tk()
        self.root.title(title)
        self.click_tracker = ClickTracker(self.update_text_box)
        self.setup_gui()

    def setup_gui(self):
        self.create_gradient_background()
        self.create_top_frame()
        self.create_text_box()

    def create_gradient_background(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

    def create_top_frame(self):
        time_frame = tk.Frame(self.canvas, **label_style)
        time_frame.pack(anchor="ne", padx=10, pady=10)

        self.time_label = tk.Label(time_frame, text="", bg="#FF6B6B", fg="#5BCB77", font=("Consolas", 13, "bold"))
        self.time_label.pack(side="left", padx=10, pady=10)

        self.start_button = tk.Button(time_frame, text="Start Walking!", command=self.click_tracker.toggle_tracking, bg="#4D96FF", fg="#FF6B6B", font=("Consolas", 13, "bold"), activebackground="#F55C47")
        self.start_button.pack(side="right", padx=10, pady=10)

    def create_text_box(self):
        self.text_box = tk.Text(self.canvas, wrap="word", bg="#FFD93D", fg="#5BCB77", font=("Consolas", 13), insertbackground="#5BCB77", relief="sunken", borderwidth=2)
        self.text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_text_box(self, message):
        self.text_box.insert(tk.END, message)
        self.text_box.see(tk.END)

    def on_resize(self, event):
        self.canvas.delete("gradient")
        self.create_gradient(event.width, event.height)
#--------------------------------------------------------------------------
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
        
def start_tracker():
    if not tracker.tracking:
        start_button.config(text="Kill it!")
        tracker_thread = threading.Thread(target=tracker.run)
        tracker_thread.daemon = True
        tracker_thread.start()
    else:
        start_button.config(text="You Killed it!!")
        startConfetti(True)
        tracker.listener.stop()

def update_text_box(message):
    text_box.insert(tk.END, message)
    text_box.see(tk.END)  # Auto-scrolls to the bottom

def on_resize(event):
    # Redraw gradient with new dimensions
    canvas.delete("gradient")
    create_gradient(canvas, background_color_start, background_color_end, event.width, event.height)

root = tk.Tk()
root.title("@5MEkailO's Beautiful Clicker Tracker")
#``````````````````````````````````````````````````````````````````````````````````````````````````````````````
# Reimagined Color Palette and Styling
background_color_start = "#FF6B6B"  # Vibrant pink for gradient start
background_color_end = "#FFD93D"    # Bright yellow for gradient end
text_color = "#6BCB77"              # Fresh green for text
button_color = "#4D96FF"            # Electric blue for buttons
button_hover_color = "#F55C47"      # Fiery orange for button hover
scrollbar_color = "#32AFA9"         # Teal for the scrollbar

custom_font = tkFont.Font(family="Consolas", size=13, weight="bold")  # Futuristic monospaced font

label_style = {
    "bg": background_color_start, 
    "fg": text_color, 
    "font": custom_font,
    "relief": "raised",  # Adds a 3D effect to the labels
    "borderwidth": 3
}
text_style = {
    "bg": background_color_end, 
    "fg": text_color, 
    "font": custom_font, 
    "insertbackground": text_color,
    "relief": "sunken",  # Gives a recessed look to the text box
    "borderwidth": 2
}
button_style = {
    "bg": button_color, 
    "fg": background_color_start,  # Contrast text color for buttons
    "font": custom_font, 
    "activebackground": button_hover_color,
    "relief": "groove",  # Adds depth to buttons
    "borderwidth": 2
}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)
create_gradient(canvas, background_color_start, background_color_end, 400, 300) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# Bind the resize event
canvas.bind("<Configure>", on_resize)
# Time display at the top
time_frame = tk.Frame(canvas, bg=background_color_start)
time_frame.pack(anchor="ne", padx=10, pady=10)

def update_time():
    current_time = datetime.datetime.now().strftime(" %H:%M:%S ")
    time_label.config(text=current_time)
    root.after(1000, update_time)

time_label = tk.Label(time_frame, text="", **label_style)
time_label.pack(side="left", padx=10, pady=10)

start_button = tk.Button(time_frame, text="Start Tracking", command=start_tracker, **button_style)
start_button.pack(side="right", padx=10, pady=10)

update_time()

# Create widgets on the canvas
duration_label = tk.Label(canvas, text="OSWS Official Clicker Tracker Bot Cracker ", **label_style)
duration_label.pack(anchor="nw", padx=10, pady=10)

text_box = tk.Text(canvas, wrap="word", **text_style)
text_box.pack(anchor="nw", padx=10, pady=10, fill="both", expand=True)

# Customized scrollbar styling
scrollbar_style = {
    "troughcolor": background_color_start, 
    "bg": scrollbar_color, 
    "activebackground": button_hover_color,
    "relief": "sunken",
    "borderwidth": 1
}
scrollbar = tk.Scrollbar(canvas, command=text_box.yview, **scrollbar_style)
scrollbar.pack(side="right", fill="y")
text_box['yscrollcommand'] = scrollbar.set

# Run the GUI main loop
tracker = ClickTracker(lambda msg: canvas.after(0, update_text_box, msg))
root.mainloop()

