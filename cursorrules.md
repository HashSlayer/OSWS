# OSWS Cursor Rules

This document outlines best practices and guidelines for developing effective, modular, and human-like automation scripts for the Open Source Workspace Suite (OSWS).

## Core Principles

1. **Human-Like Behavior**: All automation should mimic natural human behavior as closely as possible
2. **Modularity**: Use and extend the utility modules for consistent, maintainable code
3. **Randomization**: Always incorporate appropriate variability in timing, movements, and actions
4. **Performance**: Balance realism with efficient execution
5. **Educational Value**: Write code that teaches programming concepts clearly

## Mouse Movement Guidelines

### Use Bezier Curves for Mouse Movement
- Always use `bezierMove()`, 'bezierBetween()' or similar functions from `utils/movements.py`
- Never use direct linear movements (`pag.moveTo()`) without human-like curves
- Never use mouse.click
- Add small random perturbations to paths and try to make movements human like.

```python
# Good practice
from utils.movements import bezierMove
bezierMove(x, y, duration=0.3)  # Uses natural curve with randomness

# Avoid
import pyautogui as pag
pag.moveTo(x, y)  # Too linear and robotic
```

### Incorporate Random Pauses
- Use sleep functions from `utils/timmy.py` rather than direct `time.sleep()`
- Always consider optimizations to the utilities files.
- Add occasional sleep_if() calls for unpredictable pauses

```python
# Good practice
from utils.timmy import sleep, sleep_if
sleep()  # Random medium pause
if random.random() > 0.7:
    sleep_if()  # Occasional extra pause

# Avoid
import time
time.sleep(0.5)  # Fixed timing is detectable
```

### Click Patterns
- Use varied click durations with `utils/clicker.py` functions
- Mix single and double clicks appropriately
- Add occasional right-clicks when contextually appropriate
- Randomize "hold" times for mouse buttons

```python
# Good practice
from utils.clicker import click, right_click
click(hold=rnd.random() * 0.1 + 0.05, randomize=True)

# Avoid
import pyautogui as pag
pag.click()  # Too consistent/predictable
```

## Script Structure Guidelines

### Modular Organization
- Break functionality into reusable components
- Use clear function and variable names that reflect their purpose
- Keep scripts clear and concise, avoid exceeding 600 lines for any files unless needed.

### Error Handling
- Add basic error detection and recovery
- Implement stop conditions (keyboard interrupts)
- Log operations for debugging

```python
# Good practice
try:
    # Main operation
    if keyboard_interrupt_detected():
        safe_shutdown()
except Exception as e:
    log_error(e)
    safe_shutdown()
```

## Algorithm Optimization

### Balance Speed and Realism
- Focus on algorithms that balance efficiency with human-like behavior
- Incorporate occasional pauses and corrections in situations that are fitting and wont disrupt any necessary timed pauses.



```python
# Good practice - Variable timing between operations
interval = base_interval + random.random() * variance
time.sleep(interval)

# Avoid - Fixed intervals
time.sleep(1)  # Every second is too predictable
```

## Testing and Verification

### Visual Verification
- Test scripts with visual tracking enabled
- Verify that movements appear natural to human observers

### Metrics Collection

- Compare action distributions to actual human baselines
- Adjust randomization parameters occasionally

## Documentation Standards

### Code Comments
- Document the purpose of each function
- Explain non-obvious randomization techniques
- Note any specific anti-detection measures

### Script Headers
- Include a clear description of the script's purpose
- List dependencies and required Python version
- Document any configuration parameters

Remember you are still refining the utilities files and underlying foundation. Some rules or comments are subject to change.

