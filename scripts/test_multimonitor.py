#!/usr/bin/env python3
"""Multi-monitor test script for desktop automation."""

import sys
from phone_agent.desktop.screenshot import list_monitors
from phone_agent.desktop.config import set_screenshot_mode, ScreenshotMode
from phone_agent.desktop import get_screenshot, get_current_app, launch_app


def test_monitors():
    """Test monitor detection."""
    print("=== 屏幕检测 ===")
    monitors = list_monitors()
    return len(monitors)


def test_screenshot_modes():
    """Test different screenshot modes."""
    print("\n=== 截图模式测试 ===")
    
    modes = [
        (ScreenshotMode.AUTO, "自动模式（检测活动窗口）"),
        (ScreenshotMode.PRIMARY, "主屏模式"),
        (ScreenshotMode.ALL, "全屏模式（所有屏幕）"),
        (ScreenshotMode.MONITOR_1, "屏幕1"),
        (ScreenshotMode.MONITOR_2, "屏幕2"),
    ]
    
    for mode, description in modes:
        try:
            set_screenshot_mode(mode)
            screenshot = get_screenshot()
            print(f"✅ {description}: {screenshot.width}x{screenshot.height}")
        except Exception as e:
            print(f"❌ {description}: {e}")


def test_app_launch():
    """Test app launching."""
    print("\n=== 应用启动测试 ===")
    
    # Test Calculator launch
    print("启动计算器...", end=" ")
    if launch_app("计算器"):
        print("✅ 成功")
        
        # Wait a moment and check current app
        import time
        time.sleep(2)
        current = get_current_app()
        print(f"当前应用: {current}")
    else:
        print("❌ 失败")


def test_multi_monitor_scenario():
    """Test multi-monitor scenario."""
    print("\n=== 多屏幕场景测试 ===")
    
    # Launch an app
    print("1. 启动应用...")
    launch_app("TextEdit")
    
    import time
    time.sleep(2)
    
    # Test auto mode (should detect the app's screen)
    print("2. 测试自动检测模式...")
    set_screenshot_mode(ScreenshotMode.AUTO)
    screenshot = get_screenshot()
    current_app = get_current_app()
    
    print(f"   当前应用: {current_app}")
    print(f"   自动截图: {screenshot.width}x{screenshot.height}")
    
    # Compare with all screens
    print("3. 对比全屏截图...")
    set_screenshot_mode(ScreenshotMode.ALL)
    full_screenshot = get_screenshot()
    print(f"   全屏截图: {full_screenshot.width}x{full_screenshot.height}")
    
    if screenshot.width != full_screenshot.width or screenshot.height != full_screenshot.height:
        print("   ✅ 自动模式成功检测到活动窗口所在屏幕")
    else:
        print("   ℹ️  活动窗口可能跨越多个屏幕或在主屏幕上")


def main():
    """Main test function."""
    print("桌面多屏幕功能测试")
    print("=" * 50)
    
    # Test monitor detection
    monitor_count = test_monitors()
    
    if monitor_count < 2:
        print(f"\n⚠️  检测到 {monitor_count} 个屏幕，多屏幕功能可能无法完全测试")
    else:
        print(f"\n✅ 检测到 {monitor_count} 个屏幕，可以进行完整测试")
    
    # Test screenshot modes
    test_screenshot_modes()
    
    # Test app launch
    test_app_launch()
    
    # Test multi-monitor scenario
    if monitor_count >= 2:
        test_multi_monitor_scenario()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    
    print("\n使用建议：")
    if monitor_count >= 2:
        print("• 对于多屏幕环境，推荐使用 --screenshot-mode all 确保覆盖所有屏幕")
        print("• 如果应用总是在特定屏幕，可以使用 --screenshot-mode monitor_1 或 monitor_2")
    print("• 默认的 auto 模式会自动检测活动窗口所在的屏幕")


if __name__ == "__main__":
    main()