import random
import time
import tkinter as tk

def create_confetti(canvas):
    """Create confetti particles on the canvas."""
    confetti = []
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for _ in range(random.randint(30, 50)):  # Reduced number of confetti pieces
        x = random.randint(0, canvas_width)
        y = random.randint(0, canvas_height)
        color = random.choice(['red', 'blue', 'green', 'yellow', 'purple'])
        piece = canvas.create_rectangle(x, y, x+3, y+3, fill=color)
        confetti.append(piece)
    return confetti

def update_confetti(canvas, confetti, start_time, duration=1):
    """Update confetti animation frame."""
    current_time = time.time()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if current_time - start_time < duration:
        for item in confetti:
            x_move = random.randint(-3, 3)
            y_move = random.randint(-3, 3)
            canvas.move(item, x_move, y_move)
            
            coords = canvas.coords(item)
            if coords:  # Check if item still exists
                if coords[2] > canvas_width or coords[0] < 0:
                    canvas.move(item, -x_move, 0)
                if coords[3] > canvas_height or coords[1] < 0:
                    canvas.move(item, 0, -y_move)
        
        canvas.after(30, update_confetti, canvas, confetti, start_time)
    else:
        # Clean up confetti
        for item in confetti:
            try:
                canvas.delete(item)
            except:
                pass

def start_confetti(canvas, on=True):
    """Start the confetti animation."""
    if on:
        confetti = create_confetti(canvas)
        start_time = time.time()
        update_confetti(canvas, confetti, start_time) 