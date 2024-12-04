import time
import sys
import threading
import pyautogui
import random as rnd
from pynput.keyboard import Listener, KeyCode
from Utilities.MainFunctions import *


global running

ONOFF = KeyCode(char="`")
KEY = KeyCode(char ='8')

running = False
global xpus
global ypus
global burnt
fruits = 0

def winemaker():
    while True:
        if running:
            global fruits
            global xpus
            global ypus
            global burnt

            time.sleep(rnd.random() *0.1 + 3.11)
            mouse.click() #click featheR 
            time.sleep(rnd.random() *0.1 + 0.11)
            fruits = fruits + 1

            xpus = 1715
            ypus = 765
            burnt = 0

            if (fruits > 28):
                for i in range (1, 29):
                    pag.keyDown('shift')
                    pag.moveTo(rnd.randint(xpus - 3, xpus + 3), rnd.randint(ypus - 3, ypus + 3), rnd.random() * 0.13 + 0.09) # move
                    time.sleep(rnd.random() * 0.1 + 0.086)
                    mouse.click() # burn log 1 
                    burnt = burnt + 1
                    xpus = xpus + 40

                    if ((burnt) % 4 == 0):
                        ypus = ypus + 35 # drop the mouse down one row of items for the next iteration
                        xpus = xpus - 160 # pull mouse back to the first coulum for the next iteration
                        time.sleep( 0.199 + rnd.random() *0.11)

                    pag.keyUp('shift')
                fruits = 0


                pag.moveTo(rnd.randint(750, 840), rnd.randint(535, 580), rnd.random() * 0.00181 + 0.11) #move to fruit
                pag.keyUp('shift')
            #End of wine run; time to sleep and repeat     

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
        
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        sys.exit()
        exit()

click_thread = threading.Thread(target=winemaker)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()

