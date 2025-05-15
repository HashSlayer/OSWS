#!/usr/bin/env python
"""
Calibration Test Runner

This script provides easy access to all inventory calibration tests.

Usage:
  python tests/calibration/run-tests.py
"""

import os
import sys
import argparse

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

def main():
    """Run the calibration tests."""
    print("\nOSWS Calibration Test Runner")
    print("============================")
    print("\nAvailable tests:")
    print("1. Screenshot-based Calibration Test")
    print("2. Exit")
    
    choice = input("\nEnter your choice (1-2): ")
    
    if choice == "1":
        print("\nRunning Screenshot Calibration Test...")
        # Import and run the screenshot test
        import tests.calibration.test_screenshot_calibration as screenshot_test
        screenshot_test.main()
    else:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main() 