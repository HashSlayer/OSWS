import random as rnd
from .core.timing import *
from .movements import *
from .clicker import *
import tkinter as tk
from pynput.keyboard import Key

#Inventory slots can change depending on the resolution. This is a function to get the correct inventory slots for any resolution.
#Currently optimized for 1920x1080, 16:9 aspect ratio. 
#The scaling plugin should be used to scale the inventory slots to 45% as well. 



def inv_slot(slot = 1, time_multiplier = 1, x = 1625, y=638, z=10): #Can +/- 20 pixels and be fine. X and Y is the middle of the first slot in the inventory 
    slot -= 1
    row = slot // 4
    column = slot % 4
    x = x + (61 * column)
    y = y + (51 * row)
    x = rnd.randint(x - z, x + z)  # Randomize x within the range
    y = rnd.randint(y - z, y + z)  # Randomize y within the range
    if slot < 29:
        #print("Slot:", slot, " Row:", row, " Column:", column, " X:", x, " Y:", y)
        bezierMove(x, y, time_multiplier)
    else:
        sleep(.1, .9, .9)
from pynput.keyboard import Controller

keyboard = Controller()

#Dropping items, create a drop_inventory function that holds shift and clicks the inventory slots
def drop_inventory(slots = 28, time_multiplier = 1, x = 1625, y=638, z=8):
    keyboard.press(Key.shift)  # Hold shift key
    random_value = rnd.random()
    if random_value > 0.8:  # 20% chance to drop items in multiples of 4
        for i in range(4):
            for slot in range(i + 1, slots + 1, 4):
                inv_slot(slot, time_multiplier, x, y, z)  # Use inv_slot to click each slot
                sleep(.1, .1, .1)
                if rnd.random() > 0.98:
                    sleep(.1, .1, .1)
                click()
                if rnd.random() > 0.98:
                    sleep(.1, .6, .4)
    elif random_value > 0.3:  # Additional 50% chance to drop items in a zig-zag pattern
        for row in range(7):  # Assuming 7 rows for 28 slots
            if row % 2 == 0:  # Even row: left to right
                for col in range(4):
                    slot = row * 4 + col + 1
                    if slot <= slots:
                        inv_slot(slot, time_multiplier, x, y, z)
                        sleep(.1, .1, .1)
                        if rnd.random() > 0.98:
                            sleep(.1, .1, .1)
                        click()
                        if rnd.random() > 0.95:
                            sleep(.1, .4, .4)
            else:  # Odd row: right to left
                for col in range(3, -1, -1):
                    slot = row * 4 + col + 1
                    if slot <= slots:
                        inv_slot(slot, time_multiplier, x, y, z)
                        sleep(.1, .1, .1)
                        if rnd.random() > 0.95:
                            sleep(.1, .1, .1)
                        click()
                        if rnd.random() > 0.98:
                            sleep(.1, .5, .1)
    else:  # 60% chance to drop items sequentially
        for slot in range(1, slots + 1):
            inv_slot(slot, time_multiplier, x, y, z)  # Use inv_slot to click each slot
            sleep(.1, .1, .1)
            if rnd.random() > 0.98:
                sleep(.1, .1, .1)
            click()
            if rnd.random() > 0.98:
                sleep(.1, .1, 1)
    keyboard.release(Key.shift)  # Release shift key




def simp_inv_slot(slot = 1, time_multiplier = 1, x = 1625, y=638, z=8): #Can +/- 20 pixels and be fine. X and Y is the middle of the first slot in the inventory 
    slot -= 1
    row = slot // 4
    column = slot % 4
    x = x + (61 * column)
    y = y + (51 * row)
    x = rnd.randint(x - z, x + z)  # Randomize x within the range
    y = rnd.randint(y - z, y + z)  # Randomize y within the range
    if slot < 29:
        simple_move(x, y, time_multiplier)
    else:
        sleep(.1, .9, .9)

def bank_slot(slot = 1, time_multiplier = 1, sleep_for = .01, sleep_upto = .01, x = 520, y=160, z=10): #Can +/- 20 pixels and be fine X, and Y define the middle of the first item in bank
    # Add 32 to X for each slot, add 35 to Y, -32 * 8 to x for every 8 slots
    # 8 slots per row, 5 rows
    slot -= 1
    row = slot // 8
    column = slot % 8
    x = x + (69 * column)
    y = y + (52 * row)
    x = rnd.randint(x - z, x + z)  # Randomize x within the range
    y = rnd.randint(y - z, y + z)  # Randomize y within the range
    #print("Slot:", slot, " Row:", row, " Column:", column, " X:", x, " Y:", y)
    bezierMove(x, y, time_multiplier)
    sleep(sleep_for, sleep_upto, .003) #sleep

def bank_near_inv(x1=1480, x2=1540, y1=615, y2=885, time= rnd.randint(23, 48)/100, wait=.3):
    bezier_between(x1, x2, y1, y2, time) 
    sleep(.1, wait, .05) #sleep#open up the bank.
    sleep()

# Exit the bank
def exit_bank(x1=1075, x2=1100, y1=41, y2=64, time= rnd.randint(30, 52)/100, pause_upto=.2):
    if (rnd.random() > 0.6):
        bezier_between(x1, x2, y1, y2, time)
    else:
        bezier_between(x1+3, x2-5, y1+5, y2-2, time) #Disrupt entirely random location
    sleep(.05, pause_upto, .02) #Pause before exiting bank
    sleep()

#Deposit all items in inventory
def deposit_all(x=1030, y=760, size=9, time = rnd.randint(30, 45)/100, pause_upto=.5):
    if (rnd.random() > 0.7):
        bezier_between(x-size, x+size, y-size, y+size, time)
    else:
        bezier_between(x-7,x+8, y-6, y+10, time)
    sleep(.1, pause_upto, .02) #sleep


#Set as Withdraw item as note    
#def withdraw_as_note(x1 = 685, x2=705, y1 = 775, y2=780, time = rnd.randint(40, 55)/100, pause_upto = .2):
 #   if (rnd.random() > 0.8):
  #      bezier_between(x1, x2, y1, y2, time)
   # sleep(.1, pause_upto, .02) #sleep
    #click()


#RELATIVE MOVEMENT
def get_x_items(x1 = -30, x2 = 20, y1 = 93, y2 = 97, time= rnd.random() * 0.1 + rnd.randint(13, 39)/100, pause_upto=.2):
    sleep(.03, .09) #sleep
    right_click() #right click
    if (rnd.random() > 0.69420): # REFINED WAY TO LOCALIZE LOCATIONS
        bezier_relative(x1-15, x2+10, y1, y2, time) #move mouse down to quantity of X
    else:
        bezier_relative(x1, x2, y1+1, y2-1, time) #move mouse down to quantity of X
    sleep(.05, pause_upto, .02) #sleep


     # Copy the get_x_items() function with this line: pag.moveRel(rnd.randint(-30, 17), rnd.randint(101, 114), yrt * 0.12 + 0.23) #move mouse down to quantity of all


def get_all_items(x1 = -30, x2 = 20, y1 = 132, y2 = 136, time= rnd.random() * 0.15 + 0.3, pause_upto=.2):
    sleep(.03, .09) #sleep
    right_click() #right click
    if (rnd.random() > 0.69420): # REFINED WAY TO LOCALIZE LOCATIONS
        bezier_relative(x1-15, x2+10, y1, y2+5, time) #move mouse down to quantity of X add y2+5 to toggle for all but 1 on occasion
    else:
        bezier_relative(x1, x2, y1+1, y2-1, time) #move mouse down to quantity of X
    sleep(.05, pause_upto, .02) #sleep

    def get_screen_dimensions():
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height

    def suggest_inventory_scaling():
        print("Suggested inventory scaling: 45%")

    if __name__ == "__main__":
        width, height = get_screen_dimensions()
        print(f"Screen dimensions: {width}x{height}")
        suggest_inventory_scaling()
