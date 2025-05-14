import time
import random as rnd

def welcome():
    print ("Welcome to Old School Walk Scape")
    print ("Loading...")
    time.sleep(0.01 * rnd.random() + 0.013)
    print ("[-------------]")
    time.sleep(0.02 * rnd.random() + 0.015)
    print ("[\------------]")
    time.sleep(0.02 * rnd.random() + 0.024)
    print ("[\\\-----------]")
    time.sleep(0.03 * rnd.random() + 0.023)
    print ("[\\\\\\\---------]")
    time.sleep(0.03 * rnd.random() + 0.03)
    print ("[\\\\\\\\\--------]")
    time.sleep(0.03 * rnd.random() + 0.075)
    print ("[\\\\\\\\\\\\\------]")
    time.sleep(0.02 * rnd.random() + 0.03)
    print ("[\\\\\\\\\\\\\\\\\----]")
    time.sleep(0.03 * rnd.random() + 0.03)
    print ("[\\\\\\\\\\\\\\\\\\\\\--]")
    time.sleep(0.04 * rnd.random() + 0.05)
    print ("[\\\\\\\\\\\\\\\\\\\\\\\\\]")
    time.sleep(0.01 * rnd.random() + 0.05)
    print ("[|||||||||||||]")
    time.sleep(0.01 * rnd.random() + 0.01)
    print ("Press the Left CTRL Key to start the program; Right CTRL to kill the program.")
    print ("Walking initiated at time:", time.strftime("%H:%M:%S", time.localtime()), "24 Hour time") 
    print ("Enjoy your walk!")

def goodbye():
    print ("Goodbye!")
