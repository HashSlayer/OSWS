import time
import random as rnd

def welcome():
    print ("Welcome to Old School Walk Scape")
    print ("Loading...")
    time.sleep(0.1 * rnd.random() + 0.13)
    print ("[-------------]")
    time.sleep(0.2 * rnd.random() + 0.15)
    print ("[\------------]")
    time.sleep(0.2 * rnd.random() + 0.34)
    print ("[\\\-----------]")
    time.sleep(0.3 * rnd.random() + 0.33)
    print ("[\\\\\\\---------]")
    time.sleep(0.3 * rnd.random() + 0.4)
    print ("[\\\\\\\\\--------]")
    time.sleep(0.3 * rnd.random() + 0.075)
    print ("[\\\\\\\\\\\\\------]")
    time.sleep(0.2 * rnd.random() + 0.03)
    print ("[\\\\\\\\\\\\\\\\\----]")
    time.sleep(0.3 * rnd.random() + 0.03)
    print ("[\\\\\\\\\\\\\\\\\\\\\--]")
    time.sleep(0.6 * rnd.random() + 0.05)
    print ("[\\\\\\\\\\\\\\\\\\\\\\\\\]")
    time.sleep(0.1 * rnd.random() + 0.05)
    print ("[|||||||||||||]")
    time.sleep(0.1 * rnd.random() + 0.1)
    print ("Press the Left CTRL Key to start the program; Right CTRL to kill the program.")
    print ("Walking initiated at time:", time.strftime("%H:%M:%S", time.localtime()), "24 Hour time") 
    print ("Enjoy your walk!")

    