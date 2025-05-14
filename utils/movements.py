import time
import pyautogui as pag
import random as rnd
import math
import mouse
from .core.timing import *

# Configure PyAutoGUI settings for immediate execution
pag.MINIMUM_DURATION = 0
pag.MINIMUM_SLEEP = 0
pag.PAUSE = 0

def simple_move(x: int, y: int, duration: float):
    """
    Basic direct mouse movement with no humanization.
    Best used for testing or when exact movements are needed.
    
    Args:
        x: Target x coordinate
        y: Target y coordinate
        duration: Movement time in seconds (0.1-1.0 recommended)
    """
    mouse.move(x, y, duration)

def move_to(x: int = 900, y: int = 600, duration: float = 0.3):
    """
    Move to a random point within a central screen area.
    Useful for resetting mouse position or simulating idle movements.
    
    Args:
        x: Center point x (default 900)
        y: Center point y (default 600)
        duration: Base movement time, will be randomized (default 0.3)
    
    Note: Actual coordinates will be randomized:
        x: 400-1600 range
        y: 400-900 range
        duration: 0.1-0.4 seconds
    """
    x = rnd.randint(400, 1600)
    y = rnd.randint(400, 900)
    duration = rnd.random() * 0.3 + 0.1
    bezierMove(x, y, duration)

def quadratic_bezier(p0: tuple, p1: tuple, p2: tuple, t: float) -> tuple:
    """
    Calculate a point along a quadratic Bezier curve.
    Internal helper function for bezier movements.
    
    Args:
        p0: Start point (x,y)
        p1: Control point (x,y)
        p2: End point (x,y)
        t: Time parameter (0-1)
    
    Returns:
        (x,y) coordinates of point on curve
    """
    x = ((1 - t) ** 2) * p0[0] + 2 * (1 - t) * t * p1[0] + (t ** 2) * p2[0]
    y = ((1 - t) ** 2) * p0[1] + 2 * (1 - t) * t * p1[1] + (t ** 2) * p2[1]
    return (x, y)

def bezier_between(x1: int, x2: int, y1: int, y2: int, time: float = 0.4):
    """
    Move to a random point within a rectangular area using bezier curve.
    Best for UI interactions where exact position isn't critical.
    
    Args:
        x1: Min x coordinate
        x2: Max x coordinate
        y1: Min y coordinate
        y2: Max y coordinate
        time: Base movement time (actual time will be 0.2-0.6 × time)
    """
    bezierMove(
        rnd.randint(x1, x2),
        rnd.randint(y1, y2),
        (rnd.random() * time/2) + (time - time/10)
    )

def bezier_relative(x1: int, x2: int, y1: int, y2: int, time: float = 0.3):
    """
    Move relative to current position within given ranges.
    Best for small adjustments or natural-looking wandering movements.
    
    Args:
        x1: Min x offset from current position
        x2: Max x offset from current position
        y1: Min y offset from current position
        y2: Max y offset from current position
        time: Base movement time (actual time will be 0.15-0.45 × time)
    """
    bezierMoveRelative(
        rnd.randint(x1, x2),
        rnd.randint(y1, y2),
        (rnd.random() * time/2) + (time - time/5)
    )

def bezierMove(x: int, y: int, duration: float):
    """
    Move to exact coordinates using humanized bezier curve movement.
    Primary function for most mouse movements - highly human-like.
    
    Args:
        x: Target x coordinate
        y: Target y coordinate
        duration: Base time for movement
            - Actual duration scales with distance
            - Short moves (< 100px): ~0.1-0.3s
            - Medium moves (100-500px): ~0.2-0.6s
            - Long moves (>500px): ~0.4-1.0s
    
    Features:
        - Dynamic speed (slower start/end, faster middle)
        - Small random perturbations
        - Occasional micro-pauses
        - Distance-based control point variation
    """
    start_x, start_y = pag.position()
    distance = math.hypot(x - start_x, y - start_y)

    # Scale duration based on distance (longer distance = longer duration)
    duration = duration * (.02 + distance / 1800)

    # Control point variation scales with distance
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
        if rnd.random() < 0.03:  # 3% chance of micro-pause
            time.sleep(rnd.uniform(0.03, 0.1))
    mouse.move(x, y, absolute=True)  # Ensure we hit target exactly

def bezierMoveRelative(dx: int, dy: int, duration: float):
    """
    Move relative to current position using humanized bezier curve.
    Similar to bezierMove but uses relative coordinates.
    
    Args:
        dx: X distance to move (positive = right, negative = left)
        dy: Y distance to move (positive = down, negative = up)
        duration: Base time for movement (scales with distance)
    
    Note: Shares same humanization features as bezierMove
    """
    start_x, start_y = pag.position()
    end_x, end_y = start_x + dx, start_y + dy
    
    distance = math.hypot(dx, dy)
    control_variation = min(100, max(30, int(distance / 6)))
    
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

def randomMove(duration: float = 0.5):
    """
    Make small random movements around current position.
    Good for simulating slight hand tremors or idle movement.
    
    Args:
        duration: How long to perform random movements (seconds)
    
    Note: Creates tiny movements (±1px) with short pauses
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        dx, dy = rnd.randint(-1, 1), rnd.randint(-1, 1)
        pag.moveRel(dx, dy, duration=0.1)
        time.sleep(rnd.uniform(0.05, 0.2))

def Notbotting():
    """
    Perform a sequence of natural-looking movements.
    Used to simulate human-like mouse behavior during breaks.
    
    Sequence:
    1. Large wandering movement (-200 to +200 x, -100 to +400 y)
    2. Possible pause (20% chance)
    3. Small random movements
    4. Small wandering movement (-30 to +30 x, -60 to +60 y)
    
    Total duration: ~2-2.4 seconds
    """
    sleep(0.01, .01, .01)
    bezier_relative(-200, 200, -100, 400, .3)
    if rnd.random() > 0.8:
        sleep(0.02, 1, .1)
    randomMove(0.01 + 0.1 * rnd.random())
    bezier_relative(-30, 30, -60, 60, .2)
    sleep()

# Note: move_mouse_smoothly is currently unused and duplicates bezierMove functionality
# Consider removing or repurposing for specific use cases

if __name__ == "__main__":
    sleep()
    print("Hello World from movements.py") 
