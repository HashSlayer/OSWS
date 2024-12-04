import pyautogui as pag
import time
import random as rnd
from .Movement import bezierMove, bezier_between, bezier_relative
from .MainFunctions import click, sleep, right_click

#Bank at the Grand Exchange with bank near inventory
def bank_near_inv(x1=1377, x2=1560, y1=600, y2=777, time= rnd.randint(23, 48)/100, wait=.3):
    bezier_between(x1, x2, y1, y2, time) 
    sleep(.1, wait, .05) #sleep
    click() #open up the bank.
    sleep()

# Exit the bank
def exit_bank(x1=1066, x2=1084, y1=83, y2=100, time= rnd.randint(30, 52)/100, pause_upto=.2):
    if (rnd.random() > 0.6):
        bezier_between(x1, x2, y1, y2, time)
    else:
        bezier_between(x1+3, x2-5, y1+5, y2-2, time) #Disrupt entirely random location
    sleep(.05, pause_upto, .02) #Pause before exiting bank
    click() #exit bank
    sleep()

#Deposit all items in inventory
def deposit_all(x=1020, y=770, size=9, time = rnd.randint(30, 45)/100, pause_upto=.5):
    if (rnd.random() > 0.7):
        bezier_between(x-size, x+size, y-size, y+size, time)
    else:
        bezier_between(x-7,x+8, y-6, y+10, time)
    sleep(.1, pause_upto, .02) #sleep
    click()
    if rnd.random() > 0.8:
        click()


#Set as Withdraw item as note    
def withdraw_as_note(x1 = 685, x2=705, y1 = 775, y2=780, time = rnd.randint(40, 55)/100, pause_upto = .2):
    if (rnd.random() > 0.8):
        bezier_between(x1, x2, y1, y2, time)
    sleep(.1, pause_upto, .02) #sleep
    click()


#RELATIVE MOVEMENT
def get_x_items(x1 = -30, x2 = 20, y1 = 93, y2 = 97, time= rnd.random() * 0.1 + rnd.randint(13, 29)/100, pause_upto=.2):
    sleep(.03, .09) #sleep
    right_click() #right click
    if (rnd.random() > 0.69420): # REFINED WAY TO LOCALIZE LOCATIONS
        bezier_relative(x1-15, x2+10, y1, y2, time) #move mouse down to quantity of X
    else:
        bezier_relative(x1, x2, y1+1, y2-1, time) #move mouse down to quantity of X
    sleep(.05, pause_upto, .02) #sleep
    click() # Get X amount of items


     # Copy the get_x_items() function with this line: pag.moveRel(rnd.randint(-30, 17), rnd.randint(101, 114), yrt * 0.12 + 0.23) #move mouse down to quantity of all


def get_all_items(x1 = -30, x2 = 20, y1 = 132, y2 = 136, time= rnd.random() * 0.15 + 0.2, pause_upto=.2):
    sleep(.03, .09) #sleep
    right_click() #right click
    if (rnd.random() > 0.69420): # REFINED WAY TO LOCALIZE LOCATIONS
        bezier_relative(x1-15, x2+10, y1, y2+5, time) #move mouse down to quantity of X add y2+5 to toggle for all but 1 on occasion
    else:
        bezier_relative(x1, x2, y1+1, y2-1, time) #move mouse down to quantity of X
    sleep(.05, pause_upto, .02) #sleep
    click() # Get X amount of items


#To move down we increase the Y value; to move down one item slot in the bank, we increase the Y value by 35 or 38.
#Define a function that moves the mouse to an item in the bank
    
def bank_slot(slot = 1, time_multiplier = 1, sleep_for = .01, sleep_upto = .01, x = 555, y=190, z=10): #Can +/- 20 pixels and be fine
    # Add 32 to X for each slot, add 35 to Y, -32 * 8 to x for every 8 slots
    # 8 slots per row, 5 rows
    slot -= 1
    row = slot // 8
    column = slot % 8
    x = x + (64 * column)
    y = y + (46 * row)
    print("Slot:", slot, " Row:", row, " Column:", column, " X:", x, " Y:", y)
    bezierMove(rnd.randint(x-z, x+z), rnd.randint(y-z, y+z), time_multiplier)
    sleep(sleep_for, sleep_upto, .003) #sleep

def inv_slot(slot = 1, time_multiplier = 1, sleep_for = .01, sleep_upto = .01, x = 1645, y=660, z=12): #Can +/- 20 pixels and be fine
    slot -= 1
    row = slot // 4
    column = slot % 4
    x = x + (55 * column)
    y = y + (46 * row)
    if slot == 1:
        time_multiplier = 1.2
    if slot < 29:
        print("Slot:", slot, " Row:", row, " Column:", column, " X:", x, " Y:", y)
        bezierMove(rnd.randint(x-z, x+z), rnd.randint(y-z, y+z), time_multiplier)
        sleep(sleep_for, sleep_upto, sleep_upto/10) #sleep
    else:
        sleep(.1,.9,.9)

