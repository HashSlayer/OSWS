#Use this file template to set the path to the project root directory

import os
import sys
import threading
import random as rnd
from pynput.keyboard import Listener, Key
from datetime import datetime
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root to the Python path
sys.path.insert(0, project_root)
#import other relevant modules here:
#from Utilities.timmy import *
from utils.core.timing import *
from utils.core.welcome import *
from utils.movements import *
from utils.clicker import *
from utils.item_slots import *
from utils.gui.confetti import *

welcome()

# Global variables to control the clicker state
running = False
running_lock = threading.Lock()
walker_thread = None

loops = 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Walker Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


dug = 0
zed = 0

def Timebot():  
    if (rnd.random() > 0.947):
        time.sleep(rnd.random() * 0.4 + 0.03)
        if (rnd.random() > 0.917):
            Notbotting()

def walker():
    while True:
        if not running:
            break
        if running:
            print("Get ready to crawl!")
            global dug
            global zed

            if rnd.random() > 0.02:  # 95% chance to execute the ore mining
                #Ore 1 (Top ore)
                bezierMove(rnd.randint(933,983), rnd.randint(361, 421), rnd.random() * 0.281 + 0.88913) #move to top iron ore, follow by a random chance to move within closer bounds
                if (rnd.random() > 0.388):
                        bezierMove(rnd.randint(936,983), rnd.randint(381, 425), rnd.random() * 0.081 + 0.418913)
                sleep(.3,.1,.1)  # Reduced by 0.1 seconds
                if rnd.random() > 0.5:
                    sleep(.1,.1,.2)
                click()
                if (rnd.random() > 0.976):
                    click()
                    print ("Nice double click!") #click
                    if rnd.random() > 0.97:
                        click()
                time.sleep(rnd.random() *0.28 + 0.661)  # Reduced by 0.1 seconds
                sleep(.3,.2,.2)  # Reduced by 0.1 seconds
                if rnd.random() > 0.97:
                    sleep(.3, 4, 2)
                    if rnd.random() > 0.97:
                        sleep(.3, 14, 2)
                dug += 1
                if dug == 26:
                    if rnd.random() > 0.412:
                        drop_inventory(rnd.randint(23, 27))
                    else:
                        drop_inventory(26)
                    dug = 0
            else:  # 5% chance to skip and sleep
                sleep(1, 3, 3)
                if rnd.random() > 0.98:
                    sleep(1, 20)
                    Notbotting()


            if rnd.random() > 0.02:  # 95% chance to execute the ore mining
                #Ore 2 (middle ore)
                bezierMove(rnd.randint(685, 765), rnd.randint(595, 645), rnd.random() * 0.2832 + 0.881) #move to bottom ore, follow by a random chance to move within closer bounds
                if (rnd.random() > 0.381):
                    bezierMove(rnd.randint(695, 775), rnd.randint(595, 645), rnd.random() * 0.081 + 0.418913)
                time.sleep(rnd.random() *0.381 + 0.683)  # Reduced by 0.1 seconds
                if rnd.random() > 0.5:
                    sleep(.2,.1,.2)  # Reduced by 0.1 seconds
                click()
                if (rnd.random() > 0.93):
                    click()
                    print ("Nice double click!") #click
                Timebot()
                time.sleep(rnd.random() *0.36 + 0.651)  # Reduced by 0.1 seconds
                if rnd.random() > 0.97:
                    sleep(.3, 4, 2)
                dug += 1
                if dug == 26:
                    if rnd.random() > 0.112:
                        drop_inventory(25)
                    else:
                        drop_inventory(26)
                    dug = 0
            else:  # 5% chance to skip and sleep
                    sleep(1, 3, 3)
                    if rnd.random() > 0.91:
                        sleep(1, 8)
                        Notbotting()


            if rnd.random() > 0.02:  # 95% chance to execute the ore mining
                #Ore 3 (Bottom ore) 
                bezierMove(rnd.randint(909, 960), rnd.randint(765, 835), rnd.random() * 0.281 + 0.889111) 
                if (rnd.random() > 0.381):
                    bezierMove(rnd.randint(897, 963), rnd.randint(765, 835), rnd.random() * 0.081 + 0.4118913)
                time.sleep(rnd.random() *0.51 + 0.513)  # Reduced by 0.1 seconds
                click()
                if rnd.random() > 0.5:
                    sleep(.3,.3,.2)  # Reduced by 0.1 seconds
                if (rnd.random() > 0.939):
                    click()
                    print ("Nice double click!") #click
                time.sleep(rnd.random() *0.61 + 0.631)  # Reduced by 0.1 seconds
                if rnd.random() > 0.97:
                    sleep(.3, 4, 2)
                Timebot()
                dug += 1
            else:  # 5% chance to skip and sleep
                sleep(2, 3, 3)
                if rnd.random() > 0.91:
                    sleep(1, 7)
                    Notbotting()

            if dug == 26:
                if rnd.random() > 0.112:
                    drop_inventory(25)
                else:
                    drop_inventory(26)
                dug = 0


#zoomed out by 4 pixels 

# Warning holding left CTRL turning the progran on and off can crash the program
# Warning holding right CTRL will exit the program
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def toggle_program():
    """Toggle the running state and start/stop the program."""
    global running, walker_thread
    with running_lock:
        running = not running
        if running:
            if walker_thread is None or not walker_thread.is_alive():
                walker_thread = threading.Thread(target=walker, daemon=True)
                walker_thread.start()
        print("Program running" if running else "Program stopped")

def exit_program():
    """Exit the program by setting running to False and printing a message."""
    global running
    with running_lock:
        running = False
    print("Exiting program")
    exit(0)

def on_press(key):
    """Handle key press events to toggle the clicker or exit the program."""
    if key == Key.ctrl_l:
        toggle_program()
    elif key == Key.ctrl_r:
        exit_program()

def main():
    """Main function to start the keyboard listener."""
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
