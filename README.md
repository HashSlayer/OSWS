## Created by @HashSlayer


                                  _______  _______ _     _ _______ 
                                 |       ||       | | _ | |       |
                                 |   _   ||  _____|  |  | |  _____|
                                 |  | |  || |_____|     || |_____ 
                                 |  |_|  ||_____  |     ||_____  |
                                 |       | _____| |     | _____| |
                                 |_______||_______|_____||_______|
                       
                          Open Source Workspace Suite / Old School Walk Scape


# OSWS

Welcome to Old School Walk Scape, a fun interactive way to learn Python.
This guide uses a 2007 point-click game to learn Python. The concepts can be applied to other games or automative tasks.
This guide will not cover computer science concepts, complex algorithms, or complex automation. We will avoid using complex libraries such as color bots.

# Intro:

A Python-based automation and education suite designed to make inital programming concepts easy to understand, and provide a modular and customizable kit
to create automated procedures on the fly, with emulated human like behaviors. To learn, some simple and fun challenges in which this is organized for is
creating different scripts and GUIs for easily automated tasks to gain progress in a video game while we are away. To test our abilities, we have the oppurtunity
to create scripts that accomplish tasks for us, and optimize the algorithms and distribution of randomness, and breaks to learn what behavioral patterns humans make.

Do note that this is aimed to gain understand of algorithms and systems and avoids using color detection. Color detection can limit the complexity of algorithms and require more computational power. Hopefully this package can give you deeper insights about yourself, and the world we live in. As you learn and step into the world of automation and programming, the goal is to learn, to grow, to become better, and more effecient.

In this repository, we will go from zero to hero in a flash. Your journey if you decide to walk walk-scape may be different from others, and the speed and depth at which you understand these concepts will depend on how much you are willing to push yourself. It is recommened to pair this with AI assistance to ask the questions you are curious to understand, such as "What is threading?" and even "How does a CPU manage it's threads" or even "What are daemons?". Don't let these questions scare you. Although it will be helpful to know, the code provided will handle these things and it is not necesarry to fully understand the concepts just mentioned as you are learning and understanding the basics, such as developing your own algorithm, learning to properly nest loops, or maybe even just assign values to an integer for starters. We will learn how to import and use other repositories in this one, known as libraries or modules. Downloading and setting up the right enviorment, or ensuring that modules versions do not conflict with one another will not be covered. Ideally this would run in a virtual enviorment (venv) with the requirements.txt file clearly defining which versions to use.

After exploring PyAutoGUI (A library focused on automating tasks), TKinter (A library for Graphical User Interefaces (GUIs)), and even time. [If these are unfamiliar don't worry. I would suggest though a breif reading on some of these libraries to get a deeper understand of what you can do as we progress]; If you would like to take your skills to the next level, consider learning new modules, attempting to make a color bot, or even running multiple instances of one script through a farm using virtual machines, although the latter step is quite next level.

Enjoy your walk!


## 🤖 Features

- /archives: For old or archived files and folders.
- /main: This folder contains completed and functional examplatory scripts.
- /utils: This folder in the root directory contains utility files and functions, as well as utils/gui which contains our GUI components.
- /tests: Contains files to test the utilities, as well as functioning bots as well that haven't been moved to main yet.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Internet connection for installing dependencies

### Installation
1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/OSWS.git
   cd OSWS
   ```

2. Install required dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run any of the example scripts from the main directory

   ```bash
   python main/walk-test.py
   ```

### Requirements
The following Python packages are required and will be installed via the requirements.txt file:
- pyautogui - For automating mouse and keyboard actions
- pynput - For monitoring and controlling input devices
- mouse - For additional mouse control functionality
- Scaling plugin set to 45%

Tkinter is bundled with Python's standard installation and doesn't require separate installation through pip.

## User Interface

OSWS uses Tkinter to display a GUI in many scripts to handle automation processes, and visual command logging to track progress, as well as confetti to celebrate events,

## Human-like Mouse Movement
OSWS uses altered Bezier curves to create smooth, human-like mouse movements; and random pauses, stops, and occasional mistakes with path correction to simulate realistic user behavior.

## Additional Notes:
For image callibration using invetory grids, set the opacity to max and fill slots with the color value '#FFFF6A00'
