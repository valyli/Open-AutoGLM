#!/usr/bin/env python3
"""Test script for desktop module functionality."""

import sys


def test_imports():
    """Test if all desktop modules can be imported."""
    print("Testing desktop module imports...")
    try:
        from phone_agent.desktop import (
            DesktopConnection,
            get_screenshot,
            get_current_app,
            tap,
            type_text,
            list_devices,
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\nPlease install desktop dependencies:")
        print("  pip install -r requirements_desktop.txt")
        return False


def test_screenshot():
    """Test screenshot capture."""
    print("\nTesting screenshot capture...")
    try:
        from phone_agent.desktop import get_screenshot
        
        screenshot = get_screenshot()
        print(f"✅ Screenshot captured: {screenshot.width}x{screenshot.height}")
        return True
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
        return False


def test_current_app():
    """Test getting current app."""
    print("\nTesting current app detection...")
    try:
        from phone_agent.desktop import get_current_app
        
        app = get_current_app()
        print(f"✅ Current app: {app}")
        return True
    except Exception as e:
        print(f"❌ Current app detection failed: {e}")
        return False


def test_device_list():
    """Test device listing."""
    print("\nTesting device listing...")
    try:
        from phone_agent.desktop import list_devices
        
        devices = list_devices()
        print(f"✅ Found {len(devices)} device(s)")
        for device in devices:
            print(f"   - {device.device_id}: {device.model}")
        return True
    except Exception as e:
        print(f"❌ Device listing failed: {e}")
        return False


def test_device_factory():
    """Test DeviceFactory integration."""
    print("\nTesting DeviceFactory integration...")
    try:
        from phone_agent.device_factory import DeviceType, set_device_type, get_device_factory
        
        set_device_type(DeviceType.DESKTOP)
        factory = get_device_factory()
        
        screenshot = factory.get_screenshot()
        app = factory.get_current_app()
        
        print(f"✅ DeviceFactory works: {screenshot.width}x{screenshot.height}, app={app}")
        return True
    except Exception as e:
        print(f"❌ DeviceFactory test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Desktop Module Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_screenshot,
        test_current_app,
        test_device_list,
        test_device_factory,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
