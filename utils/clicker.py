# mouse clicker module

import time as time
import pyautogui as pag
import random as rnd
from .core.timing import sleep
from .core.key_timing import get_hold_duration, get_sequence_delay

pag.MINIMUM_DURATION = 0
pag.MINIMUM_SLEEP = 0
pag.PAUSE = 0

#consider using pynput.mouse to control mouse movements instead of pyautogui for more undetected behavior.

# Track key sequence for natural delays
_last_key = None

def _update_sequence(key: str):
    """Update the key sequence tracking"""
    global _last_key
    _last_key = key

def click(hold = 0.01, randomize = True):
    """
    Simulates a human-like mouse click with natural duration distribution.
    Base click time ~0.02-0.04s with occasional longer holds.
    """
    pag.mouseDown(button='left')
    
    if randomize:
        hold_time = get_hold_duration("action", hold, "neutral", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.mouseUp(button='left')
    sleep(.01, .02, .01)  # Small pause after click

def quick_click(hold=0.02, randomize=True):
    """Fast click with minimal randomization"""
    pag.mouseDown(button='left')
    if randomize:
        hold_time = get_hold_duration("action", hold, "combat", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
    pag.mouseUp(button='left')
    sleep(hold/2, hold/4, hold/4)

def right_click(hold=0.03, randomize=True):
    """
    Right click - typically held slightly longer than left click
    Often used for menus/options, so more deliberate
    Base time ~0.03-0.06s
    """
    pag.mouseDown(button='right')
    if randomize:
        hold_time = get_hold_duration("action", hold, "inventory", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
    pag.mouseUp(button='right')
    sleep(hold, hold/2, hold/2)

def spacekey(hold=0.06, randomize=True):
    """
    Space bar - varies between quick taps and medium holds
    Common for jumping/continuing/selecting
    Base tap ~0.03-0.07s
    """
    global _last_key
    pag.keyDown('space')
    
    if randomize:
        hold_time = get_hold_duration("action", hold, "combat", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('space')
    delay = get_sequence_delay(_last_key, 'space')
    sleep(delay, delay/2, delay/4)
    _update_sequence('space')

def upkey(hold=0.3, randomize=True):
    """
    Movement key - varies between taps and holds
    Base tap ~0.03-0.06s, with common longer holds
    """
    global _last_key
    pag.keyDown('up')
    
    if randomize:
        hold_time = get_hold_duration("movement", hold, "movement", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('up')
    delay = get_sequence_delay(_last_key, 'up')
    sleep(delay, delay/2, delay/4)
    _update_sequence('up')

def downkey(hold=0.3, randomize=True):
    """
    Movement key - varies between taps and holds
    Base tap ~0.03-0.06s, with common longer holds
    """
    global _last_key
    pag.keyDown('down')
    
    if randomize:
        hold_time = get_hold_duration("movement", hold, "movement", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('down')
    delay = get_sequence_delay(_last_key, 'down')
    sleep(delay, delay/2, delay/4)
    _update_sequence('down')

def leftkey(hold=0.3, randomize=True):
    """
    Movement key - varies between taps and holds
    Base tap ~0.03-0.06s, with common longer holds
    """
    global _last_key
    pag.keyDown('left')
    
    if randomize:
        hold_time = get_hold_duration("movement", hold, "movement", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('left')
    delay = get_sequence_delay(_last_key, 'left')
    sleep(delay, delay/2, delay/4)
    _update_sequence('left')

def onekey(hold=0.01, randomize=True):
    """
    First inventory slot - typically very quick access
    Muscle memory makes this the fastest inventory key
    Base press extremely quick (0.01-0.04s)
    """
    global _last_key
    pag.keyDown('1')
    
    if randomize:
        hold_time = get_hold_duration("inventory", hold, "inventory", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('1')
    delay = get_sequence_delay(_last_key, '1')
    sleep(delay, delay/2, delay/4)
    _update_sequence('1')

def twokey(hold=0.012, randomize=True):
    """
    Second inventory slot - very quick access
    Slightly more variance than first slot but still fast
    Base press quick (0.012-0.045s)
    """
    global _last_key
    pag.keyDown('2')
    
    if randomize:
        hold_time = get_hold_duration("inventory", hold, "inventory", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('2')
    delay = get_sequence_delay(_last_key, '2')
    sleep(delay, delay/2, delay/4)
    _update_sequence('2')

def threekey(hold=0.015, randomize=True):
    """
    Third inventory slot - quick access but more variance
    Base press quick (0.015-0.05s)
    """
    global _last_key
    pag.keyDown('3')
    
    if randomize:
        hold_time = get_hold_duration("inventory", hold, "inventory", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('3')
    delay = get_sequence_delay(_last_key, '3')
    sleep(delay, delay/2, delay/4)
    _update_sequence('3')

def fourkey(hold=0.018, randomize=True):
    """
    Fourth inventory slot - quick access with moderate variance
    Base press quick (0.018-0.055s)
    """
    global _last_key
    pag.keyDown('4')
    
    if randomize:
        hold_time = get_hold_duration("inventory", hold, "inventory", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('4')
    delay = get_sequence_delay(_last_key, '4')
    sleep(delay, delay/2, delay/4)
    _update_sequence('4')

def fivekey(hold=0.02, randomize=True):
    """
    Fifth inventory slot - quick access with higher variance
    Base press quick (0.02-0.06s)
    """
    global _last_key
    pag.keyDown('5')
    
    if randomize:
        hold_time = get_hold_duration("inventory", hold, "inventory", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('5')
    delay = get_sequence_delay(_last_key, '5')
    sleep(delay, delay/2, delay/4)
    _update_sequence('5')

def left_ctrl(hold=0.04, randomize=True):
    """
    Left control - modifier key with consistent timing
    Often used in combinations
    """
    global _last_key
    pag.keyDown('ctrl')
    
    if randomize:
        hold_time = get_hold_duration("modifier", hold, "neutral", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('ctrl')
    delay = get_sequence_delay(_last_key, 'left_ctrl')
    sleep(delay, delay/2, delay/4)
    _update_sequence('left_ctrl')

def right_ctrl(hold=0.04, randomize=True):
    """
    Right control - modifier key with consistent timing
    Less commonly used than left control
    """
    global _last_key
    pag.keyDown('ctrl')
    
    if randomize:
        hold_time = get_hold_duration("modifier", hold, "neutral", randomize)
        time.sleep(hold_time)
    else:
        time.sleep(hold)
        
    pag.keyUp('ctrl')
    delay = get_sequence_delay(_last_key, 'right_ctrl')
    sleep(delay, delay/2, delay/4)
    _update_sequence('right_ctrl')

def double_click():
    """Perform a double click with natural timing"""
    click(0.01, True)
    sleep(0.1, 0.05, 0.02)  # Natural pause between clicks
    click(0.01, True)

# Only run this if the script is run directly
if __name__ == "__main__":
    print("Starting click")
    sleep(0.5, 0.5, 0.5)
    click(0.1, True)
    print("Done!")
    sleep()