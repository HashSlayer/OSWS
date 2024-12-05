import time
import pyautogui as pag
import random as rnd
from .Movement import *

def welcome():
    print ("Welcome to Old School Walk Scape")
    print ("Loading...")
    time.sleep(0.1 * rnd.random() + 0.03)
    print ("[-------------]")
    time.sleep(0.2 * rnd.random() + 0.05)
    print ("[\------------]")
    time.sleep(0.2 * rnd.random() + 0.04)
    print ("[\\\-----------]")
    time.sleep(0.3 * rnd.random() + 0.03)
    print ("[\\\\\\\---------]")
    time.sleep(0.3 * rnd.random() + 0.06)
    print ("[\\\\\\\\\--------]")
    time.sleep(0.3 * rnd.random() + 0.075)
    print ("[\\\\\\\\\\\\\------]")
    time.sleep(0.2 * rnd.random() + 0.03)
    print ("[\\\\\\\\\\\\\\\\\----]")
    time.sleep(0.3 * rnd.random() + 0.03)
    print ("[\\\\\\\\\\\\\\\\\\\\\--]")
    time.sleep(0.6 * rnd.random() + 0.05)
    print ("[\\\\\\\\\\\\\\\\\\\\\\\\\]")
    time.sleep(0.1 * rnd.random() + 0.05)
    print ("[|||||||||||||]")
    time.sleep(0.1 * rnd.random() + 0.1)
    print ("Press the 1 Key to start the program; 2 to kill the program.")
    print ("Walking initiated at time:", time.strftime("%H:%M:%S", time.localtime()), "24 Hour time") 
    print ("Enjoy your walk!")

def sleep(c = .01 , x = .008, z = 0.008): #C is a constant. X and Z are both multiplied by a number between 0-1.
    time.sleep(c + rnd.random() *x + rnd.random() *z) #Set variables so sleep() is viable for a .01 ~ .05 second sleep

#Define a function for random sleep variance from .1-.5 seconds ~
def sleepif(x=0.01):
    if (rnd.random() > 0.0583):
        time.sleep(rnd.random() *0.001 + 0.001)
        if (rnd.random() > 0.0504):
            time.sleep(rnd.random() *0.001 + 0.001)
        if (rnd.random() > 0.008284):
            time.sleep(rnd.random() *0.001 + 0.001)
            if (rnd.random() > 0.09420):
                time.sleep(rnd.random() * x + 0.005)
            if (rnd.random() > 0.263):
                time.sleep(rnd.random() * x + 0.01)
            if (rnd.random() > 0.381251):
                time.sleep(rnd.random() * (x * 2) + 0.01)
            if (rnd.random() > 0.591251):  
                time.sleep(rnd.random() * (x * 2) + 0.01)
            if (rnd.random() > 0.793):
                time.sleep(rnd.random() * (x * 3) + 0.02)
            if (rnd.random() > 0.891251):
                time.sleep(rnd.random() * (x * 4) + 0.02)
            if (rnd.random() > 0.9180251):  
                time.sleep(rnd.random() * (x * 28) + 0.02)
            if (rnd.random() > 0.981251):  
                time.sleep(rnd.random() * (x * 9) + 0.04)
                if (rnd.random() > 0.89):
                    time.sleep(rnd.random() *0.09 + 0.04) 
                    if (rnd.random() > 0.871251):
                        time.sleep(rnd.random() *0.05 + 0.05)
                        print(" Long click!")
    if (rnd.random() > 0.991251):  
        time.sleep(rnd.random() *0.003 + 0.001)

#Define a more human like click.
def click(hold = 0):
    sleep(.001)
    pag.mouseDown(button='left')  # Press the right button down
    sleepif()
    time.sleep(hold)
    pag.mouseUp(button='left') # Lift right button up (Finish click)
    time.sleep(rnd.random() *0.003 + 0.003)

def quick_click(): #Another Left Click variant
    time.sleep(rnd.random() *0.0001 + 0.0003)
    pag.mouseDown(button='left')  # press the right button down
    pag.mouseUp(button='left')
    #Hold the mouse down for a period of time rather a simple click
    time.sleep(rnd.random() *0.0001 + 0.00003)

def right_click(hold =0):
    sleep(.001)
    pag.mouseDown(button='right')  # Press the right button down
    sleepif()
    time.sleep(hold)
    pag.mouseUp(button='right') # Lift right button up (Finish click)
    time.sleep(rnd.random() *0.001 + 0.001)


def upkey(hold = 2): #Hold the up key to adjust the camera view
    pag.keyDown('up')
    sleep(hold, .01, .001)
    pag.keyUp('up')
    sleep()

#Define downkey function

def downkey(hold =2): #Hold the down key to adjust camera view
    pag.keyDown('down')
    sleep(hold, .01, .001)
    pag.keyUp('down')
    sleep()

#Define a function that will push down the left key for 3 seconds, then release it.

def leftkey(x = 1):
    pag.keyDown('left')
    sleep(x, .001, .001)
    pag.keyUp('left')
    sleep()

#Define a function that will click on the map

def Compass():
    time.sleep(0.003 * rnd.random() + 0.1)
    bezierMove(rnd.randint(1716, 1729), rnd.randint(38, 48), rnd.random() * 0.181 + 0.81) #move to map
    time.sleep(0.003 * rnd.random() + 0.6)
    click()
    time.sleep(0.01 * rnd.random() + 0.1)


#Define a function that scrolls the mouse wheel down by 20 clicks, spaced out like a human would.

def Zoomout():
    for i in range (1, 12):
        pag.scroll(-1)
        time.sleep(0.13 * rnd.random() + 0.19)

#Define a function that scrolls the mouse wheel up by 20 clicks, spaced out like a human would.

def Zoomin():
    for i in range (1, 12):
        pag.scroll(1)
        time.sleep(0.13 * rnd.random() + 0.19)

# Get into birds eye view
def Birdseye():
    Compass()
    Zoomout()
    time.sleep(0.0003 * rnd.random() + 0.01)
    upkey()
    time.sleep(0.0003 * rnd.random() + 0.01)

def Flatview():
    Compass()
    Zoomin()
    time.sleep(0.0003 * rnd.random() + 0.01)
    downkey()
    time.sleep(0.0003 * rnd.random() + 0.01)

def inv_slot(slot = 1, time_multiplier = 1, sleep_for = .01, sleep_upto = .01, x = 1645, y=660, z=10): #Can +/- 20 pixels and be fine
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


#A function that iterates click through items in the inventory, clicking on the first spot at bezierMove(rnd.randint(1690,1710), rnd.randint(760, 774), rnd.random() * 0.03 + 0.197)
#and moving to the next spot at bezierMove(rnd.randint(xpus - 3, xpus + 3), rnd.randint(ypus - 3, ypus + 3), rnd.random() * 0.03 + 0.399) # move to log
#We will have to define x any y as their values and adjust them in the function. This function will be called in other functions.

def Burn(xpus=1700, ypus=766):
     xpus = 1700
     ypus = 766
     sips = 0
     pot = 0
     for i in range (1, 21):
        bezierMove(rnd.randint(xpus - 4, xpus + 3), rnd.randint(ypus - 4, ypus + 4), rnd.random() * 0.03 + 0.399) # move to top position in inventory
        time.sleep(rnd.random() * 0.01 + 0.488)
        click() # burn log 1
        if (sips % 4 == 0):
             xpus = xpus + 40 # Adjust X Position; moves mouse to right by one item in inventory
             pot += 1
        sips = sips + 1 #Add to burn count
                
        if ((sips + 1) % 4 == 0 or sips == 3):
            ypus = ypus + 35 # drop the mouse down one row of items for the next iteration
            xpus = xpus - 160 # pull mouse back to the first coulum for the next iteration
            time.sleep( 0.009 + rnd.random() *0.05)

def drop_inventory(drop_x = 24):
        drop_x_items = drop_x + 1
        if rnd.random() > 0.5:
            bezierMoveRelative(rnd.randint(-10, 10), rnd.randint(-10, 10), rnd.random() * 0.03 + 0.199) # random movement
        for i in range (1, drop_x_items):
            sleep(.1, .1, .01) #sleep
            pag.keyDown('shift')
            inv_slot(i)
            time.sleep(rnd.random() * 0.01 + 0.0078)
            click() # drop ore
            if (rnd.random() > 0.97):
                click()
                print ("Nice double click!")
        pag.keyUp('shift')

#Define a function that presses down the 1 key for a short random amount of time, then releases it.
def k1(): #Inventory
    pag.keyDown('1')
    sleepif(x=0.0102)
    pag.keyUp('1')
    time.sleep(0.1 * rnd.random() + 0.01)

#Define functions for the rest of the number keys
def k2(): #Prayer
    pag.keyDown('2')
    sleepif(x=0.0104)
    pag.keyUp('2')
    time.sleep(0.1 * rnd.random() + 0.01)

def k3(): #Combat Styles
    pag.keyDown('3')
    sleepif(x=0.0123)
    pag.keyUp('3')
    time.sleep(0.1 * rnd.random() + 0.01)

def k4(): #Spellbook
    pag.keyDown('4')
    sleepif(x=.0107)
    pag.keyUp('4')
    time.sleep(0.1 * rnd.random() + 0.01)

def k5(): #Equipment
    pag.keyDown('5')
    sleepif(x=.0111)
    pag.keyUp('5')
    time.sleep(0.1 * rnd.random() + 0.01)

def k6(): #Emotes
    pag.keyDown('6')
    sleepif(x=.0112)
    pag.keyUp('6')
    time.sleep(0.1 * rnd.random() + 0.01)

def k7(): #Clan Chat
    pag.keyDown('7')
    sleepif(x=.011)
    pag.keyUp('7')
    time.sleep(0.1 * rnd.random() + 0.01)

def k8(): #Friends List
    pag.keyDown('8')
    sleepif(x=.011)
    pag.keyUp('8')
    time.sleep(0.1 * rnd.random() + 0.01)

def k9(): #Quests
    pag.keyDown('9')
    sleepif(x=.011)
    pag.keyUp('9')
    time.sleep(0.1 * rnd.random() + 0.01)

def kminus(): #Quick Hop down a world
    pag.keyDown('-')
    sleepif()
    pag.keyUp('-')
    time.sleep(0.1 * rnd.random() + 0.01)

def kplus(): #Quick Hop up a world
    pag.keyDown('+')
    sleepif()
    pag.keyUp('+')
    time.sleep(0.1 * rnd.random() + 0.01)

def kspace(constant=.01, x=.01): #Spacebar
    pag.keyDown('space')
    sleep(constant, x, 0.01) #Control the duration of the spacebar press
    sleepif(x=0.0113)
    pag.keyUp('space')
    time.sleep(0.1 * rnd.random() + 0.01)

def kRandom(LastK = "k1"): #Press a random number key
    sleep(.1, 0.1, 0.01)
    LastK = rnd.choice([k3, k4, k5, k6, k7, k8, k9])
    LastK()
    sleep(.1, 0.1, 0.01)
    return LastK

def kAltleft(): #Press the left alt key
    pag.keyDown('altleft')
    sleepif()
    pag.keyUp('altleft')
    time.sleep(0.1 * rnd.random() + 0.01)

def kAltright(): #Press the right alt key
    pag.keyDown('altright')
    sleepif()
    pag.keyUp('altright')
    time.sleep(0.1 * rnd.random() + 0.01)