"""
Calibration Configuration Utilities

This module provides functions for managing calibration configurations
across the OSWS framework.
"""

import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
CONFIG_DIR = os.path.join(project_root, 'config')

# Inventory configuration
INVENTORY_CONFIG_FILE = os.path.join(CONFIG_DIR, 'inventory_config.json')
DEFAULT_INVENTORY_CONFIG = {
    'base_x': 1625,
    'base_y': 638,
    'x_spacing': 61,
    'y_spacing': 51
}

def load_config(config_file, default_config=None):
    """
    Load a configuration file, or return defaults if it doesn't exist.
    
    Args:
        config_file (str): Path to the config file
        default_config (dict, optional): Default configuration to use if file doesn't exist
        
    Returns:
        dict: The loaded configuration or default values
    """
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                
                # If default_config provided, use it to validate required keys
                if default_config:
                    # Verify all required keys are present
                    if all(key in config for key in default_config.keys()):
                        return config
                    else:
                        logger.warning(f"Config file {config_file} missing required keys. Using defaults.")
                else:
                    return config
    except Exception as e:
        logger.error(f"Error loading config from {config_file}: {e}")
    
    # Return default config if provided, otherwise empty dict
    return default_config if default_config else {}

def save_config(config_data, config_file):
    """
    Save configuration data to a file.
    
    Args:
        config_data (dict): Configuration data to save
        config_file (str): Path to the config file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
            
        logger.info(f"Configuration saved to {config_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving configuration to {config_file}: {e}")
        return False

def load_inventory_config():
    """
    Load inventory configuration.
    
    Returns:
        dict: Inventory configuration
    """
    return load_config(INVENTORY_CONFIG_FILE, DEFAULT_INVENTORY_CONFIG)

def save_inventory_config(config_data):
    """
    Save inventory configuration.
    
    Args:
        config_data (dict): Inventory configuration to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    return save_config(config_data, INVENTORY_CONFIG_FILE)

def reset_inventory_config():
    """
    Reset inventory configuration to default values.
    
    Returns:
        bool: True if successful, False otherwise
    """
    return save_inventory_config(DEFAULT_INVENTORY_CONFIG)

# For testing
if __name__ == "__main__":
    print("Calibration Configuration Utilities")
    print("---------------------------------")
    print(f"Default inventory config: {DEFAULT_INVENTORY_CONFIG}")
    print(f"Current inventory config: {load_inventory_config()}") 