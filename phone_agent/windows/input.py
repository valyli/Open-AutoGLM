"""Text input for Windows using pyautogui."""

import time

import pyautogui


def type_text(text: str, device_id: str | None = None) -> None:
    """
    Type text using keyboard.

    Args:
        text: Text to type.
        device_id: Ignored for Windows.
    """
    pyautogui.write(text, interval=0.05)
    time.sleep(0.5)


def clear_text(device_id: str | None = None) -> None:
    """
    Clear text by selecting all and deleting.

    Args:
        device_id: Ignored for Windows.
    """
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.press("delete")
    time.sleep(0.2)
