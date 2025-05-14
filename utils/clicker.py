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
        sleep(hold, hold/2 , hold/3)
        if rnd.random() > 0.618:
            time.sleep(rnd.random() * 0.005)
        if rnd.random() > 0.11:
            time.sleep(rnd.random() * 0.005)
            sleep_if()
        if rnd.random() > 0.995:
            time.sleep(rnd.random() * 0.2)
        if rnd.random() > 0.823:
            time.sleep(rnd.random() * 0.2 + rnd.random() * 0.07)
            if rnd.random() > 0.42:
                time.sleep(rnd.random() * 0.13)
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
        sleep(hold, hold/2 , hold/3)
        if rnd.random() > 0.618:
            time.sleep(rnd.random() * 0.05)
        if rnd.random() > 0.11:
            time.sleep(rnd.random() * 0.005)
            sleep_if()
        if rnd.random() > 0.823:
            time.sleep(rnd.random() * 0.3 + rnd.random() * 0.1)
    else:
        time.sleep(hold)
    pag.mouseUp(button='right') # Lift right button up (Finish click)
    sleep()

def upkey(hold = 1, randomize = False): #Hold the up key to adjust the camera view
    pag.keyDown('up')
    if randomize:
        sleep(hold, hold/2 , hold/3)
        if rnd.random() > 0.618:
            time.sleep(rnd.random() * 0.05)
        if rnd.random() > 0.11:
            time.sleep(rnd.random() * 0.005)
            sleep_if()
        if rnd.random() > 0.823:
            time.sleep(rnd.random() * 0.3 + rnd.random() * 0.1)
    else:
        time.sleep(hold)
    pag.keyUp('up')
    sleep()

#Define downkey function

def downkey(hold =2, randomize = False): #Hold the down key to adjust camera view
    pag.keyDown('down')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/8 , hold/10)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('down')
    sleep()

#Define a function that will push down the left key for 3 seconds, then release it.

def leftkey(hold = .5, randomize = False):
    pag.keyDown('left')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/3 , hold/7)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('left')
    sleep()

def spacekey(hold = .1, randomize = True):
    pag.keyDown('space')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/3 , hold/8)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('space')
    sleep() 

def onekey(hold = .1, randomize = True):
    pag.keyDown('1')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/3 , hold/7)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('1')
    sleep()

def twokey(hold = .1, randomize = True):
    pag.keyDown('2')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/3 , hold/3)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('2')
    sleep()

def threekey(hold = .1, randomize = True):
    pag.keyDown('3')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/2 , hold/3)
    else:
        sleep(hold, hold/10, hold/100)
    pag.keyUp('3')
    sleep()

def left_ctrl(hold = .3, randomize = True):
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/2 , hold/3)
    else:
        sleep(hold, hold/10, hold/100)
    sleep()

def right_ctrl(hold = .3, randomize = True):
    pag.keyDown('right ctrl')
    if randomize:
        if rnd.random() > 0.118:
            time.sleep(rnd.random() / 10 * hold)
            sleep_if()
        sleep(hold, hold/2 , hold/5)
    else:
        sleep(hold, hold/9, hold/100)
    pag.keyUp('right ctrl')
    sleep()

def double_click():
    pag.double_click()

# Only run this if the script is run directly
if __name__ == "__main__":
    print("Starting click")
    click(0.1, 1)
    print("Done!")
    sleep() #sleep for 1 second