import time
import threading
import pyautogui
import sys
import random as rnd
from pynput.keyboard import Listener, KeyCode
#Import the MainFunctions file which is one directory up.
from Utilities.MainFunctions import *


def cycle():
        #In the cycles function we will define 5 locations to move our mose to and click
        #The location spots are as follows: 1: (822, 397), 2: (1064, 501), 3: (1131, 573), 4: (881, 669), 5:(808, 567)

        #Location 1
        pag.moveTo(rnd.randint(816, 828), rnd.randint(391, 403), rnd.random() * 0.1 + 0.41)
        click()
        Notbotting2()
        time.sleep(rnd.random() * 0.5 + 1.1)
        #Location 2
        pag.moveTo(rnd.randint(1058, 1070), rnd.randint(495, 507), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(1063, 1069), rnd.randint(499, 506), rnd.random() * 0.1 + 0.11)
        click()
        time.sleep(rnd.random() * 0.5 + 2.3)
        #Location 3
        pag.moveTo(rnd.randint(1125, 1137), rnd.randint(567, 579), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(1130, 1136), rnd.randint(571, 578), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.5 + 2.4)
        #Location 4
        pag.moveTo(rnd.randint(875, 887), rnd.randint(663, 675), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(880, 886), rnd.randint(667, 674), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.3 + 1.91)
        #Location 5
        pag.moveTo(rnd.randint(802, 814), rnd.randint(561, 573), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(807, 813), rnd.randint(565, 572), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.1 + 1)
        Notbotting2()
        time.sleep(rnd.random() *0.1 + 1)
        Notbotting()
        time.sleep(rnd.randint(68, 79) + rnd.random())

def cycleslow():
             #In the cycles function we will define 5 locations to move our mose to and click
        #The location spots are as follows: 1: (822, 397), 2: (1064, 501), 3: (1131, 573), 4: (881, 669), 5:(808, 567)

        #Location 1
        pag.moveTo(rnd.randint(816, 828), rnd.randint(391, 403), rnd.random() * 0.1 + 0.41)
        click()
        Notbotting2()
        time.sleep(rnd.random() * 1.5 + 16.1)
        #Location 2
        pag.moveTo(rnd.randint(1058, 1070), rnd.randint(495, 507), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(1063, 1069), rnd.randint(499, 506), rnd.random() * 0.1 + 0.11)
        click()
        time.sleep(rnd.random() * 1.5 + 21.3)
        #Location 3
        pag.moveTo(rnd.randint(1125, 1137), rnd.randint(567, 579), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(1130, 1136), rnd.randint(571, 578), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.5 + 5.4)
        #Location 4
        pag.moveTo(rnd.randint(875, 887), rnd.randint(663, 675), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(880, 886), rnd.randint(667, 674), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.3 + 1.91)
        if (rnd.random() > 0.93):
            print ("quick nap time at spot 4")
            time.sleep(rnd.random() *4.1 + 0.4)
        #Location 5 (home)
        pag.moveTo(rnd.randint(802, 814), rnd.randint(561, 573), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(807, 813), rnd.randint(565, 572), rnd.random() * 0.1 + 0.31)
        click()
        Notbotting2()
        time.sleep(rnd.random() * 1.1 + 16)
        time.sleep(rnd.random() *0.1 + 1)
        Notbotting()
        time.sleep(rnd.randint(30, 40) + rnd.random())

def cycleslow2():
             #In the cycles function we will define 5 locations to move our mose to and click
        #The location spots are as follows: 1: (822, 397), 2: (1064, 501), 3: (1131, 573), 4: (881, 669), 5:(808, 567)

        #Location 1
        pag.moveTo(rnd.randint(816, 828), rnd.randint(391, 403), rnd.random() * 0.1 + 0.41)
        click()
        Notbotting2()
        time.sleep(rnd.random() * 1.5 + 9.1)
        #Location 2
        pag.moveTo(rnd.randint(1058, 1070), rnd.randint(495, 507), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(1063, 1069), rnd.randint(499, 506), rnd.random() * 0.1 + 0.11)
        click()
        time.sleep(rnd.random() * 3.5 + 24.3)
        #Location 3
        pag.moveTo(rnd.randint(1125, 1137), rnd.randint(567, 579), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(1130, 1136), rnd.randint(571, 578), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.5 + 5.4)
        #Location 4
        pag.moveTo(rnd.randint(875, 887), rnd.randint(663, 675), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(880, 886), rnd.randint(667, 674), rnd.random() * 0.1 + 0.31)
        click()
        time.sleep(rnd.random() * 0.6 + 1.91)
        if (rnd.random() > 0.93):
             time.sleep(rnd.random() * 0.6 + 0.1)
        #Location 5 (home)
        pag.moveTo(rnd.randint(802, 814), rnd.randint(561, 573), rnd.random() * 0.1 + 0.41)
        if (rnd.random() > 0.93):
            pag.moveTo(rnd.randint(807, 813), rnd.randint(565, 572), rnd.random() * 0.1 + 0.31)
        click()
        Notbotting2()
        time.sleep(rnd.random() * 1.1 + 19)
        time.sleep(rnd.random() *0.1 + 1)
        if (rnd.random() > 0.91):
             Notbotting3()
        time.sleep(rnd.randint(28, 39) + rnd.random())
     

def jog():
    Notbotting()
    #move the mouse to the upper left (154, 277), wait, click, and wait again for 9 second
    pag.moveTo(rnd.randint(151, 159), rnd.randint(275, 280), rnd.random() * 0.1 + 0.41)
    click()
    time.sleep(rnd.random() * 0.71 + 9.3)
    #then move to (745, 663) and click and wait 3 seconds with a 0.1 second random
    pag.moveTo(rnd.randint(742, 748), rnd.randint(661, 665), rnd.random() * 0.1 + 0.41)
    click()
    time.sleep(rnd.random() * 0.3 + 3.3)
    #Now for spot 3; at: (1485, 602)
    pag.moveTo(rnd.randint(1482, 1494), rnd.randint(599, 604), rnd.random() * 0.1 + 0.41)
    click()
    time.sleep(rnd.random() * 1.1 + 6)
    #then move to (1570, 668) and click and wait 5 seconds with a 0.1 second random
    pag.moveTo(rnd.randint(1567, 1573), rnd.randint(665, 671), rnd.random() * 0.1 + 0.41)
    click()
    time.sleep(rnd.random() * 0.1 + 9.9)
    Notbotting()

#From spot 1 which is where the lowest Swamp crab spwans.
def jog2():
    Notbotting()
    #move the mouse to the upper left (154, 277), wait, click, and wait again for 9 second
    pag.moveTo(rnd.randint( 20 , 160 ), rnd.randint( 433 , 622 ), rnd.random() * 0.2 + 0.23)
    pag.moveTo(rnd.randint( 50 , 60 ), rnd.randint( 533 , 542 ), rnd.random() * 0.15 + 0.33)
    if (rnd.random() > 0.83):
        pag.moveTo(rnd.randint(52 , 56 ), rnd.randint( 537 , 540 ), rnd.random() * 0.1 + 0.1)
    click()
    Notbotting()
    time.sleep(rnd.random() * 0.41 + 8.4)
    #then move to (745, 663) and click and wait 3 seconds with a 0.1 second random
    Notbotting3()
    #Now for spot 3; at: (1485, 602)
    pag.moveTo(rnd.randint(1750 , 1899), rnd.randint(511 , 600), rnd.random() * 0.2 + 0.23)
    pag.moveTo(rnd.randint(1814 , 1821), rnd.randint(530 , 538), rnd.random() * 0.15 + 0.33)
    if (rnd.random() > 0.83):
        pag.moveTo(rnd.randint(1816 , 1820), rnd.randint(532 , 537), rnd.random() * 0.1 + 0.1)
    click()
    Notbotting()
    time.sleep(rnd.random() * 1.1 + 8)
    #then move to (1570, 668) and click and wait 5 seconds with a 0.1 second random

#From spot to that leads to jog2 spot
def jog3():
        Notbotting()
    #move the mouse to the upper left (154, 277), wait, click, and wait again for 9 second
        pag.moveTo(rnd.randint( 100 , 267 ), rnd.randint( 699 , 799 ), rnd.random() * 0.2 + 0.23)
        pag.moveTo(rnd.randint( 109 , 117 ), rnd.randint( 701 , 710 ), rnd.random() * 0.15 + 0.3)
        if (rnd.random() > 0.83):
            pag.moveTo(rnd.randint( 112 , 116 ), rnd.randint( 702 , 707), rnd.random() * 0.1 + 0.1)
        click()
        Notbotting()
        time.sleep(rnd.random() * 0.41 + 9.1)
        #then move to (745, 663) and click and wait 3 seconds with a 0.1 second random
        Notbotting3()
        #Now for spot 3; at: (1485, 602)
        pag.moveTo(rnd.randint(1750 , 1899), rnd.randint(511 , 600), rnd.random() * 0.2 + 0.23)
        pag.moveTo(rnd.randint(1811 , 1821), rnd.randint(528 , 538), rnd.random() * 0.15 + 0.33)
        if (rnd.random() > 0.83):
            pag.moveTo(rnd.randint(1816 , 1820), rnd.randint(532 , 537), rnd.random() * 0.1 + 0.1)
        time.sleep(rnd.random() * 0.1 + 0.1)
        click()
        Notbotting()
        time.sleep(rnd.random() * 1.1 + 8) #ENDS BACK AT HOME (LOCATION 5); Recreate another version that will lead back to spot 2.
    