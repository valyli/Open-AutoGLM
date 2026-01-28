"""Screenshot capture for desktop using mss (cross-platform)."""

import base64
import io
from dataclasses import dataclass

import pygetwindow as gw
from mss import mss
from PIL import Image


@dataclass
class Screenshot:
    """Screenshot data container."""

    width: int
    height: int
    base64_data: str


def get_screenshot(device_id: str | None = None, timeout: int = 10) -> Screenshot:
    """
    Capture desktop screen.

    Args:
        device_id: Ignored for desktop (kept for API compatibility).
        timeout: Ignored for desktop (kept for API compatibility).

    Returns:
        Screenshot object with image data.
    """
    with mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return Screenshot(
            width=img.width,
            height=img.height,
            base64_data=base64_data,
        )


def get_current_app(device_id: str | None = None) -> str:
    """
    Get the currently active window title.

    Args:
        device_id: Ignored for desktop (kept for API compatibility).

    Returns:
        Active window title or "Desktop" if none.
    """
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title or "Unknown Window"
        return "Desktop"
    except Exception:
        return "Desktop"
