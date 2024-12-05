import random
import time
import os
from datetime import datetime
import tkinter as tk
from tkinter import font as tkFont
from pynput import mouse

def create_confetti(canvas):
    confetti = []
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for _ in range(random.randint(80, 160)):  # Create a random number of confetti pieces
        x, y = random.randint(0, canvas_width), random.randint(0, canvas_height)
        confetti.append(canvas.create_rectangle(x, y, x+5, y+5, fill=random.choice(['red', 'blue', 'green', 'pink', 'yellow', 'purple', 'orange'])))
    return confetti

def update_confetti(canvas, confetti, start_time, duration=2):
    current_time = time.time()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    if current_time - start_time < duration:  # Run the animation for the specified duration
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
        canvas.after(60, update_confetti, canvas, confetti, start_time)
    else:
        for item in confetti:
            canvas.delete(item)  # Remove confetti after animation

def startConfetti(canvas, on=True):
    if on:  # Start animation
        confetti = create_confetti(canvas)
        start_time = time.time()
        update_confetti(canvas, confetti, start_time)

class ClickTracker:
    def __init__(self, output_function, canvas):
        self.output_function = output_function
        self.canvas = canvas
        self.listener = mouse.Listener(on_click=self.on_click)
        self.tracking = False
        self.process_clicks = True  # New flag to control click processing
        self.click_count = 0

    def on_click(self, x, y, button, pressed):
        if self.process_clicks:
            if button == mouse.Button.left:
                if pressed:
                    self.start_time = time.time()
                else:
                    self.end_time = time.time()
                    duration = self.end_time - self.start_time
                    self.click_count += 1  # Increment click count

                    # Get the current time
                    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Format: HH:MM:SS.mmm

                    message = f"Total Clicks:{self.click_count}: Position: ({x}, {y}), At Time: {current_time}, For: {duration:.3f} seconds."
                    if self.click_count % 10 == 0:
                        message += f"\n❤️ +~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+ ❤️"
                        startConfetti(self.canvas)
                    #print("bezierMove(rnd.randint(",(x - 5),",",(x + 5),"), rnd.randint(",y-5,",",y+5,"), sleep(.3))")
                    print("Total Clicks:", self.click_count, ": Position: (", x, ",", y, "), At Time: ", current_time, ", For: ", duration, " seconds.")
                    self.output_function(message)
            return

    def stop(self):
        self.process_clicks = False

                
    def run(self):
        try:
            self.tracking = True
            self.process_clicks = True
            with self.listener:
                #if not self.click_tracker_thread.is_alive():
                self.listener.join()
        except Exception as e:
            print(f"Error in ClickTracker: {e}")
        finally:
            self.tracking = False

class GoodGUI:
    def __init__(self, root, output_function):
        self.root = root
        self.output_function = output_function
        self.background_color_start = "#FF6B6B"
        self.background_color_end = "#4D96FF"
        self.canvas_height = self.canvas.winfo_height()  # Get initial canvas height
        self.create_gradient_background()

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

    def on_resize(self, event):
        if event:  # Check if event is None
            width, height = event.width, event.height
        else:
            width, height = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        self.canvas.delete("gradient")
        self.create_gradient(self.canvas, self.background_color_start, self.background_color_end, width, height)
