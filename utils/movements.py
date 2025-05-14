import time
import pyautogui as pag
import random as rnd
import math
import mouse
from .core.timing import *

pag.MINIMUM_DURATION = 0
pag.MINIMUM_SLEEP = 0
pag.PAUSE = 0

#define the move function
def simple_move(x, y, duration):
    #move the mouse to the x and y coordinates
    mouse.move(x, y, duration)

def move_to(x = 900, y = 600, duration = 0.3):
    # x, and y are set to random values between 0 and 1920, and 0 and 1080
    x = rnd.randint(400, 1600)
    y = rnd.randint(400, 900)
    duration = rnd.random() * 0.3 + 0.1
    bezierMove(x, y, duration)

#Moving into bezierMove we aim to use multiple bezier curves to move the mouse in a more human like fashion, with dynamic speed and acceleration.
def quadratic_bezier(p0, p1, p2, t):
    """Calculate the quadratic Bezier curve point at t."""
    x = ((1 - t) ** 2) * p0[0] + 2 * (1 - t) * t * p1[0] + (t ** 2) * p2[0]
    y = ((1 - t) ** 2) * p0[1] + 2 * (1 - t) * t * p1[1] + (t ** 2) * p2[1]
    return (x, y)

def bezier_between(x1, x2, y1, y2, time = .4):
    bezierMove(rnd.randint(x1, x2), rnd.randint(y1, y2), (rnd.random() * time/2) + (time - time/10)) # move mouse to banker.

def bezier_relative(x1, x2, y1, y2, time = 0.3):
    bezierMoveRelative(rnd.randint(x1, x2), rnd.randint(y1, y2), (rnd.random() * time/2) + (time - time/5)) # move mouse to banker.

def bezierMove(x, y, duration):
    start_x, start_y = pag.position()
    distance = math.hypot(x - start_x, y - start_y)

    # Dynamic duration calculation based on distance
    # Base duration is adjusted by the relative distance
    duration = duration * (.02 + distance / 1800)

    control_variation = min(100, max(30, int(distance / 6)))
    control_x = rnd.choice([start_x, x]) + rnd.randint(-control_variation, control_variation)
    control_y = rnd.choice([start_y, y]) + rnd.randint(-control_variation, control_variation)

    p0 = (start_x, start_y)
    p1 = (control_x, control_y)
    p2 = (x, y)

    steps = int(duration * rnd.randint(160, 210))
    for i in range(steps):
        t = i / float(steps)
        adaptive_speed = duration / steps * (0.1 + 0.7 * math.sin(math.pi * t))
        target_x, target_y = quadratic_bezier(p0, p1, p2, t)
        perturbation_x = rnd.randint(-1, 1)
        perturbation_y = rnd.randint(-1, 1)
        pag.moveTo(target_x + perturbation_x, target_y + perturbation_y, _pause=False)
        time.sleep(adaptive_speed)
        if rnd.random() < 0.03:
            time.sleep(rnd.uniform(0.03, 0.1))
    mouse.move(x, y, absolute=True)

def bezierMoveRelative(dx, dy, duration):
    start_x, start_y = pag.position()
    end_x, end_y = start_x + dx, start_y + dy
    control_variation = min(100, max(30, int(math.hypot(dx, dy) / 6)))
    control_x = rnd.choice([start_x, end_x]) + rnd.randint(-control_variation, control_variation)
    control_y = rnd.choice([start_y, end_y]) + rnd.randint(-control_variation, control_variation)
    p0 = (start_x, start_y)
    p1 = (control_x, control_y)
    p2 = (end_x, end_y)
    steps = int(duration * 100)
    for i in range(steps):
        t = i / float(steps)
        adaptive_speed = duration / steps * (0.1 + 0.5 * math.sin(math.pi * t))
        target_x, target_y = quadratic_bezier(p0, p1, p2, t)
        perturbation_x = rnd.randint(-1, 1)
        perturbation_y = rnd.randint(-1, 1)
        pag.moveTo(target_x + perturbation_x, target_y + perturbation_y, _pause=False)
        time.sleep(adaptive_speed)
        if rnd.random() < 0.03:
            time.sleep(rnd.uniform(0.03, 0.1))
    pag.moveTo(end_x, end_y, _pause=False, duration=rnd.random() * 0.02 + 0.03)

def randomMove(duration=0.5):
    start_time = time.time()
    while time.time() - start_time < duration:
        # Random small movements
        dx, dy = rnd.randint(-1, 1), rnd.randint(-1, 1)
        pag.moveRel(dx, dy, duration=0.1)
        # Random short pauses
        time.sleep(rnd.uniform(0.05, 0.2))

#Define a function that makes random and realistic mouse movements totaling about 2 seconds. + or - 0.2 seconds.
def Notbotting():
    sleep(0.01, .01, .01) #sleep
    bezier_relative(-200, 200, -100, 400, .3)
    if rnd.random() > 0.8:
        sleep(0.02, 1, .1) #sleep 
    randomMove(0.01 + 0.1 * rnd.random())
    bezier_relative(-30, 30, -60, 60, .2)
    sleep()

def move_mouse_smoothly(distance_x):
    """
    Move the mouse horizontally (to the right if positive, left if negative) 
    using bezier curve for smooth, natural movement.
    
    Args:
        distance_x: Number of pixels to move horizontally
    """
    start_x, start_y = pag.position()
    end_x = start_x + distance_x
    
    # Generate a random variation for the control point
    control_variation = min(300, max(100, int(abs(distance_x) / 5)))
    
    # Create control point with vertical variation
    control_x = start_x + (distance_x // 2) + rnd.randint(-100, 100)
    control_y = start_y + rnd.randint(-control_variation, control_variation)
    
    # Set up bezier curve points
    p0 = (start_x, start_y)
    p1 = (control_x, control_y)
    p2 = (end_x, start_y + rnd.randint(-30, 30))  # Small vertical variation at end
    
    # Dynamic duration based on distance
    duration = 0.5 + (abs(distance_x) / 3000)
    
    # Slightly randomize number of steps
    steps = int(duration * rnd.randint(180, 220))
    
    for i in range(steps):
        t = i / float(steps)
        # Varying speed - slower at start/end, faster in middle
        adaptive_speed = duration / steps * (0.2 + 0.8 * math.sin(math.pi * t))
        
        # Calculate position along bezier curve
        target_x, target_y = quadratic_bezier(p0, p1, p2, t)
        
        # Add small random perturbations for more natural movement
        perturbation_x = rnd.randint(-2, 2)
        perturbation_y = rnd.randint(-2, 2)
        
        pag.moveTo(target_x + perturbation_x, target_y + perturbation_y, _pause=False)
        
        time.sleep(adaptive_speed)
        # Occasionally add tiny pause
        if rnd.random() < 0.05:
            time.sleep(rnd.uniform(0.01, 0.08))
    
    # Ensure we end exactly at the target
    pag.moveTo(end_x, p2[1], _pause=False, duration=rnd.random() * 0.05 + 0.02)

#Define another Notbotting function that makes random and realistic mouse movements totaling about 3 seconds. + or - 0.2 seconds, with a different range of movement.

# // This block runs only if the script is executed directly, not when imported.
if __name__ == "__main__":
    quick_sleep() 
    print("Hello World from movements.py") 
