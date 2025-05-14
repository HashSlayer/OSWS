# mouse clicker module

import time as time
import pyautogui as pag
from .core.timing import *

pag.MINIMUM_DURATION = 0
pag.MINIMUM_SLEEP = 0
pag.PAUSE = 0

def click(hold = 0.01, randomize = True):
    pag.mouseDown(button='left')  # Press the right button down
    if randomize:
        sleep(hold, hold/2 * rnd.random(), hold/3 * rnd.random())
        if rnd.random() > 0.618:
            sleep(0.002, 0.002, 0.001)  # ~0.002-0.005s
        if rnd.random() > 0.11:
            sleep(0.007, 0.008, 0.017)  # Quick action sleep ~0.007-0.032s
        if rnd.random() > 0.995:
            sleep(0.05, 0.1, 0.05)  # ~0.05-0.2s
        if rnd.random() > 0.823:
            sleep(0.05, 0.1, 0.12)  # ~0.05-0.27s
    else:
        time.sleep(hold)
    pag.mouseUp(button='left') # Lift right button up (Finish click)
    sleep(.01, .03, .03)

def quick_click(hold = 0.1):
    pag.mouseDown(button='left')  # Press the left button down
    if rnd.random() > 0.2:
        time.sleep(rnd.random() * hold)
    pag.mouseUp(button='left')    # Lift left button up (Finish click)

def right_click(hold =0.1, randomize = True):
    pag.mouseDown(button='right')  # Press the right button down
    if randomize:
        sleep(hold, hold/2 * rnd.random(), hold/3 * rnd.random())
        if rnd.random() > 0.618:
            sleep(0.01, 0.02, 0.02)  # ~0.01-0.05s
        if rnd.random() > 0.11:
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        if rnd.random() > 0.823:
            sleep(0.1, 0.1, 0.2)  # ~0.1-0.4s
    else:
        time.sleep(hold)
    pag.mouseUp(button='right') # Lift right button up (Finish click)
    sleep()

def upkey(hold = 1, randomize = False):
    pag.keyDown('up')
    if randomize:
        sleep(hold, hold/2 * rnd.random(), hold/3 * rnd.random())
        if rnd.random() > 0.618:
            sleep(0.01, 0.02, 0.02)  # ~0.01-0.05s
        if rnd.random() > 0.11:
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        if rnd.random() > 0.823:
            sleep(0.1, 0.1, 0.2)  # ~0.1-0.4s
    else:
        time.sleep(hold)
    pag.keyUp('up')
    sleep()

def downkey(hold = 2, randomize = False):
    pag.keyDown('down')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/8, hold/10)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('down')
    sleep()

def leftkey(hold = .5, randomize = False):
    pag.keyDown('left')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/3, hold/7)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('left')
    sleep()

def spacekey(hold = .3, randomize = True):
    pag.keyDown('space')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/3, hold/8)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('space')
    sleep()

def onekey(hold = .08, randomize = True):
    pag.keyDown('1')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/3, hold/7)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('1')
    sleep()

def twokey(hold = .1, randomize = True):
    pag.keyDown('2')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/3, hold/3)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('2')
    sleep()

def threekey(hold = .1, randomize = True):
    pag.keyDown('3')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/2, hold/3)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('3')
    sleep()

def left_ctrl(hold = .3, randomize = True):
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/2, hold/3)
    else:
        sleep(hold, hold/10, hold/100)
    sleep()

def right_ctrl(hold = .3, randomize = True):
    pag.keyDown('right ctrl')
    if randomize:
        if rnd.random() > 0.118:
            sleep(hold/3 * rnd.random(), hold/6 * rnd.random(), hold/9 * rnd.random())  # More random scaled sleep
            sleep(0.007, 0.008, 0.017)  # Quick action sleep
        sleep(hold, hold/2, hold/5)
    else:
        sleep(hold, hold/9, hold/100)
    pag.keyUp('right ctrl')
    sleep()

def double_click():
    pag.double_click()

# Only run this if the script is run directly
if __name__ == "__main__":
    print("Starting click")
    sleep(0.5, 0.5, 0.5)
    click(0.1, 1)
    print("Done!")
    sleep() #sleep