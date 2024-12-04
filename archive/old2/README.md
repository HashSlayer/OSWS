# Old-School-Walk-Scape - Intro to Python With 5Mekail0
## Created by @5MEkailO



Notes: 


Item 1: 1601, 660 - 1652, 616 (Bottom left to Top Right)
Item 2: 1662, 660 - X = 51 pixel size Y = 44 size
Item 3: 1722, 660 - Distance from one slot to another is:
Item 4: 1783, 660 - (X): 61 (Y): 51 from below
Item 5: 1601, 711 - We now have all the data we need for inv

With this data we can suggest 4 columns and 7 rows
The center for Item 1 = 1625, 638 [you can safely +/- 20 x]
[You can also safely +/- 20 y]

Rows = 638 + R*51 (+/-20)
Column = 1625 + C*61 (+/-20)


Bank:
Item 1: 495, 182 ~ 546, 137
Item 2: 564, 182 
Item 9: 495, 234 
X = 69 per column
Y = 52 per row
+ / - = 20








Welcome to Old School Walk Scape, a fun interactive way to learn Python.
This guide uses a 2007 point-click game to learn Python. The concepts can be applied to other games or automative tasks.
This guide will not cover computer science concepts, complex algorithms, or complex automation. We will avoid using complex libraries such as color bots.

OSWS; OSRS scripting bot for various skills. Created to improve GUI automation, made for educational purposes

Welcome to Mekail The Machine's basic OSRS skilling script using python.

It was optimized to run on a screen with 1920 x 1080 resolution, features to translate coordiantes manullay have been deprecated.
The script is safe to use on Linux, MacOS, and Windows.

Make sure to open this folder in the terminal any type pip install -r requirements.txt after succesfully installing python. From there run any file with bot logic by double clicking the file, or running it through an IDE. 

# Developer Setup <img height=20/>

1. Install Python 3.10 (not compatible with other major versions)
2. Clone/download this repository
3. Open the project folder in your IDE of choice (Visual Studio Code recommended)
4. install the depedencies pip install -r requirements.txt
5. Run the files locally, or from your terminal

## User Interface

OSWS uses Tkinter to display a GUI in many scripts to handle automation processes, and visual command logging to track progress, as well as confetti to celebrate events,

## Human-like Mouse Movement
OSWS uses altered Bezier curves to create smooth, human-like mouse movements; and random pauses, stops, and occasional mistakes with path correct. 

# Scripts

A2 Functions, and MainFunctions act as Utility files, containing definitions for various functions that automate the process of time.sleep(),
and obsfucate mouse.click with pag to click the left mouse button for a duration of .1 - .3 seconds etc..
Automation for pressing keys 1-9, recommended remapping of keys through runelite to match, and more.

BeautifulTest tracks the position of the mouse when clicked, celebrating every 10 clicks. Used to find pixel locations and replaced PixelHunter.

AutoClicker is an Auto Clicker with variables to define time between clicks, user controlled random variance, and maximum amount of clicks.

GUI3 is a template for implementing a new GUI; issues arise when importing classes and functions for reuse, as Tkinter is not exactly thread safe.

