import time
import sys
import os
import threading
import pyautogui
import random as rnd
from pynput.keyboard import Listener, KeyCode
# Get the directory of the current script
current_script_dir = os.path.dirname(__file__)
# Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
# Add the parent directory to sys.path
sys.path.append(parent_dir)
from Utilities.MainFunctions import *
from Utilities.Movement import *

welcome()


# Example usage
        
sleep(2, .01, .01)

bezierMove(420,69)
bezierMove(69,420)
bezierMove(420,69)
bezierMove(69,420)

sleep(2, .01, .01)


