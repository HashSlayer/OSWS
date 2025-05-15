"""
Screenshot-based Inventory Calibration

This module provides functions to calibrate inventory slots based on screenshots 
of the game client with highlighted inventory slot boundaries.

Key features:
- Screenshot capture with pyautogui
- Detection of yellow square inventory slots in the bottom right quadrant
- Square detection with confidence scoring
- Automatic calculation of inventory grid parameters
- Storage of calibration data
"""

import os
import json
import numpy as np
import cv2
from PIL import Image, ImageGrab
import pyautogui
import time
import sys
import logging
import glob
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
CONFIG_DIR = os.path.join(project_root, 'config')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'inventory_config.json')
DEBUG_DIR = os.path.join(project_root, 'debug')

# Yellow color constants - specifically targeting bright yellow
# Using HSV color space which is better for color detection
# H: 20-40 (yellow hue range)
# S: 100-255 (medium to full saturation)
# V: 150-255 (medium to bright)
YELLOW_HSV_LOW = np.array([20, 100, 150], dtype=np.uint8)
YELLOW_HSV_HIGH = np.array([40, 255, 255], dtype=np.uint8)

# Alternative yellow ranges to try if primary fails
ALT_YELLOW_RANGES = [
    # Broader yellow
    (np.array([15, 70, 150], dtype=np.uint8), np.array([45, 255, 255], dtype=np.uint8)),
    # Gold/orange-yellow 
    (np.array([10, 100, 150], dtype=np.uint8), np.array([30, 255, 255], dtype=np.uint8)),
    # Very broad yellow-orange
    (np.array([10, 50, 150], dtype=np.uint8), np.array([50, 255, 255], dtype=np.uint8))
]

# Default inventory configuration - used as fallback
DEFAULT_CONFIG = {
    'base_x': 1625,
    'base_y': 638,
    'x_spacing': 61,
    'y_spacing': 51
}

def clean_debug_directory():
    """
    Clean up old debug images to prevent accumulation.
    Keeps the most recent debug session (up to 20 images).
    """
    try:
        if not os.path.exists(DEBUG_DIR):
            os.makedirs(DEBUG_DIR, exist_ok=True)
            return
            
        # Get all PNG files in debug directory
        debug_files = glob.glob(os.path.join(DEBUG_DIR, "*.png"))
        
        # If fewer than 20 files, don't clean up yet
        if len(debug_files) < 20:
            return
            
        # Sort by modification time (newest first)
        debug_files.sort(key=os.path.getmtime, reverse=True)
        
        # Keep the 10 most recent files, delete the rest
        files_to_delete = debug_files[10:]
        
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                logger.debug(f"Deleted old debug file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to delete {file_path}: {e}")
                
        logger.info(f"Cleaned up {len(files_to_delete)} old debug images")
    
    except Exception as e:
        logger.warning(f"Error cleaning debug directory: {e}")

def take_screenshot():
    """
    Take a screenshot of the entire screen.
    
    Returns:
        numpy.ndarray: Screenshot as a NumPy array in BGR format
    """
    try:
        # Clean up old debug images first
        clean_debug_directory()
        
        # Take screenshot using pyautogui
        screenshot = pyautogui.screenshot()
        
        # Convert to numpy array for OpenCV
        screenshot_np = np.array(screenshot)
        
        # Convert RGB to BGR (OpenCV format)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        logger.info(f"Screenshot captured. Shape: {screenshot_bgr.shape}")
        return screenshot_bgr
    
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        return None

def save_debug_image(image, filename):
    """Save an image for debugging purposes."""
    try:
        os.makedirs(DEBUG_DIR, exist_ok=True)
        path = os.path.join(DEBUG_DIR, filename)
        cv2.imwrite(path, image)
        logger.info(f"Saved debug image to {path}")
    except Exception as e:
        logger.error(f"Error saving debug image: {e}")

def crop_bottom_right_quadrant(image):
    """
    Crop the image to the bottom right quarter, where the inventory is typically located.
    
    Args:
        image (numpy.ndarray): Full screenshot
        
    Returns:
        numpy.ndarray: Cropped image containing only bottom right quadrant
    """
    height, width = image.shape[:2]
    # Crop to bottom right quarter
    cropped = image[height//2:, width//2:]
    return cropped

def calculate_square_confidence(contour):
    """
    Calculate how "square-like" a contour is, returning a confidence score.
    
    Args:
        contour: The contour to evaluate
        
    Returns:
        float: Confidence score from 0.0 to 1.0 (1.0 = perfect square)
    """
    # Get the bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)
    rect_area = w * h
    
    # Get contour area
    contour_area = cv2.contourArea(contour)
    
    # Perfect square would have contour area close to rectangle area
    area_ratio = contour_area / rect_area if rect_area > 0 else 0
    
    # A perfect square would have width = height
    aspect_ratio = min(w, h) / max(w, h) if max(w, h) > 0 else 0
    
    # Calculate approximation error for shape
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # A square should have 4 corners
    corners_score = 0
    if len(approx) == 4:
        corners_score = 1.0
    else:
        corners_score = 4.0 / (abs(len(approx) - 4) + 4)
    
    # Combine scores, with more weight on having 4 corners and good aspect ratio
    confidence = (0.4 * corners_score) + (0.4 * aspect_ratio) + (0.2 * area_ratio)
    
    return min(confidence, 1.0)  # Cap at 1.0

def filter_contours_by_confidence(contours, min_confidence=0.7):
    """
    Filter contours by their square confidence score.
    
    Args:
        contours: List of contours to filter
        min_confidence: Minimum confidence score threshold
        
    Returns:
        list: Filtered contours that exceed confidence threshold
    """
    result = []
    confidences = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        # Basic size filter first
        if area < 100 or area > 5000:
            continue
            
        confidence = calculate_square_confidence(contour)
        if confidence >= min_confidence:
            result.append(contour)
            confidences.append(confidence)
    
    return result, confidences

def try_detect_with_color_range(image, low, high, prefix="", min_confidence=0.7):
    """
    Try to detect inventory slots with a specific color range.
    
    Args:
        image: The screenshot image (cropped to bottom right)
        low: Lower bound of color range (HSV)
        high: Upper bound of color range (HSV)
        prefix: Prefix for debug image filenames
        min_confidence: Minimum confidence for square detection
        
    Returns:
        list: Filtered contours
    """
    # Convert image to HSV for better color detection
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask for yellow color
    mask = cv2.inRange(hsv_image, low, high)
    
    # Save mask for debugging
    save_debug_image(mask, f"{prefix}mask.png")
    
    # Try to enhance the mask with morphological operations
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Close small holes
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Remove small noise
    
    # Additional dilation to connect nearby pixels
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    # Save enhanced mask
    save_debug_image(mask, f"{prefix}enhanced_mask.png")
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by confidence
    inventory_contours, confidences = filter_contours_by_confidence(contours, min_confidence)
    
    # Draw contours on a blank image for debugging
    debug_image = np.zeros_like(image)
    for i, contour in enumerate(inventory_contours):
        # Color intensity based on confidence
        color_intensity = int(255 * confidences[i]) if i < len(confidences) else 255
        cv2.drawContours(debug_image, [contour], -1, (0, color_intensity, 0), 2)
    save_debug_image(debug_image, f"{prefix}contours.png")
    
    # Also draw contours on the original image for better visualization
    original_with_contours = image.copy()
    for i, contour in enumerate(inventory_contours):
        # Color intensity based on confidence
        color_intensity = int(255 * confidences[i]) if i < len(confidences) else 255
        cv2.drawContours(original_with_contours, [contour], -1, (0, color_intensity, 0), 2)
        
        # Add confidence text
        if i < len(confidences):
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.putText(original_with_contours, f"{confidences[i]:.2f}", 
                           (cx-20, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    save_debug_image(original_with_contours, f"{prefix}original_with_contours.png")
    
    logger.info(f"Found {len(inventory_contours)} possible inventory slots with {prefix}color range")
    
    return inventory_contours, confidences

def detect_inventory_slots(image):
    """
    Detect inventory slots in a screenshot.
    
    Args:
        image (numpy.ndarray): Screenshot as a NumPy array in BGR format
        
    Returns:
        dict: Inventory slot information if successful, None otherwise
    """
    try:
        # Save a copy of the original full image for comparison
        save_debug_image(image, "original_full.png")
        
        # Crop to bottom right quadrant where inventory is located
        cropped_image = crop_bottom_right_quadrant(image)
        save_debug_image(cropped_image, "original_cropped.png")
        
        # Try main yellow color range first
        inventory_contours, confidences = try_detect_with_color_range(
            cropped_image, YELLOW_HSV_LOW, YELLOW_HSV_HIGH
        )
        
        # If not enough contours found, try alternative color ranges
        if len(inventory_contours) < 8:  # We expect to find at least 8 slots
            logger.warning(f"Found only {len(inventory_contours)} possible inventory slots. "
                           f"Expected at least 8. Trying alternative color ranges...")
            
            for i, (low, high) in enumerate(ALT_YELLOW_RANGES):
                alt_contours, alt_conf = try_detect_with_color_range(
                    cropped_image, low, high, f"alt{i+1}_"
                )
                
                # If this range found more contours, use it instead
                if len(alt_contours) > len(inventory_contours):
                    inventory_contours = alt_contours
                    confidences = alt_conf
                
                # If we found enough contours, stop trying
                if len(inventory_contours) >= 8:
                    break
        
        # If still not enough contours, we'll try with decreasing confidence threshold
        if len(inventory_contours) < 8:
            logger.warning("Trying with lower confidence threshold...")
            for confidence_threshold in [0.6, 0.5, 0.4]:
                inventory_contours, confidences = try_detect_with_color_range(
                    cropped_image, YELLOW_HSV_LOW, YELLOW_HSV_HIGH, 
                    f"low_conf{confidence_threshold}_", min_confidence=confidence_threshold
                )
                if len(inventory_contours) >= 8:
                    break
        
        # If still not enough contours, use default values
        if len(inventory_contours) < 8:
            logger.warning("Unable to detect sufficient inventory slots. Using default values.")
            
            # Return default values
            return {
                'base_x': DEFAULT_CONFIG['base_x'],
                'base_y': DEFAULT_CONFIG['base_y'],
                'x_spacing': DEFAULT_CONFIG['x_spacing'],
                'y_spacing': DEFAULT_CONFIG['y_spacing'],
                'num_detected_slots': 0,
                'using_defaults': True
            }
            
        # Calculate center points of each contour
        centers = []
        for contour in inventory_contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # Adjust coordinates relative to full image
                centers.append((cx + image.shape[1]//2, cy + image.shape[0]//2))
        
        # We need to sort the centers to organize them into a grid
        # First, sort roughly by y-coordinate (with some tolerance for slight misalignments)
        y_tolerance = 25  # Pixels - Points within this distance are considered same row
        
        # Group points by rows
        rows = []
        centers_copy = centers.copy()
        
        while centers_copy:
            # Take the first point as reference
            ref_point = centers_copy[0]
            row_points = [ref_point]
            centers_copy.remove(ref_point)
            
            # Find all points in the same row
            i = 0
            while i < len(centers_copy):
                if abs(centers_copy[i][1] - ref_point[1]) < y_tolerance:
                    row_points.append(centers_copy[i])
                    centers_copy.pop(i)
                else:
                    i += 1
            
            # Sort the row points by x-coordinate
            row_points.sort(key=lambda p: p[0])
            rows.append(row_points)
        
        # Sort rows by average y-coordinate
        rows.sort(key=lambda row: sum(p[1] for p in row) / len(row))
        
        # Calculate spacings
        x_spacings = []
        y_spacings = []
        
        # Horizontal spacing within rows
        for row in rows:
            if len(row) >= 2:
                for i in range(1, len(row)):
                    x_spacings.append(row[i][0] - row[i-1][0])
        
        # Vertical spacing between rows
        if len(rows) >= 2:
            for i in range(1, len(rows)):
                if len(rows[i]) > 0 and len(rows[i-1]) > 0:
                    # Calculate based on leftmost point in each row
                    leftmost_curr = min(rows[i], key=lambda p: p[0])
                    leftmost_prev = min(rows[i-1], key=lambda p: p[0])
                    y_spacings.append(leftmost_curr[1] - leftmost_prev[1])
        
        # Ensure we have valid spacings
        if not x_spacings or not y_spacings:
            logger.warning("Could not calculate valid spacings between inventory slots. Using defaults.")
            return {
                'base_x': DEFAULT_CONFIG['base_x'],
                'base_y': DEFAULT_CONFIG['base_y'],
                'x_spacing': DEFAULT_CONFIG['x_spacing'],
                'y_spacing': DEFAULT_CONFIG['y_spacing'],
                'num_detected_slots': len(inventory_contours),
                'using_defaults': True
            }
        
        # Filter out extreme outliers in spacings (values more than 2x the median)
        x_spacings.sort()
        y_spacings.sort()
        
        # Get median values for x and y spacings
        median_x = x_spacings[len(x_spacings) // 2]
        median_y = y_spacings[len(y_spacings) // 2]
        
        # Filter spacings that are reasonably close to the median
        filtered_x_spacings = [x for x in x_spacings if 0.5 * median_x <= x <= 2.0 * median_x]
        filtered_y_spacings = [y for y in y_spacings if 0.5 * median_y <= y <= 2.0 * median_y]
        
        # Calculate average spacings from filtered values
        if filtered_x_spacings and filtered_y_spacings:
            avg_x_spacing = sum(filtered_x_spacings) // len(filtered_x_spacings)
            avg_y_spacing = sum(filtered_y_spacings) // len(filtered_y_spacings)
        else:
            # Use unfiltered if filtering removed all values
            avg_x_spacing = sum(x_spacings) // len(x_spacings)
            avg_y_spacing = sum(y_spacings) // len(y_spacings)
        
        # Validate spacings with typical ranges for inventory slots
        if avg_x_spacing < 30 or avg_x_spacing > 100 or avg_y_spacing < 30 or avg_y_spacing > 100:
            logger.warning(f"Calculated spacings are suspicious: x={avg_x_spacing}, y={avg_y_spacing}. Using defaults.")
            return {
                'base_x': DEFAULT_CONFIG['base_x'],
                'base_y': DEFAULT_CONFIG['base_y'],
                'x_spacing': DEFAULT_CONFIG['x_spacing'],
                'y_spacing': DEFAULT_CONFIG['y_spacing'],
                'num_detected_slots': len(inventory_contours),
                'using_defaults': True
            }
        
        # Find the top-left slot as base point (should be the first element of the first row)
        if rows and rows[0]:
            base_x, base_y = rows[0][0]
            
            # Visualize results
            result_image = image.copy()
            # Draw grid lines for the inventory
            for i in range(7):  # 7 rows
                for j in range(4):  # 4 columns
                    x = base_x + j * avg_x_spacing
                    y = base_y + i * avg_y_spacing
                    cv2.circle(result_image, (x, y), 5, (0, 255, 0), -1)  # Green dot at slot center
                    # Draw rectangle around slot
                    rect_x = x - avg_x_spacing // 2
                    rect_y = y - avg_y_spacing // 2
                    cv2.rectangle(result_image, (rect_x, rect_y), 
                                  (rect_x + avg_x_spacing, rect_y + avg_y_spacing), 
                                  (0, 0, 255), 2)
            
            save_debug_image(result_image, "detected_grid.png")
            
            # Return the calculated calibration data
            return {
                'base_x': base_x,
                'base_y': base_y,
                'x_spacing': avg_x_spacing,
                'y_spacing': avg_y_spacing,
                'num_detected_slots': len(inventory_contours)
            }
        else:
            logger.warning("Could not identify a valid top-left inventory slot. Using defaults.")
            return {
                'base_x': DEFAULT_CONFIG['base_x'],
                'base_y': DEFAULT_CONFIG['base_y'],
                'x_spacing': DEFAULT_CONFIG['x_spacing'],
                'y_spacing': DEFAULT_CONFIG['y_spacing'],
                'num_detected_slots': len(inventory_contours),
                'using_defaults': True
            }
            
    except Exception as e:
        logger.error(f"Error detecting inventory slots: {e}")
        import traceback
        traceback.print_exc()
        return {
            'base_x': DEFAULT_CONFIG['base_x'],
            'base_y': DEFAULT_CONFIG['base_y'],
            'x_spacing': DEFAULT_CONFIG['x_spacing'],
            'y_spacing': DEFAULT_CONFIG['y_spacing'],
            'num_detected_slots': 0,
            'using_defaults': True,
            'error': str(e)
        }

def save_calibration(calibration_data):
    """
    Save calibration data to the config file.
    
    Args:
        calibration_data (dict): Calibration data to save
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Extract just the calibration parameters (not metadata like 'using_defaults')
        config_to_save = {
            'base_x': calibration_data['base_x'],
            'base_y': calibration_data['base_y'],
            'x_spacing': calibration_data['x_spacing'],
            'y_spacing': calibration_data['y_spacing']
        }
        
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_to_save, f, indent=4)
            
        logger.info(f"Calibration data saved to {CONFIG_FILE}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving calibration data: {e}")
        return False

def calibrate_inventory():
    """
    Perform inventory calibration using a screenshot.
    
    This function:
    1. Takes a screenshot
    2. Detects inventory slots
    3. Calculates calibration data
    4. Saves the data to config file
    
    Returns:
        dict: Calibration data if successful, None otherwise
    """
    logger.info("Starting inventory calibration via screenshot...")
    
    # Take screenshot
    logger.info("Taking screenshot in 3 seconds. Make sure inventory is visible with yellow slots...")
    time.sleep(3)
    screenshot = take_screenshot()
    
    if screenshot is None:
        logger.error("Failed to take screenshot.")
        return None
    
    # Save screenshot for debugging
    save_debug_image(screenshot, "screenshot.png")
    
    # Detect inventory slots
    calibration_data = detect_inventory_slots(screenshot)
    
    if calibration_data is None:
        logger.error("Failed to detect inventory slots.")
        return None
    
    # Save calibration data
    if not save_calibration(calibration_data):
        logger.error("Failed to save calibration data.")
        return None
    
    # Display appropriate message based on detection results
    if calibration_data.get('using_defaults', False):
        logger.info("Unable to auto-detect inventory slots. Using default values:")
    else:
        logger.info(f"Inventory calibration successful. Detected {calibration_data['num_detected_slots']} slots.")
    
    logger.info(f"Base coordinates: ({calibration_data['base_x']}, {calibration_data['base_y']})")
    logger.info(f"Spacing: {calibration_data['x_spacing']}px horizontal, {calibration_data['y_spacing']}px vertical")
    
    return calibration_data 