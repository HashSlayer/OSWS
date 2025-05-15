"""
Item Slots Module for OSWS Framework

This module handles inventory and bank slot interactions, including:
- Coordinate calculations for slots
- Movement patterns for item operations
- Bank interface interactions

Key Concepts:
1. Click Variance (z parameter):
   - Defines clickable area within an item slot
   - e.g., z=10 creates 21x21px click area (x±10, y±10)
   - Distributes clicks naturally within item bounds
   - Not related to movement distance

2. Timing Patterns:
   - Random components simulate human variance
   - Different patterns for different actions
   - Base times chosen for typical human reactions

3. Bank/Inventory Layout:
   - Fixed grid structures (4x7 inv, 8xN bank)
   - Consistent spacing between slots
   - Bank rows adjust based on items but spacing stays constant

Areas for Improvement:
1. ✓ Replace wildcard imports with specific imports (Fixed)
2. Add validation for coordinate ranges
3. Consider configuration system for timing patterns
"""

import random as rnd
import tkinter as tk
from pynput.keyboard import Key, Controller

# Core utilities
from .core.timing import sleep

# Movement utilities
from .movements import bezierMove, bezier_between, bezier_relative, simple_move

# Click utilities
from .clicker import click, right_click

# Inventory slots can change depending on the resolution. This is a function to get the correct inventory slots for any resolution.
# Currently optimized for 1920x1080, 16:9 aspect ratio. 
# The scaling plugin should be used to scale the inventory slots to 45% as well. 

# Keyboard controller for modifier keys
keyboard = Controller()

def inv_slot(slot = 1, time_multiplier = 1, x = 1625, y=638, z=10):
    """
    Calculate and move to an inventory slot position.
    
    Args:
        slot: Inventory slot number (1-28)
        time_multiplier: Movement speed multiplier
        x: Base x-coordinate for first slot (1920x1080, 45% scaling)
        y: Base y-coordinate for first slot (1920x1080, 45% scaling)
        z: Click variance radius (creates (2z+1) x (2z+1) click area, e.g. z=10 → 21x21px)
    
    Note:
    - z defines valid click area within item bounds
    - Fixed grid: 4 columns, 7 rows
    - 61px horizontal spacing, 51px vertical spacing
    """
    slot -= 1  # Convert to 0-based index
    row = slot // 4  # Calculate row (0-6)
    column = slot % 4  # Calculate column (0-3)
    
    # Calculate slot position
    x = x + (61 * column)  # 61 pixels between columns
    y = y + (51 * row)    # 51 pixels between rows
    
    # Add random variance within item bounds
    x = rnd.randint(x - z, x + z)
    y = rnd.randint(y - z, y + z)
    
    if slot < 29:
        #print("Slot:", slot, " Row:", row, " Column:", column, " X:", x, " Y:", y)
        bezierMove(x, y, time_multiplier)
    else:
        sleep(.1, .9, .9)  # Invalid slot - could be improved with error handling

# Dropping items, create a drop_inventory function that holds shift and clicks the inventory slots
def drop_inventory(slots = 28, time_multiplier = 1, x = 1625, y=638, z=8):
    """
    Drop items from inventory using various patterns.
    
    Patterns and Probabilities:
    1. Column-based (20%): 
       - Methodical dropping by columns
       - Longer pauses between columns
       - Simulates organized inventory management
       
    2. Zig-zag (50%):
       - Natural back-and-forth movement
       - Most common human pattern
       - Variable delays between rows
       
    3. Sequential (30%):
       - Quick, straightforward dropping
       - Minimal delays
       - Simulates rushed inventory clearing
    """
    keyboard.press(Key.shift)  # Hold shift key
    
    try:
        random_value = rnd.random()
        
        if random_value > 0.8:  # Column pattern
            for i in range(4):
                for slot in range(i + 1, slots + 1, 4):
                    inv_slot(slot, time_multiplier, x, y, z)
                    sleep(.1, .1, .1)
                    if rnd.random() > 0.98:  # Occasional extra delay
                        sleep(.1, .1, .1)
                    click()
                    if rnd.random() > 0.98:  # Longer pause between columns
                        sleep(.1, .6, .4)
                        
        elif random_value > 0.3:  # Zig-zag pattern
            for row in range(7):
                if row % 2 == 0:  # Left to right
                    for col in range(4):
                        slot = row * 4 + col + 1
                        if slot <= slots:
                            inv_slot(slot, time_multiplier, x, y, z)
                            sleep(.1, .1, .1)
                            if rnd.random() > 0.98:
                                sleep(.1, .1, .1)
                            click()
                            if rnd.random() > 0.95:
                                sleep(.1, .4, .4)
                else:  # Right to left
                    for col in range(3, -1, -1):
                        slot = row * 4 + col + 1
                        if slot <= slots:
                            inv_slot(slot, time_multiplier, x, y, z)
                            sleep(.1, .1, .1)
                            if rnd.random() > 0.95:
                                sleep(.1, .1, .1)
                            click()
                            if rnd.random() > 0.98:
                                sleep(.1, .5, .1)
                                
        else:  # Sequential pattern
            for slot in range(1, slots + 1):
                inv_slot(slot, time_multiplier, x, y, z)
                sleep(.1, .1, .1)
                if rnd.random() > 0.98:
                    sleep(.1, .1, .1)
                click()
                if rnd.random() > 0.98:
                    sleep(.1, .1, 1)
    finally:
        keyboard.release(Key.shift)  # Ensure shift key is released

def simp_inv_slot(slot = 1, time_multiplier = 1, x = 1625, y=638, z=8):
    """
    Simplified inventory slot movement (less human-like).
    
    This function provides a faster, less complex mouse movement to inventory slots
    when full human-like motion is not required. Uses simple_move instead of bezierMove.
    
    Use cases:
    - Rapid inventory operations where detection risk is lower
    - Testing and debugging scenarios
    - When performance is prioritized over human simulation
    
    The z value defaults to 8 (smaller than inv_slot's 10) to create a slightly more
    precise click area (17x17px vs 21x21px) since this function is often used for
    more deliberate actions.
    
    The sleep for invalid slots is maintained for consistency with the inv_slot function
    and to prevent errors if an invalid slot is accidentally requested.
    """
    slot -= 1
    row = slot // 4
    column = slot % 4
    x = x + (61 * column)
    y = y + (51 * row)
    x = rnd.randint(x - z, x + z)
    y = rnd.randint(y - z, y + z)
    if slot < 29:
        simple_move(x, y, time_multiplier)
    else:
        sleep(.1, .9, .9)

def bank_slot(slot = 1, time_multiplier = 1, sleep_for = .01, sleep_upto = .01, x = 520, y=160, z=10):
    """
    Move to a bank slot position.
    
    Bank Interface Properties:
    - 8 slots per row (fixed width)
    - Consistent 69px horizontal, 52px vertical spacing
    - z=10 provides natural click distribution
    - Short sleep times optimize banking speed
    
    Note: Bank rows adjust based on item count but spacing remains constant
    """
    slot -= 1
    row = slot // 8  # 8 slots per row (fixed)
    column = slot % 8
    x = x + (69 * column)  # 69px horizontal spacing
    y = y + (52 * row)    # 52px vertical spacing
    x = rnd.randint(x - z, x + z)
    y = rnd.randint(y - z, y + z)
    #print("Slot:", slot, " Row:", row, " Column:", column, " X:", x, " Y:", y)
    bezierMove(x, y, time_multiplier)
    sleep(sleep_for, sleep_upto, .003)

def bank_near_inv(x1=1480, x2=1540, y1=615, y2=885, time= rnd.randint(23, 48)/100, wait=.3):
    """
    Move to bank interface near inventory.
    
    The function uses a large click area (60px wide, 270px tall) to simulate
    natural variance in clicking the bank interface area adjacent to the inventory.
    
    Key characteristics:
    - Coordinates are optimized for 1920x1080 resolution with 45% RuneLite scaling
    - Wide vertical range (y1-y2) allows clicking different parts of the bank panel
    - Time randomization (0.23-0.48s) creates varied movement speeds
    - Movement duration is intentionally longer than some other bank functions
      to simulate the deliberate action of switching from inventory to bank
    
    The wait parameter (0.3s default) provides time for the bank interface to respond
    after clicking, with a double sleep pattern to create natural timing variance.
    """
    bezier_between(x1, x2, y1, y2, time) 
    sleep(.1, wait, .05) #sleep#open up the bank.
    sleep()

# Exit the bank
def exit_bank(x1=1075, x2=1100, y1=41, y2=64, time= rnd.randint(30, 52)/100, pause_upto=.2):
    """
    Click the bank interface exit button.
    
    This function has two distinct clicking patterns:
    - 60% chance: Standard target area for the X button (25x23px rectangle)
    - 40% chance: Slightly offset target area with small padding adjustments
    
    The probability split (60/40) provides a balance between:
    - Consistent clicks on the button's hotspot (most common human behavior)
    - Minor targeting variations (occasional human imprecision)
    
    The time range (0.30-0.52s) is slightly slower than bank_near_inv because:
    - Exit is typically a more deliberate action than opening
    - Users often pause briefly before closing interfaces
    
    The double sleep pattern (pause + standard sleep) creates a natural
    rhythm for finishing a banking session before continuing with gameplay.
    """
    if (rnd.random() > 0.6):
        bezier_between(x1, x2, y1, y2, time)
    else:
        bezier_between(x1+3, x2-5, y1+5, y2-2, time) #Disrupt entirely random location
    sleep(.05, pause_upto, .02) #Pause before exiting bank
    sleep()

#Deposit all items in inventory
def deposit_all(x=1030, y=760, size=9, time = rnd.randint(30, 45)/100, pause_upto=.5):
    """
    Click the deposit all button.
    
    This function has two distinct clicking patterns:
    - 70% chance: Uses a variable-sized click area (size parameter)
    - 30% chance: Uses fixed offsets for a more precise click area
    
    The longer pause_upto value (0.5s) compared to other banking functions is 
    intentional because:
    - Depositing items often requires waiting for inventory to clear
    - Users typically pause after major inventory changes
    - This creates a natural break in the interaction flow
    
    The size parameter (default 9px) is only used in the variable click pattern
    to create a natural distribution of clicks centered on the button. The fixed
    pattern uses specific offsets that create a slightly asymmetric but natural
    click area (15x16px) based on common user click patterns.
    """
    if (rnd.random() > 0.7):
        bezier_between(x-size, x+size, y-size, y+size, time)
    else:
        bezier_between(x-7,x+8, y-6, y+10, time)
    sleep(.1, pause_upto, .02) #sleep


#Set as Withdraw item as note    
#def withdraw_as_note(x1 = 685, x2=705, y1 = 775, y2=780, time = rnd.randint(40, 55)/100, pause_upto = .2):
 #   if (rnd.random() > 0.8):
  #      bezier_between(x1, x2, y1, y2, time)
   # sleep(.1, pause_upto, .02) #sleep
    #click()


#RELATIVE MOVEMENT
def get_x_items(x1 = -30, x2 = 20, y1 = 93, y2 = 97, time= rnd.random() * 0.1 + rnd.randint(13, 39)/100, pause_upto=.2):
    """
    Select X items from right-click menu.
    
    Movement Pattern:
    - Wider horizontal range (-30 to +20) matches menu shape
    - Narrow vertical range (93-97) for precise option selection
    - Time calculation combines smooth (0.1) and stepped (13-39ms) components
    - ~69% chance for wider movement adds natural variance
    
    Note: Menu options are wider than they are tall, hence movement distribution
    """
    sleep(.03, .09)
    right_click()
    if rnd.random() > 0.69420:  # ~31% chance for wider movement range (specific value not critical)
        bezier_relative(x1-15, x2+10, y1, y2, time)  # Wider movement
    else:
        bezier_relative(x1, x2, y1+1, y2-1, time)  # Precise movement
    sleep(.05, pause_upto, .02)


     # Copy the get_x_items() function with this line: pag.moveRel(rnd.randint(-30, 17), rnd.randint(101, 114), yrt * 0.12 + 0.23) #move mouse down to quantity of all


def get_all_items(x1 = -30, x2 = 20, y1 = 132, y2 = 136, time= rnd.random() * 0.15 + 0.3, pause_upto=.2):
    """
    Select all items from right-click menu.
    
    Differences from get_x_items:
    - Lower y-position (132-136) for "All" option
    - Longer base time (0.3 vs 0.1) as it's often a deliberate choice
    - Same x-range as menu width is consistent
    """
    sleep(.03, .09)
    right_click()
    if rnd.random() > 0.69420:
        bezier_relative(x1-15, x2+10, y1, y2+5, time)
    else:
        bezier_relative(x1, x2, y1+1, y2-1, time)
    sleep(.05, pause_upto, .02)

# Utility functions for screen dimensions and scaling

def get_screen_dimensions():
    """Get the current screen dimensions for scaling calculations."""
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def suggest_inventory_scaling():
    """Recommend optimal RuneLite scaling for current coordinates."""
    print("Suggested inventory scaling: 45%")

if __name__ == "__main__":
    width, height = get_screen_dimensions()
    print(f"Screen dimensions: {width}x{height}")
    suggest_inventory_scaling()
