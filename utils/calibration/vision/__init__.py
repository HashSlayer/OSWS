"""
Vision-based Calibration Utilities

This subpackage contains utilities for calibrating aspects of 
OSWS bots using computer vision techniques.
"""

__all__ = ["screenshot"]

# Import important utilities for easier access
from .screenshot import (
    take_screenshot, 
    detect_inventory_slots, 
    save_calibration,
    calibrate_inventory,
    save_debug_image
) 