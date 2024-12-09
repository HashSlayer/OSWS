#mouse movement module
from .timmy import *
import pyautogui as pag

#define the move function
def simple_move(x, y):
    #move the mouse to the x and y coordinates
    pag.moveTo(x, y)

def move_to(x, y):
    quick_sleep()
    pag.moveTo(x, y)
    sleep()


# Only run this if the script is run directly
if __name__ == "__main__":
    print("Starting move_to(100, 100)")
    move_to(100, 100)
    print("Done!")
    sleep() #sleep for 1 second
