# mouse clicker module

import pyautogui as pag
from timmy import *

def click_between(min_time, max_time):
    quick_sleep()
    pag.click()
    sleep()

def click(hold = 0.013):
    pag.mouseDown(button='left')  # Press the right button down
    sleep(hold)
    time.sleep(rnd.random() * hold/10)
    time.sleep(rnd.random() * 0.05)
    sleep_if()
    if rnd.random() > 0.6:
        time.sleep(rnd.random() * 0.05)
    pag.mouseUp(button='left') # Lift right button up (Finish click)
    quick_sleep()

def hold_click(hold = 0.53):
    pag.mouseDown(button='left')  # Press the right button down
    sleep(hold)
    time.sleep(rnd.random() * hold/10)
    if rnd.random() > 0.6:
        time.sleep(rnd.random() * hold/9)
    sleep_if()
    pag.mouseUp(button='left') # Lift right button up (Finish click)
    quick_sleep()

def double_click():
    pag.double_click()

def click_and_hold():
    pag.click(button='left', clicks=2, interval=0.08)

# Only run this if the script is run directly
if __name__ == "__main__":
    print("Starting click")
    click_between(0.1, 1)
    print("Done!")
    sleep() #sleep for 1 second