import time
import sys
import threading
import pyautogui
import random as rnd
from pynput.keyboard import Listener, KeyCode
from Utilities.MainFunctions import *


global running
global dartsessions
ONOFF = KeyCode(char="`")
KEY = KeyCode(char ='8')

dartsessions = int (0)
supsup = False
running = False
maxDarts = int(input("Enter the maximum amount of darts availble: "))
maxClix = int (maxDarts / 10)

print ( "You are set to execute," + str(maxClix) , " clicks. Press 1 to start & stop the program; press 2 to exit completely.")
dartsMade = 0


def winemaker():
    while True:
        if running:
            global dartsessions
            global supsup
            global maxClix
            global dartsMade
            if dartsessions == 0:
               print ("Bronco nation, Let's RIDE!")
            
            if rnd.random() > 0.389:
                #favorable coordinates
                pag.moveTo(rnd.randint(1180,1185), rnd.randint(483, 488), rnd.random() * 0.0281 + 0.021) #move to feather
                if rnd.random() > 0.989:
                    #move relative by 3 pixels
                    pag.moveRel(rnd.randint(-3,3), rnd.randint(-3,3), rnd.random() * 0.01 + 0.001)
            else:
                pag.moveTo(rnd.randint(1175,1185), rnd.randint(480, 490), rnd.random() * 0.0281 + 0.021) #move to feather
                if rnd.random() > 0.989:
                    #move relative by 3 pixels
                    pag.moveRel(rnd.randint(-3,3), rnd.randint(-3,3), rnd.random() * 0.01 + 0.001)
            
            sleep(0.0001, 0.0001, 0.0002)
            click() #click feather
            sleep(0.0001, 0.0001, 0.0002)
            if rnd.random() > 0.989:
                sleep(0.1, 1, 2)

            if (dartsessions % rnd.randint(87,90) == 0):
                print (" We made", dartsessions * 10, "darts this round.")
                time.sleep(rnd.randint(1,3) * rnd.random())
                supsup = True
   
            if rnd.random() > 0.239:
                #favorable coordinates for right item (darts)
                pag.moveTo(rnd.randint(1220, 1233), rnd.randint(483, 488), rnd.random() * 0.028 + 0.02)
                if rnd.random() > 0.989:
                    #move relative by 3 pixels
                    pag.moveRel(rnd.randint(-3,3), rnd.randint(-3,3), rnd.random() * 0.01 + 0.001)
            else:
                pag.moveTo(rnd.randint(1228, 1233), rnd.randint(480, 489), rnd.random() * 0.028 + 0.02) #move to dart tip
                if rnd.random() > 0.989:
                    #move relative by 3 pixels
                    pag.moveRel(rnd.randint(-3,3), rnd.randint(-3,3), rnd.random() * 0.01 + 0.001)
            sleep(0.0001, 0.0001, 0.0002)
            click() #click dart tip

            if (dartsessions % rnd.randint(28,39) == 0):
                print (" It is session:", dartsessions, ".")
                time.sleep(rnd.random() * 2)
                supsup = True
            
            dartsessions = dartsessions + 1
            dartsMade = dartsessions * 10

            if (dartsessions >= maxClix):
                print("Max clix reached.")
                sys.exit("Max clicks reached")

        time.sleep(0.0003 * rnd.random() + 0.001)

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        exit() # This will end the program entirely
        sys.exit()

click_thread = threading.Thread(target=winemaker)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()

