import time
import threading
import pyautogui
import sys
import random as rnd
from pynput.keyboard import Listener, KeyCode
import Utilities.MainFunctions as af

global running
global rounds

ONOFF = KeyCode(char="`")
KEY = KeyCode(char ='8')

running = False
rounds = 0
print("Hello! Welcome.")

def MagicSmelter():
    while True:
        if running:
            print("Time to melt some bars!")
            time.sleep(0.3)
            af.Compass()
            af.leftkey()
            af.downkey()
            af.Zoomin()
            time.sleep(rnd.random() *0.1 + 0.1)
            af.Notbotting3()
            #move the mouse to the banker between X= 645, 1068, and Y 490, 700
            pag.moveTo(rnd.randint(645, 1068), rnd.randint(490, 700), rnd.random() * 0.181 + 0.41) #Move to banker
            af.click()
            af.Deposit()
            af.Slot4()
            af.click()
            #After grabbing runes, select ores
            af.Slot3()
            af.Getitems()
            af.Xbank()
            if (rounds == 0):
                #"Tap" down the F4 key 
                pag.keyDown('f4')
                time.sleep(0.03 * rnd.random() + 0.3)
                pag.keyUp('f4')
            
            #move to the spell
            time.sleep(0.03 * rnd.random() + 0.01)
            pag.moveTo(rnd.randint(1695, 1702), rnd.randint(906, 914), rnd.random() * 0.181 + 0.41)
            time.sleep(0.03 * rnd.random() + 0.41)

            #Click on this area 22 times

            for i in range(33):
                af.click()
                time.sleep(0.03 * rnd.random() + 0.51)
            rounds = rounds + 1

        if rounds > 420:
            running = False

            

    

def togglebot(key):
    if key == ONOFF:
        global running
        print("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print("Kill switch acitaved")
        running = False
        sys.exit()

click_thread = threading.Thread(target= MagicSmelter)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()
