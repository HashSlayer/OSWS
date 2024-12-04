import time
import threading
import pyautogui
import random as rnd
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
from Utilities.MainFunctions import *

global running
global bowcount
global lag

ONOFF = KeyCode(char="`")
KEY = KeyCode(char ='8')

bowcount = int (0)
running = False
lag = (0.33 + rnd.random() + 3/27 * rnd.random())


def winemaker():
    while True:
        if running:
            print ("Bow makin time baby!")
            global lag
            global bowcount
            ## ~~~ Random mouse movement ~~~~ ####
            pag.moveTo(rnd.randint(700,980), rnd.randint(100,480), lag * 0.9 + 0.18)
            pag.moveRel(rnd.randint(-40, 74), rnd.randint(-21,20), lag * 0.8 + 0.2)
            time.sleep(lag * 0.02 + 1)
            lag = (0.32 + rnd.random() + 2/27 * rnd.random())
            pag.moveRel(rnd.randint(-40, 74), rnd.randint(2,60), lag * 1.2 + 1) # random movement
            time.sleep(lag * 0.02 + 0.05)
            lag = (0.43 + rnd.random() + 2/27 * rnd.random())
            ## ~~~ Random mouse movement ~~~~ ####
            # Begin opening bank: 
            pag.moveTo(rnd.randint(880,900), rnd.randint(220,280), lag) # move mouse to banker.
            lag = (0.33 + rnd.random() + 2/27 * rnd.random()) # change lag speed
            time.sleep(lag * 0.2 + 0.3) # wait before next action, use .1 multiplier because we aren't moving mouse position. 
            mouse.click() #open up the bank.
            time.sleep(0.02 + 0.23 * rnd.random()) # sleep.

            pag.moveTo(rnd.randint(1005,1030) ,rnd.randint(819, 834), lag *0.53 + 0.42) # Move to deposit inventory tab 
            time.sleep(rnd.random() * 13/272 + 0.1) #sleep
            mouse.click() # Deposit all inventory
            pag.moveRel(rnd.randint(-40, 74), rnd.randint(-2,60), lag * 0.123 + 0.02) # random movement
            time.sleep(rnd.random() * 13/100) #sleep

            pag.moveTo(rnd.randint(940,950), rnd.randint(166, 172), lag * 0.2 + 0.16) #move to KNIFE <---- 
            time.sleep((rnd.random() * 0.1 + rnd.random() * 13/120 + 0.05)) # Sleep
            mouse.click() # Get knife
            time.sleep(0.02 + 0.13 * rnd.random()) # sleep.
            pag.moveRel(rnd.randint(-12, 12), rnd.randint(-6,12), lag * 0.15 + 0.1) # random movement
            time.sleep(lag*0.15 + 0.08) #sleep
            print ("Getting wood.")
            pag.moveTo(rnd.randint(986, 1004), rnd.randint(166, 172), lag * 0.133 + 0.06) # move to wood
            lag = (0.02 + rnd.random() + 33/277 * rnd.random()) # YRT  change
            time.sleep(lag* 0.0173 + 0.11) #Sleep
            mouse.right_click() #open water jug options now. Last item needed
            time.sleep(0.18 * rnd.random() +0.2) #sleep
            pag.moveRel(rnd.randint(-12, 5), rnd.randint(100, 107), lag * 0.12 + 0.12) #move mouse down to quantity of 14
            time.sleep(rnd.random() * 0.19 + 0.29)
            mouse.click() #Get water
            print (" Let's Make Some Bows!")
            #
            # WINE PROCESS BEGIN !
            ## ~~~ Random mouse movement ~~~~ ####
            pag.moveRel(rnd.randint(-20,40), rnd.randint(-10,6), lag * 0.12 + 0.03) #Move around from current spot
            time.sleep(lag * 0.03 + 0.006) #Sleep
            lag = (0.33 + rnd.random() + 2/27 * rnd.random()) # Reset YRT
            ## ~~~ Random mouse movement ~~~~ ####
            pag.moveTo(rnd.randint(1058, 1065), rnd.randint(64, 68), lag * 0.13 + 0.04) # X of the bank
            time.sleep(0.01 + rnd.random() *0.098)
            mouse.click() #exit bank
            pag.moveRel(rnd.randint(-20, 12), rnd.randint(-6,12), lag * 0.3 + 0.031) # random movement
            time.sleep(rnd.random() * 0.0987 + 0.02) #sleep short
            print("Position of bank exit click:", pag.position())
            ## ~~~ Random mouse movement ~~~~ ####
            pag.moveRel(rnd.randint(-20,40), rnd.randint(100,200), lag * 0.13 + 0.05) #Move around from current spot
            pag.moveRel(rnd.randint(-2, 12), rnd.randint(6,12), lag * 0.13 + 0.05) # random movement
            time.sleep(lag * 0.13 + 0.01) #Sleep
            lag = (1.5* rnd.random() + 2/27 * rnd.random()) # Reset YRT
            ## ~~~ Random mouse movement ~~~~ ####

            pag.moveTo(rnd.randint(1709,1720), rnd.randint(752, 768), lag * 0.5 + 0.15) #use jug of water
            time.sleep(rnd.random() *0.5 + 0.07)
            mouse.click()
            pag.moveTo(rnd.randint(1747, 1767), rnd.randint(754, 769), lag * 0.23 + 0.15) #use on grapes
            time.sleep(rnd.random() * 0.14 + 0.85)
            mouse.click()

            pag.moveTo(rnd.randint(220, 240), rnd.randint(935, 985), lag * 0.5 + 1.26) #make bow!
            time.sleep(rnd.random() *0.1 + 0.013)
            mouse.click()
            bowcount = bowcount + 1

            print ("This is batch number:", bowcount)
            pag.moveTo(rnd.randint(860,940), rnd.randint(190,400), lag * 0.4 + 0.23) # move mouse to banker.

            #End of wine run; time to sleep and repeat     
        time.sleep(rnd.randint (39,42) + rnd.random() + lag * rnd.random() )

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