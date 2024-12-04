import sys
import os
import threading
import random as rnd
from pynput.keyboard import Listener, KeyCode, Key
import tkinter as tk
from tkinter import font as tkFont
from datetime import datetime
from Utilities.MainFunctions import *
from Utilities.Movement import *
from Utilities.Conffeti import *
from Utilities.Banking import *
 
#------------------------------------------------------------------
# Example usage   

sleep(1)
print("Welcome to the playground")

# Functions like sleep (1) we made ourselves.

#Let's simplify the time.sleep function slightly since we will be using it extensively..

#Here is nearly the same Sleep function; Same Function Differnet Name, so we named it "SFDN" with the "def" keyword.
#We can use this function to sleep for a random amount of time between .01 and .05 seconds.
def SFDN(c = .1 , x = .01, z = 0.005): #C is a constant. X and Z are both multiplied by a random number between 0-1.
    time.sleep(c + rnd.random() *x + rnd.random() *z) #3 variables to play around with our random distribution of sleeping. 

def badSDFN(): #Parameters are the values or inputs we define "into" the function within those paranthesis, its okay to have none.
    time.sleep(1 + rnd.random() * 0.1) #Without them the functions functionality is limited and "hard coded". 

#Currently if we call;
SFDN() #This will call time.sleep(.1 + rnd.random() * .01 + rnd.random() * .005)
#or if we call;
SFDN(5, 2) #This will call time.sleep(5 + rnd.random() * 2 + rnd.random() * .005)

#We can play around with these concepts and make our own functions to do whatever we want. This can simplify our code and make it easier to play with. Autom8 everything <3


#------------------------------------------------------------------
    

