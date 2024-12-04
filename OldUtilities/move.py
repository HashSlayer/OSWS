#import the timmy module
import timmy
import pyautogui as pag

#define the move function
def simple_move(x, y):
    #move the mouse to the x and y coordinates
    pag.moveTo(x, y)

def move_to(x, y):
    timmy.quick_sleep()
    pag.moveTo(x, y)
    timmy.sleep()


# Only run this if the script is run directly
if __name__ == "__main__":
    move_to(100, 100)