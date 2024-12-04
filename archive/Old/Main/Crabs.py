import time
import threading
import pyautogui
import sys
import random as rnd
from pynput.keyboard import Listener, KeyCode
#Import the MainFunctions file which is one directory up.
from Utilities.MainFunctions import *
from Main.CrabbyFunctions import *

global running
global rounds
global roundset

ONOFF = KeyCode(char="1")
KEY = KeyCode(char ='2')

rounds = int (1)
running = False
#create a varirable asking the user for input on what round it is
print (" ~ Welcome to the Crabby Killer! ~ ")
roundset = int(input("What round can we start on? "))
if roundset == 0:
    roundset = 1
maxRounds = int(input("What round do you want to stop at? "))    
welcome()

def crabKiller():
    while True:
        if running:
            global rounds
            global roundset
            
            print ("Let's light em Up! It is round:", rounds)
            time.sleep(rnd.random() *0.1 + 0.8)
            
            if (rounds == 0):
                Compass()
                pag.moveRel(rnd.randint(-400, -200), rnd.randint(100, 300), rnd.random() * 0.181 + 0.41)
                upkey()
                Zoomout()
                print("Lessss gooo!")
                
            #Reset auto combat by calling jog() and running away and back every 7 rounds
            if (rounds % roundset == 0):
                print ("Let's move!")
                time.sleep(rnd.random() *0.7 + 1.8)
                if rnd.random() > 0.8:
                    print ("Jogger v1 activated")
                    jog2()
                else:
                     #Location 1
                    print ("Jogger v2 activated")
                    pag.moveTo(rnd.randint(816, 828), rnd.randint(391, 403), rnd.random() * 0.1 + 0.41)
                    click()
                    time.sleep(rnd.random() * 0.5 + 1.9)
                    pag.moveRel(rnd.randint(-100, -10), rnd.randint(-30, 30), rnd.random() * 0.081 + 0.1)
                    jog3()
                roundset = roundset + 6

            #if statement; every 
            if (rnd.random() > 0.73):
                print ("Cycleslow activated")
                cycleslow()
            else:
                print ("Cycleslow v2 activated")
                cycleslow2()

            rounds = rounds + 1

            if (rounds == maxRounds):
                time.sleep(rnd.random() *0.1 + 1980) # 30 minute sleep

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        sys.exit() # This will end the program entirely

click_thread = threading.Thread(target=crabKiller)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()