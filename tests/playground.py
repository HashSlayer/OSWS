import os
import sys
# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root to the Python path
sys.path.insert(0, project_root)

#you can import other modules here
from utils.core.timing import *
from utils.core.welcome import *
from utils.clicker import *

welcome()
sleep()
print("hello from test.py")  

