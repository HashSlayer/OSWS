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


global running
ONOFF = KeyCode(char="1")
KEY = KeyCode(char ='2')
running = False
dug = 0
zed = 0
welcome()

#Define a function that calls for a time.sleep if a random number is greater than 0.5

def Timebot():  
    if (rnd.random() > 0.947):
        time.sleep(rnd.random() * 0.4 + 0.03)
        if (rnd.random() > 0.917):
            Notbotting()

def tubeclick():
    while True:
        if running:
            print("Get ready to crawl!")
            global dug
            global zed

            bezierMove(rnd.randint(864,930), rnd.randint(395, 490), rnd.random() * 0.281 + 0.88913) #move to top iron ore, follow by a random chance to move within closer bounds
            if (rnd.random() > 0.388):
                    bezierMove(rnd.randint(892,920), rnd.randint(449, 490), rnd.random() * 0.081 + 0.118913)
            sleep(.1,.1,.2)
            if rnd.random() > 0.5:
                sleep(.1,.1,.2)
            click()
            if (rnd.random() > 0.976):
                click()
                print ("Nice double click!") #click
            time.sleep(rnd.random() *0.28 + 0.761)
            sleep(.4,.3,.2)
            dug += 1
            if dug == 27:
                if rnd.random() > 0.412:
                    drop_inventory(rnd.randint(23, 24))
                else:
                    drop_inventory(25)
                dug = 0


            #Ore 2 (Bottom ore)
            bezierMove(rnd.randint(909,966), rnd.randint(807,880), rnd.random() * 0.2832 + 0.881) #move to bottom ore, follow by a random chance to move within closer bounds
            if (rnd.random() > 0.381):
                bezierMove(rnd.randint(925,970), rnd.randint(807, 850), rnd.random() * 0.081 + 0.118913)
            time.sleep(rnd.random() *0.581 + 0.783)
            if rnd.random() > 0.5:
                sleep(.1,.1,.2)
            click()
            if (rnd.random() > 0.93):
                click()
                print ("Nice double click!") #click
            Timebot()
            time.sleep(rnd.random() *0.26 + 0.711)
            dug += 1
            if dug == 27:
                if rnd.random() > 0.112:
                    drop_inventory(24)
                else:
                    drop_inventory(25)
                dug = 0


            bezierMove(rnd.randint(699, 830), rnd.randint(670, 760), rnd.random() * 0.281 + 0.889111) 
            if (rnd.random() > 0.381):
                bezierMove(rnd.randint(700, 820), rnd.randint(675, 720), rnd.random() * 0.081 + 0.1118913)
            time.sleep(rnd.random() *0.71 + 0.713)
            click()
            if rnd.random() > 0.5:
                sleep(.1,.1,.2)
            if (rnd.random() > 0.939):
                click()
                print ("Nice double click!") #click
            time.sleep(rnd.random() *0.71 + 0.731)
            Timebot()
            dug += 1

            if dug == 27:
                if rnd.random() > 0.112:
                    drop_inventory(24)
                else:
                    drop_inventory(25)
                dug = 0

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        pag.keyUp('shift')
        SystemExit()
        sys.exit()

click_thread = threading.Thread(target=tubeclick)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()

