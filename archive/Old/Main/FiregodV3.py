import time
import threading
import pyautogui
import random as rnd
import sys
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
from Utilities.MainFunctions import *

global running
global cycles
global burnt
global logsBurnt

ONOFF = KeyCode(char="`")
KEY = KeyCode(char ='8')

welcome()
print ("Let's burn up yo!")
Birdseye()
maxLogs = 900
print (" Press 1 toggle the bot OFF / ON")
print (" Press ' \ ' to kill the bot, or pull the mouse to the top left corner")
print ("Enjoy the burn!")

cycles = int (0)
burnt = int (0)
logsBurnt = int (0)
xpus = int (1755)
ypus = int(765)
running = False



def burner():
    while True:
        if running:
            print (" ~ T i m e  2  s p a r k  u p ! ~ ")
            global cycles
            global burnt
            global logsBurnt
            global maxLogs

            ## ~~~ Random mouse movement 3 seconds ~~~~ ####
            # Notbotting2()
            # Begin opening bank: 
            if (cycles % 2 == 0 or cycles == 0):
                print (" Odd session begin.")
                time.sleep(rnd.random() * 0.01 + 0.07) # wait before next action
                pag.moveTo(rnd.randint(1245,1255), rnd.randint(690,730), 0.43 + 0.151 * rnd.random() + 3/27 * rnd.random()) # move mouse to bank, sit at top left of GE.
                time.sleep(rnd.random() * 0.31 + 0.07) # wait before next action
                quick_click()
                time.sleep(rnd.random() * 0.31 + 0.07) # wait before next action
                pag.moveRel(rnd.randint(-10,10), rnd.randint(-10,14), rnd.random() * 0.43 + 0.9) #Move around from current spot
                Notbotting2()
                print ("Getting wood.")
                Slot2()
                time.sleep(rnd.random() * 0.1 + 0.1) # wait before next action
                Getall()
                time.sleep(rnd.random() * 2.1 + 1.3) # wait before next action
                if (rnd.random() > 0.50):
                    Notbotting3()
                    print (" 50% Shot hit, moving mouse to random spot.")
                time.sleep((rnd.random() * 3) + 0.9) # wait before next action
                if (rnd.random() > 0.74):
                    pag.moveRel(rnd.randint(-7,3), rnd.randint(-1,4), rnd.random() * 0.03 + 0.1) #Move around from current spot
                    time.sleep(rnd.random() * 4.5 + 1) # wait before next action
                    if (rnd.random() > 0.64):
                        pag.moveRel(rnd.randint(-17,13), rnd.randint(-10,14), rnd.random() * 0.03 + 0.3) #Move around from current spot
                # Moving to burn spot 1
                pag.moveTo(rnd.randint(1504, 1522), rnd.randint(727, 733), rnd.random() * 0.233 + 0.66) # move to burn spot 1 !
                if (rnd.random() > 0.417):
                    pag.moveTo(rnd.randint(1504, 1516), rnd.randint(731, 733), rnd.random() * 0.133 + 0.36) # move to burn spot 1 !
                time.sleep(rnd.random() * 0.1 + 0.19)
                #pag.moveRel(rnd.randint(-1,1), rnd.randint(1,2), rnd.random() * 0.13 + 0.1) #Move around from current spot
                quick_click()
                pag.moveRel(rnd.randint(-20,40), rnd.randint(-100,-20), rnd.random() * 0.131 + 0.1) #Move around from current spot
                pag.moveRel(rnd.randint(-32, 42), rnd.randint(6,12), rnd.random() * 0.131 + 0.1) # random movement
                pag.moveRel(rnd.randint(-12, 12), rnd.randint(6,12), rnd.random() * 0.135 + 0.11) # random movement
                time.sleep(rnd.random() * 0.19 + 4.329)

            if (cycles > 0 and (cycles + 1) % 2 == 0): #sesh 2 sesh 2 sesh 2 sesh 2 sesh 2 sesh 2 sesh 2 sesh 2
                print ("Even session begin.")
                pag.moveTo(rnd.randint(1196, 1208), rnd.randint(369,379), 0.43 + 0.5 * rnd.random() + 3/27 * rnd.random()) #move to bank after sesh 1
                time.sleep(rnd.random() * 0.2 + 0.3) # wait before next action, use .1 multiplier because we aren't moving mouse position. 
                quick_click() # Open up bank
                print("Mouse position at banker to start sesh 2:", pag.position()) # print position
                print ("Getting wood for the even sessions.")
                time.sleep(rnd.random() * .1 + 3.35)                 
                Slot2()
                Getall()
                print (" Let's get ready to burn!!")

                ## pag.moveRel(rnd.randint(0, 5), rnd.randint(38,40), 0.2 + 0.3 * rnd.random()) #Move mouse down to open bank when right clicked
                print("Grabbed wood at at:", pag.position()) # print position  
                pag.moveTo(rnd.randint(1375, 1380), rnd.randint(385, 390), 0.43 + 0.5 * rnd.random() + 0.73)  #Odd spot beginning   !!!!!!!!!!!!    
                time.sleep((rnd.random() * 0.2 + 0.02)) # Short sleep 
                quick_click() #Move to spot 2
                pag.moveRel(rnd.randint(-20,40), rnd.randint(-8,12), rnd.random() * 0.131 + 0.1) #Move around from current spot
                pag.moveRel(rnd.randint(-2, 12), rnd.randint(-6,12), rnd.random() * 0.0131 + 0.1) # random movement
                pag.moveRel(rnd.randint(-32, 42), rnd.randint(-6,12), rnd.random() * 0.131 + 0.1) # random movement
                pag.moveRel(rnd.randint(-12, 12), rnd.randint(6,12), rnd.random() * 0.135 + 0.1) # random movement
                time.sleep(4.22 + 0.131 * rnd.random()) # sleep extra for run to spot
                logsBurnt = logsBurnt - 1

            #sesh 2 sesh 2 sesh 2 sesh 2 sesh 2 sesh 2 sesh 2
    
            # BURN PROCESS BEGIN !
            Notbotting3()

            # Time to burn logs, this portion is extensive...
            xpus = 1740
            ypus = 770
            for i in range (1, 22):
                #if statement with a 50% chance of moving to the tinder box at closer perameters
                if (rnd.random() > 0.367621):
                    pag.moveTo(rnd.randint(1696,1708), rnd.randint(766, 771), rnd.random() * 0.03 + 0.197)
                else:
                    pag.moveTo(rnd.randint(1690,1709), rnd.randint(760, 773), rnd.random() * 0.03 + 0.197) #move to tinder box
                time.sleep(rnd.random() *0.01 + 0.236)
                quick_click() #use tinder box
                time.sleep(rnd.random() *0.01 + 0.3)
                if (rnd.random() > 0.397621):
                    pag.moveTo(rnd.randint(xpus - 3, xpus + 2), rnd.randint(ypus - 2, ypus + 4), rnd.random() * 0.03 + 0.349 + burnt/171 ) # move to log 
                else:
                    pag.moveTo(rnd.randint(xpus - 3, xpus + 3), rnd.randint(ypus - 3, ypus + 3), rnd.random() * 0.03 + 0.349 + burnt/171 ) # move to log 
                time.sleep(rnd.random() * 0.02 + 0.21 - burnt/201)
                quick_click() # burn log 1 
                xpus = xpus + 40 # Adjust X Position; moves mouse to right by one item in inventory
                burnt = burnt + 1 #Add to burn count

                if (burnt == 1):
                    time.sleep(rnd.random() *0.06 + 1.39) # Sleep for an extra 0.9 seconds on the first burn
                
                if ((burnt + 1) % 4 == 0 or burnt == 3):
                    ypus = ypus + 35 # drop the mouse down one row of items for the next iteration
                    xpus = xpus - 160 # pull mouse back to the first coulum for the next iteration
                    time.sleep( 0.009 + rnd.random() *0.005)

                if ((burnt + 2) % 4 == 0):
                    time.sleep( 0.01 + rnd.random() *0.001)
            
            
            print ("All done!")
            cycles = cycles + 1
            logsBurnt = logsBurnt + 20
            print ("This is batch number:", cycles, "with,", logsBurnt, "logs burnt.")
            print( (maxLogs - logsBurnt), "logs to go.")
            print("Keep it up !")
            time.sleep( 0.01 + rnd.random() *0.001)
            pag.moveTo(rnd.randint(856,864), rnd.randint(560,586), 0.13 + 5/27 * rnd.random()) # move mouse to banker?
            time.sleep( 0.01 + rnd.random() *0.001)
            burnt = 0

            if (logsBurnt > maxLogs):
               print ("Out of logs!")
               sys.exit()

            #End of run; time to sleep and repeat     
        time.sleep(rnd.random() * rnd.random() + 0.03)


def togglebot(key):
    if key == ONOFF:
        global running
        print ("Program is on:", not running)
        running = not running
    elif key == KEY: 
        print ("Kill switch acitaved")
        running = False
        sys.exit()

click_thread = threading.Thread(target=burner)
click_thread.start()

with Listener(on_press=togglebot) as listner:
    listner.join()