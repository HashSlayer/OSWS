import time
import pyautogui
import random as rnd
import math
from pynput.keyboard import Listener, KeyCode
from Utilities.Movement import *

# Create functions for tasks that the bots share in common.
# create a function that will push down the up key for 4 seconds, then release it.
#Define a function that welcome the player to the program "Old School Walk Scape."


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

#Let's simplify the time.sleep function slightly since we will be using it extensively..
def sleep(c = .01 , x = .008, z = 0.008): #C is a constant. X and Z are both multiplied by a number between 0-1.
    time.sleep(c + rnd.random() *x + rnd.random() *z) #Set variables so sleep() is viable for a .01 ~ .05 second sleep

#Define a function for random sleep variance from .1-.5 seconds ~
def sleepif(x=0.01):
    if (rnd.random() > 0.0503):
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
def click():
    sleep(.001)
    pag.mouseDown(button='left')  # Press the right button down
    sleepif()
    pag.mouseUp(button='left') # Lift right button up (Finish click)
    time.sleep(rnd.random() *0.001 + 0.001)

def quick_click(): #Another Left Click variant
    time.sleep(rnd.random() *0.0001 + 0.0003)
    pag.mouseDown(button='left')  # press the right button down
    pag.mouseUp(button='left')
    #Hold the mouse down for a period of time rather a simple click
    time.sleep(rnd.random() *0.0001 + 0.00003)

def right_click():
    sleep(.001)
    pag.mouseDown(button='right')  # Press the right button down
    sleepif()
    pag.mouseUp(button='right') # Lift right button up (Finish click)
    time.sleep(rnd.random() *0.001 + 0.001)


def upkey(): #Hold the up key to adjust the camera view
    pag.keyDown('up')
    sleep(2, 1, 1)
    pag.keyUp('up')
    sleep()

#Define downkey function

def downkey(): #Hold the down key to adjust camera view
    pag.keyDown('down')
    sleep(2,1,1)
    pag.keyUp('down')
    sleep()

#Define a function that will push down the left key for 3 seconds, then release it.

def leftkey(x = .70):
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


#Banking functions:
#Define a function that will move the mouse to a random spot between X= 990 and 1008, Y= 817 and 830, then click, including human like delays, and movements between clicks.
#This will deposit all items in the inventory.

def Deposit():
    time.sleep(0.1 + 0.03 * rnd.random() + rnd.random())
    bezierMove(rnd.randint(990, 1008), rnd.randint(817, 830), 0.3 + 0.1 * rnd.random() + 3/27 * rnd.random())
    #50/50 if statement to move to the same spot with closer X and Y values
    if (rnd.random() > 0.4):
        bezierMove(rnd.randint(994, 1007), rnd.randint(819, 827), 0.08 + 0.01 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.1 + 0.1 * rnd.random() + 0.1 * rnd.random())
    click()
    pag.moveRel(rnd.randint(-4, 3), rnd.randint(-2,2), 0.01 + 0.01 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.07 + 0.01 * rnd.random()) #sleep

#Define a function that drops down to get X amount of items.

def Getitems():
    time.sleep((rnd.random() * 0.01 + 0.05)) # Sleep
    pag.rightClick #open item options         
    time.sleep((0.12 + rnd.random() * 0.15)) #sleep
    if (rnd.random() > 0.619):
        pag.moveRel(rnd.randint(-21,11), rnd.randint(71,73), rnd.random() *0.12 +0.13) #move mouse down to quantity of X
    else:
        pag.moveRel(rnd.randint(-21, 1), rnd.randint(71, 73), rnd.random() * 0.121 + 0.13)
    time.sleep((rnd.random() * 0.087 + rnd.random() * 0.23 + 0.15)) #sleep
    click() # Get X amount of items
    time.sleep((0.01 + rnd.random() * 0.01)) #Short Sleep

     # Copy the Getitems() function with this line: pag.moveRel(rnd.randint(-30, 17), rnd.randint(101, 114), yrt * 0.12 + 0.23) #move mouse down to quantity of all


def Getall():
    time.sleep(rnd.random()* 0.173 + 0.21) #Sleep
    pag.rightClick  #open wood options now.
    time.sleep(0.181 * rnd.random() + 0.2) #sleep
    if (rnd.random() > 0.4):
        pag.moveRel(rnd.randint(-19, 12), rnd.randint(100, 112), rnd.random() * 0.121 + 0.25) #move mouse down to quantity of ALL
    else:
        pag.moveRel(rnd.randint(-19, 5), rnd.randint(103, 109), rnd.random() * 0.121 + 0.28)
    time.sleep(rnd.random() * 0.19 + 0.29)
    click() #Get wood
    time.sleep(rnd.random() * 0.19 + 0.29)

#To move down we increase the Y value; to move down one item slot in the bank, we increase the Y value by 35 or 38.
#Define a function that moves the mouse to an item in the bank

def Slot1():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    bezierMove(rnd.randint(977, 983), rnd.randint(140, 150), 0.2 + 0.2 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.13 + 0.01 * rnd.random() + 3/27 * rnd.random()) #sleep

#define slot 2 which is 35 pixels down from slot 1 currently wood

def Slot2():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    bezierMove(rnd.randint(977, 983), rnd.randint(175, 185), 0.23 + 0.2 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.13 + 0.01 * rnd.random() + 3/27 * rnd.random()) #sleep

#define slot 3 which is 35 pixels down from slot 2

def Slot3():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    bezierMove(rnd.randint(977, 983), rnd.randint(210, 220), 0.2 + 0.2 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.13 + 0.01 * rnd.random() + 3/27 * rnd.random()) #sleep

#define slot 4 which is 35 pixels down from slot 3

def Slot4():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    bezierMove(rnd.randint(977, 983), rnd.randint(245, 255), 0.2 + 0.2 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.13 + 0.01 * rnd.random() + 3/27 * rnd.random()) #sleep

#define slot 5 which is 35 pixels down from slot 4

def Slot5():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    bezierMove(rnd.randint(977, 983), rnd.randint(280, 290), 0.2 + 0.1 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.13 + 0.01 * rnd.random() + 3/27 * rnd.random()) #sleep

#define a function that moves the mouse to the left by 35 pixels in relation to the current position of the mouse.

def Left35():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    pag.moveRel(rnd.randint(-34, -36), rnd.randint(-2,2), 0.3 + 0.1 * rnd.random() + 3/27 * rnd.random())
    time.sleep(0.13 + 0.01 * rnd.random() + 3/27 * rnd.random()) #sleep

def Xbank():
    time.sleep(0.1 + 0.01 * rnd.random() + rnd.random()) #sleep
    bezierMove(rnd.randint(1040, 1044), rnd.randint(68, 70), rnd.random() * 0.1 + 0.24) # X of the bank
    time.sleep(0.01 + rnd.random() *0.198)
    click() #exit bank
    pag.moveRel(rnd.randint(-20, 12), rnd.randint(-6,12), rnd.random() * 0.1 + 0.04) # random movement

