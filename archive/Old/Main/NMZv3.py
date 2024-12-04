import time
import sys
import os
import threading
import random as rnd
from pynput.keyboard import Listener, KeyCode, Key
# Get the directory of the current script
current_script_dir = os.path.dirname(__file__)
# Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
from Utilities.MainFunctions import *
from Utilities.Movement import *
import tkinter as tk
from tkinter import font as tkFont
from datetime import datetime
from Utilities.Conffeti import *


# Scaling factors for the new resolution

# Adjusted global variables
global running, sips, pots, xPosition, yPosition, rangePotX, ItemGap, rows, sipped

ONOFF = Key.alt_l  # Left Alt key for toggling on/off
KEY = Key.alt_r  # Right Alt key to exit the program

running_lock = threading.Lock()
bot_thread = None

running = False
sipped = True
sips = 0
pots = 0
rows = 1
xPosition = int(1645)
yPosition = int(1743)
rangePotX = xPosition
ItemGap = int(55)


welcome()
print("Get ready to Rumble!")

def SipCounter():
    global sips, pots, xPosition, rangePotX, ItemGap
    sips = sips
    if (sips >= 4):
        print("Drank 4 sips, moving to next potion next time.")
        xPosition = xPosition + ItemGap
        sleep(.01, .1, .1)
        bezierMove(rnd.randint((rangePotX - 5), (rangePotX + 5)), rnd.randint(yPosition + ItemGap * 6) - 5, rnd.randint(yPosition + ItemGap * 6) + 5, rnd.random() * 0.293 + 0.207)
        sleep(.08, .09, .03)
        print ("Drinking potion at coordinates:", rangePotX, "and 975")
        click()
        sleep(.01, .06, .03)
        pots += 1 
        sips = 0

def PotCounter():
    global pots, rows, xPosition, yPosition, rangePotX
    pots = pots
    if (pots >= 4):
        print("Drank 4 potions, moving to next range potion.")
        yPosition += ItemGap
        xPosition -= ItemGap * 4
        rangePotX += ItemGap
        sleep(.05, .1)
        pots = 0
        rows += 1
        print ("Rows:", rows)
        if (rows >= 7):
            print("Sleeping for ever hours")
            sys.exit()


def NMZ():
    while True:
        if running:
            global sips, xPosition, yPosition, pots, rangePotX, rows, sipped

            sleep(10, 3)
            if rnd.random() > 0.889:
                Notbotting()
                Notbotting()
            sleep(10, 3)
            if rnd.random() > 0.289:
                    Notbotting()
                    if rnd.random() > 0.889:
                        Notbotting2()
            print("Starting loop!")

            if ((rnd.random() > 0.79388)):
                print ("(single sip)", "sip:", sips, "at coordinates:", xPosition, "and", yPosition, "sipped is:", sipped)
                bezierMove((rnd.randint((xPosition - 6), (xPosition + 6))), (rnd.randint((yPosition - 4), (yPosition + 4))), rnd.random() * 0.293 + 0.207)
                time.sleep(rnd.random() * 0.36 + 0.1098)
                click()
                sips += 1
                print ("sips is now:", sips)
                time.sleep(rnd.random() * 0.06 + 0.198)
                SipCounter()
                PotCounter()
            else:
                print("No single sip this lap. Time for one more.")
                sleep(10, 3)
                if rnd.random() > 0.889:
                    Notbotting()
                    if rnd.random() > 0.889:
                        Notbotting2()
                sleep(10, 3)
                if rnd.random() > 0.289:
                    Notbotting()
                    if rnd.random() > 0.889:
                        Notbotting2()
                print("Starting loop!")
                print("Done with this lap.")
                sleep(.1, .5)
                bezierMove((rnd.randint((xPosition - 6), (xPosition + 6))), (rnd.randint((yPosition - 4), (yPosition + 4))), rnd.random() * 0.293 + 0.207)
                sleep(.1, .25)
                print ("Drinking 2 sips!")
                click()
                sips += 1
                print ("sips:", sips)
                sleep(1.6, .4)
                SipCounter()
                PotCounter()
                bezierMove((rnd.randint((xPosition - 6), (xPosition + 6))), (rnd.randint((yPosition - 4), (yPosition + 4))), rnd.random() * 0.293 + 0.207)
                sleep(1.3, .5)
                click()
                sips += 1
                print ("sips:", sips)
                sipped = True
            SipCounter()    
            PotCounter()
            if (rows >= 7):
                print("Sleeping for ever hours, FAIL SAFE ACTIVATED.")
                sys.exit()
            print (" Time for another loop!")
        #Not Running
    #Not True
#End of NMZ()

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch activated")
        running = False
        sys.exit()

click_thread = threading.Thread(target=NMZ)
click_thread.start()

with Listener(on_press=togglebot) as listener:
    listener.join()
