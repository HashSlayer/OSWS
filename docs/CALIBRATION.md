# Inventory Calibration System

This document describes the inventory calibration system for the OSWS framework.

## Overview

The OSWS framework provides two methods for calibrating inventory slot positions:

1. **Manual Calibration**: A visual overlay that can be positioned over the inventory.
2. **Screenshot Calibration**: Automatic detection of inventory slots from a screenshot.

Both methods ultimately calculate the same parameters:
- Base coordinates (`base_x`, `base_y`) - The position of the first inventory slot
- Spacing (`x_spacing`, `y_spacing`) - The distance between slots horizontally and vertically

## Directory Structure

```
OSWS/
├── main/
│   └── calibration/                  # Calibration launchers
│       ├── calibrate.py              # Main launcher for both methods
│       └── screenshot.py             # Screenshot calibration launcher
│   └── Calibration/                  # Calibration implementations
│       ├── manual/                   # Manual calibration tools
│       │   └── manual_calibrator.py  # Visual overlay calibrator
│       └── color/                    # Color/screenshot calibration tools
│           └── screenshot_calibrator.py # Screenshot detection GUI
├── tests/
│   └── calibration/                  # Calibration test tools
│       ├── run-tests.py              # Test launcher
│       └── test_screenshot_calibration.py # Screenshot test
└── utils/
    ├── item_slots.py                 # Uses calibration data
    └── calibration/                  # Calibration utilities
        ├── config.py                 # Configuration management
        └── vision/                   # Computer vision utilities
            └── screenshot.py         # Screenshot detection functions
```

## Configuration

The calibration parameters are stored in `config/inventory_config.json` and are used by various utilities to ensure consistent inventory interactions:

```json
{
  "base_x": 1625,
  "base_y": 638,
  "x_spacing": 61,
  "y_spacing": 51
}
```

## Usage

### Manual Calibration

```bash
python main/calibration/calibrate.py --method visual
```

### Screenshot Calibration

```bash
python main/calibration/screenshot.py
```

### Testing Calibration

```bash
python tests/calibration/run-tests.py
```

## Utility Functions

The system provides various utilities for managing calibration:

### Configuration Management

```python
from utils.calibration.config import load_inventory_config, save_inventory_config, reset_inventory_config

# Load the current inventory configuration
config = load_inventory_config()

# Save a new configuration
save_inventory_config(new_config)

# Reset to default configuration
reset_inventory_config()
```

### Screenshot Detection

```python
from utils.calibration.vision import take_screenshot, detect_inventory_slots

# Take a screenshot
screenshot = take_screenshot()

# Detect inventory slots in the screenshot
results = detect_inventory_slots(screenshot)
```

## How It Works

### Manual Calibration

1. Displays a transparent, movable overlay on the screen
2. User positions it over their inventory
3. User clicks on inventory slots to calibrate
4. Saves configuration based on the overlay position

### Screenshot Calibration

1. Takes a screenshot when the user presses LEFT CTRL
2. Automatically detects orange-highlighted inventory slots
3. Calculates grid parameters from the detected slots
4. Shows detected coordinates for review before saving
5. Allows reverting to default values if needed

## Default Values

If no calibration has been performed, the system falls back to these default values:

```json
{
  "base_x": 1625,
  "base_y": 638,
  "x_spacing": 61,
  "y_spacing": 51
}
```

These values work well for 1920x1080 resolution with 45% RuneLite scaling. 