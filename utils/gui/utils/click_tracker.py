from datetime import datetime
import time
from pynput import mouse
from .confetti import start_confetti

class ClickTracker:
    """Track mouse clicks and provide feedback."""
    
    def __init__(self, output_function, canvas):
        self.output_function = output_function
        self.canvas = canvas
        self.listener = mouse.Listener(on_click=self.on_click)
        self.tracking = False
        self.process_clicks = True
        self.click_count = 0
        self.start_time = None
        self.end_time = None

    def on_click(self, x, y, button, pressed):
        """Handle click events and provide feedback."""
        if not self.process_clicks:
            return
            
        if button == mouse.Button.left:
            if pressed:
                self.start_time = time.time()
            else:
                self.end_time = time.time()
                duration = self.end_time - self.start_time
                self.click_count += 1

                # Format current time
                current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                # Create feedback message
                message = f"Total Clicks:{self.click_count}: Position: ({x}, {y}), At Time: {current_time}, For: {duration:.3f} seconds."
                
                # Handle milestones
                if self.click_count % 50 == 0:
                    message += f"\n❤️ +~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+~~~+ ❤️"
                    start_confetti(self.canvas)
                
                # Print debug info and update UI
                print(f"Total Clicks: {self.click_count}, Position: ({x}, {y}), At Time: {current_time}, For: {duration} seconds.")
                self.output_function(message)

    def start(self):
        """Start click tracking."""
        if not self.tracking:
            self.tracking = True
            self.process_clicks = True
            self.listener.start()

    def stop(self):
        """Stop click tracking."""
        self.process_clicks = False
        if self.listener.is_alive():
            self.listener.stop()
        self.tracking = False

    def run(self):
        """Run the click tracker."""
        try:
            self.tracking = True
            self.process_clicks = True
            with self.listener:
                self.listener.join()
        except Exception as e:
            print(f"Error in ClickTracker: {e}")
        finally:
            self.tracking = False 