import tkinter as tk

def create_gradient(canvas, color1, color2, width, height):
    """Create a gradient background between two colors."""
    for i in range(height):
        # Calculate color components based on the gradient
        r1, g1, b1 = canvas.winfo_rgb(color1)  # Get RGB components of the start color
        r2, g2, b2 = canvas.winfo_rgb(color2)  # Get RGB components of the end color
        
        # Interpolate the RGB components based on the current position
        r = (r1 + int((r2 - r1) * i / height)) & 0xff00 
        g = (g1 + int((g2 - g1) * i / height)) & 0xff00 
        b = (b1 + int((b2 - b1) * i / height)) & 0xff00 
        
        color = f'#{r:04x}{g:04x}{b:04x}'
        canvas.create_line(0, i, width, i, fill=color)

def setup_gradient_background(root, color1, color2):
    """Set up a gradient background on a tkinter window."""
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)
    
    def on_resize(event=None):
        if event:
            width, height = event.width, event.height
        else:
            width, height = root.winfo_reqwidth(), root.winfo_reqheight()
        canvas.delete("gradient")
        create_gradient(canvas, color1, color2, width, height)
    
    canvas.bind("<Configure>", on_resize)
    on_resize()  # Initial gradient creation
    
    return canvas 