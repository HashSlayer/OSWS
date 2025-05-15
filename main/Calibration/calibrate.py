#!/usr/bin/env python
"""
Inventory Calibration Tools Launcher

This script provides access to different inventory calibration methods.
You can choose between manual calibration or screenshot-based calibration.

Usage:
  python main/calibration/calibrate.py [--method METHOD]

Options:
  --method METHOD    Calibration method to use: 'visual' or 'screenshot' (default: visual)
"""

import os
import sys
import argparse

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Inventory Calibration Tools")
    parser.add_argument(
        "--method", 
        choices=["visual", "screenshot"], 
        default="visual",
        help="Calibration method to use: 'visual' or 'screenshot'"
    )
    args = parser.parse_args()
    
    # Display information about the calibration
    print("\nOSWS Inventory Calibration Tool")
    print("==============================")
    print("This tool helps calibrate the inventory slot positions.")
    
    # Launch the selected calibrator
    if args.method == "visual":
        print("\nLaunching Manual Calibration Tool...")
        import main.Calibration.manual.manual_calibrator as visual_calibrator
        visual_calibrator.main()
    else:
        print("\nLaunching Screenshot-based Calibration Tool...")
        # Use dedicated launcher script
        from main.Calibration.screenshot import main as screenshot_main
        screenshot_main()

if __name__ == "__main__":
    main() 