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


def list_monitors():
    """List all available monitors."""
    with mss() as sct:
        monitors = sct.monitors[1:]  # Skip monitor[0] (all monitors combined)
        for i, monitor in enumerate(monitors, 1):
            print(f"Monitor {i}: {monitor['width']}x{monitor['height']} at ({monitor['left']}, {monitor['top']})")
        return monitors


def get_screenshot_all_monitors(device_id: str | None = None, timeout: int = 10) -> Screenshot:
    """Capture all monitors combined."""
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[0])  # All monitors
        
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


def get_screenshot(device_id: str | None = None, timeout: int = 10) -> Screenshot:
    """
    Capture desktop screen based on configured mode.
    
    Modes:
    - AUTO: Captures the screen containing the active window
    - PRIMARY: Always captures primary monitor
    - ALL: Captures all monitors combined
    - MONITOR_1/MONITOR_2: Forces specific monitor

    Args:
        device_id: Ignored for desktop (kept for API compatibility).
        timeout: Ignored for desktop (kept for API compatibility).

    Returns:
        Screenshot object with image data.
    """
    from phone_agent.desktop.config import get_screenshot_mode, ScreenshotMode
    
    mode = get_screenshot_mode()
    
    with mss() as sct:
        if mode == ScreenshotMode.ALL:
            # Capture all monitors
            screenshot = sct.grab(sct.monitors[0])
        elif mode == ScreenshotMode.PRIMARY:
            # Always use primary monitor
            screenshot = sct.grab(sct.monitors[1])
        elif mode == ScreenshotMode.MONITOR_1:
            # Force monitor 1
            screenshot = sct.grab(sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0])
        elif mode == ScreenshotMode.MONITOR_2:
            # Force monitor 2
            screenshot = sct.grab(sct.monitors[2] if len(sct.monitors) > 2 else sct.monitors[1])
        else:  # AUTO mode
            # Try to find which monitor contains the active window
            try:
                active_window = gw.getActiveWindow()
                if active_window and hasattr(active_window, 'left') and hasattr(active_window, 'top'):
                    window_x = active_window.left
                    window_y = active_window.top
                    
                    # Find which monitor contains this window
                    for i, monitor in enumerate(sct.monitors[1:], 1):  # Skip monitor[0] (all monitors)
                        if (monitor['left'] <= window_x < monitor['left'] + monitor['width'] and
                            monitor['top'] <= window_y < monitor['top'] + monitor['height']):
                            # Found the monitor containing the active window
                            screenshot = sct.grab(monitor)
                            break
                    else:
                        # Active window not found in any monitor, use all monitors
                        screenshot = sct.grab(sct.monitors[0])
                else:
                    # No active window, use all monitors
                    screenshot = sct.grab(sct.monitors[0])
            except Exception:
                # Fallback: capture all monitors combined
                screenshot = sct.grab(sct.monitors[0])
        
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
        if active_window and hasattr(active_window, 'title'):
            title = active_window.title
            if callable(title):
                title = title()
            return title or "Unknown Window"
        return "Desktop"
    except Exception:
        return "Desktop"
