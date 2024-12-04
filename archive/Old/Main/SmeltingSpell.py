import time
import threading
import pyautogui
import sys
import random as rnd
from pynput.keyboard import Listener, KeyCode
#Import the MainFunctions file which is one directory up.
from Utilities.MainFunctions import *

global running
global rounds
global rounds2
global maxrounds
global x
global y

ONOFF = KeyCode(char="1")
KEY = KeyCode(char ='2')

rounds = int (0)
rounds2 = int (1)
running = False
maxrounds = int (147)
#ask the user for the max rounds
print ("How many rounds would you like to run?")
maxrounds = int (input())
x = int (18)
y = int (20)

welcome()


def smegic():
    while True:
        if running:
            global rounds
            global rounds2
            global x
            global y
            global maxrounds
            print ("Let's Melt Up! It is round:", rounds)
            if (rounds == 0):
                Compass()
                #Move mouse to the left and down towards middle of screen
                pag.moveRel(rnd.randint(-400, -200), rnd.randint(100, 300), rnd.random() * 0.181 + 0.41)
                leftkey()
                downkey()
                Zoomin()
            time.sleep(rnd.random() *0.1 + 0.8)
            Notbotting3()
            #move the mouse to the banker between X= 645, 1068, and Y 490, 700
            pag.moveTo(rnd.randint(645, 1068), rnd.randint(490, 700), rnd.random() * 0.181 + 0.41) #Move to banker
            click()
            Deposit()
            if (rounds > rnd.randint(50, 1000)):
                Notbotting2()
            if (rnd.random() > 0.93):
                    click()
            time.sleep( rnd.random() + 0.1)

            Slot4()
            if (rnd.random() > rnd.random()):
                time.sleep( 0.01 * rnd.random() + 0.01)
            click()
            if ((rounds > 20) & (rnd.random() > 0.5)):
                time.sleep( 0.3 * rnd.random() + 0.1)
            #After grabbing runes, select ores
            Slot3()
            if (rnd.random() > rnd.random()):
                time.sleep( 0.1 * rnd.random() + 0.01)
            if (rnd.random() > 0.420):
                Getall()
                #elif statement to call getall()
            else:
                Getitems()
            
            Xbank()
            #Another if statement giving a 4% chance to move the mouse to the center of the screen, wait, and then right click
            if (rnd.random() > 0.96):
                time.sleep(0.1 * rnd.random() + 0.1)
                pag.moveTo(960, 540, rnd.random() * 0.181 + 0.41)
                #move to the same location but with a pixel variation of 20
                pag.moveTo(rnd.randint(691, 984), rnd.randint(420, 701), rnd.random() * 0.181 + 0.41)
                time.sleep(0.1 * rnd.random() + 0.1)
                pag.rightClick()
                time.sleep(0.1 * rnd.random() + 0.1)

            if (rounds == 0 or rnd.random() > 0.42069):
                #"Tap" down the F4 key
                time.sleep(0.1 * rnd.random() + 0.3)
                time.sleep(1 * rnd.random()) 
                pag.keyDown('f4')
                time.sleep(0.1 * rnd.random() + 0.09)
                pag.keyUp('f4')
            
            #move to the spell
            time.sleep(0.03 * rnd.random() + 0.01)
            if (rnd.random() > 0.683):
                time.sleep(rnd.random() + 0.1)
            pag.moveTo(rnd.randint(1695, 1702), rnd.randint(906, 910), rnd.random() * 0.181 + 0.41)
            if (rnd.random() > 0.783):
                pag.moveTo(rnd.randint(1695, 1699), rnd.randint(910, 914), rnd.random() * 0.181 + 0.41)
            #if statement to move to the same spot but slower if past round 200
            if ((rounds > 23) & (rnd.random() > 0.6)):
                time.sleep(0.03 * rnd.random() + 0.03)
                print ("Your charater had to sneeze!")
            time.sleep(0.1 * rnd.random() + 0.41)

            #Click on this area 22 times

            for i in range(32):
                click()
                time.sleep(0.1 * rnd.random() + 0.6)
                time.sleep(0.1 * rnd.random())
                #if (rnd.random() > 0.93):
                #    quick_click()

                

            if (rounds2 % y == 0 & rounds != 0):
                print ("Let's take a break!")
                Notbotting2()
                time.sleep(0.1 * rnd.random() + rnd.randint(8, x))
                print ("Let's get back to it!")
                time.sleep(rnd.random())
                if (rnd.random() > 0.5):
                    x = x + 3
                rounds2 = 0
                y = rnd.randint(8, 20) #optimize the randomization in break times, and amounts. Y starts at 20
                if (rounds > 100):
                    y = rnd.randint(6, 17)
                    print ("Next round of sleep is in: ", y, " rounds")

            if (rounds % rnd.randint(9, 12) == 0 & rounds != 0):
                print ("Let's take a short break! We've gained: ", rounds * 16 * 22.5, "EXP" )
                Notbotting2()
                time.sleep(0.1 * rnd.random() + rnd.randint(1, 2))

            if ((rounds <150) & (rnd.random() > 0.861)):
                time.sleep( rnd.random() + x )

            if (rounds > maxrounds):
                print ("Let's end here!")
                Notbotting2()
                # Sleep for 24 hours
                time.sleep(86400)

            rounds = rounds + 1
            rounds2 = rounds2 + 1

def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        sys.exit() # This will end the program entirely

click_thread = threading.Thread(target=smegic)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()