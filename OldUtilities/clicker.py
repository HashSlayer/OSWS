# mouse clicker

import pyautogui as pag
from . import timmy

def click_between(min_time, max_time):
    timmy.quick_sleep()
    pag.click()
    timmy.sleep()

def double_click():
    pag.double_click()

