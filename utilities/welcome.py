import time
import random as rnd



class Welcomer:
    
    def welcome(self):
        print("Welcome to Old School Walk Scape")
        print("Loading...")
        time.sleep(0.1 * rnd.random() + 0.13)
        print("[-------------]")
        time.sleep(0.2 * rnd.random() + 0.15)
        print("[\\------------]")
        time.sleep(0.2 * rnd.random() + 0.24)
        print("[\\\\-----------]")
        time.sleep(0.3 * rnd.random() + 0.23)
        print("[\\\\\\---------]")
        time.sleep(0.3 * rnd.random() + 0.3)
        print("[\\\\\\\\--------]")
        time.sleep(0.3 * rnd.random() + 0.075)
        print("[\\\\\\\\\\------]")
        time.sleep(0.2 * rnd.random() + 0.03)
        print("[\\\\\\\\\\\\----]")
        time.sleep(0.3 * rnd.random() + 0.03)
        print("[\\\\\\\\\\\\\\--]")
        time.sleep(0.4 * rnd.random() + 0.05)
        print("[\\\\\\\\\\\\\\\\]")
        time.sleep(0.1 * rnd.random() + 0.05)
        print("[|||||||||||||]")
        time.sleep(0.1 * rnd.random() + 0.1)
        print("Press the Left CTRL Key to start the program; Right CTRL to kill the program.")
        print("Walking initiated at time:", time.strftime("%H:%M:%S", time.localtime()), "24 Hour time")
        print("Enjoy your walk!")

    def goodbye(self):
        print("Goodbye!")
