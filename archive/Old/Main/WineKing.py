import time
import threading
import pyautogui as pag
import sys
import random as rnd
from pynput.keyboard import Listener, KeyCode
from Utilities.MainFunctions import *
from Banking import * 

global running
global winecount
global winecount2

ONOFF = KeyCode(char="1")
KEY = KeyCode(char ='2')

winecount = int (0)
winecount2 = int (0)
running = False



def winemaker():
    while True:
        if running:
            print ("Wine makin time baby!")
            global winecount
            global winecount2

            if (winecount == 0):
                print ("First time running, let's get some grapes!")
                time.sleep(rnd.random()**2 + 0.1)
            ## ~~~ Random mouse movement ~~~~ ####
            Notbotting()

            #Begin opening bank: 
            pag.moveTo(rnd.randint(880,900), rnd.randint(220,280), rnd.random()) # move mouse to banker.
            time.sleep(rnd.random() * 0.1 + 0.01) # wait before next action, use .1 multiplier because we aren't moving mouse position. 
            click() #open up the bank.
            time.sleep(0.04 + 0.13 * rnd.random()) # sleep.

            pag.moveTo(rnd.randint(1005,1030) ,rnd.randint(820, 831), rnd.random() *0.23 + 0.42) # Move to deposit inventory tab 
            time.sleep(rnd.random() * 13/27 + 0.33) #sleep
            click() # Deposit all inventory
            time.sleep(rnd.random() * 13/272 + 0.12) #sleep
            print("Position of inv depo click:", pag.position())
            pag.moveRel(rnd.randint(-14, 7), rnd.randint(-11,12), rnd.random() * 0.123 + 0.1) # random movement
            time.sleep(rnd.random() * 0.007) #sleep
            pag.moveTo(rnd.randint(940,950), rnd.randint(132, 149), rnd.random() * 0.2 + 0.23) #move to the grapes 
            time.sleep((rnd.random() * 13/120 + 0.05)) # Sleep
            Getitems()
            pag.moveRel(rnd.randint(-12, 12), rnd.randint(-6, 2), rnd.random() * 0.08 + 0.0051) # random movement
            time.sleep(rnd.random()*0.15 + 0.08) #sleep
            print ("Getting water")
            pag.moveTo(rnd.randint(986, 1004), rnd.randint(134, 149), rnd.random() * 0.133 + 0.12) # move to water jug
            time.sleep(rnd.random()* 0.0173 + 0.01) #Sleep
            Getall()
            time.sleep( 0.03 + rnd.random() * 0.083 )
            print (" Let's Make Some Wine!")
            #
            # WINE PROCESS BEGIN !
            Notbotting3()
            Xbank()
            pag.moveRel(rnd.randint(-20, 12), rnd.randint(-6,12), rnd.random() * 0.1 + 0.071) # random movement
            #time.sleep(rnd.random() * 0.0987 + 0.02) #sleep short

            pag.moveTo(rnd.randint(1758,1762), rnd.randint(865, 872), rnd.random() * 0.21 + 0.25) #use jug of water
            time.sleep(rnd.random() *0.15 + 0.07)
            click()
            pag.moveTo(rnd.randint(1795, 1800), rnd.randint(865, 872), rnd.random() * 0.23 + 0.05) #use on grapes
            time.sleep(rnd.random() * 0.14 + 0.05)
            click()
            time.sleep(rnd.random() * 0.1 + 0.03)
            pag.keyDown('space')
            time.sleep(rnd.random() * 0.1 + 0.13)
            pag.keyUp('space')
            time.sleep(rnd.random() * 0.011 + 0.01)

            pag.moveTo(rnd.randint(269, 280), rnd.randint(955, 965), rnd.random() * 0.3 + 0.43) #make wine!
            time.sleep(rnd.random() *0.1 + 0.183)
            click()
            time.sleep(rnd.random() *0.1 + 0.313)
            pag.moveTo(rnd.randint(300, 877), rnd.randint(305, 788), rnd.random() * 0.38 + 2.0051) # random movement
            time.sleep(rnd.random() *0.1 + 0.013)
            pag.moveRel(rnd.randint(-9, 8), rnd.randint(-8, 8), rnd.random() * 0.38 + 2.0051) # random movement
            winecount = winecount + 1
            winecount2 = winecount2 + 1
            print ("Smells great! This is batch number:", winecount)
            pag.moveTo(rnd.randint(860,940), rnd.randint(190,400), rnd.random() * 0.4 + 0.23) # move mouse to banker.
            if (winecount2 % 76 == 0):
                time.sleep(rnd.randint(30, 100))
                winecount2 == 0
                print ("Break time!")
                print (" We made", winecount, "batches this round.")

            if (winecount2 % 433 == 0):
                time.sleep(rnd.randint(50, 300))
                winecount2 == 0
                print ("Break time!676767")
                print (" We made", winecount, "batches this round.")
            #End of wine run; time to sleep and repeat     
        time.sleep(5.8 + rnd.random() * 0.8) # double this time while making fert.. normally it is 10.8 + x, but for fert is 22

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        sys.exit() # This will end the program entirely

click_thread = threading.Thread(target=winemaker)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()