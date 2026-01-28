"""Windows automation module for controlling Windows desktop applications."""

from phone_agent.windows.connection import WindowsConnection, list_devices
from phone_agent.windows.device import (
    back,
    double_tap,
    home,
    launch_app,
    long_press,
    swipe,
    tap,
)
from phone_agent.windows.input import clear_text, type_text
from phone_agent.windows.screenshot import get_current_app, get_screenshot

__all__ = [
    "WindowsConnection",
    "list_devices",
    "get_screenshot",
    "get_current_app",
    "tap",
    "double_tap",
    "long_press",
    "swipe",
    "back",
    "home",
    "launch_app",
    "type_text",
    "clear_text",
]


# Dummy functions for compatibility with device_factory
def detect_and_set_adb_keyboard(device_id=None):
    """Dummy function for compatibility - Windows doesn't need keyboard setup."""
    return "native"


def restore_keyboard(ime, device_id=None):
    """Dummy function for compatibility - Windows doesn't need keyboard restore."""
    pass
