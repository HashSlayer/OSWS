"""
Key timing utilities for human-like key press simulation.
Implements sophisticated timing patterns based on key context and usage patterns.
"""

import random as rnd
import numpy as np
from typing import Tuple, Optional
from .timing import sleep

def calculate_key_duration(
    base_duration: float,
    context: str = "neutral",
    skill_level: str = "average",
    fatigue_factor: float = 0.0
) -> Tuple[float, float, float]:
    """
    Calculate key press duration parameters based on context and conditions.
    
    Args:
        base_duration: Base duration for the key press in seconds
        context: Key press context ("combat", "movement", "inventory", "neutral")
        skill_level: Simulated skill level ("beginner", "average", "expert")
        fatigue_factor: 0.0-1.0 representing simulated fatigue level
        
    Returns:
        Tuple of (base_time, variance, micro_variance)
    """
    # Context multipliers
    context_multipliers = {
        "combat": 0.8,      # Faster in combat
        "movement": 1.0,    # Normal for movement
        "inventory": 1.2,   # Slightly slower for inventory
        "neutral": 1.0      # Default
    }
    
    # Skill level variance adjustments
    skill_variances = {
        "beginner": (0.3, 0.15),    # Higher variance
        "average": (0.2, 0.1),      # Medium variance
        "expert": (0.1, 0.05)       # Low variance
    }
    
    # Apply context multiplier
    adjusted_base = base_duration * context_multipliers.get(context, 1.0)
    
    # Get variance based on skill
    variance_main, variance_micro = skill_variances.get(skill_level, (0.2, 0.1))
    
    # Apply fatigue factor (increases both base time and variance)
    fatigue_multiplier = 1.0 + (fatigue_factor * 0.5)
    adjusted_base *= fatigue_multiplier
    variance_main *= fatigue_multiplier
    
    return (adjusted_base, variance_main, variance_micro)

def get_hold_duration(
    key_type: str,
    base_duration: float,
    context: str = "neutral",
    randomize: bool = True
) -> float:
    """
    Calculate total hold duration for a key press with natural variance.
    
    Args:
        key_type: Type of key ("action", "movement", "inventory", "modifier")
        base_duration: Base duration for the key press
        context: Usage context
        randomize: Whether to add randomization
    
    Returns:
        Final hold duration in seconds
    """
    if not randomize:
        return base_duration
        
    # Get base parameters
    base, var_main, var_micro = calculate_key_duration(base_duration, context)
    
    # Calculate hold time with primary variance
    hold_time = base + (rnd.random() * var_main) - (var_main / 2)
    
    # Add micro-variance
    hold_time += (rnd.random() * var_micro) - (var_micro / 2)
    
    # Key-specific adjustments
    if key_type == "action":
        # Action keys can have occasional longer holds
        if rnd.random() > 0.8:
            hold_time *= 1.5
    elif key_type == "movement":
        # Movement keys commonly have extended holds
        if rnd.random() > 0.3:
            hold_time *= 2.0
    elif key_type == "inventory":
        # Inventory keys are usually quick
        hold_time *= 0.8
    elif key_type == "modifier":
        # Modifier keys have more consistent timing
        hold_time = base + (rnd.random() * var_micro)
    
    return max(0.01, hold_time)  # Ensure minimum duration

def get_sequence_delay(
    prev_key: Optional[str] = None,
    next_key: Optional[str] = None,
    base_delay: float = 0.05
) -> float:
    """
    Calculate natural delay between key presses in a sequence.
    
    Args:
        prev_key: Previous key in sequence (if any)
        next_key: Next key in sequence (if any)
        base_delay: Base delay between keys
        
    Returns:
        Delay duration in seconds
    """
    delay = base_delay
    
    # Adjust for key combinations
    if prev_key and next_key:
        # Common combinations get faster timing
        common_combos = [
            ('left_ctrl', '1'),
            ('left_ctrl', '2'),
            ('shift', 'space')
        ]
        if (prev_key, next_key) in common_combos:
            delay *= 0.7
            
        # Awkward combinations get slower timing
        awkward_combos = [
            ('1', '9'),
            ('left_ctrl', '0')
        ]
        if (prev_key, next_key) in awkward_combos:
            delay *= 1.3
    
    # Add natural variance
    delay += (rnd.random() * 0.02) - 0.01
    
    return max(0.01, delay)  # Ensure minimum delay 