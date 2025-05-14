# Time module for random sleep functions 
import time 
import random as rnd

# This file abstracts the time module and the datetime module for anti bot detection purposes, it is used to make the bot more human like.

# define sleep as in between medium and quick sleep
def sleep(c=0.023, x=0.128, z=0.328):
    """Sleep between ~0.023-0.513 seconds
    
    For quick actions: sleep(0.007, 0.008, 0.017)  # ~0.007-0.032s
    For long pauses: sleep(0.802, 0.421, 0.614)    # ~0.802-2.053s
    Default medium: sleep()                         # ~0.023-0.513s
    """
    time.sleep(c + rnd.random() * x + rnd.random() * z)

# These are the three main sleep functions, they are used to sleep for a random amount of time between a certain range.

# Define a function for random sleep variance from ~0.1 to ~0.5 seconds
def sleep_if(sleep_chance=0.618, sleep_amount=0.01):
    if rnd.random() > sleep_chance:  # 38.2% chance
        time.sleep(rnd.random() * sleep_amount + 0.005)  # Sleep for ~0.005 to ~0.015 seconds
        if rnd.random() > 0.09420:  # 90.58% chance
            time.sleep(rnd.random() * sleep_amount + 0.005)  # Sleep for ~0.005 to ~0.015 seconds
        if rnd.random() > 0.381251:  # 61.87% chance
            time.sleep(rnd.random() * (sleep_amount * 2) + 0.01)  # Sleep for ~0.01 to ~0.03 seconds
        if rnd.random() > 0.793:  # 20.7% chance
            time.sleep(rnd.random() * (sleep_amount * 3) + 0.02)  # Sleep for ~0.02 to ~0.05 seconds
        if rnd.random() > 0.981251:  # 1.87% chance
            time.sleep(rnd.random() * (sleep_amount * 9) + 0.04)  # Sleep for ~0.04 to ~0.13 seconds
            if rnd.random() > 0.89:  # 11% chance
                time.sleep(rnd.random() * 0.09 + 0.04)  # Sleep for ~0.04 to ~0.13 seconds
    if rnd.random() > 0.991251:  # 0.87% chance
        time.sleep(rnd.random() * 0.003 + 0.001)  # Sleep for ~0.001 to ~0.004 seconds

#--------------------------------------------------------------------------------
# // This block runs only if the script is executed directly, not when imported.
if __name__ == "__main__":
    sleep()  
    print("hello world from sleep")  # Prints message after medium sleep
    sleep()

