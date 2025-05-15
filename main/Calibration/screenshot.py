#!/usr/bin/env python
"""
Screenshot-based Inventory Calibration Tool

This tool allows you to calibrate inventory slots using a screenshot approach.
It automatically detects the orange highlighted borders around inventory slots.

Features:
- Takes a screenshot when you press LEFT CTRL
- Detects inventory slots with orange highlights (#FFFF6A00)
- Calculates the grid parameters automatically
- Shows detected coordinates for review before saving
- Allows reverting to default values if needed

Usage:
  python main/calibration/screenshot.py

Instructions:
1. Make sure your inventory is open in the game
2. Ensure inventory slots are highlighted (click on an item to show orange borders)
3. Press LEFT CTRL key to capture a screenshot
4. Review the detected coordinates
5. Click 'Save New Configuration' if they look correct
"""

import os
import sys

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

def main():
    """Launch the screenshot-based inventory calibration tool."""
    print("\nScreenshot-based Inventory Calibration Tool")
    print("========================================")
    print("Instructions:")
    print("1. Make sure your inventory is open in the game")
    print("2. Ensure inventory slots are highlighted (click on an item to show orange borders)")
    print("3. Press LEFT CTRL key to capture a screenshot")
    print("4. Review the detected coordinates")
    print("5. Click 'Save New Configuration' if they look correct")
    print("6. Use 'Revert to Defaults' if needed")
    
    # Import the calibrator components we need
    from main.Calibration.color.screenshot_calibrator import main as run_calibrator
    run_calibrator()

if __name__ == "__main__":
    main() 