"""Desktop configuration settings."""

import os
from enum import Enum


class ScreenshotMode(Enum):
    """Screenshot capture modes for multi-monitor setups."""
    
    AUTO = "auto"  # Automatically detect active window's monitor
    PRIMARY = "primary"  # Always use primary monitor
    ALL = "all"  # Capture all monitors combined
    MONITOR_1 = "monitor_1"  # Force monitor 1
    MONITOR_2 = "monitor_2"  # Force monitor 2


# Default screenshot mode
DEFAULT_SCREENSHOT_MODE = ScreenshotMode.AUTO

# Environment variable to override screenshot mode
SCREENSHOT_MODE = os.getenv("PHONE_AGENT_SCREENSHOT_MODE", DEFAULT_SCREENSHOT_MODE.value)

# Convert string to enum
try:
    SCREENSHOT_MODE = ScreenshotMode(SCREENSHOT_MODE)
except ValueError:
    SCREENSHOT_MODE = DEFAULT_SCREENSHOT_MODE


def get_screenshot_mode() -> ScreenshotMode:
    """Get current screenshot mode."""
    return SCREENSHOT_MODE


def set_screenshot_mode(mode: ScreenshotMode):
    """Set screenshot mode."""
    global SCREENSHOT_MODE
    SCREENSHOT_MODE = mode